#!/usr/bin/env python3
"""C1 demo: PS dipole matrix element via get_dipole_mat (W4)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
wav = Path(os.environ.get("VBU_TDM_WAVECAR", ROOT / ".." / "wfc_r" / "WAVECAR"))
if not wav.is_file():
    print(f"MISSING: WAVECAR at {wav}", file=sys.stderr)
    sys.exit(2)

from vaspwfc import vaspwfc

wfc = vaspwfc(str(wav))
nb = int(wfc._nbands)

# Bands 1→2 at ispin=1, ikpt=1
i, j = 1, min(2, nb)
Emk, Enk, dE, dp_mat = wfc.get_dipole_mat((1, 1, i), (1, 1, j))

print(f"bands ({i}→{j}):  Emk={Emk:.6f}  Enk={Enk:.6f}  dE={dE:.6f}")
print(f"dipole matrix shape {dp_mat.shape} dtype {dp_mat.dtype}")
print(f"  x = {dp_mat[0]:.10e}")
print(f"  y = {dp_mat[1]:.10e}")
print(f"  z = {dp_mat[2]:.10e}")

ref = ROOT / "ref"
ref.mkdir(exist_ok=True)
# Save dipole matrix as 3 rows (real / imag columns)
np.savetxt(ref / "dipole_ps.txt",
           np.column_stack([dp_mat.real, dp_mat.imag]),
           fmt="% .12e",
           header="  Re(d)           Im(d)\n"
                  "# Each row: component x, y, z  [Debye]")

# Magnitude summary
mag = np.abs(dp_mat).ravel()
(ref / "dipole_ps_abs_max.txt").write_text(f"abs_max={mag.max():.8e}\n")
print(f"abs_max={mag.max():.8e}")
print("wrote", ref / "dipole_ps.txt")
print("wrote", ref / "dipole_ps_abs_max.txt")
