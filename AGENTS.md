# Repository Guidelines

## Project Overview

**VaspBandUnfolding** (PyVaspWfc v1.0) — a collection of Python modules for reading and analyzing VASP (Vienna Ab initio Simulation Package) output files. Core capabilities:

- Read WAVECAR binary band coefficients (plane-wave, gamma-only, noncollinear/SOC)
- Unfold supercell band structures into primitive-cell effective band structure (Phys. Rev. B 85, 085201)
- Reconstruct all-electron wavefunctions from pseudo-wavefunctions via PAW one-center expansions
- Build and diagonalize the Bethe-Salpeter Equation (BSE) interaction matrix, cross-checked against VASP
- Parse BSEFATBAND exciton data and reconstruct real-space electron/hole densities
- Construct spinor WAVECARs from collinear calculations via SOC Hamiltonian
- Compute dipole transition matrix elements, non-adiabatic couplings, ELF, IPR
- Parse POTCAR (projector/partial-wave data), PROCAR (orbital projections)
- Ewald summation / Madelung constants for periodic crystals
- NEB minimum energy path plotting

Author: Qijing Zheng (zqj.kaka@gmail.com) · [GitHub](https://github.com/QijingZheng/VaspBandUnfolding)

- Full feature checklist (module / CLI / example / status): [`FEATURES.md`](FEATURES.md)
- Live engineering/citation snapshot: [`docs/STATUS.md`](docs/STATUS.md)
- Secondary development goals (scientific proof + reusable components): [`docs/GOALS.md`](docs/GOALS.md)
- Expert academic roadmap (all feature IDs, seminars, validation levels): [`docs/ACADEMIC_ROADMAP.md`](docs/ACADEMIC_ROADMAP.md)
- Assumptions & interpretation limits: [`docs/ASSUMPTIONS.md`](docs/ASSUMPTIONS.md)
- Citation policy (what you may claim): [`docs/CITATION_POLICY.md`](docs/CITATION_POLICY.md)

## Collaboration & Git policy (mandatory)

- **Never open PRs against upstream** `QijingZheng/VaspBandUnfolding` (no `gh pr create` to the original project).
- Development is **local + personal fork only**: https://github.com/duguex/VaspBandUnfolding
- Remotes (typical):
  - `origin` → upstream (fetch/reference only; do not push unless user explicitly asks)
  - `fork` → `duguex/VaspBandUnfolding` (default push target for feature branches)
- Do not propose or create pull requests “back to author” unless the user **explicitly** reverses this policy in chat.

---

## Architecture & Data Flow

### Layout

Flat single-directory package — **no `src/` layout**. All modules live at the repo root as bare `py-modules` (package name `PyVaspWfc`). `bin/` scripts inject the parent directory onto `sys.path` and call module `main()`.

### Module dependency graph

```
vasp_constant.py   — leaf: physical constants
sph_harm.py        — leaf: real/complex spherical harmonics
spline.py          — leaf: 1D cubic spline (VASP SPLCOF replica)
wfull.py           — leaf: screened potential binary reader
hse_kpts.py        — leaf (uses spglib): IBZ k-point generation
spinorb.py         — leaf (reads SocRadCar/NormalCar): SOC matrix elements

vaspwfc.py         ← vasp_constant       — core WAVECAR reader
paw.py             ← vasp_constant, sph_harm — POTCAR parser, nonlocal projectors
ewald.py           ← vasp_constant       — Ewald summation
procar.py          ← vaspwfc (optional)  — PROCAR parser
spinor.py          ← vaspwfc, spinorb    — SOC spinor construction

unfold.py          ← vaspwfc             — band unfolding
nac.py             ← vaspwfc             — non-adiabatic couplings
band_order.py      ← vaspwfc             — band re-ordering by overlap
aewfc.py           ← vaspwfc, sph_harm, paw — AE wavefunction reconstruction
bsematrix.py       ← vasp_constant, sph_harm, wfull — BSE matrix
bsefatband.py      — BSEFATBAND parser/exciton viz (uses ase/matplotlib; WAVECAR via vaspwfc)
```

### Data flow pattern

1. **Binary I/O** — VASP binary files use Fortran unformatted records. Three approaches coexist:
   - `vaspwfc.py`: `np.fromfile` + `seek` by fixed `recl` (WAVECAR record length)
   - `wfull.py`: manual 4-byte little-endian length markers (`struct.unpack('<i', ...)`)
   - `spinorb.py`: `scipy.io.FortranFile` for NormalCar/SocCar
2. **Parsing** — ASCII VASP files (POTCAR, PROCAR, OUTCAR, POSCAR, KPOINTS, BSEFATBAND) via regex/line scanning; POTCAR D-notation converted to E-notation.
3. **Computation** — Heavy numpy vectorization (meshgrid, tensordot, advanced indexing); FFT via `scipy.fftpack` / `scipy.fft`; sparse block-diagonal ops via `scipy.sparse.block_diag`.
4. **Output** — VASP-format grids (VESTA), `.npy` arrays, matplotlib figures, text dumps (`AMAT`, `BSEFATBAND`-style).

### VASP format variants handled

| Variant | How to open | Notes |
|---|---|---|
| Standard WAVECAR | `vaspwfc('WAVECAR')` | complex coeffs; `rtag=45200`→float32, `45210`→float64 |
| Gamma-only | `vaspwfc(..., lgamma=True, gamma_half='x'\|'z')` | half PW set; √2 scaling for G≠0; default half-axis `'x'` (VASP ≥5.4) |
| Noncollinear/SOC | `vaspwfc(..., lsorbit=True)` | spinor: 2×nplw coeffs (up then down); `wfc_r` returns two 3D arrays |
| Conflict | — | `lsorbit` and `lgamma` must not both be True |

### WAVECAR record addressing

`whereRec(ispin, ikpt, iband) = 2 + (ispin-1)*nkpts*(nbands+1) + (ikpt-1)*(nbands+1) + iband`  
Indices (`ispin`, `ikpt`, `iband`) are **1-based**.

---

## Key Directories

| Path | Purpose |
|---|---|
| `.` (repo root) | All Python source modules — flat layout |
| `bin/` | CLI entry-point scripts (`#!/usr/bin/env python3`) |
| `examples/` | Per-feature subdirs with VASP inputs and reference outputs |
| `doc/` | Bibliography PDF (`VaspBandUnfolding.pdf`) |
| `.gitignore` | Ignores `__pycache__/`, `build/`, `dist/`, `PyVaspWfc.*/`, `*.swp`, `.DS_Store` |

### `examples/` feature map

| Subdir | Validates |
|---|---|
| `wfc_r/` | Real-space pseudo-wavefunction FFT |
| `unfold/` | Band unfolding (MoS2 supercells, defects) |
| `spinor/` | SOC spinor WAVECAR construction |
| `projectors/` | PAW projector vs NormalCar |
| `aewfc/co2/` | All-electron reconstruction |
| `bsematrix/BP/` | BSE matrix vs VASP (40+ text refs) |
| `bseplot/` | Exciton BZ/real-space density |
| `elf_test/`, `ewald/`, `potplot/`, `band_reorder/` | ELF, Madelung, POTCAR viz, band reorder |
| `tdm/` | PS dipole gates vs local LOPTICS |
| `nac/` | Dual-frame NAC (local WAVECARs) |

---

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt           # numpy, scipy, matplotlib, ase
pip install -r requirements-optional.txt  # pySBT (spherical Bessel / AE workflows)

# Install package
pip install -e .                          # editable (preferred for development)
pip install .                             # regular install from clone
pip install git+https://github.com/QijingZheng/VaspBandUnfolding

# Run a CLI tool (after install, or via python bin/...)
wfcplot -w WAVECAR -p POSCAR -s 1 -k 1 -n 1
python bin/wfcplot -w WAVECAR -p POSCAR -s 1 -k 1 -n 1

# Run modules with __main__ blocks
python bsematrix.py ...
python bsefatband.py ...
python spinor.py ...
python band_order.py
python vaspwfc.py                         # demo block at bottom

# Smoke + unit tests (no CI)
python scripts/smoke_examples.py
PYTHONPATH=. python -m pytest tests/ -q
```

Live snapshot: [`docs/STATUS.md`](docs/STATUS.md).

**No tests, no CI, no formatter, no linter** — zero automated test infrastructure. Validation is manual against `examples/`.

### Registered vs extra CLIs

Installed via `script-files` in `pyproject.toml` / `setup.py`:

- `wfcplot`, `tdmplot`, `potplot`, `nebplot`, `bseplot`, `spinormaker`

Present in `bin/` but **not** registered for install: `bsematrix` — run as `python bin/bsematrix` or `python -m` equivalent after path setup.

---

## Code Conventions & Common Patterns

### Naming

| Convention | Where | Examples |
|---|---|---|
| `snake_case` | Functions, methods, variables | `readBandCoeff`, `save2vesta`, `make_kpath` |
| `PascalCase` | New-style classes only | `ExcitonFatband`, `KpointMatch`, `PairState` |
| `lowercase` | Old-style classes (legacy) | `class vaspwfc`, `class procar`, `class nonlq` |
| `UPPER_CASE` | Constants | `AUTOA`, `RYTOEV`, `TPI`, `HSQDTM` |
| `_prefixed` | Private/internal | `self._fname`, `_read_fortran_record`, `_lgam` |

### Type annotations (three eras coexist)

| Era | Style | Files |
|---|---|---|
| **Old** (~2015) | None — docstring-only | `vaspwfc.py`, `paw.py`, `procar.py`, `unfold.py`, `sph_harm.py`, `nac.py`, `ewald.py`, `band_order.py`, `spline.py`, `aewfc.py` |
| **Transition** (~2020) | `from __future__ import annotations` + basic types | `spinor.py`, `spinorb.py` |
| **New** (~2024) | Full annotations + dataclasses + `NDArray` | `bsematrix.py`, `bsefatband.py`, `wfull.py` |

**Prefer the new style for new code**: `from __future__ import annotations`, Python 3.10+ unions (`str | None`), `@dataclass(frozen=True)`, `NDArray` from `numpy.typing`.

### Docstrings

- **Old code**: `r'''raw triple-single-quote'''` — brief, sometimes absent
- **New code**: `"""triple-double-quote"""` with structured sections (Physical model, Args, Returns)

### Imports

- **Old code**: bare `import numpy as np`, wildcard `from vasp_constant import *`
- **New code**: specific imports only (`from vasp_constant import EDEPS, TPI`), no wildcards
- **New code**: `from __future__ import annotations` first; optional deps behind `try/except ImportError`

### Error handling

- **Old code**: bare `assert` for preconditions, `print("WARNING:...")`, `raise IOError` / `ValueError`
- **New code**: builtin exceptions with messages (`ValueError`, `FileNotFoundError`, `RuntimeError`, `EOFError`)
- **No custom exception classes** anywhere
- Example scripts: `os.path.isfile()` to skip recompute and load cached `.npy`

### CLI patterns

**Older bin scripts** (`wfcplot`, `tdmplot`, `potplot`, `nebplot`) — argparse lives in the script:

```python
def parse_cml_args(cml):
    parser = argparse.ArgumentParser(...)
    parser.add_argument(...)
    return parser.parse_args(cml)

def main(cml):
    args = parse_cml_args(cml)
    ...

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
```

**Newer modules** (`bsematrix.py`, `bsefatband.py`, `spinor.py`) — parser + `main()` live in the module; bin wrappers only import and call `main`.

Common short flags: `-w` WAVECAR, `-p` POSCAR/POTCAR, `-s` spin, `-k` k-point, `-n` band (all **1-based**).

### Binary I/O pattern (Fortran records)

```python
def _read_fortran_record(handle):
    """Read one Fortran unformatted record (4-byte length markers)."""
    size_bytes = handle.read(4)
    if not size_bytes:
        return None
    size = struct.unpack('<i', size_bytes)[0]
    data = handle.read(size)
    trailing = handle.read(4)
    # trailing must match size_bytes for a valid record
    return data
```

### Gamma-only √2 convention

Gamma-only WAVECARs store half the plane-wave coefficients. For G≠0:

- Coeffs are stored ×√2 (or must be scaled when reconstructing full set)
- Real-space reconstruction uses half-sized FFT with conjugate symmetry (`irfftn`)

### SOC / spinor convention

Noncollinear WAVECAR doubles storage:

- Spinor band has `2 * nplw` coefficients (spin-up block then spin-down)
- Scalar→spinor band map: `ib_scalar = (ib_spinor + 1) // 2`

---

## Important Files

| File | Role | ~Size |
|---|---|---|
| `vaspwfc.py` | **Core** — WAVECAR reader, real-space FFT, dipole, ELF, IPR | 51 KB |
| `bsematrix.py` | BSE Hamiltonian builder/diagonalizer (largest module) | 109 KB |
| `bsefatband.py` | BSEFATBAND parser, exciton real-space reconstruction | 100 KB |
| `paw.py` | POTCAR parser, nonlocal projector engine | 40 KB |
| `spinorb.py` | Spin-orbit matrix elements | 26 KB |
| `spinor.py` | SOC spinor WAVECAR construction | 23 KB |
| `unfold.py` | Band unfolding (supercell → primitive) | 22 KB |
| `aewfc.py` | All-electron wavefunction reconstruction | 21 KB |
| `procar.py` | PROCAR orbital-projection parser | 18 KB |
| `band_order.py` | Band reordering by Bloch overlap | 9 KB |
| `ewald.py` | Ewald / Madelung | 7 KB |
| `sph_harm.py` | Real/complex spherical harmonics — leaf | 6 KB |
| `nac.py` | Non-adiabatic couplings | 4 KB |
| `wfull.py` | Screened Coulomb potential binary reader — leaf | 3 KB |
| `spline.py` | Cubic spline (VASP SPLCOF) | 3 KB |
| `vasp_constant.py` | Physical constants — leaf | 2 KB |
| `hse_kpts.py` | Irreducible k-points via spglib | 2 KB |
| `pyproject.toml` | Build config (setuptools ≥61, primary) | — |
| `setup.py` | Legacy build config (compatibility) | — |

### CLI scripts (`bin/`)

| Script | Purpose |
|---|---|
| `wfcplot` | Real-space pseudo-wavefunction → VESTA files |
| `tdmplot` | Transition dipole matrix elements (+ optional PAW AE correction) |
| `potplot` | Visualize PAW projectors/partial waves from POTCAR |
| `nebplot` | NEB minimum-energy path from OUTCARs |
| `bseplot` | Exciton BZ density or real-space fixed e/h reconstruction |
| `bsematrix` | Build/diagonalize BSE matrix (`--mode` default **pw_only**) |
| `spinormaker` | Build SOC spinor WAVECAR from scalar/ISPIN=2 |

---

## Runtime & Tooling Preferences

| Requirement | Value |
|---|---|
| **Python** | ≥3.10; mainstream current only ([`docs/GOALS.md`](docs/GOALS.md) G2.1) |
| **Package manager** | `pip` (no Conda, no Poetry) |
| **Build system** | setuptools ≥61 (`pyproject.toml` + legacy `setup.py`) |
| **Formatting** | None — no formatter config |
| **Type checker** | None — annotations are advisory |
| **Linter / CI** | None — no Makefile, tox, or GitHub Actions |
| **Runtime** | CPython; track recent stable `numpy`/`scipy`/`matplotlib`/`ase` — no legacy version matrix |

### Dependencies

| Package | Status | Used in |
|---|---|---|
| `numpy` | Required | Every module |
| `scipy` | Required | FFT, specials, sparse, FortranFile, interpolation |
| `matplotlib` | Required | Plotting (EBS, DOS, excitons, bands) |
| `ase` | Required | POSCAR I/O, supercell, Atoms |
| `pySBT` | Optional (`requirements-optional.txt`) | Spherical Bessel / AE PAW workflows |
| `spglib` | Optional (`requirements-optional.txt`; may be commented — install manually) | `hse_kpts.py` IBZ k-points |

---

## Testing & QA

- **Smoke:** `python scripts/smoke_examples.py` — walks `docs/EXAMPLE_MATRIX.md` unique `examples/*/run.sh` (expect **19 pass** when dumps present for spinor/nac paths that need local WAVECARs).
- **Unit/infra:** `PYTHONPATH=. python -m pytest tests/ -q` (constants, spline, sph_harm, ewald, BSE CLI defaults, …).
- **No CI/CD** — no GitHub Actions, Makefile, or tox in-repo.
- **Validation strategy**: Manual + scripted gates vs VASP / analytic refs under `examples/`
  - Strongest text suite: `examples/bsematrix/BP/` (`pw_only` citable; `paw_*` / finite-q **quarantine**)
  - Dipole: `examples/tdm/ref/l2_table.md` + `run_l2.sh` (needs local LOPTICS workdir)
  - ELF: `examples/elf_test/compare_elf.py` vs ELFCAR
  - Spinor: `examples/spinor/run.sh` + optional `ref/spinor_vs_ncl.txt`
  - Live snapshot: [`docs/STATUS.md`](docs/STATUS.md) · citation: [`docs/CITATION_POLICY.md`](docs/CITATION_POLICY.md)

### What to verify before claiming changes work

1. `python -c "import vaspwfc; print('ok')"` — basic import
2. `python scripts/smoke_examples.py` and/or the touched `examples/<feature>/run.sh`
3. BSE changes: BP tables + keep CLI default `pw_only`
4. Numerical sanity: energies in eV, spectral weights ≤ 1, spinor norms, etc.

### When adding code

- Prefer new-style annotations and specific imports
- Keep 1-based VASP indexing for spin/k/band CLI args
- Validate against example reference data or a known VASP calculation
- Do not introduce a second packaging/layout convention beside the flat `py-modules` root
- Update `FEATURES.md` / `docs/EXAMPLE_MATRIX.md` / `docs/CITATION_POLICY.md` when eng. or citation level changes
