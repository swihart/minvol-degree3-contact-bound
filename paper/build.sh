#!/bin/sh
set -eu

PAPER_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$PAPER_DIR/.." && pwd)
cd "$PAPER_DIR"

export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1789776000}
export FORCE_SOURCE_DATE=${FORCE_SOURCE_DATE:-1}

python3 reconcile_certificate.py --check

rm -rf build
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=build contact_geometric_bound.tex
python3 "$REPO_ROOT/tools/markdown_pdf/normalize_pdf_id.py" \
  build/contact_geometric_bound.pdf
latexmk -c -outdir=build contact_geometric_bound.tex >/dev/null

echo "MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS"
echo "MINVOL PAPER BUILD: PASS"
echo "Built PDF: paper/build/contact_geometric_bound.pdf"
