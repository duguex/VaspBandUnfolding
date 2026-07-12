# Irreducible k-points (IBZ)

| Field | Value |
|---|---|
| Feature IDs | B5 |
| Level | L1 — experimental |
| Citation | no |
| Runner | `bash run.sh` |

## Purpose

Compute irreducible k-points in the Brillouin zone for a simple crystal
structure (CsCl) using the `get_ir_kpts` routine and spglib.

## Inputs

- `POSCAR` (copied from `examples/ewald/CsCl.vasp`)

## Requirements

- Python package `spglib` (skip exit 2 when missing)

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `2` spglib not available, `1` failure.

## Expected outputs

- `ref/ibz.txt` — irreducible k-points with weights

## Assumptions

See `docs/ASSUMPTIONS.md` sections: k-points, symmetry.
