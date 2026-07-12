#!/usr/bin/env python3
"""Read a PROCAR (existing or minimal synthetic) and dump orbital projection table."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from procar import procar  # type: ignore[import-untyped]


def _find_procar() -> Path | None:
    """Look for an existing PROCAR in the projectors directory."""
    candidates = [
        ROOT / "examples" / "projectors" / "lreal_false" / "PROCAR",
        ROOT / "examples" / "projectors" / "lreal_true" / "PROCAR",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def _write_minimal_procar(dst: Path) -> None:
    """Write a minimal synthetic PROCAR the parser can read.

    Format matches the VASP PROCAR lm decomposed output with 1 k-point,
    2 bands, and 1 ion.
    """
    content = """\
PROCAR lm decomposed
# of k-points:    1         # of bands:    2         # of ions:    1

 k-point     1 :    0.00000000 0.00000000 0.00000000     weight = 1.00000000

band     1 # energy   0.00000000 # occ.  2.00000000

ion      s     py     pz     px    dxy    dyz    dz2    dxz  x2-y2    tot
    1  1.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  1.000
tot    1.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  1.000

band     2 # energy   0.50000000 # occ.  0.00000000

ion      s     py     pz     px    dxy    dyz    dz2    dxz  x2-y2    tot
    1  0.000  1.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  1.000
tot    0.000  1.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  1.000
"""
    dst.write_text(content)
    print(f"Wrote synthetic PROCAR to {dst}")


def main() -> int:
    exdir = Path.cwd()
    procar_path = exdir / "PROCAR"

    # Try existing PROCAR from projectors first
    src = _find_procar()
    if src is not None:
        print(f"Using PROCAR from {src}")
        # Symlink or copy
        if not procar_path.exists():
            procar_path.write_text(src.read_text())
    else:
        print("No projectors PROCAR found -- generating synthetic minimal PROCAR")
        _write_minimal_procar(procar_path)

    # Parse via the procar module
    try:
        pc = procar(str(procar_path))
    except Exception as exc:
        print(f"FAILED to parse PROCAR: {exc}")
        return 1

    # Dump a simple table
    Path("ref").mkdir(exist_ok=True)
    lines: list[str] = []
    lines.append("# Band  Energy  s  py  pz  px  dxy  dyz  dz2  dxz  dx2-y2")
    for ispin in range(pc._nspin):
        for ikpt in range(pc._nkpts):
            for iband in range(pc._nbands):
                energy = pc._eband[ispin, ikpt, iband]
                # Sum over ions for this (ispin, ikpt, iband)
                proj = pc._aproj[ispin, ikpt, iband]  # shape (nions, nlmax)
                total = proj.sum(axis=0)  # sum over ions
                row = f"  {iband + 1:4d}  {energy:8.4f}"
                for v in total:
                    row += f"  {v:6.3f}"
                lines.append(row)

    text = "\n".join(lines) + "\n"
    Path("ref/procar_table.txt").write_text(text)
    print(f"Wrote ref/procar_table.txt ({len(lines)} rows)")

    print(f"  nspin={pc._nspin}  nkpts={pc._nkpts}  nbands={pc._nbands}  nions={pc._nions}")
    print(f"  orbital channel count (nlmax)={pc._nlmax}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
