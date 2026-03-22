#!/bin/bash

# Extract document ID from the URL
DOC_ID="10ZTrhiKLYtOY5Mneu69eK_osvMQh2I_S9BNzVDFeZ6E"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Download as PDF
curl -L "https://docs.google.com/document/d/${DOC_ID}/export?format=pdf" \
    -o "${SCRIPT_DIR}/proposal.pdf"

echo "PDF downloaded to: ${SCRIPT_DIR}/proposal.pdf"
