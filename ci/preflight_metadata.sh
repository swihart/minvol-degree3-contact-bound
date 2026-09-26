#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

fail() {
  echo "Metadata preflight failed: $*" >&2
  exit 2
}

EXPECTED_VERSION=v1.1.0
EXPECTED_DATE=2026-09-26
DISPLAY_DATE="September 26, 2026"
REPOSITORY_URL="https://github.com/swihart/minvol-degree3-contact-bound"
RELEASE_URL="$REPOSITORY_URL/releases/tag/$EXPECTED_VERSION"

for file in AI_ASSISTANCE.md CITATION.cff LICENSE VERSION RELEASE_DATE \
  RELEASE_CHECKLIST.md RELEASE_NOTES.md README.md \
  paper/contact_geometric_bound.tex; do
  [ -s "$file" ] || fail "missing or empty file: $file"
done

version=$(tr -d '\r\n' < VERSION)
release_date=$(tr -d '\r\n' < RELEASE_DATE)
[ "$version" = "$EXPECTED_VERSION" ] || fail "VERSION is '$version', expected $EXPECTED_VERSION"
[ "$release_date" = "$EXPECTED_DATE" ] || fail "RELEASE_DATE is '$release_date', expected $EXPECTED_DATE"

grep -F "Bruce J. Swihart" paper/contact_geometric_bound.tex >/dev/null || fail "paper author missing"
grep -F "pdfauthor={Bruce J. Swihart}" paper/contact_geometric_bound.tex >/dev/null || fail "paper PDF author metadata inconsistent"
grep -F "No institutional affiliation is asserted" paper/contact_geometric_bound.tex >/dev/null || fail "paper no-affiliation statement missing"
grep -F "GPT-5.6 Sol Pro" paper/contact_geometric_bound.tex >/dev/null || fail "paper AI-system disclosure missing"
grep -F "$REPOSITORY_URL" paper/contact_geometric_bound.tex >/dev/null || fail "paper repository URL missing"
grep -F "$RELEASE_URL" paper/contact_geometric_bound.tex >/dev/null || fail "paper release URL missing"
grep -F "$EXPECTED_VERSION" paper/contact_geometric_bound.tex >/dev/null || fail "paper version missing"
grep -F "$DISPLAY_DATE" paper/contact_geometric_bound.tex >/dev/null || fail "paper release date missing"
grep -F 'given-names: "Bruce J."' CITATION.cff >/dev/null || fail "CFF given names missing"
grep -F 'family-names: "Swihart"' CITATION.cff >/dev/null || fail "CFF family name missing"
grep -F 'version: "1.1.0"' CITATION.cff >/dev/null || fail "CFF version inconsistent"
grep -F 'date-released: "2026-09-26"' CITATION.cff >/dev/null || fail "CFF release date inconsistent"
grep -F 'status: preprint' CITATION.cff >/dev/null || fail "CFF preprint status missing"
grep -F "repository-code: \"$REPOSITORY_URL\"" CITATION.cff >/dev/null || fail "CFF repository URL inconsistent"
grep -F "url: \"$RELEASE_URL\"" CITATION.cff >/dev/null || fail "CFF release URL inconsistent"
grep -F "CC BY 4.0" LICENSE >/dev/null || fail "prose license missing"
grep -F "MIT License" LICENSE >/dev/null || fail "software license missing"
grep -F "Bruce J. Swihart" README.md >/dev/null || fail "README author metadata missing"
grep -F "$EXPECTED_VERSION" README.md >/dev/null || fail "README version missing"
grep -F "$DISPLAY_DATE" README.md >/dev/null || fail "README date missing"
grep -F "$RELEASE_URL" README.md >/dev/null || fail "README release URL missing"
grep -F "CC BY 4.0" README.md >/dev/null || fail "README prose license missing"
grep -F "MIT" README.md >/dev/null || fail "README software license missing"
grep -F "PREPARED FOR THE FINAL TAG GATE" RELEASE_CHECKLIST.md >/dev/null || fail "final-tag gate decision missing"

python3 - <<'PY2'
from pathlib import Path
text = Path('CITATION.cff').read_text(encoding='utf-8')
required = (
    'cff-version: 1.2.0', 'message:', 'title:', 'type: software',
    'authors:', 'preferred-citation:', 'type: unpublished',
    'version: "1.1.0"', 'date-released: "2026-09-26"',
    'year: 2026', 'status: preprint', 'license: CC-BY-4.0',
    'https://github.com/swihart/minvol-degree3-contact-bound',
    'releases/tag/v1.1.0',
)
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit('CITATION.cff is missing: ' + ', '.join(missing))
print('MINVOL CITATION METADATA CHECK: PASS')
PY2

echo "MINVOL METADATA PREFLIGHT: PASS"
echo "Version: $EXPECTED_VERSION"
echo "Release date: $EXPECTED_DATE"
echo "Canonical repository: $REPOSITORY_URL"
