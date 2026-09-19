#!/bin/sh
set -eu

python3 certify_universal_bound.py
python3 audit_universal_bound.py
python3 -m unittest -v test_universal_bound.py
python3 test_adversarial_mutations.py
