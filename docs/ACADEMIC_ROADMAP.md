# Academic Roadmap (All Features)

Audience: **first-principles / electronic-structure specialists** (seminar, methods discussion, research extension).  
Scope: **every user-facing and infrastructure capability** in VaspBandUnfolding / PyVaspWfc — not a beginner tutorial track.

Companion docs: [`FEATURES.md`](../FEATURES.md) (inventory) · [`GOALS.md`](GOALS.md) (dev goals) · [`ASSUMPTIONS.md`](ASSUMPTIONS.md) (limits) · [`README.md`](../README.md) (usage) · [`AGENTS.md`](../AGENTS.md) (dev conventions).

---

Live engineering status: [`STATUS.md`](STATUS.md) · citation: [`CITATION_POLICY.md`](CITATION_POLICY.md).

## 1. Purpose

| Goal | What “done” means for experts |
|---|---|
| **Academic discussion** | Each capability has: physical definition, numerical path, VASP correspondence, validation level, known limits, open questions |
| **Further development** | Each capability has: extension surface, missing benchmarks, data/repro needs, suggested API/tests — without orphan modules |

This roadmap is the **full-coverage work plan**. Nothing in the master feature list is optional for long-term stewardship; prioritization only orders *when*, not *whether*.

---

## 2. Validation levels (use everywhere)

| Level | Meaning | Typical evidence |
|---|---|---|
| **L0** | Code path exists / imports | API + docstring |
| **L1** | Internal consistency or analytic limit | unit test, sum rules, hermiticity, norm |
| **L2** | Same-input comparison to VASP (or standard ref) | tables, `max|Δ|`, plots side-by-side |
| **L3** | Multi-system + literature / independent code | paper-grade claim |

**Working rule for seminars:** only **L2+** results are presented as “agrees with VASP”; L0–L1 are labeled *implementation / exploratory*.

---

## 3. Full capability map

Every row is in scope for discussion **and** development. Status is the *current* research-readiness snapshot (update when evidence changes).

### 3.1 Wavefunction core (`vaspwfc`)

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| W1 | WAVECAR I/O (std / γ-only / ncl) | `vaspwfc.vaspwfc` | Record layout; `rtag` precision; γ half-plane (`x`/`z`); spinor packing; 1-based indexing | **L2** (widely used; format edge cases) | S1 | Fixture matrix: std / γ / ncl mini-WAVECARs; header+norm tests |
| W2 | G-vector set & plane-wave cutoff sphere | `gvectors` / internal | \(E_\mathrm{cut}\) sphere; FFT grid; γ reduced set | **L1–L2** | S1 | Document G-count vs OUTCAR; test vs known ENCUT |
| W3 | Real-space PS wavefunction | `wfc_r` / `get_ps_wfc`, `wfcplot` | FFT conventions; phase; spinor two components; VESTA scaling | **L2** (`examples/wfc_r`) | S1 | Keep mini example; optional phase-convention note |
| W4 | Transition dipole (PS, velocity → length) | `get_dipole_mat`, `tdmplot` | Velocity gauge; p–r; **periodic vs molecular**; Em=En; surface terms | **L0–L1** (caveat in README; weak benchmark) | S3 | **Must:** small-system L2 vs VASP OPTICS / finite molecule; document invalid regimes |
| W5 | IPR | IPR helpers on real-space grid | Localization measure; grid convergence; spin | **L0–L1** | S3 | Analytic limit (uniform / δ-like); one defect example + ref values |
| W6 | ELF | `elf`, `examples/elf_test` | Becke–Edgecombe / Savin; same-spin; vs VASP `ELFCAR`; VESTA volume scaling | **L0** (explicitly unverified) | S3 | Controlled validation vs VASP ELFCAR; fix or mark experimental |

