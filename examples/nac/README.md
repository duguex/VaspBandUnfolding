# Non-Adiabatic Couplings (NAC)

| Field | Value |
|---|---|
| Feature IDs | D1 |
| Level | L2 |
| Citation | yes |
| Runner | `bash run.sh` |

## Purpose

Compute the Non-Adiabatic Coupling (NAC) matrix elements between electronic
states at two different atomic geometries (consecutive ionic steps in a
molecular-dynamics trajectory).  NACs quantify how fast electronic states
mix as the nuclei move and are the key input to fewest-switches surface-hopping
(NACme) and other non-adiabatic dynamics methods.

## Inputs

- Required: two WAVECAR files, one for each ionic geometry.
  - WAVECAR file at geometry A: `WAVECAR_A` in this directory, or the path
    in environment variable `VBU_WAVECAR_A`.
  - WAVECAR file at geometry B: `WAVECAR_B` in this directory, or the path
    in environment variable `VBU_WAVECAR_B`.
- The two WAVECARs **must** correspond to different ionic steps (different
  geometries).  A NAC computed with the same frame twice is meaningless.

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `2` missing data (skip), `1` failure.

## Expected outputs

- `ref/api_present.txt` — confirms that `nac_from_vaspwfc` is importable.
  Full NAC results (e.g. `ref/nac_D1.txt`) require two distinct WAVECARs from
  a real MD trajectory (not yet provided in this example).

## Assumptions

See `docs/ASSUMPTIONS.md` sections:
- [§D1 Non-Adiabatic Couplings](../../docs/ASSUMPTIONS.md#d1-non-adiabatic-couplings)

Key limitations at this level:

1. Full NAC computation requires two real WAVECAR files from different ionic
   steps.  This example performs an **import-only** check and reports readiness.
2. Runtime scaling grows with the number of bands × k-points.
3. For degenerate or near-degenerate states special care (smooth orbital
   alignment) is needed — not yet implemented.
