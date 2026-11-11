#!/usr/bin/env python3
"""#519: the period 2.74 in D (#516) in ln sigma_2..4 and in Delta's deviation from its trend.
usage: python analysis_519.py [--selftest]       (run from I519-win2; needs ../I516-win2/fit_516.py and the logs and states of the other folders)
Part 1: for i = 1..4 the same fits as #516 on ln sigma_i over D 228.13 to 237.13: (a) line + sinusoid (the rule), (c) quadratic + sinusoid; each with the period interval and a null fraction: the fraction of 1000 trials of a
pure line plus white noise of the observed rms (period scanned the same way) whose amplitude / error is at least the observed one.
Part 2: Delta at every stored state of the clean chain (exact sum of the four double parts), its deviation from a least-squares polynomial in x = 1/n (n = D - 2) of degree 5 and of degree 7 (Chebyshev basis on [-1, 1]), the rms and largest
deviation, the difference between the two polynomials (the error bar over the degree) at D 230 and its rms over the range, and the sinusoid fit of each deviation over the whole range and over D 228.13 to 237.13.
Same period (rule of #519): within 0.15 of 2.74 with a null fraction below 1%.
--selftest: a planted sinusoid of period 2.74 in a smooth trend plus noise is found by the whole chain of part 2 (the deviation of the polynomial fit shows the period) and a series without it is not flagged."""
import glob, json, math, os, sys
import numpy as np
from mpmath import mp, mpf
mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I516-win2"))
sys.path.insert(0, os.path.join(HERE, "..", "I505-win2"))
import fit_516 as f  # noqa: E402
from table_505 import parse  # noqa: E402
RAW = os.path.join(HERE, "..")
P0 = 2.74


def null_fraction(D, sigma, ratio, trials=1000, seed=5, quad=False):
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(trials):
        yy = -1.1 * (D - D.mean()) + rng.normal(0, sigma, len(D))
        r = f.run(D, yy, quad)
        if r["amp"] / r["err"] >= ratio:
            hit += 1
    return hit / trials


def fitline(name, D, y, quad=False, trials=1000, out=print):
    r = f.run(D, y, quad)
    ratio = r["amp"] / r["err"]
    nf = null_fraction(D, r["rms"], ratio, trials, quad=quad)
    same = abs(r["P"] - P0) <= 0.15 and nf < 0.01
    out(f"  {name}: N {r['n']}, P = {r['P']:.3f} ({r['Plo']:.3f} to {r['Phi']:.3f}), amplitude {r['amp']:.4g} +- {r['err']:.2g} (ratio {ratio:.1f}), rms residual {r['rms']:.3g}, null fraction {100 * nf:.1f}%; "
        + ("SAME oscillation (P within 0.15 of 2.74 and null fraction below 1%)" if same else "not the same oscillation by the rule"))
    return r, nf, same


def delta_of(path):
    z = np.load(path, allow_pickle=True)
    return sum((mpf(float(z[k][-1])) for k in ("zh", "zl", "z2", "z3")), mpf(0))


def states():
    paths = []
    for c in ("crawlG", "crawlI", "crawlJ", "crawlL"):
        paths += glob.glob(os.path.join(RAW, "I461-win2", c, "anm_pin3_D2*.npz"))
    paths += [os.path.join(RAW, "I461-win2", "probe03125", "anm_pin3_D242.5146.npz"), os.path.join(RAW, "I461-win2", "probeH00390625", "anm_pin3_D242.5264.npz")]
    res = {}
    for p in paths:
        z = np.load(p, allow_pickle=True)
        meta = json.loads(str(z["meta"]))
        D = float(meta["D_str"]) if "D_str" in meta else float(meta["D"])
        if D < 215.9:
            continue
        res[round(D, 6)] = (delta_of(p), os.path.relpath(p, os.path.join(RAW, "I461-win2")))
    return res


def polydev(D, dl, deg):
    n = D - 2.0
    x = 1.0 / n
    t = (2 * x - (x.max() + x.min())) / (x.max() - x.min())
    C = np.polynomial.chebyshev.chebfit(t, dl, deg)
    fitv = np.polynomial.chebyshev.chebval(t, C)
    return dl - fitv, (C, x.min(), x.max())


