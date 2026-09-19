#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

PDF_ROOT=${1:-rendered/markdown}
PAPER_PDF=${2:-paper/contact_geometric_bound.pdf}

fail() {
  echo "PDF preflight failed: $*" >&2
  exit 2
}

for command_name in pdfinfo pdffonts pdftotext; do
  command -v "$command_name" >/dev/null 2>&1 || \
    fail "required command not found: $command_name"
done

check_pdf() {
  pdf=$1
  [ -s "$pdf" ] || fail "missing or empty PDF: $pdf"
  pdfinfo "$pdf" >/dev/null || fail "pdfinfo could not read: $pdf"

  pages=$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2; exit}')
  case $pages in
    ''|*[!0-9]*) fail "could not determine page count for: $pdf" ;;
  esac
  [ "$pages" -gt 0 ] || fail "PDF has no pages: $pdf"

  if ! pdffonts "$pdf" | awk '
    NR <= 2 { next }
    NF > 0 && $(NF - 4) != "yes" { bad = 1 }
    END { exit bad }
  '; then
    fail "one or more fonts are not embedded in: $pdf"
  fi

  text_file=$(mktemp)
  if ! pdftotext "$pdf" "$text_file"; then
    rm -f "$text_file"
    fail "pdftotext could not read: $pdf"
  fi
  if [ ! -s "$text_file" ]; then
    rm -f "$text_file"
    fail "PDF has no extractable text: $pdf"
  fi
  rm -f "$text_file"
}

check_pdf "$PAPER_PDF"
paper_text=$(mktemp)
trap 'rm -f "$paper_text"' EXIT HUP INT TERM
pdftotext "$PAPER_PDF" "$paper_text"
grep -Fi "Bruce J. Swihart" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the author name"
grep -F "0.411877563780302" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the theorem coefficient"
grep -Fi "release candidate v1.0.0-rc1" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the release-candidate version"
grep -Fi "no institutional affiliation is asserted" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the affiliation statement"
grep -F "github.com/swihart/minvol-degree3-contact-bound" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the intended repository URL"
grep -F "GPT-5.6 Sol Pro" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the AI-system disclosure"
grep -Fi "Meissner conjecture" "$paper_text" >/dev/null || \
  fail "paper PDF does not contain the limitation language"

python3 ci/verify_doc_pairs.py --pdf-root "$PDF_ROOT"
find "$PDF_ROOT" -type f -name '*.pdf' | LC_ALL=C sort | while IFS= read -r pdf; do
  check_pdf "$pdf"
done

echo "MINVOL PDF PREFLIGHT: PASS"
echo "Paper PDF: $PAPER_PDF"
echo "Markdown PDF root: $PDF_ROOT"
