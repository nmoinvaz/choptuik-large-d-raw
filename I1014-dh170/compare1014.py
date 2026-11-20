#!/usr/bin/env python3
"""#1014: Delta_k at M 320 against M 256, per order k = 0..12, relative difference.

    compare1014.py [--mutate]

Delta_k = delta_hi[k] + delta_lo[k] (double-double sum, taken in math.fsum). The two files are the series npz of this folder
(M 320, N 12) and dh610's I997-win2/series_D30475 (M 256, N 20, first 13 orders). The relative difference is
(D320 - D256) / |D256|. The control: the M 256 series against itself must give 0 at every order, and against a copy with
order 5 scaled by 1 + 1e-4 it must give 1e-4 there and exactly 0 elsewhere (the comparison can fail). --mutate runs the
real comparison with order 5 of the M 320 series scaled by 1 + 1e-4 and must differ from the unmutated one at order 5 only."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
F320 = os.path.join(HERE, "series_D3.0475_M320_N12.npz")
F256 = os.path.expanduser("~/scratch1014/raw/I997-win2/series_D30475/series_D3.0475_M256_N20.npz")


def deltas(p):
    z = np.load(p)
    return [math.fsum([float(h), float(l)]) for h, l in zip(z["delta_hi"], z["delta_lo"])], z


def rel(a, b):
    return [(x - y) / abs(y) for x, y in zip(a, b)]


def main():
    mutate = "--mutate" in sys.argv
    d320, z320 = deltas(F320)
    d256, z256 = deltas(F256)
    n = len(d320)
    d256 = d256[:n]
    print(f"M {int(z320['M'])} (D0 {float(z320['D0'])}) against M {int(z256['M'])} (D0 {float(z256['D0'])}), orders 0..{n - 1}")
    # control, written before the run
    c0 = rel(d256, d256)
    pert = list(d256)
    pert[5] *= 1 + 1e-4
    c1 = rel(pert, d256)
    ok = all(x == 0 for x in c0) and abs(c1[5] - 1e-4) < 1e-9 and all(c1[k] == 0 for k in range(n) if k != 5)
    print(f"control: M 256 against itself all 0: {all(x == 0 for x in c0)}; order 5 scaled by 1+1e-4 reads {c1[5]:.3e}, other orders 0: "
          f"{all(c1[k] == 0 for k in range(n) if k != 5)}: {'pass' if ok else 'FAIL'}")
    if not ok:
        sys.exit(1)
    base = rel(d320, d256)
    if mutate:
        d320m = list(d320)
        d320m[5] *= 1 + 1e-4
        mut = rel(d320m, d256)
        diff = [k for k in range(n) if mut[k] != base[k]]
        good = diff == [5] and abs((mut[5] - base[5]) - 1e-4 * d320[5] / abs(d256[5])) < 1e-12
        print(f"--mutate: order 5 of M 320 scaled by 1+1e-4 changes the table at orders {diff} by {mut[5] - base[5]:+.3e}: {'pass' if good else 'FAIL'}")
        sys.exit(0 if good else 1)
    print(f"{'k':>2} {'Delta_k (M 320)':>24} {'Delta_k (M 256)':>24} {'rel diff':>11} {'D_k/D_k-1 (320)':>16} {'D_k/D_k-1 (256)':>16}")
    for k in range(n):
        r3 = "" if k == 0 else f"{d320[k] / d320[k - 1]:+.4g}"
        r2 = "" if k == 0 else f"{d256[k] / d256[k - 1]:+.4g}"
        print(f"{k:2d} {d320[k]:24.16e} {d256[k]:24.16e} {base[k]:+11.3e} {r3:>16} {r2:>16}")
    agree = [k for k in range(n) if abs(base[k]) <= 1e-3]
    print("orders agreeing to 1e-3 relative:", agree)
    print("orders 3..6 all agree to 1e-3:", all(abs(base[k]) <= 1e-3 for k in range(3, 7)))


if __name__ == "__main__":
    main()
