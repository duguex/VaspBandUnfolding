# Assumptions & Limits Registry

Cross-cutting physical and numerical assumptions for **VaspBandUnfolding** (PyVaspWfc).  
Audience: first-principles specialists. Use this when reviewing results, citing the code, or extending methods.

Companion: feature IDs and validation levels in [`FEATURES.md`](../FEATURES.md), live status [`STATUS.md`](STATUS.md), citation [`CITATION_POLICY.md`](CITATION_POLICY.md), and [`ACADEMIC_ROADMAP.md`](ACADEMIC_ROADMAP.md).

**Rule of thumb:** If an assumption below is violated, treat the corresponding feature as **exploratory (L0–L1)** even if the code runs cleanly.

---

## 1. Global conventions

| Topic | Assumption | Implications |
|---|---|---|
| Indexing | Spin / k / band indices in public APIs and CLIs are **1-based** (VASP style) | Off-by-one vs NumPy 0-based loops is a common user error, not a physics bug |
| Units | Energies in **eV**, lengths in **Å**, unless a routine documents a.u. | See `vasp_constant` (I1); do not mix with codes that default to Hartree/Bohr without conversion |
| Pseudo nature | Most orbitals read from WAVECAR are **PAW pseudo-wavefunctions** \(\tilde\psi\), not AE \(\psi\) | Unfolding, IPR, PS dipole, NAC from WAVECAR inherit PS bias |
| FFT / grid | Real-space grids follow VASP-like FFT mesh from ENCUT / `ngrid` overrides | Quantities dense on the grid (IPR, ELF, real-space exciton) are grid-convergent observables |
| Parallelism | Some paths use process/thread settings (`omp_num_threads`, optional parallel NAC) | Bitwise reproducibility across core counts is **not** guaranteed |
| VASP version skew | Binary layouts and γ-half conventions depend on VASP vintage | Always record VASP version + `lgamma` / `gamma_half` / `lsorbit` with results |

---

## 2. WAVECAR object (W1–W3, I4)

### 2.1 Precision tags

- `rtag = 45200` → single-precision complex coefficients  
- `rtag = 45210` → double-precision  
- Downstream algebra is usually promoted to complex128; **file noise** remains.

### 2.2 Gamma-only (`lgamma=True`)

- Only **half** of the G-sphere is stored; conjugate symmetry reconstructs the rest.  
- Half-axis: `gamma_half='x'` (default, VASP ≥ 5.4 typical) or `'z'` (older parallel FFT paths). **Wrong half ⇒ wrong orbitals.**  
- Non-zero G coefficients often carry a **√2** storage convention when expanding to the full set; real-space transforms use the matching half-FFT path (`irfftn`-style logic).  
- **`lgamma` and `lsorbit` are mutually exclusive** in this codebase.

### 2.3 Noncollinear / SOC WAVECAR (`lsorbit=True`)

- Coefficients layout: **spin-up block then spin-down** for each band (length `2 * nplw`).  
- Real-space API returns **two** 3D arrays (spinor components).  
- Scalar→spinor band map used elsewhere: \(i_\mathrm{scalar} = \lfloor(i_\mathrm{spinor}+1)/2\rfloor\) style pairing in spinor tooling — do not invent alternate pairings without documenting them.

### 2.4 Phase

- Bloch states have an arbitrary **U(1) phase** per (spin, k, band).  
- Any quantity that mixes two states (dipole, NAC, overlaps for reordering, exciton real-space assembly) is only meaningful after a **stated phase policy**.  
- Single-state densities \(|\psi|^2\) are phase-invariant; \(\mathrm{Re}\,\psi\) plots are not unique.

### 2.5 Real-space export (W3, `wfcplot`)

- VESTA / CHGCAR-like readers may **divide by cell volume** depending on file type; ELF notes in README about renaming to `ELFCAR` exist for this reason.  
- Exporting \(\mathrm{Re}/\mathrm{Im}\) separately is for visualization, not a claim about gauge-invariant observables.

---

## 3. One-body response-like quantities (W4–W6, P5)

