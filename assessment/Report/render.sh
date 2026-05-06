#!/bin/bash

pandoc "COMP_3018_Report.md" -o "COMP_3018_Report.pdf" \
    --pdf-engine=xelatex \
    --from markdown+raw_tex \
    -V geometry:margin=1in \
    --listings \
    --toc \
    --toc-depth=3

echo "Rendered: COMP_3018_Report.pdf"