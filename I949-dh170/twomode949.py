#!/usr/bin/env python3
"""#949: a two-mode (avoided-crossing) fit of sigma_Delta and sigma_2 of ks_chain3b's latest states, with its planted test.

    twomode949.py --selftest [--mutate]   the planted two-branch test (README, 'The two-mode fit: law and pass criteria'): exit 0 on pass; --mutate drops the
                                          coupling term from the model and the recovery must fail (exit 1)
    twomode949.py [N]                     fit the last N (default 5) classified ks_chain3b states of track949.csv (needs the planted test to pass first, which it runs)

Law (x = D - D_last): a1 = exp(p1 - s1 x) (the Delta branch, the lower diabatic value at the last state), a2 = exp(p2 - s2 x), coupling g = gamma sqrt(a1 a2),
0 <= gamma <= 0.9; the observed pair is the eigenvalues of [[a1, g], [g, a2]]: sigma_Delta the minus root, sigma_2 the plus root. Least squares on
ln sigma_Delta and ln sigma_2, a grid of starts. D_c is where a1 = a2 and the gap there is sigma_2/sigma_Delta = (1 + gamma)/(1 - gamma)."""
import csv
import itertools
import math
import os
import sys

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
GMAX = 0.9
COUPLING = True      # --mutate sets it False: the model then has no coupling


def pair(theta, x, coupling=None):
    p1, s1, p2, s2, gam = theta
    a1, a2 = np.exp(p1 - s1 * x), np.exp(p2 - s2 * x)
    g = (gam if (COUPLING if coupling is None else coupling) else 0.0) * np.sqrt(a1 * a2)
    h = np.sqrt(((a1 - a2) / 2) ** 2 + g ** 2)
    return (a1 + a2) / 2 - h, (a1 + a2) / 2 + h


def share(theta, x):
    """the lowest vector's weight on the Delta branch (a1)"""
    p1, s1, p2, s2, gam = theta
    a1, a2 = np.exp(p1 - s1 * x), np.exp(p2 - s2 * x)
    g = (gam if COUPLING else 0.0) * np.sqrt(a1 * a2)
    return (1 + (a2 - a1) / np.sqrt((a1 - a2) ** 2 + 4 * g ** 2)) / 2


def crossing(theta, Dlast):
    p1, s1, p2, s2, gam = theta
    return Dlast + (p1 - p2) / (s1 - s2) if s1 != s2 else float("nan")


def fit(D, sd, s2, gamma_fixed=None):
    """least-squares fit of ln sigma_Delta and ln sigma_2 on the states D; returns (theta, rms residual of ln sigma). gamma_fixed pins gamma (the gap-zero fit)."""
    D, sd, s2 = map(np.asarray, (D, sd, s2))
    x = D - D[-1]
    y = np.concatenate([np.log(sd), np.log(s2)])
    best = None
    slope = -np.polyfit(x, np.log(sd), 1)[0]
    for ds1, ds2, lu, g0 in itertools.product((-0.15, -0.05, 0.0, 0.05, 0.15), (-0.15, -0.05, 0.0, 0.05, 0.15), (0.0, 0.3, 1.0, 3.0), (0.02, 0.1, 0.3)):
        s1, s2_ = slope + ds1, slope + ds2
        p1 = math.log(sd[-1]) + 0.0
        p2 = p1 + lu * 1.0 + 1e-3
        th0 = [p1, s1, p2, s2_, g0 if gamma_fixed is None else gamma_fixed]
        lo = [-np.inf, -2, -np.inf, -2, 0.0 if gamma_fixed is None else gamma_fixed]
        hi = [np.inf, 2, np.inf, 2, GMAX if gamma_fixed is None else gamma_fixed + 1e-12]

        def res(th):
            a, b = pair(th, x)
            return np.concatenate([np.log(np.maximum(a, 1e-300)), np.log(b)]) - y
        try:
            r = least_squares(res, th0, bounds=(lo, hi), xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=400)
        except Exception:
            continue
        th = r.x.copy()
        if math.exp(th[0]) > math.exp(th[2]):       # branch 1 is the lower diabatic value at the last state: swap if not
            th = np.array([th[2], th[3], th[0], th[1], th[4]])
        if best is None or r.cost < best[1]:
            best = (th, r.cost)
    th = best[0]
    a, b = pair(th, x)
    rms = math.sqrt(np.mean((np.concatenate([np.log(a), np.log(b)]) - y) ** 2))
    return th, rms


def planted(theta, Dlast, n=5, h=0.45, noise=1e-6, seed=0):
    rng = np.random.default_rng(seed)
    D = Dlast - h * np.arange(n - 1, -1, -1)
    a, b = pair(theta, D - Dlast, coupling=True)      # the planted truth always has its coupling, whatever the model under test (--mutate) does
    return D, a * np.exp(noise * rng.standard_normal(n)), b * np.exp(noise * rng.standard_normal(n))


def truth(s1, s2, gam, Dc, Dlast, p2=-41.0):
    """theta with the crossing at Dc: p1 - p2 = (s1 - s2)(Dc - Dlast), a1 the lower value at the last state"""
    p1 = p2 + (s1 - s2) * (Dc - Dlast)
    return np.array([p1, s1, p2, s2, gam])


