#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f WAVECAR ]]; then
    echo "MISSING: WAVECAR" >&2
    exit 2
fi

# Ensure PYTHONPATH includes repo root so vaspwfc etc. can be imported
export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

mkdir -p ref

# Run existing example script (non-interactive, saves .vasp / .png)
python ex.py

# Compute norm of a low-band real-space wavefunction as a quick sanity metric
python - <<'PY'
from vaspwfc import vaspwfc
import numpy as np
from pathlib import Path

w = vaspwfc("WAVECAR")
iband = min(1, int(w._nbands))
phi = w.wfc_r(iband=iband)
# wfc_r returns an ndarray for nspin=1, or a tuple for nspin>1
arr = phi if not isinstance(phi, (list, tuple)) else phi[0]
n = float(np.vdot(arr, arr).real)
Path("ref").mkdir(exist_ok=True)
Path("ref/norm.txt").write_text(f"norm={n:.8e}\n")
print("norm", n)
PY
