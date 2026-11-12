#!/usr/bin/env python3
"""#533: a nonlinear period drift for ln sigma_1..4 over the 51 equilibrated states D 210.13 to 237.13. The chirp of #522/#525 with P(D) = P0 + p1 x + p2 x^2 (x = D - 228) and a cubic trend, both hold-outs, the prediction of
sigma_1's period over D 204 to 209.6 for #535.
usage: python period_p2_533.py [--selftest] [--trials N] [--boot N]       (run from I533-win2; needs ../I525-win2/trend_525.py, residual_525.py, ../I522-win2/chirp_522.py, halfunit_522.py and the logs they read)
Model: y = trend(u) + A cos(phi) + B sin(phi), u = (D - 228) / 10, trend a polynomial of degree 3 (2 for the reference rows), phi(D) = 2 pi int_228^D dD' / P(D') (24-point Gauss-Legendre on [0, x]).
Fits are variable projection: the linear parameters by least squares, (P0, p1, p2) by Nelder-Mead from the best (P0, p1) of the grid of #522 (P0 1.50..3.50 step 0.01, p1 -0.12..0.12 step 0.002, p2 = 0, polished) and from p2 = +-0.0005 there.
The p2 = 0 fit is the grid best polished by Nelder-Mead in (P0, p1); the free fit is never worse than it.
Null fraction of p2: of N trials of (the p2 = 0 fit to the data) + white noise, the share whose R = (SS0 - SSfree) / SSfree is at least the observed one, at the noise of (i) the free fit's residual rms, (ii) the p2 = 0 fit's.
Hold-outs: H1 fits D <= 232.7 (42 states) and predicts D 233.13 to 237.13 (9); H2 fits D >= 214 (43 states) and predicts D 210.13 to 213.63 (8). Controls: p1 = p2 = 0 (a constant period, P0 on the grid), and the p2 = 0 chirp.
Acceptance of #533: p2 null fraction below 1% for sigma_1 and sigma_2; residual over the 51 states at most 0.0065 for sigma_1 and sigma_2; both hold-outs at most 0.014 for sigma_1 and sigma_2 with the control reported.
Prediction for #535: the period of the free fit over all 51 states at the centre of D 204 to 209.6 (D 206.8), with the spread of a parametric bootstrap (the free fit as the truth, white noise at its rms).
--selftest (before the data), at the D of the data, noise 0.006, amplitude 0.11, cubic trend like the data: S1 a planted p2 (P0 2.63, p1 +0.0185, p2 +0.0004): p2 recovered to within 0.0002, null fraction below 1%, residual at most
1.3 x noise; S2 a planted p2 = 0 (P0 2.60, p1 +0.014): |p2| at most 0.0002 and null fraction at least 1% (no false claim)."""
import math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import trend_525 as t  # noqa: E402
import below216_525 as b  # noqa: E402
r, c, h = t.r, t.c, t.h
D0 = 228.0
GX, GW = np.polynomial.legendre.leggauss(24)
TT, WW = (GX + 1) / 2, GW / 2
LIMIT = 0.014
CENTRE = 206.8


def phase(D, P0, p1, p2):
    x = D - D0
    xt = x[:, None] * TT[None, :]
    P = P0 + p1 * xt + p2 * xt ** 2
    if np.any(P <= 0.5) or np.any(P > 8):
        return None
    return 2 * np.pi * x * np.sum(WW[None, :] / P, axis=1)


def columns(D, deg, ph):
    u = (D - D0) / 10.0
    return np.column_stack([u ** k for k in range(deg + 1)] + [np.cos(ph), np.sin(ph)])


def ss_of(theta, D, y, deg):
    ph = phase(D, theta[0], theta[1], theta[2])
    if ph is None:
        return 1e9
    X = columns(D, deg, ph)
    beta, res, rk, sv = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    return float(e @ e)


def lin(D, y, deg, theta):
    ph = phase(D, *theta)
    X = columns(D, deg, ph)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ beta
    return beta, float(e @ e)


def nm(f, x0, steps):
    sim = [np.array(x0, float)] + [np.array(x0, float) + s for s in np.diag(steps)]
    res = minimize(f, x0, method="Nelder-Mead", options=dict(initial_simplex=np.array(sim), xatol=1e-6, fatol=1e-13, maxiter=800, maxfev=800))
    return res.x, res.fun


