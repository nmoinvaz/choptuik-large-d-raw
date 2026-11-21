#!/usr/bin/env python3
"""seriesdiff1060.py LEG10_DIR NEW_DIR: information on where a rerun of leg 10's step 17 departs from leg 10's, by exact sums (Fractions, the parts of each entry summed exactly):
the series file jet_pin3_D260.6706.npz per order row (entries that differ, max |dS| against max |S|), the base row against the stored base state anm_pin3_D260.6706.npz, and the
prediction pred_pin3_D260.8483.npz (entries that differ, max |dS|, the last component's dS). Controls first: the series against itself differs in 0 entries; against itself with one part
of one entry moved by one ulp it differs in exactly 1 (the count must be 1, else exit 1)."""
import sys
from fractions import Fraction

import numpy as np

A_DIR, B_DIR = sys.argv[1], sys.argv[2]
JK = [f"z{i}" for i in range(8)]
SK = ["zh", "zl"] + [f"z{i}" for i in range(2, 8)]


def load(p):
    d = np.load(p, allow_pickle=False)
    return {k: np.asarray(d[k]) for k in d.files}


def sums(d, keys, idx):
    return sum((Fraction(float(d[k][idx])) for k in keys if k in d), Fraction(0))


def rows(A, B, keys, o):
    n = A[keys[0]].shape[-1]
    nd, mx, mxa = 0, Fraction(0), Fraction(0)
    for i in range(n):
        a, b = sums(A, keys, (o, i)), sums(B, keys, (o, i))
        nd += a != b
        mx = max(mx, abs(a - b))
        mxa = max(mxa, abs(a))
    return nd, mx, mxa


A = load(f"{A_DIR}/jet_pin3_D260.6706.npz")
B = load(f"{B_DIR}/jet_pin3_D260.6706.npz")
C = {k: v.copy() for k, v in A.items()}
C["z4"][3, 100] = np.nextafter(C["z4"][3, 100], np.inf)
n0, _, _ = rows(A, A, JK, 3)
n1, _, _ = rows(A, C, JK, 3)
print(f"controls: series against itself, row 3: {n0} entries differ (must be 0); with one part of one entry moved one ulp: {n1} differ (must be 1)")
if n0 != 0 or n1 != 1:
    print("CONTROL WRONG")
    sys.exit(1)
f = lambda q: f"{float(q):.3e}"
print("series (8 parts per entry, 769 entries per order row):")
for o in range(A["z0"].shape[0]):
    nd, mx, mxa = rows(A, B, JK, o)
    print(f"  order row {o:2d}: {nd}/769 entries differ, max |dS| {f(mx)}, max |S| {f(mxa)}")
base = load(f"{A_DIR}/anm_pin3_D260.6706.npz")
nd = sum(sums(A, JK, (0, i)) != sums(base, SK, i) for i in range(769))
print(f"leg 10's series row 0 against its stored base state: {nd} entries differ (must be 0 for the comparison to mean anything)")
nd = sum(sums(B, JK, (0, i)) != sums(base, SK, i) for i in range(769))
print(f"this run's series row 0 against the stored base state: {nd} entries differ")
P, Q = load(f"{A_DIR}/pred_pin3_D260.8483.npz"), load(f"{B_DIR}/pred_pin3_D260.8483.npz")
pk = [k for k in P if k != "meta" and k in Q]
ds = [abs(sums(P, pk, i) - sums(Q, pk, i)) for i in range(len(P[pk[0]]))]
print(f"prediction ({'+'.join(pk)}): {sum(d != 0 for d in ds)}/{len(ds)} entries differ, max |dS| {f(max(ds))}, last component (Delta) |dS| {f(ds[-1])}")
