#!/usr/bin/env python3
"""Analytic IPR on a delta-like grid, plus optional WAVECAR band IPR."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

# ---- analytic delta-like grid ----
grid = np.zeros((16, 16, 16))
grid[8, 8, 8] = 1.0
prob = np.abs(grid) ** 2
ipr = (prob**2).sum() / (prob.sum() ** 2)

Path("ref").mkdir(exist_ok=True)
Path("ref/ipr_analytic.txt").write_text(f"ipr={ipr:.8e}\n")
print(f"Analytic grid IPR: {ipr:.8e}")

# With a single non-zero point, IPR should be exactly 1.0
assert ipr == 1.0, f"Expected IPR=1.0 for delta grid, got {ipr}"

# ---- optional WAVECAR band IPR ----
WAVECAR = ROOT / "examples" / "wfc_r" / "WAVECAR"
if WAVECAR.is_file():
    sys.path.insert(0, str(ROOT))
    from vaspwfc import vaspwfc  # type: ignore[import-untyped]

    wfc = vaspwfc(str(WAVECAR))
    iband = min(1, int(wfc._nbands))
    phi = wfc.wfc_r(iband=iband)
    arr = phi if not isinstance(phi, (list, tuple)) else phi[0]
    prob_r = np.abs(arr) ** 2
    wfc_ipr = (prob_r**2).sum() / (prob_r.sum() ** 2)
    Path("ref/ipr_wavecar.txt").write_text(f"ipr_wavecar={wfc_ipr:.8e}\n")
    print(f"WAVECAR band {iband} IPR: {wfc_ipr:.8e}")
else:
    print("No WAVECAR found -- skipping wavefunction IPR (ok for C1)")
