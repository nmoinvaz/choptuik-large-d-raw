#!/usr/bin/env python3
"""#521: do the weak subspace's two periods persist below D 228? #519's fit (a trend + one sinusoid, the period scanned, 1000-trial null test) on ln sigma_1..4 over D 216 to 237 and over D 216 to 227 alone.
usage: python analysis_521.py [--selftest]       (run from I521-win2; needs ../I516-win2/fit_516.py, ../I519-win2/analysis_519.py and the logs of #505, #510, #511, #515, #516 and this folder)
Ranges: all (D 216 to 237.2), low (D 216 to 227.2, twelve states one unit apart) and, for reference, high (D 228 to 237.2, the #519 data). Fits: (a) line + sinusoid, (c) quadratic + sinusoid.
The period scan runs from Pmin to the D range over 1.5 in steps of 0.005 (the same grid for the observed fit and for its null trials); Pmin is 1.1 where the sampling has half-unit steps and 2.05 for the unit-spaced low range
(the Nyquist period of unit sampling is 2, and a period P and 1/(1 - 1/P) cannot be told apart below it). Null fraction: the share of 1000 trials of a pure line plus white noise of the observed rms whose amplitude / error is at least the observed one.
Rule of #521: a period within 0.15 of its D 228 to 237 value with a null fraction below 1% persists; a period that drifts by more than 0.3 between the halves changes with D.
--selftest: a planted period in D 216 to 227 at unit spacing is recovered; a pure line is not flagged."""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I516-win2"))
sys.path.insert(0, os.path.join(HERE, "..", "I505-win2"))
import fit_516 as f  # noqa: E402
from table_505 import parse  # noqa: E402
RAW = os.path.join(HERE, "..")
STEP = 0.005


def grid(D, pmin):
    return np.arange(pmin, (D.max() - D.min()) / 1.5 + 1e-9, STEP)


def fit(D, y, pmin, quad):
    return f.sinfit(D, y, grid(D, pmin), quad)


def nullfrac(D, sigma, ratio, pmin, quad, trials=1000, seed=5):
    rng = np.random.default_rng(seed)
    g = grid(D, pmin)
    hit = 0
    for _ in range(trials):
        yy = -1.1 * (D - D.mean()) + rng.normal(0, sigma, len(D))
        r = f.sinfit(D, yy, g, quad)
        if r["amp"] / r["err"] >= ratio:
            hit += 1
    return hit / trials


def one(name, D, y, pmin, quad, trials=1000):
    r = fit(D, y, pmin, quad)
    ratio = r["amp"] / r["err"]
    nf = nullfrac(D, r["rms"], ratio, pmin, quad, trials)
    return dict(name=name, P=r["P"], Plo=r["Plo"], Phi=r["Phi"], amp=r["amp"], err=r["err"], ratio=ratio, rms=r["rms"], nf=nf, n=r["n"], pmin=pmin)


def line(r):
    return (f"{r['name']}: N {r['n']}, P = {r['P']:.3f} ({r['Plo']:.3f} to {r['Phi']:.3f}), amplitude {r['amp']:.4f} +- {r['err']:.4f} (ratio {r['ratio']:.1f}), rms residual {r['rms']:.4f}, null fraction {100 * r['nf']:.1f}% (scan from {r['pmin']})")


def selftest():
    rng = np.random.default_rng(4)
    D = np.arange(216.1312, 227.2, 1.0)
    y = -1.05 * (D - 222.0) + 0.12 * np.sin(2 * np.pi * (D - 220.0) / 2.5) + rng.normal(0, 0.01, len(D))
    r = one("planted 2.5", D, y, 2.05, False, trials=300)
    y0 = -1.05 * (D - 222.0) + rng.normal(0, 0.01, len(D))
    r0 = one("pure line", D, y0, 2.05, False, trials=300)
    ok = abs(r["P"] - 2.5) < 0.1 and r["nf"] < 0.01 and not (r0["nf"] < 0.01 and r0["ratio"] >= 3 and r0["amp"] > 0.05)
    print(line(r)); print(line(r0))
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def collect():
    paths = (glob.glob(os.path.join(RAW, "I505-win2/eq_D2*.log")) + glob.glob(os.path.join(RAW, "I510-win2/eq_D2*.log")) + glob.glob(os.path.join(RAW, "I511-win2/eq_D2*.log"))
             + glob.glob(os.path.join(RAW, "I516-win2/eq_crawl*_D2*.log")) + glob.glob(os.path.join(HERE, "eq_crawlG_D2*.log")))
    paths = [p for p in paths if "ctl" not in p] + [os.path.join(RAW, "I515-win2/eq_crawlE_D239.8063.log")]
    pts = {}
    for p in paths:
        r = parse(p)
        s = {x["i"]: x["sigma"] for x in r["sig"]}
        pts.setdefault(round(r["D"], 4), []).append([math.log(s[i]) for i in (1, 2, 3, 4)])
    return pts


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    pts = collect()
    Ds = sorted(pts)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    for d in Ds:
        if len(pts[d]) > 1:
            print(f"  D {d:.4f}: {len(pts[d])} runs, spread of ln sigma_1..4 {' '.join(f'{np.ptp([v[i] for v in pts[d]]):.1e}' for i in range(4))}")
    print(f"{len(D)} distinct D from {D[0]:.4f} to {D[-1]:.4f}")
    ranges = (("low D 216 to 227", D <= 227.2, 2.05), ("high D 228 to 237 (the #519 data)", (D >= 228.0) & (D <= 237.2), 1.1), ("all D 216 to 237", D <= 237.2, 1.1))
    res = {}
    for rname, sel, pmin in ranges:
        print(f"\n{rname}: {int(sel.sum())} distinct D")
        for i in (1, 2, 3, 4):
            for quad, ftag in ((False, "(a) line + sinusoid"), (True, "(c) quadratic + sinusoid")):
                r = one(f"ln sigma_{i} {ftag}", D[sel], Y[sel, i - 1], pmin, quad)
                res[(rname.split()[0], i, quad)] = r
                print("  " + line(r))
    print("\nrule of #521: period within 0.15 of the D 228 to 237 value with a null fraction below 1% persists; a drift of more than 0.3 between the halves changes with D")
    print("| series | fit | P (D 216 to 227) | P (D 228 to 237) | drift | null fraction low | persists? | changes with D? | P (all D 216 to 237) | null fraction all |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        for quad, ftag in ((False, "line"), (True, "quadratic")):
            lo, hi, al = res[("low", i, quad)], res[("high", i, quad)], res[("all", i, quad)]
            drift = lo["P"] - hi["P"]
            persists = abs(drift) <= 0.15 and lo["nf"] < 0.01
            print(f"| sigma_{i} | {ftag} | {lo['P']:.3f} | {hi['P']:.3f} | {drift:+.3f} | {100 * lo['nf']:.1f}% | {'yes' if persists else 'no'} | {'yes' if abs(drift) > 0.3 else 'no'} | {al['P']:.3f} | {100 * al['nf']:.1f}% |")
