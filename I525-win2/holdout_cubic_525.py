#!/usr/bin/env python3
"""#525 part 1, follow-up: the hold-out of holdout_525.py with a cubic trend. trend_525.py found that a cubic trend (and no second oscillation) takes ln sigma_3 and ln sigma_4 to rms 0.006, so the
quadratic trend extrapolated over 4.5 units may be what failed the hold-out. The same 30 training states (D <= 232.7), the same 9 test states, the chirp with a trend of degree 2 or 3, and the p1 = 0 control.
usage: python holdout_cubic_525.py [--selftest]       (run from I525-win2; needs holdout_525.py, trend_525.py and what they need)
Not the acceptance of #525 (that is holdout_525.py, quadratic trend, as the issue wrote it). The same limit 0.014 is shown for reference.
--selftest: 100 seeds of a planted chirp (P0 2.2, p1 +0.006, amplitude 0.125) with the quadratic trend plus a cubic term -0.09 u^3 (like sigma_3), noise 0.006: the degree-3 chirp's median prediction error must be at most 0.014
and the degree-2 chirp's median must be above 0.014 (the test tells the missing cubic term), and the p1 = 0 control's median error with degree 3 must be at least twice the chirp's."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import holdout_525 as ho  # noqa: E402
import trend_525 as t  # noqa: E402
r, c, h = t.r, ho.c, ho.h
D0 = c.D0


def design(D, P0, p1, deg):
    u = (D - D0) / 10.0
    ph = ho.phase(D, P0, p1)
    return np.column_stack([u ** k for k in range(deg + 1)] + [np.cos(ph), np.sin(ph)])


def holdout(D, y, deg, cut=ho.CUT):
    tr, te = D <= cut, D > cut
    X, XtX, valid = t.grid_columns_deg(D[tr], deg)
    out = {}
    for tag, p1z in (("chirp", False), ("p1=0", True)):
        v = valid.copy()
        if p1z:
            v[:, :] = False
            v[:, ho.J0] = valid[:, ho.J0]
        ss, P0, p1, b = r.grid_fit(X, XtX, v, y[tr])
        e = y[te] - design(D[te], P0, p1, deg) @ b
        out[tag] = dict(P0=P0, p1=p1, rin=math.sqrt(ss / tr.sum()), rms=math.sqrt(np.mean(e ** 2)), mx=float(np.max(np.abs(e))))
    return out


def selftest(seeds=100):
    D = np.array(sorted(d for d in h.collect() if d <= 237.2))
    u = (D - D0) / 10.0
    res = {2: [], 3: [], "z3": []}
    for s in range(seeds):
        y = 0.3 - 11 * u + 1.5 * u ** 2 - 0.09 * u ** 3 + 0.125 * np.sin(ho.phase(D, 2.2, 0.006) + 0.7) + np.random.default_rng(2000 + s).normal(0, 0.006, len(D))
        res[2].append(holdout(D, y, 2)["chirp"]["rms"])
        o3 = holdout(D, y, 3)
        res[3].append(o3["chirp"]["rms"]); res["z3"].append(o3["p1=0"]["rms"])
    m = {k: float(np.median(v)) for k, v in res.items()}
    print(f"planted chirp + cubic term, noise 0.006, {seeds} seeds, median prediction rms: degree 2 {m[2]:.4f}, degree 3 {m[3]:.4f}, degree 3 with p1 = 0 {m['z3']:.4f}; degree 3 <= {ho.LIMIT} in {100 * np.mean(np.array(res[3]) <= ho.LIMIT):.0f}% of seeds")
    ok = m[3] <= ho.LIMIT and m[2] > ho.LIMIT and m["z3"] >= 2 * m[3]
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    pts = h.collect()
    Ds = sorted(d for d in pts if d <= 237.2)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    print(f"{len(D)} states; training D <= {ho.CUT} ({int((D <= ho.CUT).sum())}), test {int((D > ho.CUT).sum())} states D {D[D > ho.CUT][0]:.2f} to {D[-1]:.2f}; limit for reference {ho.LIMIT}")
    print("| series | trend | chirp P0, p1 (training) | chirp in-sample rms | chirp prediction rms (max) | p1 = 0 prediction rms (max) |\n|---|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        for deg in (2, 3):
            o = holdout(D, Y[:, i - 1], deg)
            ch, z = o["chirp"], o["p1=0"]
            print(f"| ln sigma_{i} | degree {deg} | {ch['P0']:.2f}, {ch['p1']:+.3f} | {ch['rin']:.4f} | {ch['rms']:.4f} ({ch['mx']:.4f}) | {z['rms']:.4f} ({z['mx']:.4f}) |")
