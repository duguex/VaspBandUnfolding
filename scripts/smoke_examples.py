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
