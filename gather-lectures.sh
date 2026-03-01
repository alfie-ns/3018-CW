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

# Gather all markdown files into a separate folder
MD_DEST="/tmp/COMP3018-markdown"
rm -rf "$MD_DEST"
mkdir -p "$MD_DEST"

j=1
find "$SRC" -name "*.md" -type f | sort | while read -r f; do
    name=$(basename "$f")
    cp "$f" "$MD_DEST/$(printf '%02d' $j)-$name"
    echo "Copied MD: $name"
    j=$((j + 1))
done

echo ""
echo "All markdown files gathered in: $MD_DEST"

# Gather all text files into a separate folder
TXT_DEST="/tmp/COMP3018-text"
rm -rf "$TXT_DEST"
mkdir -p "$TXT_DEST"

k=1
find "$SRC" -name "*.txt" -type f | sort | while read -r f; do
    name=$(basename "$f")
    cp "$f" "$TXT_DEST/$(printf '%02d' $k)-$name"
    echo "Copied TXT: $name"
    k=$((k + 1))
done

echo ""
echo "All text files gathered in: $TXT_DEST"

open "$DEST"
open "$MD_DEST"
open "$TXT_DEST"
