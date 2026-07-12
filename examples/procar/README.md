# PROCAR Orbital Projections

| Field | Value |
|---|---|
| Feature IDs | B4 |
| Level | L1 — experimental |
| Citation | no |
| Runner | `bash run.sh` |

## Purpose

Read a VASP PROCAR file (either from an existing calculation in
`examples/projectors/` or a minimal synthetic file) and dump the orbital
projection table to `ref/procar_table.txt`.

## Inputs

- (optional) `../../projectors/lreal_false/PROCAR` or `lreal_true/PROCAR`
- (fallback) synthetic minimal PROCAR is generated

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `1` failure.

## Expected outputs

- `ref/procar_table.txt` — orbital-resolved projections per band

## Assumptions

See `docs/ASSUMPTIONS.md` sections: PROCAR, wavefunction.
