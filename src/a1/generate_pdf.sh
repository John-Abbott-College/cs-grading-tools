#!/usr/bin/env bash

set -euo pipefail

input_markdown="${1}"
stylesheet="${2}"
PANDOC_OPTS=( --standalone --highlight-style=kate --from=commonmark_x --to=html5 )
WEASYPRINT_OPTS=( --stylesheet "${stylesheet}" )

pandoc "${PANDOC_OPTS[@]}" "${input_markdown}" | weasyprint "${WEASYPRINT_OPTS[@]}" - - > "${input_markdown%.*}.pdf"
