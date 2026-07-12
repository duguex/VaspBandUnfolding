# POTCAR / PAW Projector Visualization

Visualizes the PAW projector functions and partial waves stored in a
VASP POTCAR file.

## Feature IDs

| ID | Description |
|----|-------------|
| P1 | POTCAR / partial waves: `paw.pawpotcar` and `potplot` bin |

## Level

**L1 — partial.** The plot is regenerated successfully from a POTCAR
but only for the first element. Multi-element POTCAR support is
available via `-n` in the `potplot` CLI but not exercised by this runner.

## Citation

PAW dataset format follows the VASP POTCAR specification.
See the `paw` module documentation for references.

## Runner

```bash
bash run.sh        # requires POTCAR in CWD or copies from projectors/; writes ref/ti_pot.png
```

Exit codes: `0` success, `2` missing data (no POTCAR reachable), `1` failure.
