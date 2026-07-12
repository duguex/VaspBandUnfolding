#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Check optional pySBT dependency (needed for AE wavefunction reconstruction)
python -c "from pysbt import pysbt" 2>/dev/null || {
    echo "MISSING: pySBT not installed (https://github.com/QijingZheng/pySBT)" >&2
    exit 2
}

export PYTHONPATH="$(cd ../../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

# Run the existing all-electron vs pseudo wavefunction plot
MPLBACKEND=Agg python plt_aeps_wfc.py

# Copy the generated image to ref
cp co2_homo_aeps_wfc.png ref/

echo "aewfc/co2 PASS: AE-PS wavefunction plot generated"
