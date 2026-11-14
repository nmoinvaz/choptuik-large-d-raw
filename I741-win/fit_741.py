#!/usr/bin/env python3
"""#741: Delta against the node shift: the power-law fit on S1 to S4, its prediction for S5 (1e-2) written BEFORE S5 runs, and the check of S5 against it.
usage: python fit_741.py --selftest
       python fit_741.py --table      (every polished state present: Delta (40 digits) and Delta - the unshifted root; control (c) from S0; no fit)
       python fit_741.py --fit        (needs S1 to S4: OLS of log10|Delta_s - Delta_root| on log10 s, writes fit_741_out.txt with p, c, the residuals and the prediction for s = 1e-2)
       python fit_741.py --check5     (needs S5 and fit_741_out.txt; refuses if the fit file is NOT older than S5's polished state)
The unshifted root is X2c's Delta (I727-win/X2c, the octo-double root of cont3's plan, max|F| 2.7e-93). Delta of a state = the exact sum of the last entry of every part, arb at 600 bits.
Acceptance (c): S0 reproduces the root's Delta to 1e-40. (b): the fit's prediction for S5 is within 10 % of the measured shift.
--selftest: a planted power law (p = 1.7) is recovered and predicts s = 1e-2 exactly; a planted sign change is flagged; a planted law with a quadratic part misses the 10 % bar."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I739-win"))
import cmp_739 as c          # noqa: E402  (eight-part Delta, arb precision 600)

c.flint.ctx.prec = 600
ROOT = os.path.join(RAW, "I727-win", "X2c", "base_pin13_D99.8750.npz")
SHIFT = {"S1": 1e-4, "S2": 3e-4, "S3": 1e-3, "S4": 3e-3, "S5": 1e-2}
BASE = lambda name: os.path.join(HERE, name, "base_pin13_D99.8750.npz")
OUT = os.path.join(HERE, "fit_741_out.txt")


def fit(points):
    """points: [(s, dDelta)], same sign. Returns (p, log10 c, residuals in log10, rms, max) of the OLS of log10|dDelta| on log10 s, or None when the signs differ"""
    sg = {np.sign(d) for _, d in points}
    if len(sg) != 1 or 0 in sg:
        return None
    x = np.log10([s for s, _ in points])
    y = np.log10([abs(d) for _, d in points])
    p, b = np.polyfit(x, y, 1)
    res = y - (p * x + b)
    return p, b, res, float(np.sqrt(np.mean(res ** 2))), float(np.max(np.abs(res))), sg.pop()


def predict(p, b, sign, s):
    return sign * 10 ** (p * np.log10(s) + b)


def selftest():
    bad = 0
    pts = [(s, 2.5e-20 * s ** 1.7) for s in (1e-4, 3e-4, 1e-3, 3e-3)]
    f = fit(pts)
    ok = f is not None and abs(f[0] - 1.7) < 1e-9 and abs(predict(f[0], f[1], f[5], 1e-2) / (2.5e-20 * 1e-2 ** 1.7) - 1) < 1e-9
    print(f"  planted power law p = 1.7: recovered {f[0]:.9f}, predicts s = 1e-2 to {abs(predict(f[0], f[1], f[5], 1e-2) / (2.5e-20 * 1e-2 ** 1.7) - 1):.1e} {'ok' if ok else 'WRONG'}")
    bad += not ok
    ok = fit([(1e-4, 1e-26), (3e-4, -3e-26), (1e-3, 1e-25), (3e-3, 3e-25)]) is None
    print(f"  planted sign change: flagged as not a power law {'ok' if ok else 'WRONG'}")
    bad += not ok
    a1, a2 = 1e-22, 1e-22 / 3e-3                    # the linear and the quadratic term are equal at s = 3e-3, so the law is no power law over the fitted range
    q = [(s, a1 * s + a2 * s * s) for s in (1e-4, 3e-4, 1e-3, 3e-3)]
    fq = fit(q)
    act = a1 * 1e-2 + a2 * 1e-4
    miss = abs(predict(fq[0], fq[1], fq[5], 1e-2) / act - 1)
    ok = miss > 0.10
    print(f"  planted law with a quadratic part: the fit misses s = 1e-2 by {miss:.2f} (more than 10 %) {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def states():
    root = c.delta(ROOT)
    out = {}
    for name in ("S0", "S1", "S2", "S3", "S4", "S5"):
        if os.path.exists(BASE(name)):
            out[name] = c.delta(BASE(name))
    return root, out


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    root, d = states()
    print(f"unshifted root (X2c): {root.str(40, radius=False)}")
    for name, v in d.items():
        sh = SHIFT.get(name, 0.0)
        dd = float((v - root).mid())
        print(f"{name} (node shift {sh:g}): Delta {v.str(40, radius=False)}   Delta - root {dd:+.6e}")
    if "S0" in d:
        dd0 = abs(float((d["S0"] - root).mid()))
        print(f"control (c): S0 - root = {dd0:.4e}, bar 1e-40: {'met' if dd0 <= 1e-40 else 'NOT MET'}")
    if "--fit" in sys.argv:
        pts = [(SHIFT[n], float((d[n] - root).mid())) for n in ("S1", "S2", "S3", "S4") if n in d]
        if len(pts) < 4:
            sys.exit("the fit needs S1 to S4")
        f = fit(pts)
        if f is None:
            print("the signs of the four shifts differ: NOT a power law")
            open(OUT, "w").write("signs differ: not a power law; no prediction\n")
            sys.exit(1)
        p, b, res, rms, mx, sg = f
        pred = predict(p, b, sg, 1e-2)
        lines = [f"fit of log10|Delta - root| on log10 s over S1 to S4 (OLS, 4 points): exponent p = {p:.4f}, coefficient c = {10 ** b:.4e} (sign {int(sg):+d})",
                 "residuals in log10 per point: " + ", ".join(f"{r:+.4f}" for r in res) + f"; rms {rms:.4f}, max {mx:.4f}",
                 f"prediction for the shift 1e-2 (written before S5 runs): Delta - root = {pred:+.6e}"]
        for ln in lines:
            print(ln)
        open(OUT, "w").write("\n".join(lines) + "\n")
    if "--check5" in sys.argv:
        if "S5" not in d or not os.path.exists(OUT):
            sys.exit("--check5 needs S5 and fit_741_out.txt")
        if os.path.getmtime(OUT) >= os.path.getmtime(BASE("S5")):
            sys.exit("REFUSED: fit_741_out.txt is not older than S5's state, so it is not a prediction")
        pred = float([ln for ln in open(OUT) if ln.startswith("prediction")][0].split("=")[-1])
        act = float((d["S5"] - root).mid())
        rel = (pred - act) / act
        print(f"S5: measured {act:+.6e}, predicted {pred:+.6e}, (pred - measured) / measured = {rel:+.4f}; within 10 %: {'yes' if abs(rel) <= 0.10 else 'NO'}")


if __name__ == "__main__":
    main()
