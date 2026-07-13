# Citation policy (what you may claim)

Companion: [`FEATURES.md`](../FEATURES.md) · [`ASSUMPTIONS.md`](ASSUMPTIONS.md)

| Label | Meaning | Example use in a paper |
|---|---|---|
| **yes / L2** | Same-input check vs VASP or standard ref in-repo | “Computed with PyVaspWfc, validated against …” |
| **l2-partial** | Partial gates pass; full parity not claimed | “Workflow via PyVaspWfc; partial validation …” |
| **experimental** | Runs; scientific agreement not established | Methods tool mention only; no “agrees with VASP” |
| **quarantine** | Known mismatch or incomplete physics | Do **not** use for production claims |

## Per-feature snapshot (maintain with EXAMPLE_MATRIX)

| IDs | Component | Citation now | Evidence |
|---|---|---|---|
| W1–W3 | WAVECAR / real-space PS | **l2-partial** | `examples/wfc_r` smoke + widespread use |
| W4 | PS dipole | **l2-partial** | `examples/tdm/ref/l2_table.md` (CO2 gates) |
| W5 | IPR | **experimental** | analytic/demo only |
| W6 | ELF | **experimental / quarantine** | unvalidated vs ELFCAR |
| B1–B2 | Unfold | **l2-partial** | npy/EBS demos; PS-only weights |
| B3 | Band reorder | **experimental** | works on multi-k WAVECAR |
| B4 | PROCAR | **experimental** | parse demo |
| B5 | IBZ k | **experimental** | needs spglib |
| P1–P3 | POTCAR / projectors / Qij | **l2-partial** | NormalCar suite |
| P4 | AE wfc | **l2-partial** | CO2 + pySBT |
| P5 | AE dipole | **experimental** | no L2 table yet |
| O1–O2 | SOC matrix / spinormaker | **l2-partial** | local patched VASP dumps + spinor read |
| O3 | MAE helpers | **experimental** | not gated |
| X1 | BSE `pw_only` | **l2-partial → cite BP tables carefully** | `examples/bsematrix/BP` |
| X2–X3 | BSE paw / finite-q | **quarantine** | large residuals |
| X4 | WFULL reader | **experimental** | infra |
| X5 | Exciton BZ | **l2-partial** | `bseplot` demo |
| X6 | Exciton realspace | **experimental** | needs matching WAVECAR |
| D1 | NAC | **experimental** | smoke with identical frames |
| D2 | NEB plot | **experimental** | synthetic OUTCARs |
| D3 | Ewald | **l2-partial** | Madelung demo + test |

## Hard rules

1. Never present **quarantine** modes as default recommendations.
2. Pin package git commit + VASP version when claiming validation.
3. Personal fork only; no upstream PRs unless explicitly requested.
