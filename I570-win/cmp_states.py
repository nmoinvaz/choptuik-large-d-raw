"""Exact comparison of two octo-double states: sum of the 8 parts per entry as Fractions.
usage: python cmp_states.py A.npz B.npz [out.txt]   (prints max |diff| over all entries, the Delta entry, count of nonzero diffs)
"""
import sys
from fractions import Fraction
import numpy as np
from decimal import Decimal, getcontext
getcontext().prec = 45


def dec(x):
    return Decimal(x.numerator) / Decimal(x.denominator)

KEYS = ['zh', 'zl', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']


def exact(path):
    d = np.load(path, allow_pickle=True)
    parts = [np.asarray(d[k], dtype=np.float64).ravel() for k in KEYS]
    n = len(parts[0])
    return [sum(Fraction(float(p[i])) for p in parts) for i in range(n)], d


def main():
    a, da = exact(sys.argv[1])
    b, db = exact(sys.argv[2])
    assert len(a) == len(b), (len(a), len(b))
    diffs = [abs(x - y) for x, y in zip(a, b)]
    mx = max(diffs)
    imax = diffs.index(mx)
    nz = sum(1 for x in diffs if x != 0)
    last = diffs[-1]
    scale = max(abs(x) for x in a)
    out = []
    out.append(f"A {sys.argv[1]}")
    out.append(f"B {sys.argv[2]}")
    out.append(f"entries {len(a)}, nonzero differences {nz}")
    out.append(f"max |A-B| = {float(mx):.3e} at entry {imax} (largest |A| entry {float(scale):.3e})")
    out.append(f"|A-B| at the last entry ({len(a)-1}, Delta) = {float(last):.3e}")
    out.append(f"Delta A = {dec(a[-1]):.30f}")
    out.append(f"Delta B = {dec(b[-1]):.30f}")
    out.append(f"within 1e-90: {mx <= Fraction(1, 10**90)}")
    print("\n".join(out))
    if len(sys.argv) > 3:
        open(sys.argv[3], 'w').write("\n".join(out) + "\n")


main()
