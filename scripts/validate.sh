#!/bin/sh
set -eu

hoyelam_stack_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$hoyelam_stack_root"
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
