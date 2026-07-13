# Citation policy (what you may claim)

Companion: [`FEATURES.md`](../FEATURES.md) · [`STATUS.md`](STATUS.md) · [`ASSUMPTIONS.md`](ASSUMPTIONS.md) · [`EXAMPLE_MATRIX.md`](EXAMPLE_MATRIX.md)

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
| W4 | PS dipole | **l2-partial** | `examples/tdm/ref/l2_table.md` (CO2 gates; WAVEDER not fully decoded) |
| W5 | IPR | **experimental** | analytic/demo only |
| W6 | ELF | **l2-partial** | `examples/elf_test/ref/elf_vs_vasp.txt` (corr≳0.98 demo) |
| B1–B2 | Unfold | **l2-partial** | npy/EBS demos; PS-only weights |
| B3 | Band reorder | **experimental** | multi-k WAVECAR |
| B4 | PROCAR | **experimental** | parse demo |
| B5 | IBZ k | **experimental** | needs spglib |
| P1–P3 | POTCAR / projectors / Qij | **l2-partial** | NormalCar suite |
| P4 | AE wfc | **l2-partial** | CO2 + pySBT |
| P5 | AE dipole | **experimental** | no L2 table yet |
| O1–O2 | SOC matrix / spinormaker | **l2-partial** | dumps + spinormaker; vs SCF ncl MAE~5 meV |
| O3 | MAE helpers | **experimental** | not gated |
| X1 | BSE `pw_only` | **l2-partial** | BP tables; **CLI default** |
| X2–X3 | BSE paw / finite-q | **quarantine** | large residuals |
| X4 | WFULL reader | **experimental** | infra |
| X5 | Exciton BZ | **l2-partial** | `bseplot` demo |
| X6 | Exciton realspace | **experimental** | matching WAVECAR external (`docs/repro/X6_exciton_rs.md`) |
| D1 | NAC | **l2-partial** | dual CO2 frames (local); nonzero NAC |
| D2 | NEB plot | **experimental** | synthetic OUTCARs |
| D3 | Ewald | **l2-partial** | Madelung demo + tests |

## Hard rules

1. Never present **quarantine** modes as default recommendations (BSE CLI already defaults to `pw_only`).
2. Pin package git commit + VASP version when claiming validation.
3. Personal fork only; no upstream PRs unless explicitly requested.
4. Prefer [`STATUS.md`](STATUS.md) for “what runs on this machine right now”.
