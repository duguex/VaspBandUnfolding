# X6: Exciton real-space density

## A. CO2 self-consistent demo

```bash
cd examples/bseplot/co2_demo && bash run_realspace.sh
# needs examples/tdm/vasp_optics/work/{WAVECAR,OUTCAR}
```

## B. MoSe2 reduced recompute (this host)

Primitive MoSe2, **6×6×1** SCF (`ENCUT=300`, `NBANDS=48`) then
`bsematrix` (`pw_only`, Hartree, ε=8) → `bseplot realspace`.

```bash
cd examples/bseplot/mose2_recompute
bash run_realspace.sh   # needs local vasp_std; work/ is gitignored
```

Metrics: `ref/realspace_summary.txt`.

**Not** a bit-identical remake of the bundled VASP `ALGO=BSE` fatband
(24×24×1 / NBANDS=144 / GW). That production path remains optional.

## C. Bundled MoSe2 BSEFATBAND + external WAVECAR

```bash
export VBU_BSE_WAVECAR=/path/to/matching/WAVECAR
cd examples/bseplot && bash run_realspace.sh
```

## Format

`bsematrix` writes `real +i* imag` with spaces for `bsefatband` parsing.
