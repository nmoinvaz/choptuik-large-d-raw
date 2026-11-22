#!/usr/bin/env python3
"""#1067: Delta_k per order k = 0..12 of the M 512 series against I1014-dh170's M 384 series (m384p), as (A - B)/|B|.

    compare4_1067.py [--mutate]

Derived from I1014-dh170's compare4_1014.py (blob aa941ad7, copy in ref/): FILES, PAIRS and the mutated series differ, the control code is
unchanged. Series (Delta_k = delta_hi + delta_lo summed with math.fsum, 13 orders):
  m512   this folder's series_D3.0475_M512_N12.npz (anm_lowd.py --N 12 on the 5610-step plan)
  m384p  ref/series_D3.0475_M384p_N12.npz (I1014-dh170's M 384 on the planner's converged plan, 4502 steps; blob fb93dbfc)
Control, written first: every series against itself reads 0, and a copy with order 5 scaled by 1 + 1e-4 reads 1.000e-04 at order 5 and 0
elsewhere. --mutate scales order 5 of m512 by 1 + 1e-4 and the pair table must change at order 5 only, by the expected amount."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "m512": os.path.join(HERE, "series_D3.0475_M512_N12.npz"),
    "m384p": os.path.join(HERE, "ref", "series_D3.0475_M384p_N12.npz"),
}
PAIRS = [("m512", "m384p")]
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
        mut_name = next(k for k in ("m512",) if k in have)      # the series whose order 5 is scaled
        if mut_name not in have:
            print("--mutate needs m512"); sys.exit(1)
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
