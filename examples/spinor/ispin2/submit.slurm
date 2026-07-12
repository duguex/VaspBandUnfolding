#!/bin/bash
#SBATCH -p test
#SBATCH -n 40
#SBATCH -N 1
#SBATCH --qos=qos_test
#SBATCH -o %j.log

ulimit -s unlimited
sed -i "s/\r\$//" POSCAR 2>/dev/null || true
date > .timeout
singularity exec ~/vasp_latest.sif mpirun /opt/vasp.6.5.1/bin/vasp_gam > vasp_stdout.log 2>&1
EXIT_CODE=$?
# IMPORTANT: marker write (.completed/.failed) MUST happen before
# `rm -f .timeout` and `cat vasp_stdout.log`. If SLURM OOM-kills
# the script in the gap, a missing .timeout with no .completed/
# .failed marker leaves the daemon in a "missing from queue, no
# marker" loop forever. See issue #54.
if [ $EXIT_CODE -eq 0 ]; then
    echo "CRISP_COMPLETED"
    tail -3 OUTCAR 2>/dev/null | grep "energy without entropy" || true
    echo "$(date)" > .completed
else
    echo "CRISP_FAILED"
    echo "CRISP_FAILED" > .failed
    echo "EXIT_CODE: $EXIT_CODE" >> .failed
    echo "---" >> .failed
    tail -30 "${SLURM_JOB_ID}".log >> .failed 2>/dev/null
fi
# Marker is now on disk. Safe to flush stdout and remove timeout.
cat vasp_stdout.log
rm -f .timeout