### 3.2 Band structure tools

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| B1 | Band unfolding (EBS) | `unfold`, `spectral_weight`, `EBS_*` | Popescu–Zunger; spectral weight; PBZ path ↔ SBZ fold; PS-only bias | **L1–L2** (figures + npy; recompute data-thin) | S2 | Repro protocol; weight sum rules; optional primitive-cell overlay |
| B2 | Unfold + orbital/atomic weights | `unfold` + PROCAR path, `Ce@BL-MoS2_*` | Fatband-style EBS; projector incompleteness | **L1** | S2 | Bundle weight recipe; clarify PROCAR alignment |
| B3 | Band reordering by overlap | `band_order.reorder_band` | \(\langle u_{n\mathbf{k}}|u_{m\mathbf{k}-\Delta}\rangle\); avoided crossing vs true character swap; PS `u` | **L1** | S2 | Scripted example + overlap matrix dump; failure cases (SOC, dense crossings) |
| B4 | PROCAR projections | `procar.procar` | lm / site projections; phase; collinear vs ncl; consistency with `LORBIT` | **L0–L1** | S2 | Dedicated example; cross-check vs VASP PROCAR columns |
| B5 | IBZ k generation | `hse_kpts.get_ir_kpts` | spglib symmetry; weights; HSE/hybrid k meshes | **L0–L1** | S8 | Declare `spglib` optional dep; compare weights to VASP `IBZKPT` |

### 3.3 PAW / all-electron

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| P1 | POTCAR parse + partial waves | `paw.pawpotcar`, `potplot` | Projector / AE / PS partial waves; radial grids | **L2** (viz + projectors suite) | S4 | Multi-element POTCAR; version skew notes |
| P2 | Nonlocal projectors \(\langle p_i|\tilde\psi\rangle\) | `nonlq`, `nonlr` | Reciprocal vs real (`LREAL`); NormalCar agreement | **L2** (`examples/projectors`) | S4 | Keep LREAL true/false pair as permanent L2 gate |
| P3 | PAW \(Q_{ij}\), \(\nabla_{ij}\), one-center ops | `get_Qij`, `get_nablaij`, … | Completeness inside augmentation sphere | **L1–L2** | S4 | Tabulate vs known identities; feed dipole/BSE |
| P4 | AE wavefunction reconstruction | `aewfc.vasp_ae_wfc`, `pySBT` | \(\psi=\tilde\psi+\sum(\phi-\tilde\phi)|p\rangle\langle p|\tilde\psi\rangle\); grid/`aecut` | **L1–L2** (`aewfc/co2`) | S4 | Pin pySBT version; norm/AE–PS difference metrics |
| P5 | AE dipole | `aewfc.get_dipole_mat`, `tdmplot` | One-center nabla correction vs PS-only | **L0–L1** | S3+S4 | Same L2 suite as W4 with AE on/off |

### 3.4 Spin–orbit / spinor

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| O1 | SOC matrix on PAW AE basis | `spinorb` (`paw_core_soc_mat`, `read_SocCar`, …) | \(H_\mathrm{SOC}\); radial integrals; NormalCar projectors | **L1** | S5 | Document required VASP files; unit tests on small Soc dumps |
| O2 | Spinor WAVECAR construction | `spinor.socclass`, `spinormaker` | Scalar/ISPIN=2 → ncl spinor; band pairing; vs SCF ncl | **L1** (README valley/sz snapshot) | S5 | End-to-end mini MoX2; compare to `LSORBIT` WAVECAR when possible |
| O3 | MAE / SOC eigenvalues helpers | `spinorb_eigen`, `get_mae`, … | Magnetic anisotropy estimates; limits of second variation | **L0–L1** | S5 | Clear formula doc + toy numbers |

### 3.5 BSE / excitons

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| X1 | BSE interaction matrix (Hartree / direct / both) | `bsematrix`, `bin/bsematrix` | Kernel definitions; Tamm–Dancoff; basis of pairs | **L2** for `pw_only` on BP suite | S6 | Freeze L2 gates; CI compare AMAT norms |
| X2 | Modes `pw_only` / `paw_orth_only` / `paw_full` | `bsematrix` modes | PAW completeness; FAST_AUG dumps | **L1–L2** (`pw_only` best; PAW residual) | S6 | Honest publishable error bars; fix or quarantine modes |
| X3 | Finite-q BSE | `--q-ext` path | Momentum-dependent kernel; current mismatch | **L0–L1** | S6 | Separate “research” track; do not cite as validated |
| X4 | WFULL / screened-W reader | `wfull` | Fortran records; response basis; W(q) | **L1** (infrastructure) | S6 | Standalone golden-file test; link to direct kernel |
| X5 | BSEFATBAND parse + BZ exciton weight | `bsefatband`, `bseplot bz` | Envelope in FBZ; exciton index conventions | **L2** (`examples/bseplot`) | S7 | Keep as default L2 demo |
| X6 | Real-space fixed-e/h exciton density | `bseplot realspace` | Phase restore; IBZ→FBZ; symmetry ops from OUTCAR | **L1–L2** (PNG vs VASP; WAVECAR often external) | S7 | Phase-convention writeup; small WAVECAR fixture or crisp recipe |

