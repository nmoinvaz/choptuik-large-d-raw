"""experiment 3: forms S_3, W, C = W + S_3 and C_even = W + linear, weighted, on plants over the real grid"""
import json, math, sys
import numpy as np
from scipy.optimize import minimize

d = json.load(open(sys.argv[1]))
DSTAR = 259.9033

def lin(cols, y, sig):
    A = np.vstack(cols).T
    c, *_ = np.linalg.lstsq(A / sig[:, None], y / sig, rcond=None)
    return c, (y - A @ c) / sig

def wcols(D, b, w):
    x = D - 250.0
    return [np.exp(b * x) * np.cos(w * x), np.exp(b * x) * np.sin(w * x)]

def scols(D, Ds, K=3):
    u = np.sqrt(Ds - D)
    return [u ** k for k in range(K + 1)]

def best_of(f, starts, bounds_ok):
    best = None
    for p0 in starts:
        m = minimize(lambda p: f(p) if bounds_ok(p) else 1e300, p0, method="Nelder-Mead",
                     options=dict(xatol=1e-12, fatol=1e-12, maxiter=40000, maxfev=40000))
        if best is None or m.fun < best.fun:
            best = m
    return best

def rmax(res):
    return float(np.max(np.abs(res)))

def form(D, y, sig, name):
    top = D.max()
    lr = lambda res: math.log(float(np.sqrt(np.mean(res ** 2))))
    if name == "S":
        f = lambda p: lr(lin(scols(D, p[0]), y, sig)[1])
        g = np.linspace(top + 1e-3, top + 2, 200)
        st = [[g[i]] for i in np.argsort([f([x]) for x in g])[:3]]
        m = best_of(f, st, lambda p: p[0] > top)
        c, res = lin(scols(D, m.x[0]), y, sig)
        return dict(r=rmax(res), Dstar=m.x[0], a1=c[1])
    if name in ("W", "Ce"):
        extra = (lambda: [np.ones_like(D), D - 259.0]) if name == "Ce" else (lambda: [])
        f = lambda p: lr(lin(wcols(D, *p) + extra(), y, sig)[1])
        G = [(b, w) for b in np.linspace(0, 5, 26) for w in np.linspace(0.05, 5, 50)]
        st = [list(G[i]) for i in np.argsort([f(p) for p in G])[:4]]
        m = best_of(f, st, lambda p: True)
        c, res = lin(wcols(D, *m.x) + extra(), y, sig)
        return dict(r=rmax(res), beta=m.x[0], omega=abs(m.x[1]))
    if name == "C":
        f = lambda p: lr(lin(wcols(D, p[0], p[1]) + scols(D, p[2]), y, sig)[1])
        G = [(b, w, s) for b in np.linspace(0, 5, 11) for w in np.linspace(0.1, 5, 21) for s in top + np.geomspace(1e-3, 2, 12)]
        st = [list(G[i]) for i in np.argsort([f(p) for p in G])[:6]]
        m = best_of(f, st, lambda p: p[2] > top)
        c, res = lin(wcols(D, m.x[0], m.x[1]) + scols(D, m.x[2]), y, sig)
        return dict(r=rmax(res), beta=m.x[0], omega=abs(m.x[1]), Dstar=m.x[2], a1=c[3])

def plants(D, sig):
    rng = np.random.default_rng(815)
    n = sig * rng.standard_normal(len(D))
    u = np.sqrt(DSTAR - D)
    PS = 1e-4 * (1 - 2 * u + 0.5 * u ** 2)
    R = [o for o in d if 245.6 <= o["D"] <= 255.8]
    x = np.array([o["D"] for o in R]); lp = np.log([o["p_min"] for o in R])
    pf = np.polyfit(x, lp, 1); b = -pf[0]; p250 = math.exp(np.polyval(pf, 250.0))
    kap = complex(b, 2 * math.pi / 5.3); ph = math.pi / 2 - kap.imag * 0.3
    PW = np.real(3e-39 / p250 * np.exp(1j * ph) * np.exp(kap * (D - 250)))
    # a chirp: the period lengthening from 5.3 at 250 by 10% per 5 in D (reported only)
    om = 2 * math.pi / (5.3 * (1 + 0.02 * (D - 250)))
    PWc = 3e-39 / p250 * np.exp(b * (D - 250)) * np.cos(np.cumsum(np.r_[0, np.diff(D) * (om[1:] + om[:-1]) / 2]) + om[0] * (D[0] - 250) + ph)
    sc = lambda v, ref: v / np.max(np.abs(v)) * np.max(np.abs(ref))
    u5 = np.sqrt(DSTAR + 0.5 - D)
    return dict(S=PS + n, W=PW + n, M=PS + sc(PW, PS) + n, M10=PS + 0.1 * sc(PW, PS) + n,
                S_moved=1e-4 * (1 - 2 * u5 + 0.5 * u5 ** 2) + n, Wchirp=sc(PWc, PW) + n, S_noisy=PS + 1e4 * n), b

for lo in (258.0, 248.0):
    w = [o for o in d if o["D"] >= lo]
    D = np.array([o["D"] for o in w]); sig = np.array([o["spread"] for o in w])
    P, b = plants(D, sig)
    print(f"window {lo}-259.74, {len(D)} states (plant b {b:.4f}, omega {2*math.pi/5.3:.4f}, D* {DSTAR})")
    for name, y in P.items():
        out = {k: form(D, y, sig, k) for k in ("S", "W", "C", "Ce")}
        print(f"  {name:8s} r: S {out['S']['r']:.1e}  W {out['W']['r']:.1e}  C {out['C']['r']:.1e}  C_even {out['Ce']['r']:.1e} | "
              f"ratios C_even/C {out['Ce']['r']/out['C']['r']:.1e}  S/C {out['S']['r']/out['C']['r']:.1e} | "
              f"C: D* {out['C']['Dstar']:.5f} beta {out['C']['beta']:.4f} omega {out['C']['omega']:.4f} a1 {out['C']['a1']:+.3e}")
