# Feature Inventory

Single checklist of **VaspBandUnfolding** (PyVaspWfc) capabilities: module, CLI, example, engineering status, and **academic traceability** (ID / validation level / seminar).

Companion docs:

- Expert full-coverage plan: [`docs/ACADEMIC_ROADMAP.md`](docs/ACADEMIC_ROADMAP.md)
- Assumptions & limits: [`docs/ASSUMPTIONS.md`](docs/ASSUMPTIONS.md)
- Usage: [`README.md`](README.md) · Dev: [`AGENTS.md`](AGENTS.md)

---

## Legends

### Engineering status

| Status | Meaning |
|---|---|
| **ready** | Importable; usable with bundled or typical VASP outputs |
| **optional-dep** | Works after installing an optional package |
| **needs-data** | Code works; repo lacks large inputs (`WAVECAR`, `SocCar`, …) for a full demo |
| **partial** | Runnable, but accuracy vs VASP is incomplete or still under validation |
| **unverified** | Implemented; author/docs mark as not fully tested |
| **no-example** | Library/CLI exists; no dedicated `examples/` demo |
| **infra** | Support library (always in scope for tests/docs, not a standalone science demo) |

### Validation level (academic)

| Level | Meaning |
|---|---|
| **L0** | Implementation exists |
| **L1** | Internal / analytic consistency |
| **L2** | Same-input vs VASP or standard reference |
| **L3** | Multi-system + literature / independent code |

Only **L2+** should be presented as “agrees with VASP” in seminars. Details: [`docs/ACADEMIC_ROADMAP.md`](docs/ACADEMIC_ROADMAP.md).

### Seminar slots

`S1`…`S8` — see roadmap §4. `—` = appendix / with parent feature.

CLI install note: **`bsematrix`** is in `bin/` but **not** in `pyproject.toml` `script-files` — use `python bsematrix.py` or `python bin/bsematrix`.

---

## Master table (all feature IDs)

| ID | Feature | Module / API | CLI | Example | Eng. status | Level | Seminar | Notes |
|---|---|---|---|---|---|---|---|---|
| W1 | WAVECAR I/O (std / γ-only / ncl) | `vaspwfc.vaspwfc` | — | `examples/wfc_r/` | **ready** | **L2** | S1 | `lgamma`, `lsorbit`, `gamma_half`; see ASSUMPTIONS §2 |
| W2 | G-vector set / cutoff sphere | `vaspwfc` G helpers | — | via W1/OUTCAR | **ready** | **L1–L2** | S1 | Compare G-count to OUTCAR |
| W3 | Real-space PS wavefunction | `wfc_r` / `get_ps_wfc`, `save2vesta` | `wfcplot` | `examples/wfc_r/` | **ready** | **L2** | S1 | VESTA `.vasp`; phase non-unique for Re/Im |
| W4 | Transition dipole (PS) | `get_dipole_mat` | `tdmplot` | README snippet only | **no-example** | **L0–L1** | S3 | p–r; periodic caveat PRB 87, 125301 |
| W5 | Inverse participation ratio | IPR helpers | — | README only | **no-example** | **L0–L1** | S3 | Grid-dependent |
| W6 | Electron localization function | `elf` | — | `examples/elf_test/` | **unverified** | **L0** | S3 | README: needs testing |
| B1 | Band unfolding (EBS) | `unfold`, `spectral_weight`, `EBS_*` | — | `examples/unfold/*` | **needs-data** | **L1–L2** | S2 | PS weights; npy/PNG cached |
| B2 | Unfold + atomic weights | `unfold` + PROCAR path | — | `examples/unfold/Ce@BL-MoS2_3x3x1/` | **needs-data** | **L1** | S2 | `plt_unf.py` |
| B3 | Band reordering by overlap | `band_order.reorder_band` | — | `examples/band_reorder/` | **needs-data** | **L1** | S2 | PNG present; need script+WAVECAR |
| B4 | PROCAR orbital projections | `procar.procar` | — | — | **no-example** | **L0–L1** | S2 | Parse only; no regen of projectors |
| B5 | Irreducible k-points (IBZ) | `hse_kpts.get_ir_kpts` | — | — | **optional-dep** | **L0–L1** | S8 | **spglib** not in requirements |
| P1 | POTCAR / partial waves | `paw.pawpotcar` | `potplot` | `examples/potplot/`, `projectors/` | **ready** | **L2** | S4 | potplot image-only regen gap |
| P2 | Nonlocal projectors | `nonlq`, `nonlr` | — | `examples/projectors/` | **ready** | **L2** | S4 | vs NormalCar; LREAL T/F |
| P3 | PAW \(Q_{ij}\), \(\nabla_{ij}\) | `get_Qij`, `get_nablaij`, … | — | via paw | **ready** | **L1–L2** | S4 | Partial-wave completeness |
| P4 | AE wavefunction | `aewfc.vasp_ae_wfc` | — | `examples/aewfc/co2/` | **optional-dep** | **L1–L2** | S4 | **pySBT** |
| P5 | AE transition dipole | `aewfc.get_dipole_mat` | `tdmplot` | README snippet only | **optional-dep** | **L0–L1** | S3/S4 | One-center nabla correction |
| O1 | SOC matrix (PAW AE basis) | `spinorb` | — | `examples/spinor/` (data) | **needs-data** | **L1** | S5 | SocCar / NormalCar / … |
| O2 | SOC spinor WAVECAR | `spinor.socclass` | `spinormaker` | `examples/spinor/` | **needs-data** | **L1** | S5 | ≠ automatic SCF ncl |
| O3 | SOC eigen / MAE helpers | `spinorb_eigen`, `get_mae`, … | — | — | **no-example** | **L0–L1** | S5 | Occupation policy matters |
| X1 | BSE interaction matrix | `bsematrix` | `bin/bsematrix` | `examples/bsematrix/BP/` | **partial** | **L2** (`pw_only`) | S6 | Other modes lower |
| X2 | BSE modes pw / paw_orth / paw_full | `bsematrix` `--mode` | same | BP tables | **partial** | **L1–L2** | S6 | Quarantine weak modes for citation |
| X3 | Finite-q BSE | `--q-ext` | same | BP qext artifacts | **partial** | **L0–L1** | S6 | Not validated |
| X4 | Screened potential (WFULL) | `wfull` | — | — | **no-example** | **L1** | S6 | BSE response-basis infra |
| X5 | BSEFATBAND / exciton BZ | `bsefatband` | `bseplot bz` | `examples/bseplot/` | **ready** | **L2** | S7 | Bundled BSEFATBAND |
| X6 | Exciton real-space density | `bsefatband` | `bseplot realspace` | `examples/bseplot/` PNG | **needs-data** | **L1–L2** | S7 | Needs WAVECAR+OUTCAR phases |
| D1 | Non-adiabatic couplings | `nac_from_vaspwfc` | — | — | **no-example** | **L0** | S8 | Phase fixing critical |
| D2 | NEB path plot | — | `nebplot` | — | **no-example** | **L0** | S8 | OUTCAR post-process only |
| D3 | Ewald / Madelung | `ewald.ewaldsum` | — | `examples/ewald/` | **ready** | **L2** | S8 | Classical point charges |
| I1 | Physical constants | `vasp_constant` | — | — | **infra** | **L2** | S1 | VASP unit conventions |
| I2 | Spherical harmonics | `sph_harm` | — | — | **infra** | **L1–L2** | S4 | Real/complex Ylm |
| I3 | Cubic spline (SPLCOF) | `spline.splcof` | — | — | **infra** | **L1** | S4 | PAW radial interp |
| I4 | Fortran binary record I/O | `wfull`, `FortranFile`, WAVECAR `recl` | — | — | **infra** | **L1** | S1 | Three coexisting styles |

