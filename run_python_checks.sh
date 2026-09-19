#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT/certificate"
./run_python_checks.sh
cd "$ROOT"
python3 proof/generate_exact_constants.py --check
python3 ci/verify_release_docs.py
./ci/preflight_metadata.sh
python3 paper/reconcile_certificate.py --check
