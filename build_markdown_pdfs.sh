#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"

export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1790380800}
export FORCE_SOURCE_DATE=${FORCE_SOURCE_DATE:-1}

OUT_ROOT=${1:-build/markdown}
TITLE_FILTER=tools/markdown_pdf/first_h1_title.lua
MATH_FILTER=tools/markdown_pdf/math_display_fixes.lua
PREAMBLE=tools/markdown_pdf/preamble.tex
SOURCE_LISTER=tools/markdown_pdf/list_markdown_sources.sh

for command_name in pandoc xelatex python3; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Required command not found: $command_name" >&2
    exit 2
  fi
done

rm -rf "$OUT_ROOT"
mkdir -p "$OUT_ROOT"

sh "$SOURCE_LISTER" \
  | while IFS= read -r source; do
      relative=${source#./}
      destination="$OUT_ROOT/${relative%.md}.pdf"
      mkdir -p "$(dirname -- "$destination")"

      line_count=$(wc -l < "$source" | tr -d ' ')
      set --
      if [ "$line_count" -ge 140 ]; then
        set -- --toc --toc-depth=3
      fi

      echo "Rendering $relative -> $destination"
      pandoc "$source" \
        --from='markdown+tex_math_single_backslash' \
        --standalone \
        --pdf-engine=xelatex \
        --pdf-engine-opt='-output-driver=xdvipdfmx -z 0 -C 64' \
        --lua-filter="$TITLE_FILTER" \
        --lua-filter="$MATH_FILTER" \
        --include-in-header="$PREAMBLE" \
        --listings \
        --metadata="subtitle:Repository source: $relative" \
        --variable=papersize:letter \
        --variable=geometry:margin=0.75in \
        --variable=fontsize:10pt \
        --variable=colorlinks:true \
        --variable=linkcolor:blue \
        --variable=urlcolor:blue \
        --variable=toccolor:black \
        "$@" \
        --output="$destination"

      python3 tools/markdown_pdf/normalize_pdf_id.py "$destination"
    done

manifest="$OUT_ROOT/SHA256SUMS.txt"
: > "$manifest"
find "$OUT_ROOT" -type f -name '*.pdf' | LC_ALL=C sort | while IFS= read -r pdf; do
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$pdf" >> "$manifest"
  else
    shasum -a 256 "$pdf" >> "$manifest"
  fi
done

echo "MINVOL MARKDOWN PDF BUILD: PASS"
echo "Rendered Markdown PDFs: $OUT_ROOT"
echo "Checksum manifest: $manifest"
