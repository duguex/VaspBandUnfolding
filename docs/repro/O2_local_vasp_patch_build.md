# Local VASP 5.4.4 + SOC dump patch (this machine)

## Layout (gitignored — do not commit sources)

```text
vasp.5.4.4.pl2.tgz                 # user-provided tarball (gitignored)
third_party/vasp.5.4.4.pl2/        # extracted + patched tree
third_party/vasp_patch_backups/    # original .F before patch
third_party/NAMDwithSOC/           # patch source clone
```

## Patch applied

From [ZhenfaZheng/NAMDwithSOC](https://github.com/ZhenfaZheng/NAMDwithSOC)  
`patches/soc_vasp_5.4.4/{main,paw,relativistic,stm}.F` → `third_party/vasp.5.4.4.pl2/src/`.

Verified strings in tree:

- `relativistic.F`: `OPEN(FILE='SocCar'...)`, `SocAllCar`, `SocRadCar`
- `stm.F`: `OPEN(... FILE='NormalCAR'...)`

Originals saved under `third_party/vasp_patch_backups/*.orig`.

## Build

```bash
cd third_party/vasp.5.4.4.pl2
# makefile.include already points at system OpenMPI/OpenBLAS/FFTW
make std -j$(nproc)    # and/or make ncl
# binaries: bin/vasp_std  bin/vasp_ncl (if built)
```

If link errors appear, adjust `makefile.include` library names for this host.

## After binary exists

1. Run a small SCF (prefer ncl + LSORBIT if required by your dump path) in a work dir with POSCAR/POTCAR/KPOINTS/INCAR.
2. Expect dumps: `SocCar`, `SocRadCar`, `NormalCAR` (and maybe `SocAllCar`).
3. Copy into `examples/spinor/ispin2/` with WAVECAR and run `spinormaker`.

Alternatively generate **NormalCAR only** without this binary:

```bash
rsgrad normalcar --wavecar WAVECAR --poscar POSCAR --potcar POTCAR -o NormalCAR
```

## License

VASP sources are proprietary. Keep them **out of git** (see root `.gitignore`).
