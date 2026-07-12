# X1/X2/X3: BSE Matrix Benchmarks (BP example)

## Overview

The `examples/bsematrix/BP/` directory contains text-format benchmark
artifacts for the BSE interaction matrix (X1), PAW modes (X2), and
finite-q kernels (X3).  A full regeneration requires a working VASP
tree (v.5.4.4) and the GW/BSE workflow.

## Reproduction outline

Full step-by-step instructions are in the example README:

[`examples/bsematrix/BP/README.md`](../../examples/bsematrix/BP/README.md)

The sequence is:

1.  **WAVEDER** — one-shot `LOPTICS=.TRUE.` run from a converged
    ground state.
2.  **GW** — single-shot `INCAR.gw` settings.
3.  **VASP BSE** — three INCAR variants (exchange-only, direct-only,
    both).
4.  **Python BSE** — `bsematrix.py` with `--mode pw_only` (and
    optionally `paw_orth_only`/`paw_full`).
5.  **Compare** — `max|ΔA|` and eigenvalue tables (already in README).

## Data requirements (crisp)

| Artifact | Location in VASP run dir | Comment |
|----------|--------------------------|---------|
| `WAVECAR` | `$SCRATCH` | From ground-state SCF |
| `CHGCAR` | `$SCRATCH` | From ground-state SCF |
| `WAVEDER` | `$SCRATCH` | From LOPTICS step |
| `BSEFATBAND` | `$SCRATCH` | From VASP BSE step |
| `BSE_AMAT.bin` | `$SCRATCH` | Binary matrix dump for text comparison |

## Current status

- **pw_only**: L2 (agrees with VASP within a few meV for eigenvalues,
  `max|ΔA|` < 0.006 eV).
- **paw_orth_only / paw_full**: L1–L2 (visible gaps; see README tables).
- **finite-q**: L0–L1 (quarantine — not validated; do not cite).

> See `FEATURES.md` X1–X3 notes for the current level assignments.
