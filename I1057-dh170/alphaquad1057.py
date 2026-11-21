#!/usr/bin/env python3
"""#1057: a quadratic extrapolation of the Delta direction's angle alpha(D) (alpha1057.py's definition) through the states since the maximum, and what it says about item (e).

    alphaquad1057.py [--mutate]        fit on the states D 260.9271 to the latest (c3b_ks293 records of this folder), residuals, forecast table
    alphaquad1057.py --selftest [--mutate]   planted: alpha = 50 - 60 (D - 261)^2 sampled at the real states' D must be recovered to 1e-9 degrees by the quadratic and not by --mutate (a straight line)

alpha = 0 means the Delta mode is wholly in the lowest vector (share of v1 = w), 90 degrees wholly in the upper one. Item (e) needs a share of 0.9 in some vector: share of v1 >= 0.9 is alpha <= 17.6 degrees
(w 0.9922), share of v2 >= 0.9 is alpha >= 72.2 degrees. A registered extrapolation of the last six states, not a fit of a law."""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alpha1057 as al  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ["260.9271", "261.0721", "261.1415", "261.2061", "261.2697", "261.3914", "261.5124", "261.6229", "261.6746", "261.7748", "261.8239"]
DEG = 2


def fit(D, a, deg):
    D0 = D[-1]
    c = np.polyfit(D - D0, a, deg)
    return c, D0


def selftest(mutate):
    D = np.array([float(n) for n in NAMES])
    a = 50 - 60 * (D - 261.0) ** 2
    c, D0 = fit(D, a, 1 if mutate else 2)
    err = max(abs(np.polyval(c, D - D0) - a))
    ok = err < 1e-9
    print(f"selftest: planted alpha = 50 - 60 (D - 261)^2, fit degree {1 if mutate else 2}: max residual {err:.2e} degrees: {'pass' if ok else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main(mutate):
    rows = []
    for n in NAMES:
        p = os.path.join(HERE, f"c3b_ks293_D{n}.json")
        if os.path.exists(p):
            r = json.load(open(p)); v = r["vectors"]
            rows.append((r["D"], al.alpha_of(v[0]["delta"], v[1]["delta"]), v[0]["delta"] + v[1]["delta"]))
    D = np.array([r[0] for r in rows]); a = np.array([r[1] for r in rows]); w = rows[-1][2]
    c, D0 = fit(D, a, DEG)
    res = a - np.polyval(c, D - D0)
    print(f"quadratic fit of alpha(D) on {len(rows)} states D {D[0]:.4f} to {D[-1]:.4f}: alpha = {c[2]:.3f} + {c[1]:.2f} x + {c[0]:.2f} x^2, x = D - {D0:.4f}")
    print("residuals (degrees): " + ", ".join(f"{x:+.2f}" for x in res) + f"; max {abs(res).max():.2f}")
    xm = -c[1] / (2 * c[0])
    print(f"maximum of the parabola at D {D0 + xm:.3f}, alpha {np.polyval(c, xm):.2f}; the last step's rate {np.polyval(np.polyder(c), 0):.1f} deg/D at D {D0:.4f}")
    print(f"{'D':>8} {'alpha':>7} {'share v1':>9} {'share v2':>9}")
    for d in (261.45, 261.50, 261.60, 261.70, 261.80, 262.00):
        x = d - D0; al_ = float(np.polyval(c, x)); al_c = max(al_, 0.0)
        s1, s2 = al.shares_of(al_c, w)
        print(f"{d:8.2f} {al_:7.2f} {s1:9.3f} {s2:9.3f}" + ("  (alpha below 0: the parabola has left the physical range)" if al_ < 0 else ""))
    # share of v1 = 0.9: alpha = 17.6
    a90 = math.degrees(math.asin(math.sqrt(1 - 0.9 / w)))
    roots = np.roots([c[0], c[1], c[2] - a90]); real = [float(r.real) for r in roots if abs(r.imag) < 1e-12 and r.real > 0]
    print(f"share of v1 = 0.9 needs alpha <= {a90:.1f}: the parabola reaches it at D {D0 + min(real):.3f}" if real else "the parabola does not reach alpha = 17.6 degrees")


if __name__ == "__main__":
    m = "--mutate" in sys.argv
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest(m) else 1)
    main(m)
