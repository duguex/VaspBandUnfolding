# X6: Exciton Real-Space Density — Reproduction Recipe

## Overview

X6 reconstructs the real-space electron/hole density of a selected
exciton from `BSEFATBAND` and the full `WAVECAR`.  The reconstruction
requires the Bloch-state phases from `WAVECAR` to assemble the
exciton envelope in real space, which is why the `WAVECAR` must be
from the **same** VASP run that produced the `BSEFATBAND`.

The example `examples/bseplot/` only bundles the `BSEFATBAND` file
(for X5 / `bseplot bz`), not the full `WAVECAR`.

## Reproduction outline

1.  Run a VASP GW/BSE workflow that produces both `BSEFATBAND`
    and the matching `WAVECAR` / `OUTCAR` / `POSCAR`.
2.  Copy `WAVECAR`, `OUTCAR`, `POSCAR`, `BSEFATBAND`,
    `BSEFATBAND_bse` into a working directory.
3.  Run:
    ```bash
    bseplot realspace \
        --bsefatband BSEFATBAND \
        --wavecar WAVECAR \
        --poscar POSCAR \
        --outcar OUTCAR \
        --exciton 1 \
        --output x1_density.vasp
    ```

## Data requirements (crisp)

| Artifact | Role |
|----------|------|
| `WAVECAR` | Phase information for Bloch states |
| `OUTCAR` | Band energies, symmetry ops |
| `POSCAR` | Lattice vectors |
| `BSEFATBAND` | Exciton coefficients |
| `BSEFATBAND_bse` | VASP binary (if available) |

## Current status

- **X6**: L1–L2 (`bseplot realspace` works when a WAVECAR is
  supplied; the bundled example only covers X5 (BZ density) because
  the WAVECAR is not checked in).
- The example is `skip` in the C1 smoke test for this reason.

> See `examples/bseplot/README.md` and `FEATURES.md` for current
> level assignments.