class Fitter:
    def __init__(self, D, deg):
        self.D, self.deg = D, deg
        self.X, self.XtX, self.valid = t.grid_columns_deg(D, deg)
        self.j0 = int(np.argmin(np.abs(c.P1S)))

    def fit0(self, y):
        """the p2 = 0 chirp: grid best polished"""
        ss, P0, p1, bb = r.grid_fit(self.X, self.XtX, self.valid, y)
        x, f = nm(lambda th: ss_of([th[0], th[1], 0.0], self.D, y, self.deg), [P0, p1], [0.03, 0.004])
        if f > ss:
            x, f = np.array([P0, p1]), ss
        return dict(theta=np.array([x[0], x[1], 0.0]), ss=f)

    def const(self, y):
        """p1 = p2 = 0 control: P0 on the grid"""
        v = np.zeros_like(self.valid)
        v[:, self.j0] = self.valid[:, self.j0]
        ss, P0, p1, bb = r.grid_fit(self.X, self.XtX, v, y)
        return dict(theta=np.array([P0, 0.0, 0.0]), ss=ss)

    def fit_free(self, y, f0=None):
        f0 = f0 or self.fit0(y)
        best = dict(theta=f0["theta"].copy(), ss=f0["ss"])
        for p2 in (0.0, 0.0005, -0.0005):
            x0 = [f0["theta"][0], f0["theta"][1], p2]
            x, f = nm(lambda th: ss_of(th, self.D, y, self.deg), x0, [0.03, 0.004, 0.0004])
            if f < best["ss"]:
                best = dict(theta=np.array(x), ss=f)
        return best, f0


def predict(Dte, D, y, deg, theta):
    beta, ss = lin(D, y, deg, theta)
    return columns(Dte, deg, phase(Dte, *theta)) @ beta


def nullfrac(F, y, trials, which, seed):
    best, f0 = F.fit_free(y)
    n = len(y)
    beta0, _ = lin(F.D, y, F.deg, f0["theta"])
    truth = columns(F.D, F.deg, phase(F.D, *f0["theta"])) @ beta0
    sig = math.sqrt(best["ss"] / n) if which == "ext" else math.sqrt(f0["ss"] / n)
    Robs = (f0["ss"] - best["ss"]) / best["ss"]
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(trials):
        yy = truth + rng.normal(0, sig, n)
        bb, ff = F.fit_free(yy)
        if (ff["ss"] - bb["ss"]) / bb["ss"] >= Robs:
            hit += 1
    return hit / trials, Robs


def planted(D, P0, p1, p2, seed, noise=0.006):
    u = (D - D0) / 10.0
    ph = phase(D, P0, p1, p2)
    return 0.3 - 11 * u + 1.5 * u ** 2 - 0.09 * u ** 3 + 0.11 * np.sin(ph + 0.7) + np.random.default_rng(seed).normal(0, noise, len(D))


def collect51():
    old = h.collect()
    new = b.collect_new()
    new = {d: v for d, v in new.items() if d < 216.0}
    pts = dict(old)
    pts.update(new)
    Ds = sorted(d for d in pts if d <= 237.2)
    D = np.array(Ds)
    return D, np.array([np.mean(pts[d], axis=0) for d in Ds])


