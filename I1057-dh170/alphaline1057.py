#!/usr/bin/env python3
"""#1057: a straight-line fit of the Delta direction's angle alpha(D) through the last five states (the rotation rate has been constant, -44 to -47 deg/D, since D 261.52), and where a share of 0.9 in v1 falls.

    alphaline1057.py [N]            least-squares line on the last N (default 5) states of NAMES, residuals, forecast table, D of share v1 = 0.9 (alpha <= 17.8 degrees for w 0.9923)
    alphaline1057.py --selftest [--mutate]   planted: alpha = 40 - 46.6 (D - 261.5) sampled at the real states' D must be recovered to 1e-9 (slope and intercept); --mutate fits a constant and must fail

alpha as alpha1057.py defines it (0 = all Delta weight in the lowest vector). A registered extrapolation, not a law."""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alpha1057 as al  # noqa: E402
import alphaquad1057 as aq  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def selftest(mutate):
    D = np.array([float(n) for n in aq.NAMES[-5:]])
    a = 40 - 46.6 * (D - 261.5)
    c = np.polyfit(D - D[-1], a, 0 if mutate else 1)
    ok = (not mutate) and abs(c[0] + 46.6) < 1e-9 and abs(c[1] - (40 - 46.6 * (D[-1] - 261.5))) < 1e-9
    if mutate:
        ok = abs(np.polyval(c, D - D[-1]) - a).max() < 1e-9
    print(f"selftest: planted line, fit {'constant' if mutate else 'degree 1'}: {'pass' if ok else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main(n):
    rows = []
    for nm in aq.NAMES[-n:]:
        r = json.load(open(os.path.join(HERE, f"c3b_ks293_D{nm}.json"))); v = r["vectors"]
        rows.append((r["D"], al.alpha_of(v[0]["delta"], v[1]["delta"]), v[0]["delta"] + v[1]["delta"]))
    D = np.array([r[0] for r in rows]); a = np.array([r[1] for r in rows]); w = rows[-1][2]
    c = np.polyfit(D - D[-1], a, 1)
    res = a - np.polyval(c, D - D[-1])
    print(f"line fit of alpha(D) on the last {n} states D {D[0]:.4f} to {D[-1]:.4f}: alpha = {c[1]:.3f} {c[0]:+.2f} x, x = D - {D[-1]:.4f}")
    print("residuals (degrees): " + ", ".join(f"{x:+.2f}" for x in res) + f"; max {abs(res).max():.2f}")
    print(f"{'D':>8} {'alpha':>7} {'share v1':>9}")
    for d in (261.85, 261.90, 261.95, 262.00, 262.05):
        al_ = float(np.polyval(c, d - D[-1])); print(f"{d:8.2f} {al_:7.2f} {al.shares_of(max(al_, 0), w)[0]:9.3f}")
    a90 = math.degrees(math.asin(math.sqrt(1 - 0.9 / w)))
    print(f"share of v1 = 0.9 needs alpha <= {a90:.1f}: the line reaches it at D {D[-1] + (a90 - c[1]) / c[0]:.3f} (a 3 degree band moves that by {3 / abs(c[0]):.3f} in D)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    main(int(next((x for x in sys.argv[1:] if x.isdigit()), 5)))
