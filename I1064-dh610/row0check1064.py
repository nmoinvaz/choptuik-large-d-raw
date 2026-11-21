#!/usr/bin/env python3
"""row0check1064.py JET.npz STATE.npz | --selftest [--break]: the order-0 row of a jet (z0..z7, row 0) against a stored state's eight parts (zh, zl, z2..z7) as float64 bits: the number of differing entries per part and the largest relative
difference of the exact sums. Exit 0 identical, 1 different. --selftest plants an identical row, a row with one part-5 entry changed by one ulp (must be found: 1 differing entry in part 5, relative about 1e-100 or smaller) and a row
with a part-2 entry changed by 1e-40 relative (must be found); --break flips the one-ulp expectation and must exit 1."""
import sys
from fractions import Fraction

import numpy as np


def row0(rows):  # rows: (8, orders, unknowns)
    return rows[:, 0, :]


def compare(a, st):
    bits = [int((a[q].view(np.uint64) != st[q].view(np.uint64)).sum()) for q in range(8)]
    w = 0.0
    for i in range(a.shape[1]):
        x = sum((Fraction(float(a[q][i])) for q in range(8)), Fraction(0))
        y = sum((Fraction(float(st[q][i])) for q in range(8)), Fraction(0))
        if x != y:
            w = max(w, float(abs(x - y) / abs(y)) if y != 0 else float("inf"))
    return bits, w


def selftest(brk):
    rng = np.random.default_rng(5)
    st = np.stack([rng.standard_normal(6) * 10.0 ** (-17 * q) for q in range(8)])
    jet = np.zeros((8, 3, 6))
    jet[:, 0, :] = st
    a = row0(jet).copy()
    b = a.copy(); b[5, 2] = np.nextafter(b[5, 2], 1.0)
    c = a.copy(); c[2, 4] += 1e-40 * abs(a[0, 4])
    cases = [("identical row", compare(a, st), lambda r: r[0] == [0] * 8 and r[1] == 0.0),
             ("one part-5 entry changed by one ulp", compare(b, st), lambda r: r[0][5] == 1 and sum(r[0]) == 1 and r[1] > 0),
             ("a part-2 entry changed by 1e-40 relative", compare(c, st), lambda r: r[0][2] == 1 and 0.5e-40 < r[1] < 2e-40)]
    if brk:
        cases[1] = (cases[1][0], cases[1][1], lambda r: sum(r[0]) == 0)
    bad = 0
    for name, r, chk in cases:
        ok = chk(r)
        print(f"  {name}: {r}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    z = np.load(sys.argv[1], allow_pickle=True)
    jet = np.stack([z[f"z{q}"] for q in range(8)])
    s = np.load(sys.argv[2], allow_pickle=True)
    st = np.stack([s[k] for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")])
    bits, w = compare(row0(jet), st)
    print(f"order-0 row against the stored state: differing entries per part {bits}, largest relative difference {w:.4e}")
    sys.exit(0 if sum(bits) == 0 else 1)
