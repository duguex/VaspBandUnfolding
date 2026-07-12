#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Prefer a multi-k WAVECAR; fall back to sibling demo data.
if [[ ! -f WAVECAR ]]; then
  if [[ -f ../wfc_r/WAVECAR ]]; then
    ln -sfn ../wfc_r/WAVECAR WAVECAR
  else
    echo "MISSING: WAVECAR (need multi-k band-structure WAVECAR)" >&2
    exit 2
  fi
fi

if [[ ! -f KPOINTS ]]; then
  if [[ -f ../wfc_r/KPOINTS ]]; then
    ln -sfn ../wfc_r/KPOINTS KPOINTS
  fi
fi

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"
mkdir -p ref

python - <<'PY'
from __future__ import annotations

from pathlib import Path

import numpy as np

from band_order import reorder_band
from vaspwfc import vaspwfc

wfc = vaspwfc("WAVECAR")
nk = int(wfc._nkpts)
# Line-mode segments: use all k-points as one segment when KPOINTS is not line-mode.
nkseg = nk if nk > 0 else 1
max_nb = min(8, int(wfc._nbands))
ebands, bands_new, kpath, kbound = reorder_band(
    wavecar="WAVECAR",
    max_nbnds=max_nb,
    olap_cut=0.5,
    save_olap=False,
    save_idx=True,
    nkseg=nkseg,
)
ref = Path("ref")
ref.mkdir(exist_ok=True)
np.save(ref / "bands_new.npy", bands_new)
(ref / "reorder_summary.txt").write_text(
    f"nkpts={nk}\nmax_nbnds={max_nb}\nkpath_end={float(kpath[-1]):.8f}\n"
    f"kbound={np.array2string(np.asarray(kbound), precision=6)}\n"
    f"bands_new_shape={tuple(np.asarray(bands_new).shape)}\n"
)
print("wrote", ref / "reorder_summary.txt")
PY

echo "band_reorder PASS"
