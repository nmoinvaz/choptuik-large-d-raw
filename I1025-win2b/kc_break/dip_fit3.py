#!/usr/bin/env python3
"""#1025 win2b, the k_c break scans at D 18.375: every ln|det| local minimum WITHOUT a sign change of a scan (an interior point below both neighbours' ln|det|, the hybrid sign the same on both sides), fitted with the
dip model of kc55/fine_dip_fit.py and kc55/dip_fit2.py: ln|det| = a + ln((l - l0)^2 + e^2) + b (l - l0) + c (l - l0)^2 (a pair of complex roots l0 +- i e times a smooth factor), over the points within HALF steps of the
minimum, with the 1-sigma uncertainties of l0 and e from the Jacobian, and quartic and quadratic polynomials over the same points. The fit is information, not a reading. Version 3 adds the two limits found at D 18.25
(the centre l0 outside the fit window; a quartic polynomial fitting the same points better): each is a flag, and a fit is flagged NOT RESOLVED when |e| is below half a step, its uncertainty exceeds |e|, l0 is outside the window,
or the quartic polynomial leaves a smaller maximum residual than the model.
usage: dip_fit3.py SCAN.jsonl [--half 5]  |  dip_fit3.py selftest"""
import json, sys
import numpy as np
from scipy.optimize import least_squares


def model(p, x):
    a, l0, e, b, c = p
    return a + np.log((x - l0) ** 2 + e ** 2) + b * (x - l0) + c * (x - l0) ** 2


def fit(x, y):
    best = None
    for e0 in (0.2, 0.5, 1.0, 2.0):
        for l00 in np.linspace(x.min(), x.max(), 7)[1:-1]:
            h = x[1] - x[0]
            r = least_squares(lambda p: model(p, x) - y, [y.mean(), l00, e0 * h, 0.0, 0.0])
            if best is None or r.cost < best.cost:
                best = r
    r = best
    dof = max(len(x) - 5, 1)
    s2 = 2 * r.cost / dof
    try:
        cov = np.linalg.inv(r.jac.T @ r.jac) * s2
        sig = np.sqrt(np.abs(np.diag(cov)))
    except np.linalg.LinAlgError:
        sig = np.full(5, np.inf)
    return r, sig


def report(x, y, step):
    r, sig = fit(x, y)
    a, l0, e, b, c = r.x
    e = abs(e)
    mx = float(np.abs(r.fun).max()); rms = float(np.sqrt((r.fun ** 2).mean()))
    res = {d: float(np.abs(np.polyval(np.polyfit(x - x.mean(), y, d), x - x.mean()) - y).max()) for d in (2, 4) if len(x) > d + 1}
    outside = not (x.min() - 1e-12 <= l0 <= x.max() + 1e-12)
    quartic_better = 4 in res and res[4] < mx
    small_e = e < 0.5 * step
    big_sig = sig[2] > e
    return dict(l0=l0, e=e, sl0=sig[1], se=sig[2], mx=mx, rms=rms, res=res, outside=outside, quartic_better=quartic_better, small_e=small_e, big_sig=big_sig,
                unres=outside or quartic_better or small_e or big_sig)


def flags(R):
    out = []
    if R["small_e"]: out.append("|e| below half a step")
    if R["big_sig"]: out.append("the uncertainty of e exceeds |e|")
    if R["outside"]: out.append("l0 is OUTSIDE the fit window")
    if R["quartic_better"]: out.append("the quartic polynomial fits the same points better than the model")
    return out


def minima_without_change(P):
    return [i for i in range(1, len(P) - 1) if P[i]["ln"] < P[i - 1]["ln"] and P[i]["ln"] < P[i + 1]["ln"] and P[i]["sign"] == P[i - 1]["sign"] == P[i + 1]["sign"]]