### 3.1 Transition dipole (W4, P5)

**What the code does (PS path):**

1. Momentum / velocity-gauge matrix elements from plane-wave coefficients:  
   \(\langle u_{n\mathbf{k}}| \mathbf{k}-i\nabla |u_{m\mathbf{k}}\rangle \sim \sum_G C_n^* C_m (\mathbf{k}+\mathbf{G})\).  
2. Convert to length gauge via a **p–r** relation  
   \(\langle r\rangle \sim \langle p\rangle / (i m (E_n-E_m))\) (see README for exact prefactors).  
3. If \(E_n \approx E_m\), dipole is set to **0** (no special degenerate perturbation treatment).

**Assumptions / limits:**

| Assumption | Risk if violated |
|---|---|
| Electric-dipole approximation | No multipoles, no finite-q photon |
| p–r valid as used | **Periodic solids**: position operator ill-defined; surface/Berry terms missing — README cites PRB 87, 125301. Prefer molecular / finite systems or treat as approximate |
| Same k for initial/final | Inter-k transitions not the primary contract |
| PS only (W4) | Missing PAW one-center velocity corrections |
| AE path (P5) | Adds one-center \(\nabla\) corrections from partial waves; still not a full modern Berry-phase dipole formalism |
| No many-body renormalization | Single-particle KS/QP energies only |

**Citation policy:** Do not claim quantitative optical matrix elements for bulk crystals without an external L2 benchmark and an explicit gauge statement.

### 3.2 IPR (W5)

- Defined on the **discrete real-space grid** of the PS (or chosen) density.  
- Sensitive to **grid density**, vacuum padding, and whether AE or PS density is used.  
- Comparative use (same grid, same code path) is safer than absolute cross-code comparison.

### 3.3 ELF (W6)

- README marks ELF as **still needing testing**.  
- Kinetic-energy density and same-spin pair probabilities follow standard DFT-ELF ideas, but **agreement with VASP `ELFCAR` is not established** in-repo.  
- Visualization: volume scaling differs for `ELFCAR` vs `CHGCAR`-like files in VESTA.  
- **Treat as experimental (L0)** until an L2 table exists.

---

## 4. Band unfolding & character (B1–B4)

### 4.1 Spectral weight (B1)

- Implementation follows the Popescu–Zunger effective band structure idea (spectral weight of supercell states onto primitive \(\mathbf{k}\)).  
- Weights are built from **pseudo** Bloch states in WAVECAR → projector incompleteness and PAW one-center pieces are **not** fully restored.  
- Spectral function plots depend on **smearing** (Lorentz/Gaussian) and `nedos` — cosmetic and peak-height sensitive.  
- Empty regions can be **missing bands** (`NBANDS` too small in the supercell), not physical gaps.

### 4.2 Atomic / orbital weights on EBS (B2)

- Layers PROCAR-like site/lm weights onto unfolded weights.  
- Inherits PROCAR `LORBIT` definitions and PS projectors.  
- Alignment of band indices between WAVECAR and PROCAR must be guaranteed by the user (same run).

### 4.3 Band reordering (B3)

- Maximizes \(|\langle u_{n\mathbf{k}}|u_{m\mathbf{k}-\Delta}\rangle|\) using **PS** periodic parts in **real space** (plane-wave counts differ by k).  
- Resolves labeling continuity, **not** topological character in the Berry sense.  
- Dense avoided crossings, SOC entanglement, and near-degeneracies can produce **ambiguous** swaps; `olap_cut` is a heuristic.

### 4.4 PROCAR (B4)

- Parses VASP projection tables; does not re-derive projectors from POTCAR.  
- Collinear vs noncollinear PROCAR layouts differ; do not feed the wrong dialect.  
- Phase of complex projections (if present) is VASP-defined; fatband intensities usually use moduli squared.

---

## 5. PAW / AE (P1–P5, I2–I3)

### 5.1 Projectors (P1–P2)