def evalpoly(model, D):
    C, xmin, xmax = model
    x = 1.0 / (D - 2.0)
    t = (2 * x - (xmax + xmin)) / (xmax - xmin)
    return np.polynomial.chebyshev.chebval(t, C)


def part2(series, out=print, trials=1000):
    Ds = sorted(series)
    D = np.array(Ds)
    ref = series[Ds[-1]][0]
    dl = np.array([float(series[d][0] - ref) for d in Ds])       # Delta minus Delta(last state): exact differences in mp, then float
    out(f"Delta at {len(D)} stored states, D {D[0]:.4f} to {D[-1]:.4f}; Delta(first) {mp.nstr(series[Ds[0]][0], 16)}, Delta(last) {mp.nstr(ref, 16)}")
    devs = {}
    for deg in (5, 7):
        dev, model = polydev(D, dl, deg)
        devs[deg] = (dev, model)
        out(f"  degree {deg}: rms deviation {np.sqrt(np.mean(dev ** 2)):.3e}, largest {np.max(np.abs(dev)):.3e}")
    d230 = float(evalpoly(devs[5][1], np.array([230.0]))[0] - evalpoly(devs[7][1], np.array([230.0]))[0])
    diff = evalpoly(devs[5][1], D) - evalpoly(devs[7][1], D)
    out(f"  the degree 5 and degree 7 polynomials differ by {abs(d230):.3e} at D 230 (the coordinator's error bar over the degree, about 3e-11) and by rms {np.sqrt(np.mean(diff ** 2)):.3e}, largest {np.max(np.abs(diff)):.3e} over the range")
    res = {}
    for deg in (5, 7):
        dev = devs[deg][0]
        out(f" degree {deg} deviation, line + sinusoid fits (the deviation has no trend left; the line absorbs what remains):")
        res[(deg, "all")] = fitline("all D", D, dev, trials=trials, out=out)
        sel = (D >= 228.0) & (D <= 237.2)
        res[(deg, "mid")] = fitline("D 228.13 to 237.13", D[sel], dev[sel], trials=trials, out=out)
    return res, devs, D


def selftest():
    rng = np.random.default_rng(2)
    D = np.concatenate([np.arange(216.1312, 232.2, 1.0), np.arange(232.6312, 237.2, 0.5), [237.6312, 238.1312, 238.7562, 239.5375, 240.0258, 240.5141, 241.1244, 241.8874, 242.3642, 242.4834, 242.5146, 242.5225, 242.5264]])
    n = D - 2
    base = 1.68 + 3.0 / n + 1e3 / n ** 3 + 1e5 / n ** 5          # a smooth trend in 1/n
    y_per = base + 3e-11 * np.sin(2 * np.pi * (D - 230.0) / 2.74) + rng.normal(0, 3e-12, len(D))
    y_no = base + rng.normal(0, 3e-12, len(D))
    ok = True
    for name, y in (("planted period", y_per), ("no period", y_no)):
        series = {round(d, 6): (mpf(float(v)), "") for d, v in zip(D, y)}
        sink = []
        res, devs, DD = part2(series, out=sink.append, trials=300)
        r, nf, same = res[(5, "all")]
        print(f"selftest {name}: degree 5 deviation, all D: P {r['P']:.3f}, amplitude {r['amp']:.3g} +- {r['err']:.2g}, null fraction {100 * nf:.1f}% -> {'same period' if same else 'not the same period'}")
        ok = ok and (same if name == "planted period" else not same)
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def collect_sigma():
    paths = (glob.glob(os.path.join(RAW, "I505-win2/eq_D2*.log")) + glob.glob(os.path.join(RAW, "I510-win2/eq_D2*.log")) + glob.glob(os.path.join(RAW, "I511-win2/eq_D2*.log"))
             + glob.glob(os.path.join(RAW, "I516-win2/eq_crawl*_D2*.log")))
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
    pts = collect_sigma()
    Ds = sorted(pts)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    sel = (D >= 228.0) & (D <= 237.2)
    print(f"Part 1: ln sigma_i over D 228.13 to 237.13 ({int(sel.sum())} distinct D)")
    for i in (1, 2, 3, 4):
        print(f" ln sigma_{i}:")
        fitline("(a) line + sinusoid", D[sel], Y[sel, i - 1])
        fitline("(c) quadratic + sinusoid", D[sel], Y[sel, i - 1], quad=True)
    print("\nPart 2:")
    series = states()
    part2(series)
