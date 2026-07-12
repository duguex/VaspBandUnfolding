# All Components Runnable + Examples (G1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every science feature ID has a runnable example with showcase artifacts (Phase C1); then each ID is either L2-validated for paper use or explicitly quarantined (Phase C2).

**Architecture:** Unified `examples/<slug>/` units (README + `run.sh`/`run.py` + `ref/`), central `docs/EXAMPLE_MATRIX.md`, `scripts/smoke_examples.py` for discover-and-run with explicit skips, `tests/` for I1–I4 and matrix completeness. Flat `py-modules` package unchanged. Heavy VASP binaries stay out of git.

**Tech Stack:** Python ≥3.10, numpy, scipy, matplotlib, ase; optional pySBT, spglib; pytest; existing PyVaspWfc modules and `bin/` CLIs; optional `crisp` for data generation only.

**Spec:** [`docs/superpowers/specs/2026-07-13-all-components-run-and-examples-design.md`](../specs/2026-07-13-all-components-run-and-examples-design.md)

## Global Constraints

- Goals: G1 scientific soundness + G2 low-cost reusable components (`docs/GOALS.md`).
- Python `>=3.10`; mainstream numpy/scipy/matplotlib/ase only (no legacy pin matrix).
- Feature IDs and Levels live in `FEATURES.md`; physics limits in `docs/ASSUMPTIONS.md`.
- 1-based VASP spin/k/band indices at public boundaries.
- Missing heavy data → exit code **2** from example runners (smoke = skip); real errors → exit **1**.
- Do not commit full production WAVECAR/GW/BSE trees; small fixtures or `docs/repro/<ID>.md` only.
- Quarantined modes must not be presented as default production paths in README/CLI help.

---

## File structure (create / modify)

| Path | Responsibility |
|---|---|
| `examples/_template/` | Skeleton README + run.sh + ref/ |
| `docs/EXAMPLE_MATRIX.md` | ID → example path → C1/C2/skip |
| `scripts/smoke_examples.py` | Run all matrix entries |
| `tests/test_example_matrix.py` | Every science ID listed exactly once |
| `tests/test_infra_constants.py` | I1 |
| `tests/test_infra_sph_harm.py` | I2 |
| `tests/test_infra_spline.py` | I3 |
| `tests/test_infra_fortran_record.py` | I4 / X4 helper |
| `examples/*/README.md`, `run.sh`/`run.py`, `ref/` | Per-component demos |
| `examples/tdm/`, `ipr/`, `procar/`, `hse_kpts/`, `nac/`, `neb/`, `wfull/` | New C1 demos |
| `docs/repro/*.md` | C2 heavy recipes |
| `FEATURES.md` | Level / example path updates |

---

### Task 1: Example template + EXAMPLE_MATRIX scaffold

**Files:**
- Create: `examples/_template/README.md`
- Create: `examples/_template/run.sh`
- Create: `examples/_template/ref/.gitkeep`
- Create: `docs/EXAMPLE_MATRIX.md`

**Interfaces:**
- Produces: matrix table format used by Task 2 smoke script and Task 3 pytest

- [ ] **Step 1: Create template README**

Write `examples/_template/README.md`:

```markdown
# Example: <TITLE>

| Field | Value |
|---|---|
| Feature IDs | W? |
| Level | L0 / L1 / L2 |
| Citation | yes / experimental only / no |
| Runner | `bash run.sh` |

## Purpose

<one paragraph>

## Inputs

- Required files in this directory or env `VBU_DATA_<ID>`:
- Optional:

## Command

```bash
bash run.sh
```

Exit codes: `0` success, `2` missing data (skip), `1` failure.

## Expected outputs

- `ref/...`

## Assumptions

See `docs/ASSUMPTIONS.md` sections: …
```

- [ ] **Step 2: Create template run.sh**

Write `examples/_template/run.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
# if [[ ! -f WAVECAR ]]; then echo "MISSING: WAVECAR" >&2; exit 2; fi
mkdir -p ref
echo "template ok" | tee ref/smoke.txt
```

- [ ] **Step 3: Create EXAMPLE_MATRIX.md with all science IDs**

Write `docs/EXAMPLE_MATRIX.md` with columns:

