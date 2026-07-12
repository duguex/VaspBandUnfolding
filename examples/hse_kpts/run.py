#!/usr/bin/env python3
"""Compute irreducible k-points (IBZ) for a simple POSCAR using spglib."""

try:
    import spglib  # noqa: F401
except ImportError:
    raise SystemExit(2)  # skip when spglib unavailable

import sys
from pathlib import Path

import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from hse_kpts import get_ir_kpts  # type: ignore[import-untyped]


def main() -> int:
    poscar = Path("POSCAR")
    if not poscar.is_file():
        print("MISSING: POSCAR", file=sys.stderr)
        return 2

    atoms = read(str(poscar))
    # Use a small mesh for a fast result
    kpts = get_ir_kpts(atoms, [10, 10, 10])
    print(f"Number of irreducible k-points: {kpts.shape[0]}")
    print(f"IBZ k-points (frac coords + weight):")
    for row in kpts:
        print(f"  {row[0]:.8f}  {row[1]:.8f}  {row[2]:.8f}  weight={row[3]:.1f}")

    Path("ref").mkdir(exist_ok=True)
    np.savetxt(Path("ref/ibz.txt"), kpts, fmt="%.8f", header="kx ky kz weight")
    print("Wrote ref/ibz.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
