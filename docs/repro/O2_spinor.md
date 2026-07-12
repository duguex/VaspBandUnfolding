# O1/O2/O3: Spin–Orbit / Spinor — Reproduction Recipe

## Overview

O1 (SOC matrix elements) and O2 (spinor WAVECAR construction) require
binary files produced by VASP's spinor patch (`SocCar`, `SocRadCar`,
`NormalCar`).  These are **not bundled** in the repo due to size and
version sensitivity.

## Reproduction outline

1.  Set up a non-collinear+SOC VASP calculation (`LSORBIT=.TRUE.`,
    `ISYM=0`, `ISPIN=1` with `LNONCOLLINEAR=.TRUE.`).
2.  Run SCF — VASP produces `SocCar`, `SocRadCar`, `NormalCar` in
    addition to `WAVECAR`.
3.  Copy these files into `examples/spinor/`.
4.  Run the example script:
    ```bash
    cd examples/spinor
    python socclass.py
    ```

## Data requirements (crisp)

| Artifact | Produced by VASP | Size estimate |
|----------|------------------|--------------|
| `WAVECAR` | SCF (ncl) | ~1 MB (monolayer) |
| `SocCar` | SCF (ncl, LSORBIT) | ~10 KB |
| `SocRadCar` | SCF (ncl, LSORBIT) | ~10 KB |
| `NormalCar` | SCF (ncl) | ~10 KB |
| `OUTCAR` | SCF | ~50 KB |

## Current status

- **O1**: L1 (SOC matrix read path works; cross-checked on small
  systems).
- **O2**: L1 (spinor construction demo exists; comparison to
  ncl-WAVECAR pending).
- **O3**: L0–L1 (MAE helpers; not exercised in example).

> All three are `skip` in the C1 smoke test because the required
> binary inputs are missing from the checkout.
