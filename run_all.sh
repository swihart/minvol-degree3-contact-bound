#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
./run_python_checks.sh
./run_r_checks.sh

echo "MINVOL UNIVERSAL CONTACT-BOUND REPLAY: PASS"
