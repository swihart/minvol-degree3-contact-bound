#!/bin/sh
set -eu
cd "$(dirname "$0")/certificate"
./run_python_checks.sh
