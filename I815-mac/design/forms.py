"""experiment: forms S_K (fold Puiseux, D* free) and W (Re A e^{kappa (D - 250)}) on plants over the real grid"""
import json, math, sys
import numpy as np
from scipy.optimize import minimize, minimize_scalar

d = json.load(open(sys.argv[1]))
DSTAR = 259.9033

def fit_S(D, y, K, Dtop):
    def solve(Ds):
        u = np.sqrt(Ds - D)
        A = np.vstack([u ** k for k in range(K + 1)]).T
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        return c, y - A @ c
    grid = Dtop + np.geomspace(1e-4, 2.0, 400)
    r = [np.sqrt(np.mean(solve(g)[1] ** 2)) for g in grid]
    i = int(np.argmin(r))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    m = minimize_scalar(lambda g: np.sqrt(np.mean(solve(g)[1] ** 2)), bounds=(lo, hi), method="bounded",
                        options=dict(xatol=1e-10))
    c, res = solve(m.x)
    return dict(Dstar=m.x, c=c, res=res)

def fit_W(D, y):
    x = D - 250.0
    def solve(p):
        b, w = p
        A = np.vstack([np.exp(b * x) * np.cos(w * x), np.exp(b * x) * np.sin(w * x)]).T
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        return c, y - A @ c
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

for lo in (258.0, 257.0, 256.0, 254.0, 252.0, 250.0, 248.0):
    w = [o for o in d if o["D"] >= lo]
    D = np.array([o["D"] for o in w]); sig = np.array([o["spread"] for o in w])
    P, truth = plants(D, sig)
    print(f"window {lo}-259.74, {len(D)} states, sigma max {sig.max():.1e}; W plant b {truth['b']:.4f} omega {truth['omega']:.4f}")
    for name, y in P.items():
        sc = np.max(np.abs(y))
        for K in (2, 3, 4, 5):
            f = fit_S(D, y, K, D.max())
            print(f"  plant {name}: S_{K}: D* {f['Dstar']:.5f} max|res|/max|y| {np.max(np.abs(f['res']))/sc:.1e}  max|res|/sigma {np.max(np.abs(f['res'])/sig):.1e}")
        f = fit_W(D, y)
        print(f"  plant {name}: W  : beta {f['beta']:.5f} omega {f['omega']:.5f} max|res|/max|y| {np.max(np.abs(f['res']))/sc:.1e}  max|res|/sigma {np.max(np.abs(f['res'])/sig):.1e}")
