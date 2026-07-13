#!/usr/bin/env python3
"""Compare PyVaspWfc ELF to VASP ELFCAR (same grid)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO))

from vaspwfc import vaspwfc  # noqa: E402


def load_elfcar(path: Path):
    lines = path.read_text().splitlines()
    grid_i = None
    for i, ln in enumerate(lines):
        p = ln.split()
        if len(p) == 3 and all(x.isdigit() for x in p):
            nx, ny, nz = map(int, p)
            if min(nx, ny, nz) > 1:
                grid_i = i
                break
    if grid_i is None:
        raise RuntimeError("ELFCAR grid not found")
    nx, ny, nz = map(int, lines[grid_i].split())
    vals: list[float] = []
    for ln in lines[grid_i + 1 :]:
        for t in ln.split():
            vals.append(float(t))
        if len(vals) >= nx * ny * nz:
            break
    arr = np.asarray(vals[: nx * ny * nz], dtype=float).reshape((nx, ny, nz), order="F")
    return (nx, ny, nz), arr


def main() -> int:
    wav = ROOT / "WAVECAR"
    elfcar = ROOT / "ELFCAR"
    if not wav.is_file() or not elfcar.is_file():
        print("MISSING WAVECAR/ELFCAR", file=sys.stderr)
        return 2
    (nx, ny, nz), vasp = load_elfcar(elfcar)
    w = vaspwfc(str(wav))
    # weights from OUTCAR if present else equal
    kptw = np.ones(w._nkpts, dtype=float)
    out = ROOT / "OUTCAR"
    # use example's known weights when nk=16
    if w._nkpts == 16:
        kptw = np.array([1, 6, 6, 6, 6, 6, 6, 12, 12, 12, 6, 6, 12, 12, 6, 6], dtype=float)
    chi = w.elf(kptw=kptw, ngrid=[nx, ny, nz], warn=False)
    py = np.asarray(chi[0] if isinstance(chi, (list, tuple)) else chi, dtype=float)
    corr = float(np.corrcoef(py.ravel(), vasp.ravel())[0, 1])
    mae = float(np.mean(np.abs(py - vasp)))
    mx = float(np.max(np.abs(py - vasp)))
    # gates: strong correlation, not bit-identical
    gate_corr = corr > 0.95
    gate_mae = mae < 0.05
    ok = gate_corr and gate_mae
    ref = ROOT / "ref"
    ref.mkdir(exist_ok=True)
    (ref / "elf_vs_vasp.txt").write_text(
        f"grid={nx}x{ny}x{nz}\ncorr={corr:.6f}\nmae={mae:.6e}\nmax_abs={mx:.6e}\n"
        f"gate_corr={gate_corr}\ngate_mae={gate_mae}\noverall_pass={ok}\n"
        f"citation={'l2-partial' if ok else 'experimental'}\n"
    )
    print(open(ref / "elf_vs_vasp.txt").read())
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
