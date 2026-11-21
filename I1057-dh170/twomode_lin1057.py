#!/usr/bin/env python3
"""#1057: the two-mode (avoided-crossing) fit with D-linear slopes, and its planted test. Law and pass criteria: README, 'The two-mode fit with D-linear slopes' (written before this code).

    twomode_lin1057.py --selftest [--mutate | --mutate=curve]   the planted test (exit 0 on pass; each mutation must exit 1)
    twomode_lin1057.py A|B|C                                   the fit on window A (D 259.7352 to 260.8483), B (D 260.0073 to 260.8483) or C (D 259.4568 to 260.8483)
                                                                of c3b_ks293 state records, vectors 1 and 2 (sorted by sigma) taken as they are, no classification

Law (x = D - D_last): a_i = exp(p_i - s_i x - c_i x^2 / 2) for the Delta branch and the second branch (the log slope of each is linear in D), coupling
g = gamma sqrt(a_Delta a_2), 0 <= gamma <= 0.9; the observed pair is the eigenvalues of [[a_Delta, g], [g, a_2]] (sigma_lowest the minus root, sigma_upper the plus root).
The Delta branch is the one that is lower at the first state of the window. Least squares on ln sigma_lowest and ln sigma_upper; the shares are not fitted."""
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq, least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
GMAX = 0.9
COUPLING = True          # --mutate: the model under test has no coupling
CURVE = True             # --mutate=curve: the model under test has no curvature terms
WINDOWS = {"A": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483],
           "B": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483],
           "C": [259.4568, 259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483],
           "A7": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271],
           "B6": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271],
           "A8": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721],
           "B7": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721],
           "A9": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415],
           "B8": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415],
           "A10": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415, 261.2061],
           "B9": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415, 261.2061],
           "A11": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415, 261.2061, 261.2697],
           "B10": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415, 261.2061, 261.2697],
           "A12": [259.7352, 260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415, 261.2061, 261.2697, 261.3914],
           "B11": [260.0073, 260.2515, 260.4708, 260.6706, 260.8483, 260.9271, 261.0721, 261.1415, 261.2061, 261.2697, 261.3914]}
RATIO_MEASURED = 1.160


def ln_a(th, x, curve):
    pD, sD, cD, p2, s2, c2, gam = th
    cD, c2 = (cD, c2) if curve else (0.0, 0.0)
    return pD - sD * x - cD * x * x / 2, p2 - s2 * x - c2 * x * x / 2


def pair(th, x, coupling=None, curve=None):
    """sigma_lowest, sigma_upper; the planted truth always has its coupling and curvature, whatever the model under test (the mutations) does"""
    x = np.asarray(x, float)
    coupling = COUPLING if coupling is None else coupling
    curve = CURVE if curve is None else curve
    lD, l2 = ln_a(th, x, curve)
    aD, a2 = np.exp(lD), np.exp(l2)
    g = (th[6] if coupling else 0.0) * np.sqrt(aD * a2)
    h = np.sqrt(((aD - a2) / 2) ** 2 + g ** 2)
    return (aD + a2) / 2 - h, (aD + a2) / 2 + h


def share(th, x, coupling=None, curve=None):
    """the lowest vector's weight on the Delta branch"""
    x = np.asarray(x, float)
    coupling = COUPLING if coupling is None else coupling
    curve = CURVE if curve is None else curve
    lD, l2 = ln_a(th, x, curve)
    aD, a2 = np.exp(lD), np.exp(l2)
    g = (th[6] if coupling else 0.0) * np.sqrt(aD * a2)
    return (1 + (a2 - aD) / np.sqrt((aD - a2) ** 2 + 4 * g ** 2)) / 2


def relabel(th, x0):
    """the Delta branch is the one that is lower at the first state: swap the labels when the fit has them the other way round"""
    lD, l2 = ln_a(th, x0, CURVE)
    if lD <= l2:
        return th
    t = list(th)
    t[0:3], t[3:6] = th[3:6], th[0:3]
    return np.array(t)


def crossing(th, lo, hi):
    f = lambda x: (lambda a: a[0] - a[1])(ln_a(th, x, CURVE))
    xs = np.linspace(lo, hi, 400)
    v = [f(x) for x in xs]
    for i in range(len(xs) - 1):
        if v[i] == 0 or v[i] * v[i + 1] < 0:
            return brentq(f, xs[i], xs[i + 1])
    return float("nan")


