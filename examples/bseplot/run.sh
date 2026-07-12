#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f BSEFATBAND ]]; then
    echo "MISSING: BSEFATBAND" >&2
    exit 2
fi

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

python ../../bin/bseplot bz \
    --input BSEFATBAND \
    --poscar POSCAR \
    --exciton 1 \
    --output-dir ref \
    --dpi 150
