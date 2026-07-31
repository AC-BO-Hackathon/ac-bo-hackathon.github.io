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

# Flatten \input{|python3 <script>} pipes into literal text.
flatten() {
    local tree="$1" out="$2"
    ( cd "$tree" && python3 - "$out" ) <<'PY'
import re
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1])
src = Path("main.tex").read_text(encoding="utf-8")

PIPE = re.compile(r"\\input\{\|python3\s+([^}]+)\}")


def expand(match):
    script = match.group(1).strip()
    result = subprocess.run(
        [sys.executable, script], capture_output=True, text=True, check=True
    )
    return result.stdout


out.write_text(PIPE.sub(expand, src), encoding="utf-8")
print(f"flattened -> {out}")
PY
}

flatten "$OLD_TREE" "$BUILD/old-main.tex"
flatten "$REPO_ROOT" "$BUILD/new-main.tex"

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