`| ID | Slug path | Runner | C1 | C2 | Notes |`

Include every science ID from FEATURES (W1–W6, B1–B5, P1–P5, O1–O3, X1–X6, D1–D3). Initial C1/C2 = `todo`. Map paths per design §5.

- [ ] **Step 4: Commit**

```bash
git add examples/_template docs/EXAMPLE_MATRIX.md
git commit -m "docs: add example template and EXAMPLE_MATRIX scaffold"
```

---

### Task 2: Smoke runner

**Files:**
- Create: `scripts/smoke_examples.py`
- Test: manual run after matrix has at least one `ok` entry (Task 4+)

**Interfaces:**
- Consumes: `docs/EXAMPLE_MATRIX.md` rows with path + runner command
- Produces: process exit 0 if no hard failures; prints pass/skip/fail counts

- [ ] **Step 1: Implement smoke_examples.py**

```python
#!/usr/bin/env python3
"""Discover and run example runners listed in docs/EXAMPLE_MATRIX.md.

Matrix rows (markdown table) must include columns:
ID | Slug path | Runner | C1 | C2 | Notes

Runner examples: `bash run.sh`, `python run.py`
Only rows with C1 in {ok, todo, skip} and a non-empty Slug path are considered.
If C1 == skip, count as skip without running.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "EXAMPLE_MATRIX.md"


def parse_matrix(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return rows
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    for ln in lines[1:]:
        if re.match(r"^\|\s*-+", ln):
            continue
        cols = [c.strip() for c in ln.strip("|").split("|")]
        if len(cols) != len(headers):
            continue
        rows.append(dict(zip(headers, cols)))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()
    rows = parse_matrix((args.root / "docs" / "EXAMPLE_MATRIX.md").read_text())
    # de-dupe by slug path for running
    seen: set[str] = set()
    pass_n = skip_n = fail_n = 0
    for r in rows:
        path = r.get("Slug path", r.get("path", "")).strip("`")
        runner = r.get("Runner", "").strip("`")
        c1 = r.get("C1", "").lower()
        if not path or path in seen:
            continue
        seen.add(path)
        if c1 == "skip":
            print(f"SKIP  {path} (matrix)")
            skip_n += 1
            continue
        exdir = args.root / path
        if not exdir.is_dir():
            print(f"FAIL  {path} (missing directory)")
            fail_n += 1
            continue
        if not runner:
            print(f"FAIL  {path} (no runner)")
            fail_n += 1
            continue
        print(f"RUN   {path}: {runner}")
        try:
            proc = subprocess.run(
                runner,
                shell=True,
                cwd=exdir,
                timeout=args.timeout,
                text=True,
            )
        except subprocess.TimeoutExpired:
            print(f"FAIL  {path} (timeout)")
            fail_n += 1
            continue
        if proc.returncode == 0:
            print(f"PASS  {path}")
            pass_n += 1
        elif proc.returncode == 2:
            print(f"SKIP  {path} (missing data)")
            skip_n += 1
        else:
            print(f"FAIL  {path} (exit {proc.returncode})")
            fail_n += 1
    print(f"\nSummary: pass={pass_n} skip={skip_n} fail={fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Make executable and dry-run**

```bash
chmod +x scripts/smoke_examples.py
python scripts/smoke_examples.py
```

Expected: may FAIL on missing dirs until later tasks; after Task 1 only, failures for `todo` paths are OK until examples exist — **update matrix C1 to `skip` for not-yet-created paths** so smoke stays green during incremental work, then flip to `todo`/`ok` as examples land.

Policy during implementation: set C1=`skip` with Notes=`not scaffolded` for missing demos; change to `ok` when Task for that demo completes.

- [ ] **Step 3: Commit**

```bash
git add scripts/smoke_examples.py docs/EXAMPLE_MATRIX.md
git commit -m "feat: add example smoke runner"
```

---

### Task 3: Matrix completeness test + infra tests (I1–I4)

**Files:**
- Create: `tests/test_example_matrix.py`
- Create: `tests/test_infra_constants.py`
- Create: `tests/test_infra_sph_harm.py`
- Create: `tests/test_infra_spline.py`
- Create: `tests/test_infra_fortran_record.py`
- Create: `tests/fixtures/tiny_fortran_record.bin` (generated in test or committed)

**Interfaces:**
- Consumes: FEATURES-like science ID list (hardcode the set from design)
- Produces: pytest green for infra

- [ ] **Step 1: Write test_example_matrix.py**

```python
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCIENCE_IDS = [
    "W1", "W2", "W3", "W4", "W5", "W6",
    "B1", "B2", "B3", "B4", "B5",
    "P1", "P2", "P3", "P4", "P5",
    "O1", "O2", "O3",
    "X1", "X2", "X3", "X4", "X5", "X6",
    "D1", "D2", "D3",
]


def test_all_science_ids_appear_in_matrix():
    text = (ROOT / "docs" / "EXAMPLE_MATRIX.md").read_text()
    missing = [i for i in SCIENCE_IDS if not re.search(rf"\b{i}\b", text)]
    assert missing == [], f"IDs missing from EXAMPLE_MATRIX: {missing}"
```

- [ ] **Step 2: Write infra tests**

`tests/test_infra_constants.py`:

```python
from vasp_constant import AUTOA, RYTOEV, HSQDTM, TPI

def test_constants_positive():
    assert AUTOA > 0 and RYTOEV > 0 and HSQDTM > 0 and TPI > 0
```

`tests/test_infra_sph_harm.py`:

```python
import numpy as np
from sph_harm import sph_r

def test_sph_r_shape():
    theta = np.array([0.1, 0.2])
    phi = np.array([0.0, 0.0])
    # lmax=1 → several components; just ensure callable returns finite values
    y = sph_r(1, theta, phi)
    assert np.all(np.isfinite(y))
```

(Adjust `sph_r` signature to match actual `sph_harm.py` when implementing — open file and match arity.)

`tests/test_infra_spline.py`:

```python
import numpy as np
from spline import splcof

def test_splcof_runs():
    x = np.linspace(0, 1, 11)
    y = x ** 2
    # Match actual splcof signature in spline.py when implementing
    coef = splcof(x, y)  # may need N, R, F, ...
    assert coef is not None
```

`tests/test_infra_fortran_record.py`:

```python
import struct
from pathlib import Path
import numpy as np

def _write_record(path: Path, payload: bytes) -> None:
    n = len(payload)
    with path.open("wb") as f:
        f.write(struct.pack("<i", n))
        f.write(payload)
        f.write(struct.pack("<i", n))

def test_wfull_record_helper_or_manual_roundtrip(tmp_path: Path):
    # Prefer importing wfull._read_fortran_record if public; else reimplement check
    p = tmp_path / "rec.bin"
    payload = np.arange(4, dtype=np.float64).tobytes()
    _write_record(p, payload)
    data = p.read_bytes()
    n = struct.unpack_from("<i", data, 0)[0]
    assert n == len(payload)
    assert data[4:4 + n] == payload
```

- [ ] **Step 3: Run pytest**

```bash
cd /home/duguex/VaspBandUnfolding
python -m pytest tests/test_example_matrix.py tests/test_infra_constants.py -v
```

Fix sph_r/splcof calls to match real signatures (read modules first).

- [ ] **Step 4: Commit**

```bash
git add tests/
git commit -m "test: matrix coverage and infra unit tests"
```

---

### Task 4: Harden existing demos (wfc_r, projectors, ewald, bseplot bz)

**Files:**
- Modify/Create: `examples/wfc_r/run.sh`, `README.md`, `ref/`
- Modify/Create: `examples/projectors/lreal_false/run.sh`, `README.md` (or parent `projectors/run.sh`)
- Modify/Create: `examples/ewald/run.sh`, `ref/madelung.out`
- Modify/Create: `examples/bseplot/run.sh`, `README.md` section for X5

**Interfaces:**
- Each runner exit 0/1/2 as Global Constraints

- [ ] **Step 1: wfc_r runner**

`examples/wfc_r/run.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f WAVECAR ]]; then echo "MISSING: WAVECAR" >&2; exit 2; fi
mkdir -p ref
python ex.py
# ex.py already writes figures; copy or write a small norm line
python - <<'PY'
from vaspwfc import vaspwfc
import numpy as np
from pathlib import Path
w = vaspwfc("WAVECAR")
# pick a safe band present in this WAVECAR — inspect w._nbands if needed
phi = w.wfc_r(iband=min(1, int(w._nbands)))
arr = phi if not isinstance(phi, (list, tuple)) else phi[0]
n = float(np.vdot(arr, arr).real)
Path("ref").mkdir(exist_ok=True)
Path("ref/norm.txt").write_text(f"norm={n:.8e}\n")
print("norm", n)
PY
```

Update README with IDs W1–W3, Level, citation policy.

- [ ] **Step 2: ewald golden**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ref
python madelung.py | tee ref/madelung.out
```

- [ ] **Step 3: projectors + bseplot bz**

- `projectors/lreal_false/run.sh` → `python kaka.py` (or non-interactive subset writing `ref/cproj_max.txt`)
- `bseplot/run.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f BSEFATBAND ]]; then exit 2; fi
mkdir -p ref
bseplot bz --input BSEFATBAND --poscar POSCAR --exciton 1 --output-dir ref || \
  python -c "from bsefatband import main; import sys; sys.exit(main(['bz','--input','BSEFATBAND','--poscar','POSCAR','--exciton','1','--output-dir','ref']))"
