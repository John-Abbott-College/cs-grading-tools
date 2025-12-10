#!/usr/bin/env bash

set -euo pipefail

GRADING_DIR="${1}"
OUTPUT_ZIP="$(dirname "$GRADING_DIR")/Assignments.zip"

# Create the output directory
# mkdir -p $OUTPUT_DIR

# Find the markdown files and make pdfs
find ${GRADING_DIR} -type f -name "*.md" \
  -exec sh -c 'echo "Creating ${0%.*}.pdf..."; ./generate_pdf.sh "${0}"' {} \;


# Find the pdfs and make the zip
find ${GRADING_DIR} -type f -name "*.pdf" \
  -exec zip -j -r $OUTPUT_ZIP {} +

# List the created archive files for reassurance :)
unzip -l $OUTPUT_ZIP