def fit(D, lo, up):
    """least squares on ln sigma_lowest and ln sigma_upper, a grid of starts; returns (theta, rms of the residuals)"""
    D, lo, up = np.asarray(D, float), np.asarray(lo, float), np.asarray(up, float)
    x = D - D[-1]
    y = np.concatenate([np.log(lo), np.log(up)])

    def res(th):
        a, b = pair(th, x)
        return np.concatenate([np.log(a) - y[:len(x)], np.log(b) - y[len(x):]])
    pl, pu = np.log(lo[-1]), np.log(up[-1])
    lb = [y.min() - 3, -3, -30, y.min() - 3, -3, -30, 0.0]
    ub = [y.max() + 3, 4, 30, y.max() + 3, 4, 30, GMAX]
    best = None
    for p1, p2 in ((pl, pu), (pu, pl), (pl, pl), (pu, pu)):
        for s1 in (0.3, 0.7):
            for s2 in (0.4, 0.9):
                for c1 in (-1.0, 1.0):
                    for c2 in (-1.0, 1.0):
                        for g in (0.03, 0.1):
                            th0 = np.clip([p1, s1, c1, p2, s2, c2, g], lb, ub)
                            try:
                                r = least_squares(res, th0, bounds=(lb, ub), x_scale=[1, 1, 1, 1, 1, 1, 0.1], max_nfev=400)
                            except Exception:
                                continue
                            if best is None or r.cost < best.cost:
                                best = r
    th = relabel(best.x, x[0])
    return th, float(np.sqrt(np.mean(best.fun ** 2)))


def load(names):
    D, lo, up, s1, s2 = [], [], [], [], []
    for n in names:
        rec = json.load(open(os.path.join(HERE, n + ".json")))
        v = rec["vectors"]
        assert v[0]["sigma"] <= v[1]["sigma"] <= v[2]["sigma"], n
        D.append(float(rec["D"])); lo.append(v[0]["sigma"]); up.append(v[1]["sigma"]); s1.append(v[0]["delta"]); s2.append(v[1]["delta"])
    return D, lo, up, s1, s2


def criteria(th, D, s1, s2):
    """the pass criteria of the README for a window"""
    x = np.asarray(D) - D[-1]
    w = share(th, x)
    d1 = np.abs(w - np.asarray(s1))
    d2 = np.abs((1 - w) - np.asarray(s2))
    gap = (1 + th[6]) / (1 - th[6])
    a, b = pair(th, [0.0])
    rat = float(b[0] / a[0])
    ok1 = bool(d1.max() <= 0.1 and d2.max() <= 0.1)
    ok2 = abs(gap - RATIO_MEASURED) / RATIO_MEASURED <= 0.2
    return dict(w=w, d1=d1, d2=d2, gap=gap, ratio_last=rat, ok1=ok1, ok2=ok2, ok=ok1 and ok2)


def planted(gam, xc, seed=0):
    """a six-state grid spaced 0.22 ending at x = 0 with curved slopes and the crossing at xc (D_c); returns D, lo, up, true shares, truth"""
    pD, sD, cD, s2, c2 = np.log(3e-20), 0.35, 0.25, 0.80, -0.30
    p2 = pD + (s2 - sD) * xc + (c2 - cD) * xc * xc / 2
    th = np.array([pD, sD, cD, p2, s2, c2, gam])
    x = -0.22 * np.arange(5, -1, -1)
    lo, up = pair(th, x, True, True)
    rng = np.random.default_rng(seed)
    lo = lo * (1 + 1e-6 * rng.standard_normal(len(x)))
    up = up * (1 + 1e-6 * rng.standard_normal(len(x)))
    return 260.0 + x, lo, up, share(th, x, True, True), th


