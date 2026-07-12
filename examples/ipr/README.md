# Inverse Participation Ratio (IPR)

| Field | Value |
|---|---|
| Feature IDs | W5 |
| Level | L1 — experimental |
| Citation | no |
| Runner | `bash run.sh` |

## Purpose

Compute the inverse participation ratio (IPR) for a delta-like analytic grid
and, when a WAVECAR is available in `examples/wfc_r/`, for a real-space
wavefunction band.

## Inputs

- (optional) `../../wfc_r/WAVECAR` for band IPR

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `2` missing data, `1` failure.

## Expected outputs

- `ref/ipr_analytic.txt` — analytic delta-grid IPR (= 1.0)
- `ref/ipr_wavecar.txt` — (optional) WAVECAR band IPR

## Assumptions

See `docs/ASSUMPTIONS.md` sections: wavefunction, WAVECAR.
