#!/bin/sh
set -eu
cd "$(dirname "$0")/certificate"
./run_r_checks.sh
