#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd):${PYTHONPATH:-}"

WCA="${VBU_WAVECAR_A:-}"
WCB="${VBU_WAVECAR_B:-}"

if [[ -z "$WCA" ]]; then
    if [[ -f WAVECAR_A ]]; then
        WCA=WAVECAR_A
    else
        echo "MISSING: WAVECAR_A (set VBU_WAVECAR_A env or place WAVECAR_A locally)" >&2
        exit 2
    fi
fi

if [[ -z "$WCB" ]]; then
    if [[ -f WAVECAR_B ]]; then
        WCB=WAVECAR_B
    else
        echo "MISSING: WAVECAR_B (set VBU_WAVECAR_B env or place WAVECAR_B locally)" >&2
        exit 2
    fi
fi

if [[ "$WCA" == "$WCB" ]]; then
    echo "WARNING: WAVECAR_A and WAVECAR_B point to the same file; NAC requires two different frames." >&2
fi

mkdir -p ref
python run.py "$WCA" "$WCB"
echo "nac PASS"
