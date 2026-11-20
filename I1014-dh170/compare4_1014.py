#!/usr/bin/env python3
"""#1014: Delta_k per order k = 0..12 across the series of this folder and dh610's M 256 series, relative differences in pairs.

    compare4_1014.py [--mutate]

Series (Delta_k = delta_hi + delta_lo summed with math.fsum; the M 256 series is cut to 13 orders):
  m256     I997-win2 M 256 series (T82-win's M 256 state, 1557-step plan)
  m320t82  series_D3.0475_M320t82_N12.npz (T82-win's own M 320 state, 1619-step plan)
  m384     series_D3.0475_M384_N12.npz (T82-win's M 384 state, 1623-step plan)
  m320own  series_D3.0475_M320_N12.npz (my lifted M 320 state, 4388-step plan)
Pairs: M 320 own against M 320 T82 (the plan's and the state's share), M 384 against M 320 T82 and against M 320 own, M 320 T82 and own against
M 256, M 384 against M 256. The relative difference is (A - B)/|B|. Control, written first: every series against itself reads 0, and a
copy with order 5 scaled by 1 + 1e-4 reads 1.000e-04 at order 5 and 0 elsewhere. --mutate scales order 5 of m384 (m320t82 when there is no m384: stage 3 was stopped as unconverged and m384 is not used) by 1 + 1e-4 and the pair table
must change at order 5 only (by the expected amount), in every pair that has that series."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "m256": os.path.expanduser("~/scratch1014/raw/I997-win2/series_D30475/series_D3.0475_M256_N20.npz"),
    "m320t82": os.path.join(HERE, "series_D3.0475_M320t82_N12.npz"),
    "m384": os.path.join(HERE, "series_D3.0475_M384_N12.npz"),
    "m320own": os.path.join(HERE, "series_D3.0475_M320_N12.npz"),
}
PAIRS = [("m320own", "m320t82"), ("m320t82", "m256"), ("m320own", "m256"), ("m384", "m320t82"), ("m384", "m320own"), ("m384", "m256")]    # m384 is not used (unconverged)
N = 13


def deltas(p):
    z = np.load(p)
    return [math.fsum([float(h), float(l)]) for h, l in zip(z["delta_hi"], z["delta_lo"])][:N]


def rel(a, b):
    return [(x - y) / abs(y) for x, y in zip(a, b)]


def main():
    mutate = "--mutate" in sys.argv
    have = {k: deltas(p) for k, p in FILES.items() if os.path.exists(p)}
    print("series present:", ", ".join(have), "; missing:", ", ".join(k for k in FILES if k not in have) or "none")
    ok = True
    for k, d in have.items():
        pert = list(d)
        pert[5] *= 1 + 1e-4
        c0, c1 = rel(d, d), rel(pert, d)
        good = all(x == 0 for x in c0) and abs(c1[5] - 1e-4) < 1e-9 and all(c1[i] == 0 for i in range(N) if i != 5)
        ok &= good
        print(f"control {k}: itself 0 at every order, planted 1e-4 at order 5 reads {c1[5]:.3e} and 0 elsewhere: {'pass' if good else 'FAIL'}")
    if not ok:
        sys.exit(1)
    pairs = [(a, b) for a, b in PAIRS if a in have and b in have]
    base = {(a, b): rel(have[a], have[b]) for a, b in pairs}
    if mutate:
        mut_name = "m384" if "m384" in have else "m320t82"      # the series whose order 5 is scaled (m384 was never converged and is not used: stage 3 stopped)
        if mut_name not in have:
            print("--mutate needs m384 or m320t82"); sys.exit(1)
        dm = list(have[mut_name])
        dm[5] *= 1 + 1e-4
        good = True
        for a, b in pairs:
            if a != mut_name:
                continue
            mut = rel(dm, have[b])
            diff = [i for i in range(N) if mut[i] != base[(a, b)][i]]
            exp = 1e-4 * have[mut_name][5] / abs(have[b][5])
            g = diff == [5] and abs((mut[5] - base[(a, b)][5]) - exp) < 1e-12
            good &= g
            print(f"--mutate {mut_name} order 5 x (1+1e-4), pair {a} vs {b}: table changes at orders {diff} by {mut[5] - base[(a, b)][5]:+.3e}: {'pass' if g else 'FAIL'}")
        sys.exit(0 if good else 1)
    print("relative difference (A - B)/|B| per order k:")
    print(f"{'k':>2} " + " ".join(f"{a + ' v ' + b:>20}" for a, b in pairs))
    for i in range(N):
        print(f"{i:2d} " + " ".join(f"{base[p][i]:+20.3e}" for p in pairs))
    print("Delta_k ratio D_k/D_k-1:")
    print(f"{'k':>2} " + " ".join(f"{k:>12}" for k in have))
    for i in range(1, N):
        print(f"{i:2d} " + " ".join(f"{have[k][i] / have[k][i - 1]:+12.5g}" for k in have))
    for a, b in pairs:
        r = base[(a, b)]
        print(f"{a} v {b}: orders agreeing to 1e-3: {[i for i in range(N) if abs(r[i]) <= 1e-3]}; orders 3..6 all agree: {all(abs(r[i]) <= 1e-3 for i in range(3, 7))}")


if __name__ == "__main__":
    main()
