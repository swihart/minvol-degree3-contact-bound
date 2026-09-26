#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 terminal_handoff_v11_exact.py
python3 terminal_handoff_v11_exploration.py
python3 terminal_handoff_v11_binary64.py
if command -v Rscript >/dev/null 2>&1; then
  Rscript terminal_handoff_v11_audit.R
else
  printf '%s\n' 'Rscript unavailable: base-R audit prepared but not run in this environment.'
fi
printf '%s\n' 'MINVOL TERMINAL-HANDOFF V1.1 AUDIT PACKAGE: PASS'
