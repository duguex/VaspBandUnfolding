# Feature Inventory

Single checklist of **VaspBandUnfolding** (PyVaspWfc): module, CLI, example, engineering status, and academic level.

**Live status:** [`docs/STATUS.md`](docs/STATUS.md) · **Citation:** [`docs/CITATION_POLICY.md`](docs/CITATION_POLICY.md) · **C1/C2 matrix:** [`docs/EXAMPLE_MATRIX.md`](docs/EXAMPLE_MATRIX.md)

Companion: [`docs/GOALS.md`](docs/GOALS.md) · [`docs/ASSUMPTIONS.md`](docs/ASSUMPTIONS.md) · [`docs/ACADEMIC_ROADMAP.md`](docs/ACADEMIC_ROADMAP.md) · [`AGENTS.md`](AGENTS.md)

---

## Legends

### Engineering status

| Status | Meaning |
|---|---|
| **ready** | Importable; usable with bundled or typical VASP outputs |
| **optional-dep** | Needs optional package (`pySBT`, `spglib`, …) |
| **needs-data** | Code works; large/local dumps not in git (see `docs/repro/`) |
| **partial** | Runnable; accuracy vs VASP incomplete for some modes |
| **infra** | Support library (tests, not a science demo) |

### Validation / citation (align with CITATION_POLICY)

| Level | Meaning |
|---|---|
| **L0** | Implementation exists |
| **L1** | Internal / analytic consistency |
| **L2-partial** | Partial gates vs VASP/ref; not full parity |
| **L2** | Same-input vs VASP/ref suitable for careful citation |
| **quarantine** | Known residual / incomplete — do not cite as validated |

Only **L2** (and carefully worded **L2-partial**) should appear as validation claims. Never cite **quarantine** as production accuracy.

### Seminar slots

`S1`…`S8` — [`docs/ACADEMIC_ROADMAP.md`](docs/ACADEMIC_ROADMAP.md).

CLI: `bsematrix` is in `pyproject.toml` `script-files`. Default `--mode pw_only`.

---

## Master table