### 3.6 Dynamics / geometry-related post-processing

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| D1 | Non-adiabatic couplings | `nac_from_vaspwfc`, `parallel_nac_calc` | \(\langle\psi_i(t)|\partial_t\psi_j\rangle\); phase fixing; γ; time step | **L0** | S8 | Two-frame fixture; phase convention; vs finite-difference literature |
| D2 | NEB path visualization | `nebplot` | Reaction coordinate; spline; forces from OUTCAR | **L0** (tooling) | S8 | Tiny multi-image OUTCAR fixture; energy table ref |
| D3 | Ewald / Madelung | `ewald.ewaldsum`, `examples/ewald` | Ewald convergence; charged cells; reference crystals | **L2** (classic Madelung numbers) | S8 | Pin `madelung.ref`; convergence parameters in doc |

### 3.7 Numerical infrastructure (must not be “forgotten”)

| ID | Capability | Primary API / CLI | Academic discussion points | Current level | Seminar slot | Dev / repro actions |
|---|---|---|---|---|---|---|
| I1 | Physical constants / unit system | `vasp_constant` | eV/Å vs a.u.; align with VASP | **L2** (by convention) | S1 / appendix | Single table in METHODS; unit tests for key ratios |
| I2 | Spherical harmonics (real/complex) | `sph_harm` | Real Ylm vs complex; Condon–Shortley; PAW angular | **L1–L2** | S4 appendix | Orthogonality / known values tests |
| I3 | Cubic spline (VASP `SPLCOF`) | `spline.splcof` | Match VASP radial interpolation | **L1** | S4 appendix | Compare to SciPy spline on sample radial data |
| I4 | Fortran binary record I/O patterns | `wfull`, `spinorb`/`FortranFile`, WAVECAR `recl` | Portability; endian; record markers | **L1** | S1 appendix | Golden tiny binaries in `tests/fixtures/` |

### 3.8 CLI surface (all entry points)

| ID | CLI | Maps to | Discussion / dev note |
|---|---|---|---|
| C1 | `wfcplot` | W3 | Keep flag parity with library |
| C2 | `tdmplot` | W4, P5 | Needs reference runbook |
| C3 | `potplot` | P1 | Ship scripted regen, not only PNG |
| C4 | `nebplot` | D2 | Needs fixture |
| C5 | `bseplot` | X5, X6 | Subcommands `bz` / `realspace` |
| C6 | `spinormaker` | O2 | Document Soc\* prerequisites |
| C7 | `bsematrix` (`bin/`, not installed) | X1–X3 | Register install **or** document `python bsematrix.py` only — pick one |

---

## 4. Seminar series (covers **all** IDs)

Format per session (60–90 min): **physics → this code’s equations → VASP correspondence → numbers on screen → open problems**.  
Every ID appears in at least one session (primary or appendix).

| Session | Title | Feature IDs (primary) | Appendix IDs | Evidence to bring |
|---|---|---|---|---|
| **S1** | WAVECAR as a scientific object | W1–W3 | I1, I4 | `wfc_r` orbitals; G-count vs OUTCAR |
| **S2** | Spectral weight, character, projections | B1–B4 | — | unfold EBS; Ce fat-EBS; band reorder figure; PROCAR demo (to be built) |
| **S3** | Response-ish one-body: dipole, IPR, ELF | W4–W6 | P5 | TDM numbers (to be built); IPR; ELF vs ELFCAR honesty |
| **S4** | PAW one-center universe | P1–P4 | I2, I3 | projectors vs NormalCar; CO2 AE/PS |
| **S5** | From collinear to spinor SOC | O1–O3 | — | spinormaker snapshots; limits vs SCF ncl |
| **S6** | Building the BSE kernel | X1–X4 | C7 | BP AMAT tables; mode-by-mode residuals; WFULL role |
| **S7** | Exciton observables in BZ and real space | X5–X6 | — | `bseplot` BZ + e/h density comparisons |
| **S8** | Auxiliary but legitimate tools | D1–D3, B5 | C4 | Madelung; NAC design; NEB; IBZ weights |

