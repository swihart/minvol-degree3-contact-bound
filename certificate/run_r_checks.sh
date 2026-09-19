#!/bin/sh
set -eu

if ! command -v Rscript >/dev/null 2>&1; then
  echo "MINVOL UNIVERSAL CONTACT-BOUND BASE-R AUDIT: NOT RUN (Rscript unavailable)" >&2
  echo "Install base R and rerun ./run_r_checks.sh." >&2
  exit 2
fi

Rscript audit_universal_bound.R .
