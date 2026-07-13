# MoSe2 X6 recompute (reduced)

Self-consistent pipeline for exciton real-space density:

1. SCF → `work/WAVECAR` (6×6×1, ENCUT=300, NBANDS=48)
2. `bsematrix` pw_only / Hartree / ε=8 → `BSEFATBAND`
3. `bseplot realspace` → `ref/mose2_x1_001_electron_rho.vasp`

Not VASP GW+BSE parity with the large bundled `examples/bseplot/BSEFATBAND`.

```bash
bash run_realspace.sh
```

Large dumps under `work/` and density `.vasp` are gitignored; keep
`ref/realspace_summary.txt`.