| ID | Feature | Module / API | CLI | Example | Eng. | Level | Seminar | Notes |
|---|---|---|---|---|---|---|---|---|
| W1 | WAVECAR I/O | `vaspwfc` | — | `examples/wfc_r/` | ready | **L2-partial** | S1 | std / γ / ncl flags |
| W2 | G-vectors / cutoff | `vaspwfc` | — | via W1 | ready | **L1–L2** | S1 | vs OUTCAR G-count |
| W3 | Real-space PS wfc | `wfc_r`, `save2vesta` | `wfcplot` | `examples/wfc_r/` | ready | **L2-partial** | S1 | VESTA grids |
| W4 | PS dipole | `get_dipole_mat` | `tdmplot` | `examples/tdm/` | ready | **L2-partial** | S3 | CO2 gates `ref/l2_table.md`; WAVEDER not fully decoded |
| W5 | IPR | IPR helpers | — | `examples/ipr/` | ready | **L0–L1** | S3 | experimental |
| W6 | ELF | `elf` | — | `examples/elf_test/` | ready | **L2-partial** | S3 | vs ELFCAR corr≈0.986 |
| B1 | Band unfolding | `unfold` | — | `examples/unfold/*` | needs-data | **L1–L2** | S2 | npy demos; PS weights |
| B2 | Unfold + weights | `unfold`+PROCAR | — | `Ce@BL-MoS2_*` | needs-data | **L1** | S2 | experimental |
| B3 | Band reorder | `reorder_band` | — | `examples/band_reorder/` | ready | **L1** | S2 | multi-k; PS overlaps |
| B4 | PROCAR | `procar` | — | `examples/procar/` | ready | **L0–L1** | S2 | parse demo |
| B5 | IBZ k | `hse_kpts` | — | `examples/hse_kpts/` | optional-dep | **L0–L1** | S8 | **spglib** |
| P1 | POTCAR / partial waves | `pawpotcar` | `potplot` | `potplot/`, `projectors/` | ready | **L2-partial** | S4 | |
| P2 | Nonlocal projectors | `nonlq`/`nonlr` | — | `examples/projectors/` | ready | **L2-partial** | S4 | vs NormalCar |
| P3 | \(Q_{ij}\), \(\nabla_{ij}\) | `get_Qij`, … | — | `projectors/` | ready | **L1–L2** | S4 | |
| P4 | AE wavefunction | `vasp_ae_wfc` | — | `examples/aewfc/co2/` | optional-dep | **L2-partial** | S4 | **pySBT** |
| P5 | AE dipole | `aewfc.get_dipole_mat` | `tdmplot` | `examples/tdm/` | optional-dep | **L0–L1** | S3 | experimental |
| O1 | SOC PAW matrix | `spinorb` | — | `examples/spinor/` | needs-data | **L2-partial** | S5 | Soc\* via patched VASP |
| O2 | Spinor WAVECAR | `spinor` / `spinormaker` | `spinormaker` | `examples/spinor/` | needs-data | **L2-partial** | S5 | vs ncl MAE~5 meV |
| O3 | MAE helpers | `get_mae`, … | — | via spinor dumps | needs-data | **L0–L1** | S5 | experimental |
| X1 | BSE matrix | `bsematrix` | `bsematrix` | `examples/bsematrix/BP/` | partial | **L2-partial** | S6 | **default `pw_only`** |
| X2 | BSE `paw_*` modes | `--mode` | same | BP tables | partial | **quarantine** | S6 | do not cite as parity |
| X3 | Finite-q BSE | `--q-ext` | same | BP qext | partial | **quarantine** | S6 | do not cite |
| X4 | WFULL | `wfull` | — | `examples/wfull/` | ready | **L1** | S6 | infra demo |
| X5 | Exciton BZ | `bsefatband` | `bseplot bz` | `examples/bseplot/` | ready | **L2-partial** | S7 | bundled BSEFATBAND |
| X6 | Exciton realspace | `bsefatband` | `bseplot realspace` | `run_realspace.sh` | needs-data | **L1** | S7 | matching WAVECAR external |
| D1 | NAC | `nac_from_vaspwfc` | — | `examples/nac/` | needs-data | **L2-partial** | S8 | dual CO2 frames (local) |
| D2 | NEB path | — | `nebplot` | `examples/neb/` | ready | **L0–L1** | S8 | synthetic OUTCARs ok for smoke |
| D3 | Ewald / Madelung | `ewaldsum` | — | `examples/ewald/` | ready | **L2-partial** | S8 | classical refs |
| I1 | Constants | `vasp_constant` | — | tests | infra | **L2** | S1 | |
| I2 | Spherical harmonics | `sph_harm` | — | tests | infra | **L1–L2** | S4 | |
| I3 | Spline SPLCOF | `spline` | — | tests | infra | **L1** | S4 | |
| I4 | Fortran records | `wfull` / WAVECAR | — | tests + `wfull/` | infra | **L1** | S1 | |

---

## CLI summary

| ID | Command | Installed? | Feature IDs |
|---|---|---|---|
| C1 | `wfcplot` | yes | W3 |
| C2 | `tdmplot` | yes | W4, P5 |
| C3 | `potplot` | yes | P1 |
| C4 | `nebplot` | yes | D2 |
| C5 | `bseplot` | yes | X5, X6 |
| C6 | `spinormaker` | yes | O2 |
| C7 | `bsematrix` | yes | X1–X3 (default **pw_only**) |

---

## Dependencies

| Package | Feature IDs | Declared? |
|---|---|---|
| numpy, scipy, matplotlib, ase | core | yes |
| pySBT | P4, P5 | optional |
| spglib | B5 | optional (`requirements-optional.txt`) |

---

## Verify

```bash
python scripts/smoke_examples.py
PYTHONPATH=. python -m pytest tests/ -q
```

Details: [`docs/STATUS.md`](docs/STATUS.md).