def selftest(trials=200):
    D, _ = collect51()
    F = Fitter(D, 3)
    ok = True
    for name, (P0, p1, p2), seed in (("S1 planted p2 = +0.0004", (2.63, 0.0185, 0.0004), 5), ("S2 planted p2 = 0", (2.60, 0.014, 0.0), 6)):
        y = planted(D, P0, p1, p2, seed)
        best, f0 = F.fit_free(y)
        nf1, Robs = nullfrac(F, y, trials, "ext", 11)
        nf2, _ = nullfrac(F, y, trials, "m0", 12)
        rms = math.sqrt(best["ss"] / len(D))
        th = best["theta"]
        print(f"{name}: free fit P0 {th[0]:.3f}, p1 {th[1]:+.4f}, p2 {th[2]:+.5f}, rms {rms:.4f} (p2 = 0 fit rms {math.sqrt(f0['ss'] / len(D)):.4f}); R {Robs:.3f}; null fraction {100 * nf1:.1f}% (noise = free rms), {100 * nf2:.1f}% (noise = p2 = 0 rms)")
        if p2 != 0:
            good = abs(th[2] - p2) <= 0.0002 and max(nf1, nf2) < 0.01 and rms <= 1.3 * 0.006
        else:
            good = abs(th[2]) <= 0.0002 and min(nf1, nf2) >= 0.01
        print(f"  -> {'pass' if good else 'FAIL'}")
        ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def holdouts(D, y, deg, i):
    out = {}
    for tag, tr, te in (("H1 fit D <= 232.7, predict D 233.13 to 237.13", D <= 232.7, D > 232.7), ("H2 fit D >= 214, predict D 210.13 to 213.63", D >= 214.0, D < 214.0)):
        F = Fitter(D[tr], deg)
        yt = y[tr]
        best, f0 = F.fit_free(yt)
        cst = F.const(yt)
        row = {}
        for nm_, th in (("p2 chirp", best["theta"]), ("p2 = 0 chirp", f0["theta"]), ("p1 = p2 = 0", cst["theta"])):
            e = y[te] - predict(D[te], D[tr], yt, deg, th)
            row[nm_] = (math.sqrt(np.mean(e ** 2)), float(np.max(np.abs(e))), th)
        out[tag] = (row, int(tr.sum()), int(te.sum()))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest(int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 200))
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 500
    boot = int(sys.argv[sys.argv.index("--boot") + 1]) if "--boot" in sys.argv else 200
    D, Y = collect51()
    print(f"{len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; {trials} null trials; {boot} bootstrap trials; acceptance: null below 1%, residual <= 0.0065, both hold-outs <= {LIMIT} (sigma_1, sigma_2)")
    summ = {}
    for deg in (3, 2):
        F = Fitter(D, deg)
        print(f"\n== trend of degree {deg}: fits to all 51 states")
        print("| series | p2 = 0: P0, p1 | rms | free: P0, p1, p2 | rms | period at D 213 / 228 / 237 | R | null fraction (i) / (ii) |\n|---|---|---|---|---|---|---|---|")
        for i in (1, 2, 3, 4):
            y = Y[:, i - 1]
            best, f0 = F.fit_free(y)
            th, t0 = best["theta"], f0["theta"]
            Pof = lambda x: th[0] + th[1] * (x - D0) + th[2] * (x - D0) ** 2
            if deg == 3 and i in (1, 2):
                nf1, Robs = nullfrac(F, y, trials, "ext", 21 + i)
                nf2, _ = nullfrac(F, y, trials, "m0", 31 + i)
                nfs = f"{100 * nf1:.1f}% / {100 * nf2:.1f}%"
            else:
                Robs = (f0["ss"] - best["ss"]) / best["ss"]
                nfs = "not run"
            n = len(D)
            summ[(deg, i)] = (th, math.sqrt(best["ss"] / n))
            print(f"| sigma_{i} | {t0[0]:.3f}, {t0[1]:+.4f} | {math.sqrt(f0['ss'] / n):.4f} | {th[0]:.3f}, {th[1]:+.4f}, {th[2]:+.5f} | {math.sqrt(best['ss'] / n):.4f} | {Pof(213):.3f} / {Pof(228):.3f} / {Pof(237):.3f} | {Robs:.3f} | {nfs} |", flush=True)
    print("\n== hold-outs")
    for deg in (3, 2):
        print(f"\ntrend of degree {deg}")
        print("| series | hold-out | p2 chirp rms (max) | p2 = 0 chirp rms (max) | p1 = p2 = 0 rms (max) | p2 chirp: P0, p1, p2 | meets 0.014 |\n|---|---|---|---|---|---|---|")
        for i in (1, 2, 3, 4):
            ho = holdouts(D, Y[:, i - 1], deg, i)
            for tag, (row, ntr, nte) in ho.items():
                a, z, cst = row["p2 chirp"], row["p2 = 0 chirp"], row["p1 = p2 = 0"]
                th = a[2]
                print(f"| sigma_{i} | {tag[:2]} ({ntr} fit, {nte} predicted) | {a[0]:.4f} ({a[1]:.4f}) | {z[0]:.4f} ({z[1]:.4f}) | {cst[0]:.4f} ({cst[1]:.4f}) | {th[0]:.3f}, {th[1]:+.4f}, {th[2]:+.5f} | {'yes' if a[0] <= LIMIT else 'no'} |", flush=True)
    print(f"\n== prediction of the period over D 204 to 209.6 (centre D {CENTRE}), cubic trend, all 51 states")
    print("| series | p2 chirp | p2 = 0 chirp | p1 = p2 = 0 | bootstrap sd of the p2 chirp's value |\n|---|---|---|---|---|")
    F = Fitter(D, 3)
    for i in (1, 2, 3, 4):
        y = Y[:, i - 1]
        best, f0 = F.fit_free(y)
        cst = F.const(y)
        P = lambda th: th[0] + th[1] * (CENTRE - D0) + th[2] * (CENTRE - D0) ** 2
        beta, _ = lin(D, y, 3, best["theta"])
        truth = columns(D, 3, phase(D, *best["theta"])) @ beta
        rng = np.random.default_rng(90 + i)
        vals = []
        for _ in range(boot):
            bb, _ = F.fit_free(truth + rng.normal(0, math.sqrt(best["ss"] / len(D)), len(D)))
            vals.append(P(bb["theta"]))
        print(f"| sigma_{i} | {P(best['theta']):.3f} | {P(f0['theta']):.3f} | {cst['theta'][0]:.3f} | {np.std(vals):.3f} |", flush=True)
