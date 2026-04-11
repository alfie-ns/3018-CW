#!/bin/bash

# Extract document ID from the URL
DOC_ID="1ZR_CWbcd3vEIIw9HCK18JX4gvBWI256iahyTYR9zY2s"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Download as PDF
curl -L "https://docs.google.com/document/d/${DOC_ID}/export?format=pdf" \
    -o "${SCRIPT_DIR}/global-origin-gdoc-report.pdf"

echo "PDF downloaded to: ${SCRIPT_DIR}/global-origin-gdoc-report.pdf"

# Open in Google Chrome
open -a "Google Chrome" "https://docs.google.com/document/d/${DOC_ID}/edit"