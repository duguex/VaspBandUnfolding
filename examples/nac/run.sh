#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"
mkdir -p ref

# Prefer explicit dual frames; else demo with two paths (may be same file for API smoke).
WA="${VBU_NAC_WAVECAR_A:-}"
WB="${VBU_NAC_WAVECAR_B:-}"
if [[ -z "$WA" || -z "$WB" ]]; then
  if [[ -f WAVECAR_A && -f WAVECAR_B ]]; then
    WA=WAVECAR_A
    WB=WAVECAR_B
  elif [[ -f ../wfc_r/WAVECAR ]]; then
    # Same-structure smoke: identical WAVECARs => NAC ~ 0 (API + import exercise).
    WA=../wfc_r/WAVECAR
    WB=../wfc_r/WAVECAR
    echo "NOTE: using identical WAVECARs for C1 smoke (NAC~0). For real NAC set WAVECAR_A/B or VBU_NAC_WAVECAR_{A,B}." >&2
  else
    echo "MISSING: two WAVECARs (WAVECAR_A/B or VBU_NAC_WAVECAR_A/B)" >&2
    exit 2
  fi
fi

python - <<PY
from __future__ import annotations

from pathlib import Path

import numpy as np

from nac import nac_from_vaspwfc
from vaspwfc import vaspwfc

wa, wb = "$WA", "$WB"
# Standard (non-gamma) WAVECARs need gamma=False
lgam = bool(vaspwfc(wa)._lgam)
ent, nacs = nac_from_vaspwfc(
    wa, wb, gamma=lgam, bmin=1, bmax=min(4, int(vaspwfc(wa)._nbands)), dt=1.0, ikpt=1, ispin=1
)
ref = Path("ref")
ref.mkdir(exist_ok=True)
np.savetxt(ref / "nac_matrix.txt", np.asarray(nacs).real if np.iscomplexobj(nacs) else nacs)
(ref / "nac_summary.txt").write_text(
    f"gamma={lgam}\nshape={np.asarray(nacs).shape}\n"
    f"max_abs={float(np.max(np.abs(nacs))):.8e}\n"
    f"energies={np.array2string(np.asarray(ent), precision=6)}\n"
    f"waveA={wa}\nwaveB={wb}\n"
)
print("wrote", ref / "nac_summary.txt")
PY

echo "nac PASS"
