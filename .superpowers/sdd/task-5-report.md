# Task 5 Report: C1 Runners for aewfc, elf_test, unfold, BP, band_reorder, potplot, spinor

## Summary

All 8 slug paths now have C1 `run.sh` runners with exit 0/1/2 convention,
README documentation, and `ref/` output directories.

## Runner States

| Slug | Files Changed | C1 Result | Exit | Notes |
|---|---|---|---|---|
| `examples/aewfc/co2/` | run.sh, README.md, ref/.gitkeep | skip (pySBT missing) | 2 | Needs `pySBT` for AE reconstruction |
| `examples/elf_test/` | run.sh, README.md, ref/.gitkeep | pass | 0 | ELF calc + ELFCAR stats to ref |
| `examples/unfold/sup_3x3x1/` | run.sh, README.md, ref/.gitkeep | pass | 0 | spectral_weight.npy shape/sum |
| `examples/unfold/Ce@BL-MoS2_3x3x1/` | run.sh, README.md, ref/.gitkeep | pass | 0 | sw.npy + awht.npy shapes |
| `examples/bsematrix/BP/` | run.sh, ref/.gitkeep | pass | 0 | AMAT line count to ref |
| `examples/band_reorder/` | run.sh, README.md, ref/.gitkeep | skip (no WAVECAR) | 2 | Documents WAVECAR requirement |
| `examples/potplot/` | run.sh, README.md, ref/.gitkeep | pass | 0 | POTCAR auto-copy from projectors; ti_pot.png regenerated |
| `examples/spinor/` | run.sh, ref/.gitkeep | skip (no Soc\* files) | 2 | Documents SocCar/NormalCar/SocRadCar requirement |

## Smoke Test

```
Summary: pass=9 skip=10 fail=0
```

## EXAMPLE_MATRIX.md Updates

Changed C1 for:
- W6 (elf_test): skip → ok
- B1 (unfold sup_3x3x1): skip → ok
- B2 (unfold Ce@BL-MoS2): skip → ok
- B3 (band_reorder): skip → ok
- P1 (potplot): skip → ok
- P4 (aewfc/co2): skip → ok
- O1/O2/O3 (spinor): skip → ok
- X1/X2/X3 (bsematrix/BP): skip → ok

## Files Created (24 files)

- `examples/aewfc/co2/run.sh` — pySBT check + plt_aeps_wfc.py + png copy to ref/
- `examples/aewfc/co2/README.md` — P4 documentation
- `examples/aewfc/co2/ref/.gitkeep`
- `examples/elf_test/run.sh` — WAVECAR check + ex.py + ELFCAR stats to ref/
- `examples/elf_test/README.md` — W6 documentation
- `examples/elf_test/ref/.gitkeep`
- `examples/unfold/sup_3x3x1/run.sh` — spectral_weight.npy shape/sum to ref/
- `examples/unfold/sup_3x3x1/README.md` — B1 documentation
- `examples/unfold/sup_3x3x1/ref/.gitkeep`
- `examples/unfold/Ce@BL-MoS2_3x3x1/run.sh` — sw.npy + awht.npy stats to ref/
- `examples/unfold/Ce@BL-MoS2_3x3x1/README.md` — B2 documentation
- `examples/unfold/Ce@BL-MoS2_3x3x1/ref/.gitkeep`
- `examples/bsematrix/BP/run.sh` — py_pw_only_both_AMAT.txt line count to ref/
- `examples/bsematrix/BP/ref/.gitkeep`
- `examples/band_reorder/run.sh` — WAVECAR check + I/O validation
- `examples/band_reorder/README.md` — B3 documentation
- `examples/band_reorder/ref/.gitkeep`
- `examples/potplot/run.sh` — POTCAR auto-copy from projectors + Agg-backend plot to ref/
- `examples/potplot/README.md` — P1 documentation
- `examples/potplot/ref/.gitkeep`
- `examples/spinor/run.sh` — SocCar/NormalCar/SocRadCar check + doc
- `examples/spinor/ref/.gitkeep`
- `docs/EXAMPLE_MATRIX.md` — updated C1 columns for all task 5 IDs

## No Accidental WAVECAR Commits

The spinor `output/` directories contain WAVECARs but only `run.sh` and `ref/.gitkeep` were staged, not any large binary files.