def selftest():
    global COUPLING
    Dlast, ok = 253.0, True
    cases = []
    for gam, (s1, s2) in itertools.product((0.06, 0.15), ((0.43, 0.47), (0.47, 0.43))):
        offs = (0.05, 0.5) if s1 < s2 else (-0.05, -0.5, -1.3)     # D_c - D_last; a1 stays the lower value at the last state (crossing after it if s1 < s2, before it if s1 > s2)
        cases += [(gam, s1, s2, Dlast + o) for o in offs]
    print(f"selftest (a): {len(cases)} planted cases (gamma 0.06, 0.15; s1/s2 0.43/0.47 and 0.47/0.43; D_c 0.05 and 0.5 after the last state, or 0.05, 0.5 and 1.3 before it)")
    for gam, s1, s2, Dc in cases:
        th0 = truth(s1, s2, gam, Dc, Dlast)
        D, sd, sg = planted(th0, Dlast)
        th, rms = fit(D, sd, sg)
        dDc, dg = crossing(th, Dlast) - Dc, th[4] / gam - 1
        good = abs(dDc) <= 0.1 and abs(dg) <= 0.2 and abs(th[1] - s1) <= 0.02 and abs(th[3] - s2) <= 0.02
        ok &= good
        print(f"  gamma {gam} s1 {s1} s2 {s2} D_c {Dc:.3f}: fitted D_c {crossing(th, Dlast):.3f} ({dDc:+.3f}), gamma {th[4]:.4f} ({dg:+.1%}), s1 {th[1]:.4f}, s2 {th[3]:.4f}, rms {rms:.1e}: {'pass' if good else 'FAIL'}")
    # (b) true crossing: gamma = 0
    for s1, s2, Dc in ((0.43, 0.47, Dlast + 0.5), (0.47, 0.43, Dlast - 0.5)):
        th0 = truth(s1, s2, 0.0, Dc, Dlast)
        D, sd, sg = planted(th0, Dlast)
        th, rms = fit(D, sd, sg)
        good = th[4] <= 0.01
        ok &= good
        print(f"selftest (b): gamma 0 (true crossing, D_c {Dc:.2f}): fitted gamma {th[4]:.4f}, rms {rms:.1e}: {'pass' if good else 'FAIL'}")
    # (c) the gap-zero fit on gapped data is rejected
    for gam in (0.06, 0.15):
        th0 = truth(0.43, 0.47, gam, Dlast + 0.5, Dlast)
        D, sd, sg = planted(th0, Dlast)
        _, rms_free = fit(D, sd, sg)
        _, rms_zero = fit(D, sd, sg, gamma_fixed=0.0)
        good = rms_zero > 1e-4 and rms_zero >= 100 * rms_free and rms_free < 1e-5
        ok &= good
        print(f"selftest (c): data with gamma {gam}: free fit rms {rms_free:.1e}, gap-zero fit rms {rms_zero:.1e}: {'rejected, pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate (coupling dropped)" if not COUPLING else "") + ":", "pass" if ok else "FAIL")
    return ok


def real(n):
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "track949.csv"))) if r["chain"] == "4" and r["classified"] == "1"]
    rows.sort(key=lambda r: float(r["D"]))
    rows = rows[-n:]
    import json
    sys.path.insert(0, HERE)
    import row949
    D, sd, s2, sh = [], [], [], []
    for r in rows:
        rec = json.load(open(os.path.join(HERE, f"c3b_ks{r['ks']}_D{float(r['D']):.4f}.json")))
        d, k2 = row949.picks(rec)
        D.append(float(r["D"])); sd.append(rec["vectors"][d]["sigma"]); s2.append(rec["vectors"][k2]["sigma"]); sh.append(rec["vectors"][d]["delta"])
    return D, sd, s2, sh


def main():
    global COUPLING
    if "--selftest" in sys.argv:
        COUPLING = "--mutate" not in sys.argv
        sys.exit(0 if selftest() else 1)
    log = os.path.join(HERE, "selftest_twomode949.log")      # the planted test's own log (twomode949.py --selftest), newer than this script and passing
    if not (os.path.exists(log) and os.path.getmtime(log) > os.path.getmtime(__file__) and "selftest: pass" in open(log).read() and open(log).read().rstrip().endswith("exit 0")):
        print("the planted test (twomode949.py --selftest > selftest_twomode949.log) has not passed since the last change of this script: no fit on real states")
        sys.exit(1)
    n = int(next((a for a in sys.argv[1:] if a.isdigit()), 5))
    D, sd, s2, sh = real(n)
    th, rms = fit(D, sd, s2)
    x = np.array(D) - D[-1]
    a, b = pair(th, x)
    print(f"\nreal states D {D[0]:.4f} to {D[-1]:.4f} ({len(D)}): s1 {th[1]:.4f} (the Delta branch's own slope), s2 {th[3]:.4f}, gamma {th[4]:.4f} (gap {(1 + th[4]) / (1 - th[4]):.3f}),"
          f" D_c {crossing(th, D[-1]):.3f}, rms residual of ln sigma {rms:.2e}")
    print("fitted Delta share of the lowest vector against the measured one:", ", ".join(f"{s:.3f}/{m:.3f}" for s, m in zip(share(th, x), sh)))
    print("sigma_Delta, sigma_2 fitted/measured:", ", ".join(f"{a_ / s_:.4f}/{b_ / t_:.4f}" for a_, s_, b_, t_ in zip(a, sd, b, s2)))


if __name__ == "__main__":
    main()
