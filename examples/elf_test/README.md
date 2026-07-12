# ELF: Electron Localization Function

Computes the electron localization function (ELF) from a VASP WAVECAR.

## Feature IDs

| ID | Description |
|----|-------------|
| W6 | Electron localization function via `vaspwfc.elf()` |

## Level

**L0 — experimental.** The ELF computation runs but has not been validated
against reference VASP ELFCAR output for general cases.

## Citation

The ELF implementation follows standard definitions (Becke & Edgecombe 1990).
No separate publication exists for this demo — cite the base reference.

## Runner

```bash
bash run.sh        # requires WAVECAR; writes ref/elf_stats.txt
```

Exit codes: `0` success, `2` missing data (no WAVECAR), `1` failure.
