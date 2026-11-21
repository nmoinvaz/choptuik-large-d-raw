#!/usr/bin/env python3
"""jetstats1064.py A.npz B.npz: per order, the largest and the median relative difference |a - b| / |b| per coefficient of two jets (exact sums of the eight parts, as jetdiff1064.py), and the counts of coefficients above
1e-40, 1e-30, 1e-20, 1e-16 and 1e-14. Information for the front test's control (comment on #1064)."""
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from jetdiff1064 import exact, load  # noqa: E402

A, B = load(sys.argv[1]), load(sys.argv[2])
a, b = exact(A), exact(B)
n, m = a.shape
rel = np.zeros((n, m))
for i in range(n):
    for j in range(m):
        d = abs(a[i, j] - b[i, j])
        rel[i, j] = 0.0 if d == 0 else (float(d / abs(b[i, j])) if b[i, j] != 0 else float("inf"))
print("order  max            median         identical")
for i in range(n):
    print(f"{i:5d}  {rel[i].max():.3e}  {np.median(rel[i]):.3e}  {int((rel[i] == 0).sum())}")
for t in (1e-40, 1e-30, 1e-20, 1e-16, 1e-14):
    print(f"above {t:g}: {int((rel > t).sum())} of {rel.size}")
