"""experiment: forms S_K (fold Puiseux, D* free) and W (Re A e^{kappa (D - 250)}) on plants over the real grid"""
import json, math, sys
import numpy as np
from scipy.optimize import minimize, minimize_scalar

d = json.load(open(sys.argv[1]))
DSTAR = 259.9033

def fit_S(D, y, K, Dtop, sig):
    def solve(Ds):
        u = np.sqrt(Ds - D)
        A = np.vstack([u ** k for k in range(K + 1)]).T
        c, *_ = np.linalg.lstsq(A / sig[:, None], y / sig, rcond=None)
        return c, (y - A @ c) / sig
    grid = Dtop + np.geomspace(1e-4, 2.0, 400)
    r = [np.sqrt(np.mean(solve(g)[1] ** 2)) for g in grid]
    i = int(np.argmin(r))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    m = minimize_scalar(lambda g: np.sqrt(np.mean(solve(g)[1] ** 2)), bounds=(lo, hi), method="bounded",
                        options=dict(xatol=1e-10))
    c, res = solve(m.x)
    return dict(Dstar=m.x, c=c, res=res)

def fit_W(D, y, sig):
    x = D - 250.0
    def solve(p):
        b, w = p
        A = np.vstack([np.exp(b * x) * np.cos(w * x), np.exp(b * x) * np.sin(w * x)]).T
        c, *_ = np.linalg.lstsq(A / sig[:, None], y / sig, rcond=None)
        return c, (y - A @ c) / sig
    best = None
    for b in np.linspace(0.0, 5.0, 51):
        for w in np.linspace(0.05, 5.0, 100):
            r = np.sqrt(np.mean(solve((b, w))[1] ** 2))
            if best is None or r < best[0]:
                best = (r, b, w)
    m = minimize(lambda p: np.log(np.sqrt(np.mean(solve(p)[1] ** 2))), [best[1], best[2]], method="Nelder-Mead",
                 options=dict(xatol=1e-12, fatol=1e-14, maxiter=20000))
    c, res = solve(m.x)
    return dict(beta=m.x[0], omega=m.x[1], c=c, res=res)

def plants(D, sig, seed=815):
    rng = np.random.default_rng(seed)
    u = np.sqrt(DSTAR - D)
    PS = 1e-4 * (1 - 2 * u + 0.5 * u ** 2)
    # #807's W with lam_g's law constant: K = 3e-39/p_min(250), kappa = b + 2 pi i/5.3, zero at 250.3
    R = [o for o in d if 245.6 <= o["D"] <= 255.8]
    x = np.array([o["D"] for o in R]); lp = np.log([o["p_min"] for o in R])
    pf = np.polyfit(x, lp, 1); b = -pf[0]; p250 = math.exp(np.polyval(pf, 250.0))
    K = 3e-39 / p250
    kap = complex(b, 2 * math.pi / 5.3)
    ph = math.pi / 2 - kap.imag * 0.3
    PW = np.real(K * np.exp(1j * ph) * np.exp(kap * (D - 250)))
    n = sig * rng.standard_normal(len(D))
    return dict(S=PS + n, W=PW + n), dict(b=b, omega=kap.imag)

for lo in (258.0, 248.0):
    w = [o for o in d if o["D"] >= lo]
    D = np.array([o["D"] for o in w]); sig = np.array([o["spread"] for o in w])
    P, truth = plants(D, sig)
    n = sig * np.random.default_rng(815).standard_normal(len(D))
    PS, PW = P["S"] - n, P["W"] - n
    cases = dict(S=PS + n, W=PW + n, S_moved=None, noisy_S=PS + 1e4 * n, noisy_W=PW + 1e4 * n)
    u = np.sqrt(DSTAR + 0.5 - D); cases["S_moved"] = 1e-4 * (1 - 2 * u + 0.5 * u ** 2) + n
    for a in (1.0, 0.1, 0.01, 0.001):
        cases[f"S+{a}W"] = PS + a * PW / np.max(np.abs(PW)) * np.max(np.abs(PS)) + n
        cases[f"W+{a}S"] = PW + a * PS / np.max(np.abs(PS)) * np.max(np.abs(PW)) + n
    print(f"window {lo}-259.74, {len(D)} states")
    for name, y in cases.items():
        f = fit_S(D, y, 3, D.max(), sig); g = fit_W(D, y, sig)
        print(f"  {name:10s} S_3: r {np.max(np.abs(f['res'])):.1e} D* {f['Dstar']:.5f} a1 {f['c'][1]:+.4e} | W: r {np.max(np.abs(g['res'])):.1e} beta {g['beta']:.5f} omega {g['omega']:.5f}")
