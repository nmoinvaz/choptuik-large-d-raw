#!/usr/bin/env python3
"""gate971.py LOG OUTDIR: the verdict of one base polish (#971). 'converged' when the log has an octo-double Newton line that ends
'converged' with max|F| <= 1e-60 and OUTDIR holds a saved base (base_pin3_D*.npz); else 'failed' with the reason. Exit 0 for converged."""
import glob
import re
import sys

log, outdir = sys.argv[1], sys.argv[2]
text = open(log, errors="replace").read()
lines = re.findall(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan|inf), (NOT converged|converged)", text)
base = glob.glob(f"{outdir}/base_pin3_D*.npz")
if not lines:
    print("failed: no octo-double Newton line"); sys.exit(1)
n, F, c = lines[-1]
ok = c == "converged" and float(F) <= 1e-60 and bool(base)
print(f"{'converged' if ok else 'failed'}: last octo-double Newton line {n} steps, max|F| {F}, {c}, base saved {bool(base)}")
sys.exit(0 if ok else 1)
