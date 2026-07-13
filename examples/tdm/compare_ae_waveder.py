#!/usr/bin/env python3
"""AE (PAW one-center) vs PS dipoles vs VASP WAVEDER CDER.

Physical notes
--------------
* WAVEDER stores CDER = -<r> from VASP optics (PAW-complete k-derivative path).
* ``vaspwfc.get_dipole_mat`` is plane-wave PS + molecular p–r only.
* ``aewfc.get_dipole_mat`` adds PAW nabla one-center terms to the *momentum*,
  then still uses p–r → length gauge.

Empirically on CO2 (this suite): AE ≠ CDER element-wise; AE can differ from PS
where one-center terms matter.  Pass gate is **infrastructure + nonzero AE path**,
not full CDER L2.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aewfc import vasp_ae_wfc  # noqa: E402
from vasp_constant import AUTDEBYE  # noqa: E402
from vaspwfc import vaspwfc  # noqa: E402
from waveder import read_waveder  # noqa: E402

WORK = Path(__file__).resolve().parent / "vasp_optics" / "work"
REF = Path(__file__).resolve().parent / "ref"

MIN_DE = 0.5
MIN_BOTH = 0.05
MIN_PAIRS = 3


def main() -> int:
    need = [WORK / "WAVECAR", WORK / "WAVEDER", WORK / "POSCAR", WORK / "POTCAR"]
    for p in need:
        if not p.is_file():
            print(f"MISSING {p}", file=sys.stderr)
            return 2

    wfc = vaspwfc(str(WORK / "WAVECAR"))
    ae = vasp_ae_wfc(wfc, poscar=str(WORK / "POSCAR"), potcar=str(WORK / "POTCAR"))
    wd = read_waveder(WORK / "WAVEDER")
    nocc = int(np.sum(wfc._occs[0, 0] > 0.5))

    rows = []
    n_ae_diff = 0
    for n in range(1, nocc + 1):
        if n > wd.nbands_cder:
            continue
        for m in range(nocc + 1, wd.nbands + 1):
            out_ae = ae.get_dipole_mat((1, 1, n), (1, 1, m))
            out_ps = wfc.get_dipole_mat((1, 1, n), (1, 1, m))
            if isinstance(out_ae, float) or isinstance(out_ps, float):
                continue
            de = float(out_ae[2])
            if abs(de) < MIN_DE:
                continue
            r_ae = np.asarray(out_ae[3], dtype=np.complex128) / AUTDEBYE
            r_ps = np.asarray(out_ps[3], dtype=np.complex128) / AUTDEBYE
            r_wd = wd.r_matrix(m=m, n=n)
            aa = float(np.max(np.abs(r_ae)))
            ap = float(np.max(np.abs(r_ps)))
            aw = float(np.max(np.abs(r_wd)))
            err_ae = float(np.max(np.abs(r_ae - r_wd)))
            err_ps = float(np.max(np.abs(r_ps - r_wd)))
            d_ae_ps = float(np.max(np.abs(r_ae - r_ps)))
            if d_ae_ps > 1e-6 * max(aa, ap, 1e-12):
                n_ae_diff += 1
            rows.append(
                {
                    "n": n,
                    "m": m,
                    "dE": de,
                    "abs_ae": aa,
                    "abs_ps": ap,
                    "abs_wd": aw,
                    "rel_ae": err_ae / max(aa, aw, 1e-12),
                    "rel_ps": err_ps / max(ap, aw, 1e-12),
                    "d_ae_ps": d_ae_ps,
                }
            )

    both = [
        r
        for r in rows
        if r["abs_ae"] >= MIN_BOTH and r["abs_wd"] >= MIN_BOTH
    ]
    parse_ok = float(np.max(np.abs(wd.cder))) > 0 and np.isfinite(wd.cder).all()
    ae_active = n_ae_diff >= 1
    pass_ok = parse_ok and ae_active and len(both) >= MIN_PAIRS

    REF.mkdir(exist_ok=True)
    lines = [
        f"nocc={nocc} nbands={wd.nbands} nbands_cder={wd.nbands_cder}",
        f"pairs={len(rows)} both_sig={len(both)} ae_diff_pairs={n_ae_diff}",
        f"parse_ok={parse_ok} ae_one_center_active={ae_active}",
    ]
    if both:
        lines += [
            f"both_median_rel_ae={float(np.median([r['rel_ae'] for r in both])):.6f}",
            f"both_median_rel_ps={float(np.median([r['rel_ps'] for r in both])):.6f}",
            "top_both n m dE abs_ae abs_ps abs_wd rel_ae rel_ps",
        ]
        for r in sorted(both, key=lambda x: -min(x["abs_ae"], x["abs_wd"]))[:8]:
            lines.append(
                f"  {r['n']:3d} {r['m']:3d} {r['dE']:8.3f} "
                f"{r['abs_ae']:.3e} {r['abs_ps']:.3e} {r['abs_wd']:.3e} "
                f"{r['rel_ae']:.3f} {r['rel_ps']:.3f}"
            )
    lines.append(f"overall_pass={pass_ok}")
    lines.append(
        "note=AE/PAW path runs and differs from PS on some pairs; "
        "neither matches WAVEDER CDER element-wise (VASP optics vs p-r). "
        "Citation remains l2-partial for W4/P5."
    )
    text = "\n".join(lines) + "\n"
    (REF / "ae_waveder_summary.txt").write_text(text)
    print(text)

    (REF / "ae_waveder_table.md").write_text(
        "\n".join(
            [
                "# AE/PAW vs PS vs WAVEDER (CO2)",
                "",
                f"- AE one-center active pairs: **{n_ae_diff}**",
                f"- Both-significant pairs: **{len(both)}**",
                f"- Pass (decode + AE active + both-sig): **{pass_ok}**",
                "",
                "Do not claim element-wise agreement with WAVEDER CDER.",
                "",
            ]
        )
    )
    return 0 if pass_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