def selftest():
    ok = True
    for gam, xc in ((0.06, -0.1), (0.12, -0.1), (0.06, 0.05), (0.12, 0.05)):
        D, lo, up, sh, tr = planted(gam, xc)
        th, rms = fit(D, lo, up)
        xs = np.asarray(D) - D[-1]
        w = share(th, xs)
        dc = crossing(th, xs[0] - 1, xs[-1] + 1)
        good = abs(dc - xc) <= 0.02 and abs(th[6] - gam) <= 0.2 * gam and np.abs(w - sh).max() <= 0.02
        ok &= bool(good)
        print(f"selftest (a): planted gamma {gam}, D_c {xc:+.2f}: fitted gamma {th[6]:.4f}, D_c {dc:+.3f}, largest share error {np.abs(w - sh).max():.3f}, rms {rms:.1e}: {'pass' if good else 'FAIL'}")
    D, lo, up, sh, tr = planted(0.0, -0.1)
    th, rms = fit(D, lo, up)
    good = th[6] < 0.01
    ok &= bool(good)
    print(f"selftest (b): planted gamma 0: fitted gamma {th[6]:.4f}: {'pass' if good else 'FAIL'}")
    global CURVE
    D, lo, up, sh, tr = planted(0.08, -0.1)
    xs = np.asarray(D) - D[-1]
    keep = CURVE
    CURVE = False                       # the constant-slope law on curved data
    th0, rms0 = fit(D, lo, up)
    miss0 = np.abs(share(th0, xs) - sh).max()
    CURVE = True
    th1, rms1 = fit(D, lo, up)
    miss1 = np.abs(share(th1, xs) - sh).max()
    CURVE = keep
    good = miss0 > 0.1 and miss1 <= 0.1
    ok &= bool(good)
    print(f"selftest (c): curved planted data: the constant-slope fit misses the shares by {miss0:.3f} (rms {rms0:.1e}), the D-linear fit by {miss1:.3f} (rms {rms1:.1e}): {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if not COUPLING else "") + (" --mutate=curve" if not CURVE else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    global COUPLING, CURVE
    if "--selftest" in sys.argv:
        COUPLING = "--mutate" not in sys.argv
        CURVE = "--mutate=curve" not in sys.argv
        sys.exit(0 if selftest() else 1)
    win = next(a for a in sys.argv[1:] if a in WINDOWS)
    names = [f"c3b_ks293_D{d:.4f}" for d in WINDOWS[win]]
    D, lo, up, s1, s2 = load(names)
    th, rms = fit(D, lo, up)
    x = np.asarray(D) - D[-1]
    a, b = pair(th, x)
    c = criteria(th, D, s1, s2)
    dc = crossing(th, x[0] - 1, x[-1] + 1)
    print(f"window {win}: {len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; parameters: Delta branch p {th[0]:+.4f} s {th[1]:+.4f} c {th[2]:+.4f}; second branch p {th[3]:+.4f} s {th[4]:+.4f} c {th[5]:+.4f}; gamma {th[6]:.4f} (gap {c['gap']:.3f}); D_c {dc + D[-1]:.3f}; rms of ln sigma {rms:.2e}")
    print(f"{'D':>9} {'dln lo':>9} {'dln up':>9} {'fit lo':>11} {'meas lo':>11} {'fit up':>11} {'meas up':>11} {'fit w':>7} {'meas v1':>8} {'fit 1-w':>8} {'meas v2':>8}")
    for i in range(len(D)):
        print(f"{D[i]:9.4f} {np.log(a[i] / lo[i]):+9.4f} {np.log(b[i] / up[i]):+9.4f} {a[i]:11.4e} {lo[i]:11.4e} {b[i]:11.4e} {up[i]:11.4e} {c['w'][i]:7.3f} {s1[i]:8.3f} {1 - c['w'][i]:8.3f} {s2[i]:8.3f}")
    print(f"criterion 1: largest |fitted - measured| share, vector 1 {c['d1'].max():.3f}, vector 2 {c['d2'].max():.3f} (bar 0.1): {'pass' if c['ok1'] else 'FAIL'}")
    print(f"criterion 2: gap at the crossing (1+gamma)/(1-gamma) = {c['gap']:.3f} against the measured 1.160 (bar 20%, [0.928, 1.392]), the model's ratio at the last state {c['ratio_last']:.3f}: {'pass' if c['ok2'] else 'FAIL'}")
    print(f"window {win}: {'PASS' if c['ok'] else 'FAIL'}")


if __name__ == "__main__":
    main()