- `nonlq` / `nonlr` target VASP nonlocal projector algebra inside the augmentation sphere.  
- **LREAL** true/false switches real vs reciprocal projector paths — both are validated against NormalCar in `examples/projectors`, but grids and cutoffs must match the generating VASP run.  
- POTCAR generation date / GW vs standard POTCAR changes radial data — keep POTCAR hash with benchmarks.

### 5.2 One-center matrices (P3)

- \(Q_{ij}\), \(\nabla_{ij}\), etc., are only as complete as the **partial-wave basis** in POTCAR.  
- Soft PS partial waves do not restore true AE cusp physics beyond the PAW construction.

### 5.3 AE wavefunction (P4)

- \(\psi = \tilde\psi + \sum_i (|\phi_i\rangle - |\tilde\phi_i\rangle)\langle p_i|\tilde\psi\rangle\) (schematic).  
- Requires consistent projector coefficients and radial data; **pySBT** used for spherical Bessel / radial transforms in AE workflows — pin version for reproducibility.  
- `aecut` / denser grids change AE visualization and norms; report them.

### 5.4 Angular / radial numerics (I2–I3)

- Real vs complex spherical harmonics must match VASP’s PAW angular convention when comparing projector channels.  
- `spline.splcof` aims to mirror VASP `SPLCOF`; independent SciPy splines may differ at the level of radial interpolation noise.

---

## 6. SOC spinor construction (O1–O3)

| Assumption | Detail |
|---|---|
| Input orbitals | Collinear or ISPIN=2 WAVECAR + PAW SOC dumps (`NormalCAR`, `SocCar`, `SocRadCar` as required by the path) |
| Physics | Second-variation / basis-expansion style SOC assembly — **not** automatically identical to self-consistent noncollinear SCF |
| Band pairing | Odd/even spinor pairs and `mixwave-ibs` selection are part of the method definition |
| Validation | MoSe2: `examples/spinor/ref/spinor_vs_ncl.txt` — eigenvalue MAE ~ few meV vs SCF ncl+LSORBIT; **not** identity. Dumps via patched VASP ([`repro/O2_local_vasp_patch_build.md`](repro/O2_local_vasp_patch_build.md)) |
| MAE helpers (O3) | Estimators depend on occupation / Fermi policy in helpers — document occupations when quoting meV-scale MAE |

---

## 7. BSE & excitons (X1–X6, C7)

### 7.1 Kernel modes (X1–X2)

| Mode | Intent | Present stance |
|---|---|---|
| `pw_only` | Plane-wave / full-grid-like pieces without full PAW kernel | **CLI default**; best BP residuals; only mode for careful citation (**l2-partial**) |
| `paw_orth_only` | Partial PAW orthogonalization path | **quarantine** vs VASP BP tables |
| `paw_full` | FAST_AUG-oriented reconstruction needing VASP dumps (`BSE_TRANS_MATRIX_FOCK.bin`, `BSE_FASTAUG_FOCK.bin`) | **quarantine** for production claims |

**Interaction channels:** direct vs Hartree/exchange naming follows the bsematrix/BP README (exchange-only ↔ Hartree-term example naming). Always state which channel was built.

### 7.2 Finite-q (X3)

- Finite momentum transfer (`q_ext` / `KPOINT_BSE` style) is **implemented but mismatched** vs VASP in published BP tables.  
- **Do not present as validated.** Research-only until L2 is recovered.

### 7.3 Screened W / WFULL (X4)

- Reader assumes VASP Fortran record layout for WFULL-like files.  
- Using W in a response basis inherits **all GW/BSE input choices** (ENCUTGW, bands, k-mesh) from the generating run — this library does not re-derive W from first principles.

### 7.4 Model Hamiltonian limits

- Typical path is **Tamm–Dancoff-like** pair spaces as configured by band windows / energy windows — state `vb-num`, `cb-num`, `ewin`.  
- Single-particle energies entering the diagonal are whatever WAVECAR/OUTCAR path supplies (KS vs QP depends on upstream VASP workflow).  
- No automatic inclusion of phonon-assisted or higher-order kernels.

### 7.5 Exciton BZ maps (X5)

