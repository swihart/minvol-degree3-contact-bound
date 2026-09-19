#!/bin/sh
set -eu

./run_python_checks.sh
./run_r_checks.sh

echo "MINVOL UNIVERSAL CONTACT-BOUND REPLAY: PASS"
