#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"
mkdir -p ref

WA="${VBU_NAC_WAVECAR_A:-}"
WB="${VBU_NAC_WAVECAR_B:-}"
if [[ -z "$WA" || -z "$WB" ]]; then
  if [[ -f WAVECAR_A && -f WAVECAR_B ]]; then
    WA=WAVECAR_A; WB=WAVECAR_B
  elif [[ -f md_frames/frame0/WAVECAR && -f md_frames/frame1/WAVECAR ]]; then
    WA=md_frames/frame0/WAVECAR
    WB=md_frames/frame1/WAVECAR
  elif [[ -f ../wfc_r/WAVECAR ]]; then
    WA=../wfc_r/WAVECAR; WB=../wfc_r/WAVECAR
    echo "NOTE: identical WAVECARs smoke (NAC~0)." >&2
  else
    echo "MISSING dual WAVECARs" >&2; exit 2
  fi
fi

python - <<PY
from pathlib import Path
import numpy as np
from nac import nac_from_vaspwfc
from vaspwfc import vaspwfc
wa, wb = "$WA", "$WB"
lgam = bool(vaspwfc(wa)._lgam)
nb = int(vaspwfc(wa)._nbands)
ent, nacs = nac_from_vaspwfc(wa, wb, gamma=lgam, bmin=1, bmax=min(8, nb), dt=1.0, ikpt=1, ispin=1)
ref = Path("ref"); ref.mkdir(exist_ok=True)
arr = np.asarray(nacs)
np.savetxt(ref / "nac_matrix.txt", arr.real if np.iscomplexobj(arr) else arr)
(ref / "nac_summary.txt").write_text(
    f"waveA={wa}\nwaveB={wb}\ngamma={lgam}\nshape={arr.shape}\n"
    f"max_abs={float(np.max(np.abs(arr))):.8e}\n"
)
print(open(ref / "nac_summary.txt").read())
PY
echo "nac PASS"
