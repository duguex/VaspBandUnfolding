#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Check optional pySBT dependency (needed for AE wavefunction reconstruction)
python -c "from pysbt import pysbt" 2>/dev/null || {
    echo "MISSING: pySBT not installed (https://github.com/QijingZheng/pySBT)" >&2
    echo "  pip install 'pySBT @ git+https://github.com/QijingZheng/pySBT.git'" >&2
    exit 2
}

export PYTHONPATH="$(cd ../../.. && pwd):${PYTHONPATH:-}"
mkdir -p ref

if [[ ! -f WAVECAR ]]; then
  echo "MISSING: WAVECAR" >&2
  exit 2
fi

MPLBACKEND=Agg python plt_aeps_wfc.py

if [[ -f co2_homo_aeps_wfc.png ]]; then
  cp -f co2_homo_aeps_wfc.png ref/
fi

python - <<'PY'
from pathlib import Path
from vaspwfc import vaspwfc
from aewfc import vasp_ae_wfc

ps = vaspwfc("WAVECAR", lgamma=True)
ae = vasp_ae_wfc(ps, aecut=-25)
phi = ae.get_ae_wfc(iband=8)
import numpy as np
n = float(np.vdot(phi, phi).real)
Path("ref/ae_norm.txt").write_text(f"iband=8 ae_norm={n:.8e}\n")
print("ae_norm", n)
PY

echo "aewfc/co2 PASS: AE-PS wavefunction plot generated"
