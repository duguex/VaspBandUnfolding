# X6: Exciton real-space density

## Runnable demo (CO2, self-consistent)

No external BSE WAVECAR required:

```bash
cd examples/bseplot/co2_demo
bash run_realspace.sh
# needs: examples/tdm/vasp_optics/work/{WAVECAR,OUTCAR} (local LOPTICS)
```

Pipeline: `bsematrix` (`pw_only`, Hartree, ε=5) → `BSEFATBAND` → `bseplot realspace`.

**Citation:** l2-partial (pipeline). **Not** VASP BSE parity for MoSe2.

## MoSe2 / production BSE

Bundled `examples/bseplot/BSEFATBAND` (+ comparison PNGs) still need the original
matching WAVECAR (not in git). Set:

```bash
export VBU_BSE_WAVECAR=/path/to/WAVECAR
cd examples/bseplot && bash run_realspace.sh
```

## Format fix

`bsematrix._write_bsefatband` writes `real +i* imag` with spaces so
`bsefatband` can parse amplitudes (VASP-compatible field split).
