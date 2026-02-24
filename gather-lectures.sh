#!/bin/bash
# Gathers all lecture PDFs into a single flat folder for easy dragging.
# Re-run this anytime you add new lectures.

SRC="/Users/alfienurse/Library/Mobile Documents/com~apple~CloudDocs/Desktop/gitdev/Uni/Undergrad/year-3/Work/1st Year/Semester 2/3018-CW/learning/lectures"
DEST="/tmp/COMP3018-lectures"

rm -rf "$DEST"
mkdir -p "$DEST"

# Find all PDFs recursively and copy with numbered prefixes
i=1
find "$SRC" -name "*.pdf" -type f | sort | while read -r f; do
    name=$(basename "$f")
    cp "$f" "$DEST/$(printf '%02d' $i)-$name"
    echo "Copied: $name"
    i=$((i + 1))
done

echo ""
echo "All lecture PDFs gathered in: $DEST"

open "$DEST"