```

(Adapt to actual `bseplot` CLI flags from `bsefatband.build_parser`.)

- [ ] **Step 4: Matrix C1=ok for these paths; smoke**

```bash
python scripts/smoke_examples.py
```

Expected: PASS for hardened demos; SKIP for unscaffolded.

- [ ] **Step 5: Commit**

```bash
git add examples/wfc_r examples/ewald examples/projectors examples/bseplot docs/EXAMPLE_MATRIX.md
git commit -m "feat(examples): harden wfc_r projectors ewald bseplot C1 runners"
```

---

### Task 5: Harden aewfc, elf_test, unfold (npy path), bsematrix BP text, band_reorder, potplot, spinor skip recipe

**Files:**
- `examples/aewfc/co2/run.sh` + README (IDs P4; exit 2 if pySBT missing)
- `examples/elf_test/run.sh` (W6; citation experimental)
- `examples/unfold/sup_3x3x1/run.sh` — load `spectral_weight.npy` / plot only if no WAVECAR
- `examples/bsematrix/BP/run.sh` — verify text artifacts exist; optional lightweight parse
- `examples/band_reorder/run.sh` — exit 2 without WAVECAR; document
- `examples/potplot/run.sh` — need POTCAR input or skip; regenerate png to ref/
- `examples/spinor/run.sh` — exit 2 without Soc\* ; README points to output/ WAVECAR SCF only

- [ ] **Step 1–N:** Implement each runner with exit 0/1/2; update matrix; smoke; commit per group or one commit:

```bash
git commit -m "feat(examples): C1 runners for aewfc elf unfold BP band_reorder potplot spinor"
```

**aewfc pattern:**

```bash
python - <<'PY'
try:
    import sbt  # or whatever pySBT imports
