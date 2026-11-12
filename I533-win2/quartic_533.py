#!/usr/bin/env python3
"""#533 follow-up (not an acceptance): the same p2 chirp with a quartic trend, fits to all 51 states and both hold-outs, to see whether the sigma_3 and sigma_4 hold-outs (and sigma_1's H2) that miss 0.014 with the cubic trend are a trend problem.
usage: python quartic_533.py        (run from I533-win2; needs period_p2_533.py)"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import period_p2_533 as m  # noqa: E402

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    D, Y = m.collect51()
    F = m.Fitter(D, 4)
    print("trend of degree 4, all 51 states\n| series | free: P0, p1, p2 | rms | period at D 213 / 228 / 237 |\n|---|---|---|---|")
    for i in (1, 2, 3, 4):
        best, f0 = F.fit_free(Y[:, i - 1])
        th = best["theta"]
        P = lambda x: th[0] + th[1] * (x - m.D0) + th[2] * (x - m.D0) ** 2
        print(f"| sigma_{i} | {th[0]:.3f}, {th[1]:+.4f}, {th[2]:+.5f} | {math.sqrt(best['ss'] / len(D)):.4f} | {P(213):.3f} / {P(228):.3f} / {P(237):.3f} |", flush=True)
    print("\nhold-outs, trend of degree 4\n| series | hold-out | p2 chirp rms (max) | p2 = 0 chirp rms (max) | p1 = p2 = 0 rms (max) | meets 0.014 |\n|---|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        for tag, (row, ntr, nte) in m.holdouts(D, Y[:, i - 1], 4, i).items():
            a, z, c = row["p2 chirp"], row["p2 = 0 chirp"], row["p1 = p2 = 0"]
            print(f"| sigma_{i} | {tag[:2]} | {a[0]:.4f} ({a[1]:.4f}) | {z[0]:.4f} ({z[1]:.4f}) | {c[0]:.4f} ({c[1]:.4f}) | {'yes' if a[0] <= m.LIMIT else 'no'} |", flush=True)
