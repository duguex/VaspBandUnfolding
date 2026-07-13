# Reproduction Recipes

This directory holds per-ID recipes for running VASP calculations that produce
the heavy inputs (WAVECAR, SocCar, BSEFATBAND, etc.) needed by examples that
cannot bundle them in the git tree.

## Recipes

- [x] **O2**: [`O2_spinor_patch.md`](O2_spinor_patch.md) — how to get `NormalCAR` (`rsgrad`) and `SocCar`/`SocRadCar` (VASP 5.4.4 patches from NAMD with SOC); related repos
- [ ] **B1**: `examples/unfold/sup_3x3x1` — full supercell SCF → spectral weights
- [ ] **X6**: `examples/bseplot` — exciton realspace density from full WAVECAR
- [ ] **X1**: `examples/bsematrix/BP` — BSE matrix rebuild from dielectric / WAVEDER tree
- [ ] **W4**: `examples/tdm/vasp_optics` — LOPTICS job for dipole L2 (INCAR checked in; re-run if WAVECAR empty)

## Policy

Personal-fork development only; do not open PRs to upstream unless requested.
