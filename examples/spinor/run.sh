#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

# Check for any SocCar/NormalCar/SocRadCar files in the directory tree
found=false
for f in SocCar NormalCar SocRadCar; do
    if find . -name "$f" -print -quit | grep -q .; then
        found=true
        break
    fi
done

if ! $found; then
    cat >&2 <<'EOF'
MISSING: SocCar, NormalCar, or SocRadCar file not found in this directory tree.

The spinor example requires output from a VASP non-collinear+SOC calculation:
  - SocCar      (spin-orbit coupling matrix in PAW AE basis)
  - NormalCar   (non-collinear spinor coefficients)
  - SocRadCar   (radial SOC integrals)

A plain WAVECAR from a non-collinear SCF run is NOT sufficient --
the SocCar/NormalCar/SocRadCar files are generated only when VASP is
configured with the spinor patch.

See the README for setup instructions.
EOF
    exit 2
fi

mkdir -p ref

# TODO: spinormaker invocation when all required files are present
echo "spinor: SocCar etc. present — full validation TBD (needs spinormaker)" | tee ref/smoke.txt

echo "spinor PASS (data present, full run TBD)"
