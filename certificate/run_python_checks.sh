#!/bin/sh
set -eu

python3 certify_universal_bound.py
python3 audit_universal_bound.py
python3 -m unittest -v test_universal_bound.py
python3 test_adversarial_mutations.py
python3 terminal_handoff_v11/terminal_handoff_v11_exact.py
python3 terminal_handoff_v11/terminal_handoff_v11_exploration.py
python3 terminal_handoff_v11/terminal_handoff_v11_binary64.py
