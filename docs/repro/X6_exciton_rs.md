# X6: Exciton real-space density

## Requirement

`BSEFATBAND` + **matching** `WAVECAR` (+ `OUTCAR` for symmetry/IBZ) from the same BSE calculation.

Bundled under `examples/bseplot/`: `BSEFATBAND`, `OUTCAR`, `POSCAR` — **not** the production WAVECAR (size).

## How to run when you have WAVECAR

```bash
export VBU_BSE_WAVECAR=/path/to/WAVECAR
cd examples/bseplot
bash run_realspace.sh
# or:
bseplot realspace --bsefatband BSEFATBAND --wavecar "$VBU_BSE_WAVECAR" \
  --poscar POSCAR --exciton 1 --hole 0.5,0.5,0.5 --output-dir ref
```

## BZ-only path (no WAVECAR)

```bash
cd examples/bseplot && bash run.sh   # bseplot bz
```

## Status

- **X5 bz**: ok / l2-partial  
- **X6 realspace**: experimental until matching WAVECAR is supplied
