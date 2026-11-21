#!/usr/bin/env python3
"""series_agree1060.py (written after the report, not pre-registered): how far apart are the two runs' saved series (jet_pin3_D260.6706.npz, orders x 769 components, eight parts each)?
For each order k (row), the exact sum S of the eight parts per component (mpmath, 600 bits); the worst relative difference max_i |S2_i - S1_i| / max_i |S1_i| over components, per order, and over all orders.
    python series_agree1060.py A.npz B.npz"""
import sys
import numpy as np
import mpmath as mp
mp.mp.prec = 600
A = np.load(sys.argv[1], allow_pickle=False)
B = np.load(sys.argv[2], allow_pickle=False)
KEYS = [f"z{i}" for i in range(8)]
nk, nc = A["z0"].shape
worst = []
for k in range(nk):
    d = mp.mpf(0)
    mx = mp.mpf(0)
    for i in range(nc):
        sa = mp.fsum(mp.mpf(float(A[q][k, i])) for q in KEYS)
        sb = mp.fsum(mp.mpf(float(B[q][k, i])) for q in KEYS)
        d = max(d, abs(sb - sa))
        mx = max(mx, abs(sa))
    worst.append((k, d / mx if mx != 0 else mp.mpf(0), mx))
print(f"series {sys.argv[1]} against {sys.argv[2]}: {nk} orders x {nc} components")
for k, r, mx in worst:
    print(f"  order {k:2d}: max |dS| / max |S| = {mp.nstr(r, 4)} (max |S| {mp.nstr(mx, 4)})")
print("worst over orders: " + mp.nstr(max(r for _, r, _ in worst), 4))
