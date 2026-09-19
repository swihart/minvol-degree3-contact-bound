#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

fail() {
  echo "Metadata preflight failed: $*" >&2
  exit 2
}

for file in AI_ASSISTANCE.md CITATION.cff LICENSE VERSION RELEASE_DATE \
  RELEASE_CHECKLIST.md RELEASE_NOTES.md README.md \
  paper/contact_geometric_bound.tex; do
  [ -s "$file" ] || fail "missing or empty file: $file"
done

version=$(tr -d '\r\n' < VERSION)
release_date=$(tr -d '\r\n' < RELEASE_DATE)
[ "$version" = "v1.0.0-rc1" ] || fail "VERSION is '$version', expected v1.0.0-rc1"
[ "$release_date" = "UNRELEASED" ] || fail "release candidate must retain RELEASE_DATE=UNRELEASED"

grep -F "Bruce J. Swihart" paper/contact_geometric_bound.tex >/dev/null || fail "paper author missing"
grep -F "pdfauthor={Bruce J. Swihart}" paper/contact_geometric_bound.tex >/dev/null || fail "paper PDF author metadata inconsistent"
grep -F "No institutional affiliation is asserted" paper/contact_geometric_bound.tex >/dev/null || fail "paper no-affiliation statement missing"
grep -F "GPT-5.6 Sol Pro" paper/contact_geometric_bound.tex >/dev/null || fail "paper AI-system disclosure missing"
grep -F "github.com/swihart/minvol-degree3-contact-bound" paper/contact_geometric_bound.tex >/dev/null || fail "paper repository URL missing"
grep -F 'given-names: "Bruce J."' CITATION.cff >/dev/null || fail "CFF given names missing"
grep -F 'family-names: "Swihart"' CITATION.cff >/dev/null || fail "CFF family name missing"
grep -F 'version: "1.0.0-rc1"' CITATION.cff >/dev/null || fail "CFF version inconsistent"
grep -F 'status: preprint' CITATION.cff >/dev/null || fail "CFF preprint status missing"
grep -F 'repository-code: "https://github.com/swihart/minvol-degree3-contact-bound"' CITATION.cff >/dev/null || fail "CFF repository URL inconsistent"
grep -F "CC BY 4.0" LICENSE >/dev/null || fail "prose license missing"
grep -F "MIT License" LICENSE >/dev/null || fail "software license missing"
grep -F "Bruce J. Swihart" README.md >/dev/null || fail "README author metadata missing"
grep -F "v1.0.0-rc1" README.md >/dev/null || fail "README version missing"
grep -F "CC BY 4.0" README.md >/dev/null || fail "README prose license missing"
grep -F "MIT" README.md >/dev/null || fail "README software license missing"
grep -F "DO NOT RELEASE YET" RELEASE_CHECKLIST.md >/dev/null || fail "no-release decision missing"

python3 - <<'PY2'
from pathlib import Path
text = Path('CITATION.cff').read_text(encoding='utf-8')
required = (
    'cff-version: 1.2.0', 'message:', 'title:', 'type: software',
    'authors:', 'preferred-citation:', 'type: unpublished',
    'version: "1.0.0-rc1"', 'year: 2026', 'status: preprint',
    'license: CC-BY-4.0',
    'https://github.com/swihart/minvol-degree3-contact-bound',
)
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit('CITATION.cff is missing: ' + ', '.join(missing))
print('MINVOL CITATION METADATA CHECK: PASS')
PY2

echo "MINVOL METADATA PREFLIGHT: PASS"
echo "Candidate version: v1.0.0-rc1"
echo "Intended repository: https://github.com/swihart/minvol-degree3-contact-bound"
