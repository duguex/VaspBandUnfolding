#!/usr/bin/env python3
"""CO2 PS dipole L2-partial checks against a local LOPTICS VASP run.

Gates (honest / molecular):
1. WAVECAR band energies match OUTCAR eigenvalues for sampled bands.
2. HOMO→LUMO (degenerate π) dipole is dark (|r|_max small).
3. At least one low-lying occ→virt transition is bright (|r|_max large).

Im(ε) from LOPTICS in a small-molecule supercell is a broadened continuum and
is **not** used as a hard energy gate here.

Exit: 0 all gates pass, 1 gate fail, 2 missing data.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO))

from vaspwfc import vaspwfc  # noqa: E402


def find_work() -> Path:
    for p in (
        ROOT / "vasp_optics" / "work",
        ROOT / "vasp_optics" / "output",
        ROOT / "vasp_optics",
    ):
        wav = p / "WAVECAR"
        if wav.is_file() and wav.stat().st_size > 1000:
            return p
    raise FileNotFoundError("No usable WAVECAR under examples/tdm/vasp_optics")


def parse_nelect(outcar: Path) -> float:
    m = re.search(r"NELECT\s*=\s*([\d.]+)", outcar.read_text(errors="replace"))
    if not m:
        raise ValueError("NELECT not found in OUTCAR")
    return float(m.group(1))


def parse_outcar_eigs(outcar: Path, nbands: int) -> np.ndarray:
    """Parse first k-point band energies from OUTCAR (spin-unpolarized)."""
    lines = outcar.read_text(errors="replace").splitlines()
    # look for last "k-point" band block
    idx = None
    for i, ln in enumerate(lines):
        if re.search(r"k-point\s+1\s*:", ln) and "band No" in lines[i + 1]:
            idx = i + 2
    if idx is None:
        # alternate: EIGENVAL-like section
        for i, ln in enumerate(lines):
            if "band No." in ln and "occupation" in ln:
                idx = i + 1
                break
    if idx is None:
        raise ValueError("Could not find eigenvalue table in OUTCAR")
    eigs = []
    for ln in lines[idx:]:
        parts = ln.split()
        if len(parts) < 3:
            if eigs:
                break
            continue
        try:
            band_no = int(parts[0])
            ene = float(parts[1])
        except ValueError:
            if eigs:
                break
            continue
        eigs.append(ene)
        if band_no >= nbands:
            break
    arr = np.asarray(eigs[:nbands], dtype=float)
    if arr.size < nbands:
        raise ValueError(f"Only parsed {arr.size}/{nbands} eigenvalues")
    return arr


def main() -> int:
    try:
        work = find_work()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 2

    wav = work / "WAVECAR"
    outcar = work / "OUTCAR"
    if not outcar.is_file():
        print("MISSING OUTCAR", file=sys.stderr)
        return 2

    wfc = vaspwfc(str(wav))
    nb = int(wfc._nbands)
    nelect = parse_nelect(outcar)
    nocc = int(nelect // 2)
    e_wfc = np.asarray(wfc._bands[0, 0, :], dtype=float)
    e_out = parse_outcar_eigs(outcar, nb)
    e_err = float(np.max(np.abs(e_wfc - e_out)))

    rows = []
    for i in range(max(1, nocc - 2), nocc + 1):
        for j in range(nocc + 1, min(nb, nocc + 5) + 1):
            Emk, Enk, dE, dip = wfc.get_dipole_mat((1, 1, i), (1, 1, j))
            dip = np.atleast_1d(np.asarray(dip, dtype=np.complex128))
            abs_max = float(np.max(np.abs(dip))) if dip.size else 0.0
            rows.append((i, j, float(Emk), float(Enk), float(dE), abs_max))

    # CO2: bands nocc-1 and nocc are degenerate HOMOs; LUMO ~ nocc+1
    dark = [r for r in rows if r[0] in (nocc - 1, nocc) and r[1] == nocc + 1]
    dark_max = max((r[5] for r in dark), default=0.0)
    bright_max = max((r[5] for r in rows), default=0.0)
    bright = max(rows, key=lambda r: r[5]) if rows else None

    gate_eig = e_err < 1e-4  # eV
    gate_dark = dark_max < 1e-3  # Debye
    gate_bright = bright_max > 0.1  # Debye
    ok = gate_eig and gate_dark and gate_bright

    ref = ROOT / "ref"
    ref.mkdir(exist_ok=True)
    lines = [
        "# CO2 dipole L2-partial table",
        "",
        f"- workdir: `{work}`",
        f"- NELECT={nelect}, nocc={nocc}, nbands={nb}",
        f"- max |E_WAVECAR - E_OUTCAR| = {e_err:.3e} eV → "
        f"{'PASS' if gate_eig else 'FAIL'} (<1e-4 eV)",
        f"- HOMO→LUMO dark |r|_max = {dark_max:.3e} Debye → "
        f"{'PASS' if gate_dark else 'FAIL'} (<1e-3)",
        f"- brightest |r|_max = {bright_max:.3e} Debye → "
        f"{'PASS' if gate_bright else 'FAIL'} (>0.1)",
        "",
        "| i | j | E_i (eV) | E_j (eV) | dE (eV) | |r|_max (Debye) |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for i, j, em, en, de, am in rows:
        lines.append(
            f"| {i} | {j} | {em:.6f} | {en:.6f} | {de:.6f} | {am:.6e} |"
        )
    lines += [
        "",
        "## Notes",
        "",
        f"- brightest pair: {bright[0]}→{bright[1]}" if bright else "",
        "- Im(ε) continuum onset is **not** used as a hard gate for this "
        "molecular supercell IPA spectrum.",
        "- Length-gauge p–r for finite systems only (ASSUMPTIONS).",
        "",
        "## Citation",
        "",
        "- **l2-partial** if all three gates PASS.",
        "- Not full L2 vs VASP element-wise optics matrix elements.",
        "",
        f"**Overall: {'PASS' if ok else 'FAIL'}**",
        "",
    ]
    (ref / "l2_table.md").write_text("\n".join(lines))
    (ref / "l2_summary.txt").write_text(
        f"workdir={work}\n"
        f"e_err_eV={e_err}\n"
        f"dark_max_Debye={dark_max}\n"
        f"bright_max_Debye={bright_max}\n"
        f"gate_eig={gate_eig}\n"
        f"gate_dark={gate_dark}\n"
        f"gate_bright={gate_bright}\n"
        f"overall_pass={ok}\n"
    )
    print(open(ref / "l2_summary.txt").read())
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
