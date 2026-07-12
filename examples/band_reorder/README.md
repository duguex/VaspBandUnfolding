# Band Reordering by Wavefunction Overlap

Demonstrates band reordering by computing wavefunction overlap between
neighbouring k-points. This is useful when bands cross and VASP's default
ordering is not sufficient for post-processing.

## Feature IDs

| ID | Description |
|----|-------------|
| B3 | Band reordering: track band character across the BZ |

## Level

**L0 — placeholder.** The runner validates WAVECAR I/O but the actual
band-reordering logic is not yet implemented for this example.

## Citation

See the `vaspwfc` module documentation. No separate publication exists
for this demo.

## Runner

```bash
bash run.sh        # requires WAVECAR; writes ref/wavecar_info.txt
```

Exit codes: `0` success, `2` missing data (no WAVECAR), `1` failure.
