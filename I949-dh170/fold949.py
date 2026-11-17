#!/usr/bin/env python3
"""#949: the fold fit of sigma_Delta(D) and its planted test.

    fold949.py --selftest [--mutate]        planted series with known D*; exit 1 if any check fails (--mutate must fail)
    fold949.py --noise                      Monte Carlo: the error of D* at 1e-3 relative noise on sigma, by distance D* - D_last
    fold949.py fit D1:SIGMA1 D2:SIGMA2 ...  fit the given (D, sigma_Delta) pairs (the last five are used)

Model of the issue: sigma_Delta^2 = c (D* - D) (a fold makes sigma vanish as sqrt(D* - D)). The chain's sigma_Delta also falls as
a pure exponential (log slope 0.405 at order 240, #941), so the series is sigma^2 = c (D* - D) exp(-2 s (D - D_last)), and the
fit has three parameters, c, D* and s, on the last five states of one leg (one ks):

  A  s fixed at 0: the issue's literal linear fit of sigma^2 on D. It cannot return D* of a series with the exponential in it
     (a planted control below shows it), so it is printed beside B and never used for a claim.
  B  s free: for each D* ln sigma^2 - ln(D* - D) is a straight line in D (ordinary least squares gives ln c and s), and D* is
     the minimum of the sum of squares over a log-spaced scan of D* - D_last in [0.01, 1e5], refined by Brent. A minimum at
     the end of the scan is reported as "no interior minimum" (no fold: the series is a pure exponential to the fit).
  C  s fixed from outside (the baseline slope of the leg's earlier states): A on sigma^2 exp(2 s (D - D_last)).

Residuals are relative: (sigma^2 - fit) / sigma^2 over the five states. The fit is valid when every |residual| <= 0.10 and D* is
past the last state (the issue's rule). Planted truth: sigma^2 = 0.3 (D* - D) exp(-2 s (D - 232)) with D* 260 and 262, s 0.405,
on the five #941 states and two other grids, must give D* within 0.05 of the planted one."""
import math
import sys

import numpy as np
from scipy.optimize import minimize_scalar

P = 1.0                 # sigma^2 ~ (D* - D)^P; --mutate sets 2 (a wrong fold law) and the planted check must fail
U_LO, U_HI = 0.01, 1e5  # scan of D* - D_last


def _ols(D, z):
    X = np.column_stack([np.ones_like(D), D])
    beta = np.linalg.lstsq(X, z, rcond=None)[0]
    return beta, float(np.sum((z - X @ beta) ** 2))


def fit_A(D, s2):
    """s fixed at 0: sigma^2 = c (D* - D), least squares on the relative error"""
    D, y = np.asarray(D, float), np.asarray(s2, float)
    w = 1 / y
    (a, b) = np.linalg.lstsq(np.column_stack([np.ones_like(D), D]) * w[:, None], y * w, rcond=None)[0]
    res = (y - (a + b * D)) / y
    return dict(model="A", Dstar=(-a / b if b != 0 else math.inf), c=-b, s=0.0, res=res, interior=b < 0)


def fit_C(D, s2, s):
    """s fixed: A on sigma^2 exp(2 s (D - D_last))"""
    D, y = np.asarray(D, float), np.asarray(s2, float)
    r = fit_A(D, y * np.exp(2 * s * (D - D[-1])))
    return dict(r, model="C", s=s, c=r["c"] * 1.0)


def fit_B(D, s2):
    """s free (module docstring)"""
    D, y = np.asarray(D, float), np.asarray(s2, float)
    Dl = D[-1]

    def ssr(x):
        u = math.exp(x)
        z = np.log(y) - P * np.log(u + Dl - D)
        return _ols(D - Dl, z)

    xs = np.linspace(math.log(U_LO), math.log(U_HI), 600)
    v = [ssr(x)[1] for x in xs]
    i = int(np.argmin(v))
    if i in (0, len(xs) - 1):
        beta, _ = ssr(xs[i])
        return dict(model="B", Dstar=math.inf if i else Dl + U_LO, c=math.exp(beta[0]), s=-beta[1] / 2,
                    res=np.full(len(D), np.nan), interior=False)
    x = minimize_scalar(lambda t: ssr(t)[1], bracket=(xs[i - 1], xs[i], xs[i + 1]), tol=1e-14).x
    beta, _ = ssr(x)
    u = math.exp(x)
    fit = math.exp(beta[0]) * (u + Dl - D) ** P * np.exp(beta[1] * (D - Dl))
    return dict(model="B", Dstar=Dl + u, c=math.exp(beta[0]), s=-beta[1] / 2, res=(y - fit) / y, interior=True)


def valid(r, D):
    return bool(r["interior"] and np.all(np.abs(r["res"]) <= 0.10) and r["Dstar"] > D[-1])