---

## CLI summary

| ID | Command | Source | `pip install`? | Feature IDs | Purpose |
|---|---|---|---|---|---|
| C1 | `wfcplot` | `bin/wfcplot` | yes | W3 | Real-space wavefunction → VESTA |
| C2 | `tdmplot` | `bin/tdmplot` | yes | W4, P5 | Dipole / TDM spectrum |
| C3 | `potplot` | `bin/potplot` | yes | P1 | POTCAR projectors / partial waves |
| C4 | `nebplot` | `bin/nebplot` | yes | D2 | NEB path from OUTCARs |
| C5 | `bseplot` | `bin/bseplot` | yes | X5, X6 | Exciton BZ or real-space density |
| C6 | `spinormaker` | `bin/spinormaker` | yes | O2 | SOC spinor WAVECAR |
| C7 | `bsematrix` | `bin/bsematrix` | **no** | X1–X3 | Build/diagonalize BSE matrix |

Common flags (1-based VASP indices): `-w` WAVECAR, `-p` POSCAR/POTCAR, `-s` spin, `-k` k-point, `-n` band.

---

## Examples coverage map

| `examples/` path | Feature IDs | Runnable as shipped? |
|---|---|---|
| `wfc_r/` | W1–W3 | **Yes** (has `WAVECAR`) |
| `unfold/` | B1, B2 | Partial (plots/`.npy`; often no `WAVECAR`) |
| `spinor/` | O1, O2 | Partial (inputs + README; Soc\* often missing) |
| `projectors/` | P1, P2 | **Yes** |
| `aewfc/co2/` | P4 | **Yes** if `pySBT` installed |
| `bsematrix/BP/` | X1–X3 | Compare text artifacts; full rebuild needs VASP tree |
| `bseplot/` | X5, X6 | **`bz` yes**; `realspace` needs `WAVECAR` |
| `elf_test/` | W6 | Runnable; physics **L0** |
| `ewald/` | D3 | **Yes** (stdout; add ref file for CI) |
| `potplot/` | P1 | Result image only |
| `band_reorder/` | B3 | Partial (no full script+`WAVECAR`) |

**No dedicated example directory:** B4 PROCAR, D1 NAC, D2 NEB, W4/P5 TDM end-to-end, B5 HSE k, X4 standalone WFULL, W5 IPR, O3 MAE.

---

## Dependencies

| Dependency | Feature IDs | Declared? |
|---|---|---|
| `numpy`, `scipy`, `matplotlib`, `ase` | core | yes |
| `pySBT` | P4, P5 | optional (`requirements-optional.txt`) |
| `spglib` | B5 | **no** — install manually |

---

## Quick “what works out of the box”

```bash
python -c "import vaspwfc, unfold, paw, ewald, bsefatband; print('ok')"
python examples/wfc_r/ex.py
python examples/ewald/madelung.py
python examples/projectors/lreal_false/kaka.py
bseplot bz --input examples/bseplot/BSEFATBAND --poscar examples/bseplot/POSCAR --exciton 1
```

Needs external VASP outputs or cluster jobs: B1 recompute, O2 with Soc\*, X6, full X1 rebuild, D1, D2.

---

## Related docs

- [`docs/GOALS.md`](docs/GOALS.md) — secondary development goals (G1 proof, G2 reuse)
- [`docs/ACADEMIC_ROADMAP.md`](docs/ACADEMIC_ROADMAP.md) — seminars, phases, coverage matrix  
- [`docs/ASSUMPTIONS.md`](docs/ASSUMPTIONS.md) — physics/numerics limits  
- [`README.md`](README.md) · [`AGENTS.md`](AGENTS.md) · [`doc/VaspBandUnfolding.pdf`](doc/VaspBandUnfolding.pdf)
