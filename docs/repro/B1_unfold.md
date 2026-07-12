# B1/B2: Band Unfolding — Reproduction Recipe

## Overview

B1 (spectral-weight unfolding) and B2 (atomic-weight EBS) require a
supercell VASP calculation.  The example data in
`examples/unfold/sup_3x3x1/` and `examples/unfold/Ce@BL-MoS2_3x3x1/`
do **not** bundle the full `WAVECAR` due to size.

## Reproduction outline

1.  Build the supercell `POSCAR` from the primitive cell (3×3×1
    MoS₂, or a defected supercell for B2).
2.  Run a ground-state VASP calculation (standard or gamma-only,
    `NBANDS` large enough to cover the energy window of interest).
3.  Copy the resulting `WAVECAR` and `OUTCAR` into the example
    directory.
4.  Run the unfolding script:
    ```bash
    cd examples/unfold/sup_3x3x1
    python ../ebs_unfold.py
    ```
    or for the Ce@BL-MoS2 case:
    ```bash
    cd examples/unfold/Ce@BL-MoS2_3x3x1
    python plt_unf.py
    ```

## Data requirements (crisp)

| Artifact | Notes |
|----------|-------|
| Supercell `POSCAR` | 3×3×1 or as desired |
| `WAVECAR` | Ground-state, NBANDS ≥ ~64 |
| `OUTCAR` | Band energies, Fermi level |
| `KPOINTS` | Γ-centred mesh covering PBZ path |
| Primitive-cell `POSCAR` | For PBZ k-path generation |

## Current status

- **B1**: L1–L2 (cached `.npy` files present; full recompute needs
  WAVECAR).
- **B2**: L1 (atomic-weight overlay; WAVECAR-dependent).

> See `examples/unfold/README.md` and the main `FEATURES.md` for
> current level assignments.
