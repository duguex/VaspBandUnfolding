# Reproduction Recipes

This directory holds per-ID recipes for running VASP calculations that produce
the heavy inputs (WAVECAR, SocCar, BSEFATBAND, etc.) needed by examples that
cannot bundle them in the git tree.

## Planned recipes

- [ ] **B1**: `examples/unfold/sup_3x3x1` — full supercell SCF → spectral weights
- [ ] **O2**: `examples/spinor` — non-collinear+SOC with spinor patch → SocCar / NormalCar
- [ ] **X6**: `examples/bseplot` — exciton realspace density from full WAVECAR
- [ ] **X1**: `examples/bsematrix/BP` — BSE matrix rebuild from dielectric / WAVEDER tree

Each recipe will live as `<ID>.md` in this directory (e.g. `B1.md`, `O2.md`).
Include VASP version, INCAR flags, `crisp submit` commands, and expected output hashes.
