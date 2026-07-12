#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

# Prefer lreal_false (reciprocal-space projectors) as the C1 demo
if [[ ! -f lreal_false/cproj.npy ]]; then
    echo "MISSING: lreal_false/cproj.npy" >&2
    exit 2
fi

mkdir -p ref

python run_check.py
python run_qij.py
