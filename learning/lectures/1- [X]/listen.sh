#!/bin/bash
# Open lecture.pdf with Speechify (web or app)

DIR="$(cd "$(dirname "$0")" && pwd)"
PDF="$(find "$DIR" -maxdepth 1 -name 'lecture*.pdf' -print -quit)"

if [ -z "$PDF" ]; then
  echo "Error: no lecture PDF found in $DIR"
  exit 1
fi

case "${1:-web}" in
  web)
    echo "Opening Speechify web app — upload lecture.pdf when prompted."
    echo "PDF location: $PDF"
    open "https://app.speechify.com"
    ;;
  app)
    if open -Ra "Speechify" 2>/dev/null; then
      echo "Opening lecture.pdf in Speechify app..."
      open -a "Speechify" "$PDF"
    else
      echo "Speechify app not found. Falling back to web..."
      open "https://app.speechify.com"
    fi
    ;;
  *)
    echo "Usage: ./listen.sh [web|app]"
    echo "  web  — Open Speechify in your browser (default)"
    echo "  app  — Open with the Speechify desktop app"
    exit 1
    ;;
esac
