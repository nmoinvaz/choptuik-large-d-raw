#!/usr/bin/env python3
"""order0_rows.py STATE.npz DH370_JET.npz MY_JET.npz MY_BASE.npz: the order-0 row of the jets and the bases against the stored state file, as float64 bits per part and as the largest relative difference of the exact sums
(the one-off analysis of the #1064 front test, written out for the record). Prints the four comparisons of order0_rows.txt."""
import sys
from fractions import Fraction

import numpy as np


def state(p):
    z = np.load(p, allow_pickle=True)
    return np.stack([z[k] for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")])


def row0(p):
    z = np.load(p, allow_pickle=True)
    return np.stack([z[f"z{q}"][0] for q in range(8)])


def bits(a, b):
    return [int((a[q].view(np.uint64) != b[q].view(np.uint64)).sum()) for q in range(8)]


def maxrel(a, b):
    w, loc = 0.0, None
    for i in range(a.shape[1]):
        x = sum((Fraction(float(a[q][i])) for q in range(8)), Fraction(0))
        y = sum((Fraction(float(b[q][i])) for q in range(8)), Fraction(0))
        if x != y:
            r = float(abs(x - y) / abs(y)) if y != 0 else float("inf")
            if r > w:
                w, loc = r, i
    return w, loc


st, dj, mj, mb = state(sys.argv[1]), row0(sys.argv[2]), row0(sys.argv[3]), state(sys.argv[4])
for name, a in (("dh370's jet row 0 against the stored state", dj), ("my jet row 0 against the stored state", mj), ("my saved base against the stored state", mb)):
    print(f"{name}: differing entries per part {bits(a, st)}, largest relative difference {maxrel(a, st)}")
print(f"my jet row 0 against my saved base: differing entries per part {bits(mj, mb)}")