if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    bad = 0
    x = np.array([1.70 + 0.02 * i for i in range(11)])
    rng = np.random.default_rng(3)

    def case(name, y, want, notwant=()):
        global bad
        R = report(x, y, 0.02); fl = flags(R)
        ok = all(any(w in f for f in fl) if w != "none" else not fl for w in want) and not any(any(nw in f for f in fl) for nw in notwant)
        bad += not ok
        print(f"selftest {name}: l0 {R['l0']:.4f} (+- {R['sl0']:.4f}), e {R['e']:.4f}, quartic {R['res'].get(4, float('nan')):.1e} vs model {R['mx']:.1e}; flags {fl} (want {list(want)}) -> {'ok' if ok else 'WRONG'}")
    case("a resolved pair inside the window (l0 1.80, e 0.06)", model([-1597.0, 1.80, 0.06, 4.9, -13.0], x) + 1e-4 * rng.standard_normal(x.size), ["none"])
    case("an unresolved pair (e 0.004 at step 0.02)", model([-1597.0, 1.80, 0.004, 4.9, -13.0], x) + 1e-4 * rng.standard_normal(x.size), ["below half a step"])
    case("a planted pair with the centre outside the window (l0 2.05)", model([-1597.0, 2.05, 0.06, 4.9, -13.0], x) + 1e-4 * rng.standard_normal(x.size), ["OUTSIDE"])
    q = np.polyval([3.0e3, -2.0e2, 5.0e1, 1.0, -1600.0], x - 1.80) + 1e-7 * rng.standard_normal(x.size)
    case("a smooth quartic polynomial (no dip model): the quartic fits better", q, ["quartic polynomial fits"])
    P = [dict(lam=1.7 + 0.02 * i, ln=-1600.0 + 40.0 * (1.7 + 0.02 * i - 1.8) ** 2, sign=-1) for i in range(11)]
    ok = minima_without_change(P) == [5]
    bad += not ok
    print(f"selftest minimum finder: a V at the middle point -> {minima_without_change(P)} (want [5]) -> {'ok' if ok else 'WRONG'}")
    P2 = [dict(p, sign=(-1 if i <= 5 else 1)) for i, p in enumerate(P)]
    ok = minima_without_change(P2) == []
    bad += not ok
    print(f"selftest minimum finder: the same V with the sign changing at the minimum is beside a change -> {minima_without_change(P2)} (want []) -> {'ok' if ok else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)")
    sys.exit(1 if bad else 0)
half = 5
args = sys.argv[1:]
if "--half" in args:
    i = args.index("--half"); half = int(args[i + 1]); del args[i:i + 2]
P = sorted((json.loads(l) for l in open(args[0]) if l.strip()), key=lambda r: r["lam"])
step = round(P[1]["lam"] - P[0]["lam"], 6)
ms = minima_without_change(P)
print(f"D {P[0]['D']} k_c {P[0]['kc']}: {len(P)} points, step {step:g}; ln|det| local minima WITHOUT a change: {[round(P[i]['lam'], 3) for i in ms] if ms else 'none'}")
for i in ms:
    lo, hi = max(0, i - half), min(len(P), i + half + 1)
    xs = np.array([P[j]["lam"] for j in range(lo, hi)]); ys = np.array([P[j]["ln"] for j in range(lo, hi)])
    drop = (P[i]["ln"] - P[i - 1]["ln"], P[i]["ln"] - P[i + 1]["ln"])
    print(f"minimum at {P[i]['lam']:.3f} (ln {P[i]['ln']:.6f}, below its neighbours by {-drop[0]:.4f} and {-drop[1]:.4f}); dip fit over {len(xs)} points {xs[0]:.3f} to {xs[-1]:.3f}:")
    R = report(xs, ys, step); fl = flags(R)
    pol = ", ".join(f"degree {d}: {v:.2e}" for d, v in R["res"].items())
    print(f"  l0 {R['l0']:.5f} (+- {R['sl0']:.5f}), e {R['e']:.5f} (+- {R['se']:.5f}), max |residual| {R['mx']:.2e}, rms {R['rms']:.2e}; polynomial max |residual| over the same points, {pol}; "
          f"{'NOT RESOLVED: ' + '; '.join(fl) if fl else 'resolved at this step, l0 inside the window, the model fits better than the quartic'} (a model fit, information, not a reading)")
