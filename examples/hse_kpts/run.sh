#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Copy a simple POSCAR if not present (CsCl from ewald)
if [[ ! -f POSCAR ]]; then
    cp ../../examples/ewald/CsCl.vasp POSCAR
fi

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref
python run.py
