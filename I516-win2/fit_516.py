#!/usr/bin/env python3
"""#516: ln sigma_1 (equilibrated, near_null_eq.py logs) against D, fitted to a line plus one sinusoid: y = c0 + c1 (D - Dm) + A cos(2 pi D / P) + B sin(2 pi D / P).
usage: python fit_516.py            (run from I516-win2: reads the logs of ../I505-win2, ../I510-win2, ../I511-win2, ../I515-win2 (crawlE only) and this folder)
       python fit_516.py --selftest (a planted period is recovered with amplitude / error above 3; a planted line with the same noise is not)
Per period P on a grid (1.1 up to the D range divided by 1.5, step 0.002; periods at which the design is nearly rank deficient are skipped) the four linear parameters are fitted by least squares; the best P minimises the sum of squares.
Amplitude = sqrt(A^2 + B^2), its error by the delta method from the covariance of (A, B) at the best P with the residual variance (dof = N - 5). Rule of #516: report the period if the amplitude is at least
3 times its error. Fits: (a) the half-unit region D 228.13 to 237.13 (the rule's data, dense in D); (b) all D 216.13 to 242.53; (c) region (a) with a quadratic trend added to the line (robustness, not the rule)."""
import glob, math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "I505-win2"))
from table_505 import parse  # noqa: E402

def sinfit(D, y, Pgrid, quad=False):
    Dm = D.mean()
    best = None
    prof = []
    for P in Pgrid:
        cols = [np.ones_like(D), D - Dm] + ([(D - Dm) ** 2] if quad else []) + [np.cos(2 * np.pi * D / P), np.sin(2 * np.pi * D / P)]
        X = np.column_stack(cols)
        if np.linalg.cond(X) > 1e6:        # the design is nearly rank deficient at this period (for example P = 1.0 with D at only two phases): skip it
            continue
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        r = y - X @ beta
        ss = float(r @ r)
        prof.append((P, ss))
        if best is None or ss < best[0]:
            best = (ss, P, beta, X, r)
    ss, P, beta, X, r = best
    k = X.shape[1] + 1   # the period counts as a parameter
    dof = len(D) - k
    s2 = ss / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    ia = X.shape[1] - 2
    A, B = beta[ia], beta[ia + 1]
    amp = math.hypot(A, B)
    g = np.array([A, B]) / amp
    var = g @ cov[ia:ia + 2, ia:ia + 2] @ g
    thr = ss * (1 + 1.0 / dof)       # sum of squares within one residual variance of the best: the period's interval
    ok = [q for q, v in prof if v <= thr]
    k0 = [i for i, (q, v) in enumerate(prof) if q == P][0]
    lo = k0
    while lo > 0 and prof[lo - 1][1] <= thr:
        lo -= 1
    hi = k0
    while hi < len(prof) - 1 and prof[hi + 1][1] <= thr:
        hi += 1
    return dict(Plo=prof[lo][0], Phi=prof[hi][0], P=P, amp=amp, err=math.sqrt(var), ss=ss, rms=math.sqrt(ss / len(D)), maxres=float(np.max(np.abs(r))), dof=dof, slope=-beta[1], n=len(D))

def run(D, y, quad=False):
    Pgrid = np.arange(1.1, (D.max() - D.min()) / 1.5 + 1e-9, 0.002)   # above the Nyquist period of the half-unit sampling
    return sinfit(D, y, Pgrid, quad)

def report(name, f, out=print):
    out(f"{name}: N {f['n']}, best period P = {f['P']:.3f} (within one residual variance: {f['Plo']:.3f} to {f['Phi']:.3f}), amplitude {f['amp']:.4f} +- {f['err']:.4f} (ratio {f['amp'] / f['err']:.1f}), mean rate {f['slope']:.3f}, rms residual {f['rms']:.4f}, largest {f['maxres']:.4f}, dof {f['dof']}; "
        + (f"=> report the period {f['P']:.2f}" if f['amp'] >= 3 * f['err'] else "=> amplitude below 3 times its error: no single period"))

def null_ratios(D, sigma, trials=300, seed=11):
    """amp / err of the scanned line + sinusoid fit to pure line + white noise of rms sigma at the same D (the false positives of the rule: the period is scanned)"""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(trials):
        yy = -1.1 * (D - D.mean()) + rng.normal(0, sigma, len(D))
        f = run(D, yy)
        out.append((f["amp"], f["amp"] / f["err"]))
    return np.array(out)

