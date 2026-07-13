#!/usr/bin/env python3
"""Decode VASP WAVEDER and compare to PS-only p–r dipoles (honest gate).

WAVEDER ``CDER`` is VASP's length-gauge matrix (includes PAW completeness in the
optics path).  ``vaspwfc.get_dipole_mat`` is **plane-wave pseudo only** via the
molecular p–r relation — it is **not** expected to match CDER element-wise.

Pass criteria (L2-partial infrastructure):
  1. WAVEDER parses (shapes, finite CDER).
  2. At least a few occ→virt pairs have both |r_PS| and |r_CDER| above a floor
     (pipeline sanity).
  3. Report median relative |r_PS − r_CDER| for those pairs (informational;
     no tight threshold — PAW gap is the physics).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vasp_constant import AUTDEBYE  # noqa: E402
from vaspwfc import vaspwfc  # noqa: E402
from waveder import read_waveder  # noqa: E402

WORK = Path(__file__).resolve().parent / "vasp_optics" / "work"
REF = Path(__file__).resolve().parent / "ref"

MIN_BOTH_ANG = 0.05
MIN_DE_EV = 0.3
MIN_BOTH_SIGNIFICANT = 3


def main() -> int:
    wavecar = WORK / "WAVECAR"
    wder_path = WORK / "WAVEDER"
    if not wavecar.is_file() or not wder_path.is_file():
        print("MISSING WAVECAR or WAVEDER under vasp_optics/work", file=sys.stderr)
        return 2

    wfc = vaspwfc(str(wavecar))
    wd = read_waveder(wder_path)
    nocc = int(np.sum(wfc._occs[0, 0] > 0.5))

    rows = []
    for n in range(1, nocc + 1):
        for m in range(nocc + 1, wd.nbands + 1):
            if n > wd.nbands_cder:
                continue
            out = wfc.get_dipole_mat((1, 1, n), (1, 1, m))
            if isinstance(out, float):
                continue
            _em, _en, de, dip = out
            if abs(de) < MIN_DE_EV:
                continue
            r_ps = np.asarray(dip, dtype=np.complex128) / AUTDEBYE
            r_wd = wd.r_matrix(m=m, n=n)
            ap = float(np.max(np.abs(r_ps)))
            aw = float(np.max(np.abs(r_wd)))
            err = float(np.max(np.abs(r_ps - r_wd)))
            rows.append(
                {
                    "n": n,
                    "m": m,
                    "dE": float(de),
                    "abs_ps": ap,
                    "abs_wd": aw,
                    "abs_err": err,
                    "rel": err / max(ap, aw, 1e-12),
                }
            )

    both = [
        r
        for r in rows
        if r["abs_ps"] >= MIN_BOTH_ANG and r["abs_wd"] >= MIN_BOTH_ANG
    ]
    cder_finite = bool(np.isfinite(wd.cder).all()) and float(np.max(np.abs(wd.cder))) > 0

    REF.mkdir(exist_ok=True)
    lines = [
        f"waveder_nbands={wd.nbands}",
        f"waveder_nbands_cder={wd.nbands_cder}",
        f"nkpts={wd.nkpts} nspin={wd.nspin} nocc={nocc}",
        f"nodes={wd.nodes_in_dielectric_function:.6f}",
        f"cder_max_abs={float(np.max(np.abs(wd.cder))):.6e}",
        f"cder_finite={cder_finite}",
        f"occ_virt_pairs={len(rows)} both_significant={len(both)}",
        f"floor_Ang={MIN_BOTH_ANG} min_dE_eV={MIN_DE_EV}",
    ]
    if both:
        rels = [r["rel"] for r in both]
        lines += [
            f"both_median_rel={float(np.median(rels)):.6f}",
            f"both_max_rel={float(np.max(rels)):.6f}",
            "top_both n m dE abs_ps abs_wd rel",
        ]
        for r in sorted(both, key=lambda x: -min(x["abs_ps"], x["abs_wd"]))[:8]:
            lines.append(
                f"  {r['n']:3d} {r['m']:3d} {r['dE']:9.4f} "
                f"{r['abs_ps']:.4e} {r['abs_wd']:.4e} {r['rel']:.4f}"
            )
        median_rel = float(np.median(rels))
    else:
        median_rel = float("nan")
        lines.append("both_median_rel=nan")

    parse_ok = cder_finite and wd.cder.shape[0] == wd.nbands
    pass_ok = parse_ok and len(both) >= MIN_BOTH_SIGNIFICANT
    lines.append(f"parse_ok={parse_ok}")
    lines.append(f"overall_pass={pass_ok}")
    lines.append(
        "note=CDER is VASP optics (PAW-complete); PS p-r is not element-wise L2. "
        "Gate = decode + both-significant pairs exist."
    )
    text = "\n".join(lines) + "\n"
    (REF / "waveder_summary.txt").write_text(text)
    print(text)

    md = [
        "# WAVEDER reader vs PS p–r (CO2)",
        "",
        f"- Reader: NB={wd.nbands}, NB_CDER={wd.nbands_cder}, "
        f"max|CDER|={float(np.max(np.abs(wd.cder))):.3e}",
        f"- Occ→virt pairs with both |r|≥{MIN_BOTH_ANG} Å: **{len(both)}**",
        f"- Median |r_PS−r_CDER|/max (informational): **{median_rel}**",
        f"- Pass (decode + ≥{MIN_BOTH_SIGNIFICANT} both-significant): **{pass_ok}**",
        "",
        "Do **not** cite PS `get_dipole_mat` as WAVEDER-parity. "
        "Use WAVEDER as the VASP length-gauge reference; PS path remains L2-partial "
        "via optics selection rules (`ref/l2_table.md`).",
        "",
    ]
    (REF / "waveder_table.md").write_text("\n".join(md))
    return 0 if pass_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
