#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

fail() {
  echo "Release preflight failed: $*" >&2
  exit 2
}

EXPECTED_VERSION=v1.0.0
EXPECTED_DATE=2026-09-26
DISPLAY_DATE="September 26, 2026"
REPOSITORY_URL="https://github.com/swihart/minvol-degree3-contact-bound"
RELEASE_URL="$REPOSITORY_URL/releases/tag/$EXPECTED_VERSION"

for file in VERSION RELEASE_DATE RELEASE_NOTES.md README.md CITATION.cff \
  REPRODUCIBILITY.md VERIFICATION_STATUS.md AI_ASSISTANCE.md LICENSE \
  RELEASE_CHECKLIST.md paper/README.md paper/contact_geometric_bound.tex \
  build_release_assets.sh verify_release_assets.sh \
  release/build_release_assets.py release/verify_release_assets.py; do
  [ -s "$file" ] || fail "missing or empty file: $file"
done

version=$(tr -d '\r\n' < VERSION)
release_date=$(tr -d '\r\n' < RELEASE_DATE)
[ "$version" = "$EXPECTED_VERSION" ] || fail "VERSION is '$version', expected '$EXPECTED_VERSION'"
[ "$release_date" = "$EXPECTED_DATE" ] || fail "RELEASE_DATE is '$release_date', expected '$EXPECTED_DATE'"

for file in README.md RELEASE_NOTES.md REPRODUCIBILITY.md \
  VERIFICATION_STATUS.md paper/README.md paper/contact_geometric_bound.tex \
  CITATION.cff LICENSE RELEASE_CHECKLIST.md; do
  grep -F "$EXPECTED_VERSION" "$file" >/dev/null || fail "$file does not contain $EXPECTED_VERSION"
done

for file in README.md RELEASE_NOTES.md VERIFICATION_STATUS.md \
  paper/README.md paper/contact_geometric_bound.tex LICENSE RELEASE_CHECKLIST.md; do
  grep -F "$DISPLAY_DATE" "$file" >/dev/null || fail "$file does not contain $DISPLAY_DATE"
done

for file in README.md RELEASE_NOTES.md paper/README.md \
  paper/contact_geometric_bound.tex CITATION.cff; do
  grep -F "$RELEASE_URL" "$file" >/dev/null || fail "$file does not contain the versioned release URL"
done

grep -F "non-peer-reviewed" README.md >/dev/null || fail "README status boundary missing"
grep -F "non-peer-reviewed" RELEASE_NOTES.md >/dev/null || fail "release-note status boundary missing"
grep -F "PREPARED FOR THE FINAL TAG GATE" RELEASE_CHECKLIST.md >/dev/null || fail "release decision missing"

for obsolete in \
  "v1.0.0-rc1" \
  "UNRELEASED" \
  "not yet public" \
  "Candidate version" \
  "Target final tag" \
  "DO NOT RELEASE YET"; do
  if grep -F "$obsolete" README.md RELEASE_NOTES.md paper/README.md \
      paper/contact_geometric_bound.tex CITATION.cff LICENSE AI_ASSISTANCE.md >/dev/null 2>&1; then
    fail "obsolete release wording remains in a public-facing file: $obsolete"
  fi
done

[ -x build_release_assets.sh ] || fail "build_release_assets.sh is not executable"
[ -x verify_release_assets.sh ] || fail "verify_release_assets.sh is not executable"
[ -x release/build_release_assets.py ] || fail "release asset builder is not executable"
[ -x release/verify_release_assets.py ] || fail "release asset verifier is not executable"

echo "MINVOL RELEASE PREFLIGHT: PASS"
echo "Version: $EXPECTED_VERSION"
echo "Release date: $EXPECTED_DATE"
echo "Canonical repository: $REPOSITORY_URL"
echo "Versioned release: $RELEASE_URL"
