#!/usr/bin/env python3
"""#1025 macm3b kc87_d195 (my analysis script, information only): this machine's k_c 87 D 19.5 regrid against dh610's (a Linux regrid of the same source state).
Usage: compare_regrid.py MINE_RECORD MINE_STATE REF_RECORD REF_STATE  (run with the venv python, -I)."""
import json, sys
import numpy as np
mr, ms, rr, rs = sys.argv[1:5]
a = json.loads(open(mr).readline()); b = json.loads(open(rr).readline())
print("record field: mine | dh610's | mine - dh610's")
for k in ("F", "F_start", "steps", "constraint", "Delta", "seconds"):
    x, y = a[k], b[k]
    print("  %-10s %.12g | %.12g | %+.3e" % (k, x, y, x - y))
A = np.load(ms, allow_pickle=False); B = np.load(rs, allow_pickle=False)
print("state arrays: mine shape %s dtype %s | dh610's shape %s dtype %s" % (A.shape, A.dtype, B.shape, B.dtype))
if A.shape == B.shape:
    d = np.abs(A - B); n = np.abs(B).max()
    print("  max |mine - dh610's| %.3e, max |dh610's| %.3e, ratio %.3e; max abs diff at index %s; bitwise equal %s" % (d.max(), n, d.max() / n, np.unravel_index(d.argmax(), d.shape), bool(np.array_equal(A, B))))
else:
    print("  shapes differ: no elementwise comparison")