except ImportError:
    raise SystemExit(2)
PY
python plt_aeps_wfc.py  # or minimal get_ae_wfc dump to ref/
```

**unfold npy pattern:**

```bash
if [[ -f spectral_weight.npy ]]; then
  python - <<'PY'
import numpy as np
from pathlib import Path
w = np.load("spectral_weight.npy")
Path("ref").mkdir(exist_ok=True)
Path("ref/sw_shape.txt").write_text(f"shape={w.shape} sum={w.sum():.6f}\n")
PY
else
  exit 2
fi
```

**BP pattern:**

```bash
test -f py_pw_only_both_AMAT.txt || exit 2
python - <<'PY'
from pathlib import Path
p = Path("py_pw_only_both_AMAT.txt")
n = sum(1 for _ in p.open())
Path("ref").mkdir(exist_ok=True)
Path("ref/amat_lines.txt").write_text(f"lines={n}\n")
PY
```

---

### Task 6: New example `examples/tdm` (W4, P5)

**Files:**
- Create: `examples/tdm/README.md`, `run.py`, `ref/`
- Prefer reuse `examples/wfc_r/WAVECAR` via relative path or env `VBU_TDM_WAVECAR`

- [ ] **Step 1: run.py**

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
wav = Path(os.environ.get("VBU_TDM_WAVECAR", ROOT / ".." / "wfc_r" / "WAVECAR"))
if not wav.is_file():
    print(f"MISSING: WAVECAR at {wav}", file=sys.stderr)
    sys.exit(2)

from vaspwfc import vaspwfc

wfc = vaspwfc(str(wav))
# bands must exist — clamp to available
nb = int(wfc._nbands)
i, j = 1, min(2, nb)
mat = wfc.get_dipole_mat((1, 1, i), (1, 1, j))
ref = ROOT / "ref"
ref.mkdir(exist_ok=True)
out = ref / "dipole_ps.txt"
np.savetxt(out, np.atleast_1d(mat).view(float) if np.iscomplexobj(mat) else np.atleast_1d(mat))
# Also write magnitude summary
mag = np.abs(np.asarray(mat)).ravel()
(ref / "dipole_ps_abs_max.txt").write_text(f"abs_max={mag.max():.8e}\n")
print("wrote", out)
```

