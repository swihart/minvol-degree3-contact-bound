#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT/certificate"
./run_python_checks.sh
cd "$ROOT"
python3 paper/reconcile_certificate.py --check
