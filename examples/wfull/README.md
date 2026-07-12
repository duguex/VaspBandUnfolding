# Screened Potential (WFULL) Fortran Record

| Field | Value |
|---|---|
| Feature IDs | X4 |
| Level | L1 — experimental |
| Citation | no |
| Runner | `bash run.sh` |

## Purpose

Verify the Fortran unformatted record read/write logic used by the `wfull`
module (`_read_fortran_record`). Writes, reads, and validates a tiny binary
record.

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `1` failure.

## Expected outputs

- `ref/roundtrip.txt` — comparison of original vs. recovered float values

## Assumptions

See `docs/ASSUMPTIONS.md` sections: screened potential, WFULL.
