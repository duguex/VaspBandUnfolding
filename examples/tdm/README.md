# Example: Transition dipole (PS)

| Field | Value |
|---|---|
| Feature IDs | W4 (P5 optional, see below) |
| Level | L0–L1 |
| Citation | experimental only until C2 L2 |
| Runner | `bash run.sh` |

## Purpose

Compute a transition dipole matrix element between two pseudo-wavefunction
bands via `get_dipole_mat`.  The code uses the velocity-gauge momentum matrix
from plane-wave coefficients and converts to the length gauge via the p–r
relation.  This is the pseudo-potential (PS) path only — no PAW one-center
corrections.

W4 covers the PS-only path.  P5 (all-electron dipole, requiring
`aewfc.get_dipole_mat`) is **optional** and not exercised by this runner.

## Inputs

- Required: a WAVECAR file readable by `vaspwfc`.
  - Default location: `../wfc_r/WAVECAR` (relative to this directory).
  - Override via environment variable `VBU_TDM_WAVECAR`.

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `2` missing data (skip), `1` failure.

## Expected outputs

- `ref/dipole_ps.txt` — complex dipole matrix components (x, y, z) in Debye,
  each row real / imag.
- `ref/dipole_ps_abs_max.txt` — `abs_max=…` of the absolute dipole vector.

## Assumptions

See `docs/ASSUMPTIONS.md` sections:
- [§3.1 Transition dipole (W4, P5)](../../docs/ASSUMPTIONS.md#31-transition-dipole-w4-p5)

Key limitations for this level:

1. **p–r relation** is approximate in periodic solids — position operator is
   ill-defined in Bloch states (PRB **87**, 125301, 2013).
2. Only the **PS** path is exercised; PAW one-center corrections (P5) are
   absent.
3. Degenerate bands (\(E_n \approx E_m\)) yield zero — no special perturbation
   treatment.
4. No many-body renormalisation — single-particle KS energies only.
