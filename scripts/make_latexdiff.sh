#!/usr/bin/env bash
# Build a latexdiff PDF of the current manuscript against the version submitted
# to Digital Discovery (DD-ART-06-2026-000353).
#
# The baseline commit is recorded in latex/SUBMITTED_BASELINE.txt.  Override it
# with the first positional argument, e.g.
#
#     scripts/make_latexdiff.sh origin/main
#
# main.tex pulls Table 1 and the per-project summaries in through shell-escape
# pipes (\input{|python3 ...}).  latexdiff cannot see through those, so both the
# baseline and the current manuscript are "flattened" first: each pipe is
# replaced with the text that the corresponding script produces *in that tree*.
# Without this step the diff silently reports no change to the project listing.
#
# Output: build/latexdiff/main-diff.pdf
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

BASELINE="${1:-$(sed -n 's/^baseline:[[:space:]]*//p' latex/SUBMITTED_BASELINE.txt)}"
BUILD="$REPO_ROOT/build/latexdiff"
OLD_TREE="$BUILD/old"

for tool in latexdiff latexmk pdflatex python3 git; do
    command -v "$tool" >/dev/null || { echo "error: $tool not found on PATH" >&2; exit 1; }
done

rm -rf "$BUILD"
mkdir -p "$OLD_TREE"

echo "==> baseline: $BASELINE ($(git log -1 --format='%h %ad %s' --date=short "$BASELINE"))"
git archive "$BASELINE" | tar -x -C "$OLD_TREE"

# Flatten \input{|python3 <script>} pipes into literal text.  For the baseline
# tree, additionally relocate float environments that the revision moved (the
# figure block and the rankings table) to the positions they occupy in the
# revision.  latexdiff has no concept of a move: left in place, a moved float
# renders as its caption struck through mid-body at the old location plus an
# all-new float at the new one, which misleads reviewers into thinking the
# caption text sat in the body.  With the baseline floats pre-relocated, the
# diff pairs each float with its counterpart and marks caption edits inside
# the caption itself.
flatten() {
    local tree="$1" out="$2" is_old="${3:-0}"
    ( cd "$tree" && python3 - "$out" "$is_old" ) <<'PY'
import re
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1])
is_old = sys.argv[2] == "1"
src = Path("main.tex").read_text(encoding="utf-8")

PIPE = re.compile(r"\\input\{\|python3\s+([^}]+)\}")

# Floats moved by the revision, in the order they appear at the destination.
# Each is inserted directly after the (unique) anchor sentence, so the list is
# processed in reverse to preserve the order.  Anchors are plain sentences that
# are identical in the submitted and revised manuscripts.
RELOCATIONS = [
    ("tab:winners", "Collectively, 35 judges cast 319 votes."),
    ("tab:project_topics", "Collectively, 35 judges cast 319 votes."),
    ("fig:map", "Collectively, 35 judges cast 319 votes."),
    ("fig:preparation", "Collectively, 35 judges cast 319 votes."),
    ("fig:gathertown", "Collectively, 35 judges cast 319 votes."),
    ("fig:poster", "Collectively, 35 judges cast 319 votes."),
]

FLOAT_ENV = re.compile(
    r"^\\begin\{(figure\*?|table\*?)\}.*?^\\end\{\1\}[ \t]*\n?",
    re.MULTILINE | re.DOTALL,
)


def relocate_floats(text):
    moved = 0
    for label, anchor in reversed(RELOCATIONS):
        block = None
        for m in FLOAT_ENV.finditer(text):
            if f"\\label{{{label}}}" in m.group(0):
                block = m.group(0)
                break
        if block is None or text.count(anchor) != 1:
            print(f"warning: cannot relocate {label}", file=sys.stderr)
            continue
        text = text.replace(block, "", 1)
        i = text.index(anchor)
        j = text.index("\n", i) + 1
        if not block.endswith("\n"):
            block += "\n"
        text = text[:j] + "\n" + block + text[j:]
        moved += 1
    return text, moved

# The per-project headings used to be \subsection*{\href{video}{Project N: Name}}
# and are now \subsection*{Project N: Name}: the heading *text* is unchanged,
# only the hyperlink wrapper is gone.  latexdiff cannot see that, so it strikes
# out all 45 headings and reinserts each one verbatim, which buries the real
# changes.  Unwrapping \href inside \subsection* in BOTH trees before diffing
# makes the headings compare equal, so the diff shows them as untouched.  This
# is deliberately scoped to \subsection* headings; \href elsewhere (notably the
# repository links in the projects table) still diffs normally.
HREF_HEADING = re.compile(
    r"\\subsection\*\{\\href\{[^{}]*\}\{((?:[^{}]|\{[^{}]*\})*)\}\}"
)


def expand(match):
    script = match.group(1).strip()
    result = subprocess.run(
        [sys.executable, script], capture_output=True, text=True, check=True
    )
    return result.stdout


flat = PIPE.sub(expand, src)
flat, unwrapped = HREF_HEADING.subn(r"\\subsection*{\1}", flat)
moved = 0
if is_old:
    flat, moved = relocate_floats(flat)
out.write_text(flat, encoding="utf-8")
print(
    f"flattened -> {out} ({unwrapped} \\subsection* href wrappers unwrapped, "
    f"{moved} floats relocated)"
)
PY
}

flatten "$OLD_TREE" "$BUILD/old-main.tex" 1
flatten "$REPO_ROOT" "$BUILD/new-main.tex" 0

echo "==> running latexdiff"
latexdiff --encoding=utf8 --append-safecmd="gls,Gls,cref,Cref,zenodolink,orcidlink" \
    "$BUILD/old-main.tex" "$BUILD/new-main.tex" > "$BUILD/main-diff.tex"

# The diff document is compiled in place so that latex/, python_scripts/ and the
# bibliography resolve exactly as they do for main.tex.
cp "$BUILD/main-diff.tex" "$REPO_ROOT/main-diff.tex"
trap 'rm -f "$REPO_ROOT/main-diff.tex"' EXIT

# latexmk is not used here: \bibliography{latex/references, ...} uses paths
# relative to the repository root, and bibtex runs with the output directory as
# its working directory, so BIBINPUTS has to be set explicitly.  Driving the
# passes by hand keeps that under control.
export BIBINPUTS="$REPO_ROOT:${BIBINPUTS:-}"

echo "==> compiling"
run_pdflatex() {
    pdflatex -interaction=nonstopmode -shell-escape \
        -output-directory="$BUILD" "$REPO_ROOT/main-diff.tex" >/dev/null || true
}

run_pdflatex
run_pdflatex
( cd "$BUILD" && bibtex main-diff >/dev/null ) || {
    echo "warning: bibtex reported errors; see $BUILD/main-diff.blg" >&2
}
run_pdflatex
run_pdflatex

unresolved=$(grep -cE 'Citation .* undefined|Reference .* undefined' "$BUILD/main-diff.log" || true)
echo "==> $BUILD/main-diff.pdf (${unresolved} unresolved refs/citations)"
