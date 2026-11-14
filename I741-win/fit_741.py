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


def quad_fit(points):
    """the POST-HOC two-term model dDelta = a s + b s^2 (adopted after S1 and S2 had opposite signs, so not the pre-registered fit): weighted least squares with weights 1/|dDelta|
    (relative residuals). Returns (a, b, relative residuals (model - measured) / measured)"""
    s = np.array([p[0] for p in points])
    d = np.array([p[1] for p in points])
    w = 1.0 / np.abs(d)
    A = np.stack([s * w, s * s * w], axis=1)
    sol = np.linalg.lstsq(A, d * w, rcond=None)[0]
    return float(sol[0]), float(sol[1]), (sol[0] * s + sol[1] * s * s - d) / d


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
    a, b = -1.6748e-23, 6.4617e-20                                     # a planted two-term law with a sign change, recovered from four of its points
    pts2 = [(s, a * s + b * s * s) for s in (1e-4, 3e-4, 1e-3, 3e-3)]
    qa, qb, qres = quad_fit(pts2)
    ok = abs(qa / a - 1) < 1e-9 and abs(qb / b - 1) < 1e-9 and np.max(np.abs(qres)) < 1e-9 and fit(pts2) is None
    print(f"  planted two-term law with a sign change: recovered a, b to {abs(qa / a - 1):.1e}, {abs(qb / b - 1):.1e}; the power law is flagged {'ok' if ok else 'WRONG'}")
    bad += not ok
    pq = [(s, a * s + b * s * s + 0.3 * abs(a * s + b * s * s)) for s in (1e-4, 3e-4, 1e-3, 3e-3)]   # planted noise of 30 % must show in the relative residuals
    _, _, rq = quad_fit(pq)
    ok = np.max(np.abs(rq)) > 0.05
    print(f"  planted 30 % deviation shows in the relative residuals (max {np.max(np.abs(rq)):.2f}) {'ok' if ok else 'WRONG'}")
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
        lines = []
        if f is None:
            signs = ", ".join(f"{n} {'+' if v > 0 else '-'}" for n, (_, v) in zip(("S1", "S2", "S3", "S4"), pts))
            lines.append(f"PRE-REGISTERED power law (acceptance (b)): NOT MET, the signs of the four shifts differ ({signs}), so Delta - root is not a power law of the node shift.")
        else:
            p, b, res, rms, mx, sg = f
            lines += [f"PRE-REGISTERED power law: fit of log10|Delta - root| on log10 s over S1 to S4 (OLS, 4 points): exponent p = {p:.4f}, coefficient c = {10 ** b:.4e} (sign {int(sg):+d})",
                      "residuals in log10 per point: " + ", ".join(f"{r:+.4f}" for r in res) + f"; rms {rms:.4f}, max {mx:.4f}",
                      f"prediction for the shift 1e-2 (power law, written before S5 runs): Delta - root = {predict(p, b, sg, 1e-2):+.6e}"]
        qa, qb, qres = quad_fit(pts)
        s1, s2 = pts[0], pts[1]
        A = np.array([[s1[0], s1[0] ** 2], [s2[0], s2[0] ** 2]])
        a12, b12 = np.linalg.solve(A, np.array([s1[1], s2[1]]))
        lines += [f"POST-HOC two-term model (adopted after the sign change, not pre-registered): Delta - root = a s + b s^2 over S1 to S4 (weighted LS, relative residuals): a = {qa:.4e}, b = {qb:.4e}, sign change at s = {-qa / qb:.3e}",
                  "relative residuals (model - measured) / measured per point: " + ", ".join(f"{r:+.4f}" for r in qres) + f"; max {np.max(np.abs(qres)):.4f}",
                  f"out of sample: the model fitted to S1 and S2 alone (a = {a12:.4e}, b = {b12:.4e}, recorded in the README before S3 and S4 finished) predicted S3 {a12 * 1e-3 + b12 * 1e-6:+.4e} and S4 {a12 * 3e-3 + b12 * 9e-6:+.4e}; measured {pts[2][1]:+.4e} and {pts[3][1]:+.4e}",
                  f"post hoc prediction for the shift 1e-2 (two-term model, written before S5 runs): Delta - root = {qa * 1e-2 + qb * 1e-4:+.6e}"]
        for ln in lines:
            print(ln)
        open(OUT, "w").write("\n".join(lines) + "\n")
        if f is None:
            sys.exit(1)
    if "--check5" in sys.argv:
        if "S5" not in d or not os.path.exists(OUT):
            sys.exit("--check5 needs S5 and fit_741_out.txt")
        if os.path.getmtime(OUT) >= os.path.getmtime(BASE("S5")):
            sys.exit("REFUSED: fit_741_out.txt is not older than S5's state, so it is not a prediction")
        act = float((d["S5"] - root).mid())
        for ln in open(OUT):
            if ln.startswith("prediction") or ln.startswith("post hoc prediction"):
                kind = "pre-registered power law" if ln.startswith("prediction") else "POST-HOC two-term model"
                pred = float(ln.split("=")[-1])
                rel = (pred - act) / act
                print(f"S5 against the {kind}: measured {act:+.6e}, predicted {pred:+.6e}, (pred - measured) / measured = {rel:+.4f}; within 10 %: {'yes' if abs(rel) <= 0.10 else 'NO'}")


if __name__ == "__main__":
    main()
