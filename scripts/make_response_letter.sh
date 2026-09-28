#!/usr/bin/env bash
# Build RESPONSE_TO_REVIEWERS.pdf from RESPONSE_TO_REVIEWERS.md.
# The markdown-preview styling (gray referee quotes behind a left bar, heading
# underlines) lives in latex/response_letter_style.tex.
# Needs: pandoc and pdflatex with mdframed and titlesec
# (apt: pandoc texlive-latex-extra texlive-fonts-recommended lmodern).
set -euo pipefail
cd "$(dirname "$0")/.."

filter="$(mktemp --suffix=.lua)"
trap 'rm -f "$filter"' EXIT
cat > "$filter" <<'LUA'
-- Markdown '---' separators: full-width thin gray rule, as in a markdown preview
function HorizontalRule()
  return pandoc.RawBlock('latex',
    '\\par\\medskip\\noindent{\\color{bordergray}\\rule{\\linewidth}{1pt}}\\par\\medskip')
end
LUA

pandoc RESPONSE_TO_REVIEWERS.md \
  --pdf-engine=pdflatex \
  --lua-filter "$filter" \
  -H latex/response_letter_style.tex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V colorlinks=true \
  -o RESPONSE_TO_REVIEWERS.pdf

if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo RESPONSE_TO_REVIEWERS.pdf | grep '^Pages'
fi