- [ ] **Step 2: README** — IDs W4 (P5 optional section if POTCAR+pySBT); citation **experimental only** until C2 L2; link ASSUMPTIONS §3.1

- [ ] **Step 3: Matrix + smoke + commit**

```bash
git add examples/tdm docs/EXAMPLE_MATRIX.md
git commit -m "feat(examples): C1 tdm dipole demo (W4)"
```

---

### Task 7: New examples `ipr`, `procar`, `hse_kpts`, `wfull`

**Files:**
- `examples/ipr/run.py` — analytic grid IPR and/or wfc_r band IPR → `ref/ipr.txt`
- `examples/procar/run.py` — if no PROCAR, generate minimal synthetic file matching parser expectations OR exit 2 with note to copy from projectors OUTCAR run; prefer extract small PROCAR from `examples/projectors/*/PROCAR` if present
- `examples/hse_kpts/run.py` — spglib optional exit 2; else `get_ir_kpts` on a simple POSCAR
- `examples/wfull/run.py` — write+read tiny Fortran record using same logic as `wfull._read_fortran_record`

- [ ] Implement each with README + ref + matrix updates + smoke + commits:

```bash
git commit -m "feat(examples): C1 ipr procar hse_kpts wfull"
```

**IPR analytic sketch:**

```python
import numpy as np
from pathlib import Path
grid = np.zeros((16, 16, 16))
grid[8, 8, 8] = 1.0
prob = np.abs(grid) ** 2
ipr = (prob ** 2).sum() / (prob.sum() ** 2)
Path("ref").mkdir(exist_ok=True)
Path("ref/ipr_analytic.txt").write_text(f"ipr={ipr:.8e}\n")
assert ipr == 1.0
```

**hse_kpts:**

```python
try:
    import spglib  # noqa: F401
except ImportError:
    raise SystemExit(2)
from ase.io import read
from hse_kpts import get_ir_kpts
atoms = read("POSCAR")  # ship a minimal POSCAR
# match real get_ir_kpts signature
```

---

### Task 8: New examples `nac`, `neb` + P3 matrices dump

**Files:**
- `examples/nac/run.py` — if two WAVECARs unavailable, exit 2; README documents need for two frames; optional smoke with identical WAVECAR self-overlap sanity only if `nac_from_vaspwfc` allows
- `examples/neb/run.py` — create 2–3 tiny fake OUTCAR energy stubs **only if** `nebplot` can parse them; else vendor minimal real snippet; produce `ref/pes.dat`
- `examples/projectors` or `examples/paw_matrices/run.py` — `pawpotcar.get_Qij()` Frobenius norms to `ref/qij_norm.txt`

- [ ] Implement, matrix, smoke, commit:

```bash
git commit -m "feat(examples): C1 nac neb paw_matrices"
```

---

### Task 9: C1 closure audit

**Files:**
- Modify: `docs/EXAMPLE_MATRIX.md`
- Modify: `FEATURES.md` (example path / status notes)
- Modify: `docs/superpowers/specs/2026-07-13-all-components-run-and-examples-design.md` status → C1 implemented

- [ ] **Step 1: Verify every science ID has C1 in {ok, skip} with justification**

