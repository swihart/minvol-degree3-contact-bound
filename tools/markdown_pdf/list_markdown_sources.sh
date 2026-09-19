#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$ROOT"

# Render repository documentation, not Markdown files installed inside ignored
# environments (for example, package LICENSE.md files under .venv/).
# Include tracked files and untracked files that are not excluded by .gitignore,
# so newly drafted repository documentation can be previewed before it is added.
if command -v git >/dev/null 2>&1 && \
   git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files --cached --others --exclude-standard | \
    awk '
      /\.md$/ &&
      $0 !~ /^rendered\// &&
      $0 !~ /^ci-artifacts\// &&
      $0 !~ /(^|\/)\.venv\// {
        print
      }
    ' | LC_ALL=C sort -u
else
  # Fallback for a source tree copied without its .git directory.
  find . \
    \( -type d \( \
      -name .git -o \
      -name .venv -o \
      -name rendered -o \
      -name ci-artifacts \
    \) -prune \) -o \
    \( -type f -name '*.md' -print \) | \
    sed 's#^\./##' | \
    LC_ALL=C sort
fi