**Full-coverage check:** W1–W6, B1–B5, P1–P5, O1–O3, X1–X6, D1–D3, I1–I4, C1–C7 all listed above.

Optional **S9 (capstone):** pick one materials story that *crosses* stacks (e.g. MoSe2: unfold or spinor → BSEFATBAND → real-space exciton) and state which links are L2 vs aspirational.

---

## 5. Development program (all features, phased)

Phases order effort; **backlog retains every ID**.

### Phase A — Contract & honesty (all features labeled)

- [x] Publish this roadmap + maintain levels in [`FEATURES.md`](../FEATURES.md) (columns: `ID`, `Level`, `Seminar`).
- [x] One-page **assumptions registry**: [`ASSUMPTIONS.md`](ASSUMPTIONS.md) (γ √2, p–r, PS-only unfold, BSE PAW modes, spinor ≠ full ncl, ELF experimental).
- [ ] CLI policy for C7 (`bsematrix` install).
- [ ] Optional deps: `pySBT` (P4/P5), `spglib` (B5) declared and version-pinned in docs / packaging.

### Phase B — L1 safety net (no large VASP binaries)

| Tests / fixtures | Covers |
|---|---|
| Constants ratios | I1 |
| Ylm orthonormality / values | I2 |
| Spline vs reference nodes | I3 |
| Fortran record round-trip | I4, X4 |
| k fold / unique K / path helpers | B1 helpers |
| Madelung for NaCl, CsCl, … | D3 |
| PROCAR parse on tiny synthetic or clipped file | B4 |
| IPR on analytic grid fields | W5 |

### Phase C — L2 gates where examples already strong

| Gate | IDs |
|---|---|
| `projectors` NormalCar agreement | P2, P1 |
| `wfc_r` norm / smoke | W1–W3 |
| `bsematrix/BP` AMAT + eigenvalues for **declared** modes | X1–X2 |
| `bseplot bz` deterministic PNG or weight table | X5 |
| `ewald` ref file | D3 |
| `aewfc/co2` AE–PS metrics (with pinned pySBT) | P4 |

### Phase D — Close expert-critical holes (still full list, ranked by discussion value)

| Priority | IDs | Work |
|---|---|---|
| P0 | W4, P5 | Dipole L2 suite + invalid-regime doc |
| P0 | X2, X3 | BSE PAW / finite-q: fix or quarantine with explicit level |
| P1 | B1, B2 | Unfold recompute recipe (`crisp`) + weight sum rules |
| P1 | O1, O2 | Spinor end-to-end + file prerequisites |
| P1 | X6 | Real-space exciton phase writeup + data recipe |
| P2 | W6 | ELF vs VASP validate or deprecate |
| P2 | B3, B4 | Reorder + PROCAR first-class examples |
| P2 | D1 | NAC definition + two-frame fixture |
| P3 | D2, B5, O3, C* | NEB fixture; IBZ vs VASP; MAE doc; CLI polish |

### Phase E — Research extensions (after L2 honesty)

Examples (non-exclusive): Berry-phase consistent dipole; full BSE beyond TDA; spinor unfold; AE-based NAC; hybrid-k workflows with B5; W-from-WFULL diagnostics for GW/BSE coupling.

---

## 6. Data & reproducibility policy (all heavy features)

| Feature class | In git | External / `crisp` |
|---|---|---|
| Text AMAT, eigenvalues, small npy, PNG, Madelung ref | yes | — |
| Mini WAVECAR / clipped NormalCar for CI | yes if small | generate via documented job |
| Full BSE/GW, large SOC trees, production supercell WAVECAR | no | `docs/repro/<ID>.md` + `crisp submit` from fixed input dirs |

Every **needs-data** ID must eventually have either a **mini fixture** or a **repro doc** — no permanent “only on my cluster” for roadmap items.

Suggested repro doc names: `docs/repro/W1_wavecar.md`, `docs/repro/X1_bse_bp.md`, `docs/repro/O2_spinor.md`, …