def selftest():
    rng = np.random.default_rng(3)
    D = np.arange(228.1312, 237.2, 0.5)
    y = -1.1 * (D - 232.0) + 0.15 * np.sin(2 * np.pi * (D - 231.0) / 2.4) + rng.normal(0, 0.01, len(D))
    f1 = run(D, y)
    nul = null_ratios(D, 0.01, trials=200)
    frac = float(np.mean(nul[:, 1] >= 3))
    p99 = float(np.percentile(nul[:, 1], 99))
    ok1 = abs(f1["P"] - 2.4) < 0.1 and f1["amp"] >= 3 * f1["err"] and abs(f1["amp"] - 0.15) < 0.02
    ok0 = f1["amp"] / f1["err"] > p99
    print(f"selftest: planted period 2.4 found as {f1['P']:.3f}, amplitude {f1['amp']:.3f} +- {f1['err']:.3f} (ratio {f1['amp'] / f1['err']:.0f}); pure line + the same noise reaches ratio >= 3 in {100 * frac:.0f}% of 200 trials (99th percentile {p99:.1f}): the rule as written has false positives because the period is scanned")
    print("selftest: ok" if ok1 and ok0 else "selftest FAILED")
    return 0 if ok1 and ok0 else 1

def collect():
    here = os.path.dirname(os.path.abspath(__file__))
    paths = (glob.glob(os.path.join(here, "../I505-win2/eq_D2*.log")) + glob.glob(os.path.join(here, "../I510-win2/eq_D2*.log")) + glob.glob(os.path.join(here, "../I511-win2/eq_D2*.log"))
             + glob.glob(os.path.join(here, "eq_crawl*_D2*.log")))
    paths = [p for p in paths if "ctl" not in p]
    paths += [os.path.join(here, "../I515-win2/eq_crawlE_D239.8063.log")]
    pts = {}
    for p in paths:
        r = parse(p)
        y = math.log({x["i"]: x["sigma"] for x in r["sig"]}[1])
        pts.setdefault(round(r["D"], 4), []).append((y, os.path.basename(os.path.dirname(os.path.abspath(p))) + "/" + os.path.basename(p), r["passed"]))
    return pts

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    pts = collect()
    Ds = sorted(pts)
    print(f"{len(Ds)} distinct D")
    for d in Ds:
        ys = [v[0] for v in pts[d]]
        spread = max(ys) - min(ys)
        print(f"  D {d:.4f}  ln sigma_1 {np.mean(ys):.6f}  ({len(ys)} state(s){'; spread between them ' + format(spread, '.4f') if len(ys) > 1 else ''}; planted checks {'pass' if all(v[2] for v in pts[d]) else 'FAIL'})")
    D = np.array(Ds)
    y = np.array([np.mean([v[0] for v in pts[d]]) for d in Ds])
    sel = (D >= 228.0) & (D <= 237.2)
    fa = run(D[sel], y[sel])
    report("(a) D 228.13 to 237.13, line + sinusoid", fa)
    nul = null_ratios(D[sel], fa["rms"], trials=300)
    print(f"    null calibration (not part of the rule): pure line + white noise of the same rms ({fa['rms']:.4f}) at the same D, 300 trials: ratio >= 3 in {100 * np.mean(nul[:, 1] >= 3):.0f}%, ratio >= the observed {fa['amp'] / fa['err']:.1f} in "
          f"{100 * np.mean(nul[:, 1] >= fa['amp'] / fa['err']):.1f}%, amplitude >= the observed {fa['amp']:.4f} in {100 * np.mean(nul[:, 0] >= fa['amp']):.1f}%")
    report("(b) all D, line + sinusoid", run(D, y))
    report("(c) D 228.13 to 237.13, quadratic + sinusoid (robustness, not the rule)", run(D[sel], y[sel], quad=True))
    print("local rates of sigma_1 per unit of D between neighbouring D (half-unit steps in the dense region):")
    for a, b in zip(Ds, Ds[1:]):
        if 228.0 <= a and b <= 237.2:
            print(f"  {a:.4f} to {b:.4f}  dD {b - a:.4f}  rate {(np.mean([v[0] for v in pts[a]]) - np.mean([v[0] for v in pts[b]])) / (b - a):.3f}")