def planted(Dstar, s, D, c=0.3, noise=0.0, rng=None):
    D = np.asarray(D, float)
    y = c * (Dstar - D) * np.exp(-2 * s * (D - 232.0))   # the fold law is planted as 1, whatever P the fit uses
    if noise:
        y = y * np.exp(2 * noise * rng.standard_normal(len(D)))
    return D, y


GRIDS = {"941": [229.0509, 229.9822, 230.9281, 231.7466, 232.0], "leg8": [233.0, 234.0, 235.0, 236.0, 237.0],
         "wide": [232.0, 234.0, 236.0, 238.0, 240.0]}


def selftest():
    ok = True
    s = 0.405
    for Dstar in (260.0, 262.0):
        for name, g in GRIDS.items():
            D, y = planted(Dstar, s, g)
            b = fit_B(D, y)
            c = fit_C(D, y, s)
            a = fit_A(D, y)
            good = abs(b["Dstar"] - Dstar) <= 0.05 and abs(c["Dstar"] - Dstar) <= 0.05 and valid(b, D) and valid(c, D)
            # the literal fit (s = 0) is the control: it must miss, so the planted series does test the exponential
            miss = not (abs(a["Dstar"] - Dstar) <= 0.05)
            ok &= good and miss
            print(f"planted D* {Dstar:g}, grid {name:<5}: B D* {b['Dstar']:.4f} (c {b['c']:.4f}, s {b['s']:.4f}, max |res| "
                  f"{np.abs(b['res']).max():.1e}), C D* {c['Dstar']:.4f}, A (s=0) D* {a['Dstar']:.2f} max |res| "
                  f"{np.abs(a['res']).max():.2f}: {'pass' if good else 'FAIL'}, control A misses: {'yes' if miss else 'NO'}")
    # no fold: a pure exponential must not give an interior D*
    D = np.asarray(GRIDS["wide"])
    b = fit_B(D, np.exp(-2 * s * (D - 232.0)))
    nofold = not valid(b, D)
    ok &= nofold
    print(f"pure exponential, no fold: B interior {b['interior']}, D* {b['Dstar']}: {'pass (no fold claimed)' if nofold else 'FAIL'}")
    # the fit must see a fold when the series has one and the exponential is not there (s = 0): the issue's plain case
    D, y = planted(260.0, 0.0, GRIDS["leg8"])
    a, b = fit_A(D, y), fit_B(D, y)
    pure = abs(a["Dstar"] - 260) <= 0.05 and abs(b["Dstar"] - 260) <= 0.05
    ok &= pure
    print(f"pure fold (s = 0): A D* {a['Dstar']:.4f}, B D* {b['Dstar']:.4f}: {'pass' if pure else 'FAIL'}")
    print(f"selftest{' --mutate' if P != 1.0 else ''}: {'pass' if ok else 'FAIL'}")
    return ok


def noise_table(noise=1e-3, n=400):
    """the error of B's D* at relative noise 1e-3 on sigma (the convergence level of near_null.py), by D* - D_last, on five
    states 1 unit apart and on five states 2 units apart"""
    rng = np.random.default_rng(949)
    print(f"B's D* at {noise:g} relative noise on sigma_Delta (planted s 0.405, D* 260), {n} draws:")
    print("  spacing  D*-D_last  returned (valid)  median |D*-260|  16-84% of D*          no interior min")
    for h in (1.0, 2.0):
        for dist in (28.0, 18.0, 10.0, 5.0, 3.0, 1.5):
            Dl = 260.0 - dist
            D = Dl - h * np.arange(4, -1, -1)
            got, nb = [], 0
            for _ in range(n):
                _, y = planted(260.0, 0.405, D, noise=noise, rng=rng)
                b = fit_B(D, y)
                if b["interior"]:
                    got.append(b["Dstar"])
                else:
                    nb += 1
            got = np.array(got) if got else np.array([np.nan])
            q = np.nanpercentile(got, [16, 50, 84])
            print(f"  {h:<7g}  {dist:<9g}  {len(got):>4}/{n}           {np.nanmedian(np.abs(got - 260)):<14.3g}  "
                  f"{q[0]:.1f} {q[1]:.1f} {q[2]:.1f}      {nb}")


def main():
    global P
    if "--mutate" in sys.argv:
        P = 2.0
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    if "--noise" in sys.argv:
        noise_table()
        return
    if sys.argv[1] == "fit":
        pts = [tuple(float(x) for x in a.split(":")) for a in sys.argv[2:]][-5:]
        D = np.array([p[0] for p in pts])
        s2 = np.array([p[1] ** 2 for p in pts])
        for r in (fit_A(D, s2), fit_B(D, s2)):
            print(r["model"], "D*", r["Dstar"], "c", r["c"], "s", r["s"], "valid", valid(r, D), "res", np.round(r["res"], 4))
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