---

## 7. Documentation deliverables (full coverage)

| Deliverable | Content |
|---|---|
| This file | Plan + seminar map + phases |
| [`ASSUMPTIONS.md`](ASSUMPTIONS.md) | Cross-cutting physics/numerics limits |
| `docs/METHODS/<ID>.md` (progressive) | One method card per ID or per tight group (W1–W3, X1–X3, …) |
| Per-example “Evidence” section | Level, VASP version, figures/tables, what is *not* claimed |
| `FEATURES.md` columns | ID · Level · Seminar · Eng. status |

---

## 8. Coverage matrix (checklist)

Use this as a living “nothing dropped” audit.

| ID | In seminar | Level labeled | Example or fixture | Repro doc | L1 test | L2 gate | Notes |
|---|---|---|---|---|---|---|---|
| W1 | S1 | yes | wfc_r | | | partial | |
| W2 | S1 | yes | | | | | |
| W3 | S1 | yes | wfc_r | | | partial | |
| W4 | S3 | yes | **missing** | | | | P0 |
| W5 | S3 | yes | **missing** | | | | |
| W6 | S3 | yes | elf_test | | | | unverified |
| B1 | S2 | yes | unfold | | | partial | |
| B2 | S2 | yes | Ce@BL | | | | |
| B3 | S2 | yes | band_reorder PNG | | | | need script |
| B4 | S2 | yes | **missing** | | | | |
| B5 | S8 | yes | **missing** | | | | spglib |
| P1 | S4 | yes | potplot | | | | |
| P2 | S4 | yes | projectors | | | yes | |
| P3 | S4 | yes | via paw | | | | |
| P4 | S4 | yes | aewfc/co2 | | | partial | pySBT |
| P5 | S3/S4 | yes | **missing** | | | | P0 |
| O1 | S5 | yes | spinor data | | | | |
| O2 | S5 | yes | spinor | | | | |
| O3 | S5 | yes | | | | | |
| X1 | S6 | yes | bsematrix/BP | | | yes pw_only | |
| X2 | S6 | yes | BP modes | | | partial | |
| X3 | S6 | yes | BP qext | | | no | |
| X4 | S6 | yes | via BSE | | | | |
| X5 | S7 | yes | bseplot | | | yes | |
| X6 | S7 | yes | PNG only | | | partial | |
| D1 | S8 | yes | **missing** | | | | |
| D2 | S8 | yes | **missing** | | | | |
| D3 | S8 | yes | ewald | | | yes-ish | |
| I1 | S1 | yes | | | | | |
| I2 | S4 | yes | | | | | |
| I3 | S4 | yes | | | | | |
| I4 | S1 | yes | | | | | |
| C1–C7 | with parents | yes | CLIs | | | | C7 policy |

---

## 9. Immediate next actions (still full-scope oriented)

1. **Adopt IDs** in `FEATURES.md` (traceability for every capability).  
2. **Draft `docs/ASSUMPTIONS.md`** covering W4, B1, O2, X2–X3, W6 in one place.  
3. **S6 + S1 materials first** if only two seminars: kernel honesty + WAVECAR object (sets tone).  
4. **P0 benchmarks** W4/P5 and quarantine rules for X2/X3 — unblocks credible discussion of half the stack.  
5. **Fill missing example slots** for B4, D1, D2, W5, B5 so no ID remains seminar-only vapor.  
6. **L1 tests** for I1–I4, D3, B1 helpers so infrastructure features are not eternally “untested glue.”

---

## 10. Explicit non-goals (for this roadmap)

- Replacing VASP.
- Claiming L3 for all IDs.
- Beginner onboarding curriculum (separate, optional).
- Dropping low-glamour IDs (NAC, NEB, constants, spline) from stewardship — they stay in the matrix even if seminar time is short (appendix is enough).

---

## 11. Related paths

| Path | Role |
|---|---|
| [`FEATURES.md`](../FEATURES.md) | Short inventory |
| [`examples/`](../examples/) | Evidence packs |
| [`doc/VaspBandUnfolding.pdf`](../doc/VaspBandUnfolding.pdf) | External publications using the code |
| `docs/repro/` (to create) | Cluster/`crisp` reproduction |
| `docs/METHODS/` (to create) | Per-ID method cards |