- Weights come from **BSEFATBAND** amplitudes as written by VASP or by `bsematrix` exporters.  
- Comparing VASP vs Python fatbands requires **same pair basis ordering** and exciton index conventions.

### 7.6 Real-space exciton density (X6)

- Fixed-hole or fixed-electron densities reconstruct envelopes from amplitudes × Bloch orbitals.  
- **IBZ WAVECAR + symmetry:** phases and full-BZ maps need OUTCAR symmetry ops / `IBZKPT_HF`-style information — wrong OUTCAR ⇒ spatially wrong density even if \(|A|^2\) BZ maps look fine.  
- Supercell visualization grids and wrapping conventions must be reported.

### 7.7 CLI install (C7)

- `bsematrix` is installed via `pyproject.toml` `script-files` (with `bin/bsematrix`). Default `--mode pw_only`.  
- Prefer `python -m` / installed entry points over ad-hoc path hacks in new docs.

---

## 8. Dynamics & geometry helpers (D1–D3, B5)

### 8.1 NAC (D1)

- Finite-difference style couplings between two WAVECARs (e.g. MD steps).  
- Requires **phase alignment** between frames; raw \(\langle\psi_i|\psi_j\rangle\) without phase fixing is gauge-dependent.  
- Time step `dt` enters as a scale — units must match the trajectory.  
- γ-only and spin-polarized cases need matching flags on both WAVECARs.  
- Dual CO2 frames: `examples/nac/md_frames/` (local/gitignored) + `ref/nac_md_summary.txt` — **l2-partial** smoke, not full MD validation.

### 8.2 NEB plotting (D2)

- Post-processing only: energies / tangent forces from OUTCARs, spline smoothing optional.  
- Not an optimizer; barrier heights inherit VASP convergence and image density.

### 8.3 Ewald / Madelung (D3)

- Classical point-charge Ewald; electronic dielectric screening **not** included.  
- Charged cells / dipole corrections are outside the simple Madelung demo unless explicitly implemented in the call path.  
- Reference crystal values assume ideal ionic models (NaCl, CsCl, …).

### 8.4 IBZ k (B5)

- Relies on **spglib** (optional; listed in `requirements-optional.txt`, may need manual `pip install spglib`).  
- Symmetry tolerance `symprec` changes irreducible sets near higher-symmetry structures.  
- Not guaranteed to match VASP’s symmetry engine bit-for-bit; compare weights to `IBZKPT` before production hybrid runs.

---

## 9. What may be claimed vs not

| Claim type | Allowed when |
|---|---|
| “Matches VASP on this table/figure” | L2 evidence in-repo or attached, same inputs, stated software versions |
| “Physically complete AE optical matrix element” | Never from PS-only W4; P5 still needs explicit formalism + L2 |
| “Equivalent to self-consistent SOC” | Not from spinormaker alone; ncl compare shows ~meV MAE, not identity |
| “Production BSE kernel (all modes)” | Only **`pw_only`** (l2-partial); never paw\*/finite-q as validated |
| “ELF identical to VASP” | No — demo ELFCAR corr high but grid/order caveats remain |
| “Unfolded EBS is AE-accurate” | No — PS spectral weights |
| “Full L2 dipole vs VASP optics” | No until WAVEDER/element-wise matrix is gated |


## 10. Recording checklist (for any serious result)

Copy into seminar slides or SI:

```text
VaspBandUnfolding git commit:
VASP version:
Feature IDs used:
lgamma / gamma_half / lsorbit:
POTCAR titles / dates:
k-mesh / ENCUT / NBANDS:
Band windows (BSE) / q:
Optional deps (pySBT, spglib) versions:
Validation level claimed (L0–L3):
Assumptions from this file that apply:
```

---

## 11. Maintenance

- When a feature gains a new L2 gate, update **level** in [`FEATURES.md`](../FEATURES.md) and strike or narrow the matching row here.  
- When a new approximation is introduced, add a subsection **before** merging the feature.  
- Open research problems stay in [`ACADEMIC_ROADMAP.md`](ACADEMIC_ROADMAP.md); this file is only **constraints on interpretation**.