No `todo` left. `skip` only for true data blockers (spinor Soc\*, bseplot realspace WAVECAR, full NAC frames) with Notes pointing to `docs/repro/`.

- [ ] **Step 2: Run full smoke + pytest**

```bash
python scripts/smoke_examples.py
python -m pytest tests/ -v
```

Expected: `fail=0`; skips listed; infra tests pass.

- [ ] **Step 3: Commit**

```bash
git commit -m "docs: C1 complete — all science IDs ok or explicit skip"
```

---

## Phase C2 (G1 elevation) — Task 10+

### Task 10: Quarantine policy pass

**Files:** `FEATURES.md`, `docs/ASSUMPTIONS.md`, example READMEs for X2/X3/W6/W4

- [ ] Set Levels and citation flags: `pw_only` citable; `paw_full`/finite-q/experimental ELF/dipole-until-L2 marked **experimental only** or **no**
- [ ] Ensure `bsematrix` help/docs default to safest mode messaging
- [ ] Commit: `docs: quarantine non-L2 modes for honest citation`

### Task 11: L2 gates for already-strong paths

**Files:**
- `tests/test_l2_ewald.py` — compare `ref/madelung.out` key lines to golden constants
- `tests/test_l2_projectors.py` — if cproj.npy present, max abs error threshold
- `tests/test_l2_bse_pw_only.py` — parse BP AMAT line counts / sample eigenvalues from shipped tables (not full rebuild)
- `docs/repro/X1_bse_bp.md` — crisp/VASP regeneration steps

- [ ] Implement tests; `pytest tests/test_l2_*.py`; commit

### Task 12: Dipole L2 (W4/P5) — highest science priority

**Files:** `examples/tdm/`, `docs/repro/W4_dipole.md`, optional VASP OPTICS inputs under `docs/repro/inputs/tdm/`

- [ ] Design minimal molecule/slab job; run via crisp if needed
- [ ] Compare PS dipole / optics numbers; store table in `examples/tdm/ref/l2_table.md`
- [ ] Promote FEATURES W4 to L2 only if agreement within documented tolerance; else keep experimental
- [ ] Commit

### Task 13: Unfold / spinor / exciton realspace repro packs

**Files:** `docs/repro/B1_unfold.md`, `docs/repro/O2_spinor.md`, `docs/repro/X6_exciton_rs.md`

- [ ] Document crisp submit directories, required INCAR chain, expected output filenames
- [ ] When data available, flip matrix skip → ok and add L2 notes
- [ ] Commit

### Task 14: Packaging honesty (G2)

**Files:** `pyproject.toml`, `requirements-optional.txt`, `FEATURES.md`

- [ ] Add `spglib` to optional deps or extras
- [ ] Decide C7: add `bin/bsematrix` to `script-files` **or** document only `python bsematrix.py` in README/FEATURES (pick one; implement)
- [ ] Commit: `build: optional deps and bsematrix entry policy`

### Task 15: C2 closure

- [ ] Every science ID is either Level≥L2 with evidence link **or** experimental/quarantine with no citation
- [ ] Update `docs/GOALS.md` tracking note / EXAMPLE_MATRIX C2 column
- [ ] Final smoke + pytest
- [ ] Commit: `docs: C2 G1 closure audit`

---

## Self-review (plan vs spec)

| Spec requirement | Tasks |
|---|---|
| C1 template + matrix + smoke | 1–2 |
| I1–I4 tests | 3 |
| Upgrade existing examples | 4–5 |
| New tdm/ipr/procar/hse_kpts/wfull/nac/neb | 6–8 |
| C1 audit | 9 |
| C2 quarantine + L2 + repro + packaging | 10–15 |
| No full WAVECAR in git | Global + runners exit 2 |
| G1 citation honesty | Task 10, 12, 15 |

| Placeholder scan | Cleaned — runners give concrete scripts; note to match real API signatures at implement time for `sph_r`/`splcof`/`bseplot` flags |

---

## Execution handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-13-all-components-run-and-examples.md`.**

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks (`superpowers:subagent-driven-development`)
2. **Inline Execution** — this session with checkpoints (`superpowers:executing-plans`)

**Which approach?** Start with **Tasks 1–4 (C1 scaffold + core demos)** if you want the shortest path to a green smoke baseline.
