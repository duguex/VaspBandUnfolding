#!/usr/bin/env python3
"""Compare vaspwfc dipole matrix elements to VASP LOPTICS output if present.

Exit codes:
  0 — comparison written (or self-check only)
  2 — missing WAVECAR / optics data
  1 — failure
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO))

from vaspwfc import vaspwfc


def parse_outcar_transitions(outcar: Path, max_lines: int = 50) -> list[str]:
    """Pull a few OPTICS-related lines for human inspection (format varies by VASP)."""
    text = outcar.read_text(errors="replace")
    keys = ("optical", "dielectric", "transition", "LOPTICS", "frequency dependent")
    hits = []
    for ln in text.splitlines():
        low = ln.lower()
        if any(k in low for k in keys):
            hits.append(ln.rstrip())
        if len(hits) >= max_lines:
            break
    return hits


def main() -> int:
    wav = ROOT / "vasp_optics" / "output" / "WAVECAR"
    if not wav.is_file():
        wav = ROOT / "vasp_optics" / "WAVECAR"
    if not wav.is_file():
        # fall back to demo WAVECAR for structural self-check
        wav = ROOT.parent / "wfc_r" / "WAVECAR"
        mode = "fallback_wfc_r"
    else:
        mode = "optics_wavecar"

    if not wav.is_file():
        print("MISSING: WAVECAR", file=sys.stderr)
        return 2

    wfc = vaspwfc(str(wav))
    nb = int(wfc._nbands)
    i, j = 1, min(2, nb)
    mat = np.asarray(wfc.get_dipole_mat((1, 1, i), (1, 1, j)))
    ref = ROOT / "ref"
    ref.mkdir(exist_ok=True)
    abs_max = float(np.max(np.abs(mat)))
    (ref / "l2_dipole_ps.txt").write_text(
        f"mode={mode}\nwavecar={wav}\nibands={i}->{j}\n"
        f"dipole={mat}\nabs_max={abs_max:.8e}\n"
        "citation=experimental until matched to VASP OPTICS tables\n"
    )

    outcar = ROOT / "vasp_optics" / "output" / "OUTCAR"
    if not outcar.is_file():
        outcar = ROOT / "vasp_optics" / "OUTCAR"
    if outcar.is_file():
        hits = parse_outcar_transitions(outcar)
        (ref / "l2_optics_outcar_hits.txt").write_text(
            "\n".join(hits) if hits else "(no optics keywords matched in OUTCAR)\n"
        )
        print("wrote optics OUTCAR hits + PS dipole")
    else:
        print("PS dipole only (no optics OUTCAR yet); mode=", mode)

    print("abs_max", abs_max)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
