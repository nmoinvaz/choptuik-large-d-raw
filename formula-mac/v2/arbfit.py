# 256-bit (python-flint arb) versions of the whole-range zeta fits. float64 is not adequate there: the weighted
# design has cond 1e11-1e14 and the float64 basis itself carries 1e-16 errors that the 1/sigma = 1e15 weights turn
# into chi2 ~ 1e3 (cond_probe.py). Data in: D (float64, exact), y = hi + lo, sigma. Models return (hi, lo) floats.
import numpy as np
from flint import arb, arb_mat, ctx
from scipy.optimize import minimize_scalar
ctx.prec = 256

def A(x): return arb(float(x))
def split(v):
    hi = float(v); return hi, float(v - arb(hi))

def zeta_arb(D, ns):
    ns = A(ns); out = []
    for d in np.atleast_1d(D):
        n = A(d) - 2; u = (2 * n - (1 + ns)) / (1 - ns); out.append(u - (u * u - 1).sqrt())
    return out

def cheb(u, K):
    T = [arb(1), u]
    for _ in range(K - 1): T.append(2 * u * T[-1] - T[-2])
    return T[:K + 1]

def mid(v): return arb(v.mid())

def msolve(N, g):
    """Solve with midpoints (radii dropped: arb cannot certify cond^2 ~ 1e28 systems, but 256 bits carry them)."""
    Nm = arb_mat([[mid(N[i, j]) for j in range(N.ncols())] for i in range(N.nrows())])
    gm = arb_mat([[mid(g[i, 0])] for i in range(g.nrows())])
    return Nm.solve(gm, nonstop=True) if False else Nm.solve(gm)

def ls(rows, b):
    """Weighted rows (lists of arb) and right side (arb): normal equations at 256 bits. Returns coefficient list."""
    W = arb_mat(rows); B = arb_mat([[v] for v in b]); Wt = W.transpose()
    c = msolve(Wt * W, Wt * B)
    return [mid(c[i, 0]) for i in range(c.nrows())]

def yarb(H, L): return [A(h) + A(l) for h, l in zip(H, L)]

def chi2_of(vals, y, s):
    return float(sum((((v - yy) / A(si)) ** 2 for v, yy, si in zip(vals, y, s)), arb(0)))

def tolist(vals):
    hl = [split(v) for v in vals]; return np.array([a for a, _ in hl]), np.array([b for _, b in hl])

# ---- zeta polynomial (+ optional D = 3 log columns (1 - zeta)^j ln(1 - zeta)) ----
def _zp_basis(z, K, logs):
    out = []
    for zz in z:
        row = cheb(2 * zz - 1, K)
        if logs:
            w = 1 - zz; lw = w.log()
            for j in logs:
                p = arb(1)
                for _ in range(j): p = p * w          # products, not powers (python-flint 0.9 pitfall)
                row.append(p * lw)
        out.append(row)
    return out

def zpoly_at(D, H, L, s, K, ns, logs=()):
    z = zeta_arb(D, ns); Bz = _zp_basis(z, K, logs); y = yarb(H, L)
    rows = [[v / A(si) for v in r] for r, si in zip(Bz, s)]; b = [yy / A(si) for yy, si in zip(y, s)]
    c = ls(rows, b)
    vals = [sum((ci * v for ci, v in zip(c, r)), arb(0)) for r in Bz]
    return c, chi2_of(vals, y, s)

def zpoly_eval(c, D, K, ns, logs=()):
    z = zeta_arb(D, ns); Bz = _zp_basis(z, K, logs)
    return tolist([sum((ci * v for ci, v in zip(c, r)), arb(0)) for r in Bz])

def fit_zpoly(D, H, L, s, K, ns0=-11.0, free=False, logs=()):
    if free:
        r = minimize_scalar(lambda ns: zpoly_at(D, H, L, s, K, ns, logs)[1], bounds=(-40.0, -3.0), method='bounded',
                            options=dict(xatol=1e-2))
        ns = float(r.x)
    else:
        ns = ns0
    c, _ = zpoly_at(D, H, L, s, K, ns, logs)
    ev = lambda DD: zpoly_eval(c, DD, K, ns, logs)
    Dinf = sum((ci * (1 if k % 2 == 0 else -1) for k, ci in enumerate(c[:K + 1])), arb(0))
    D3 = sum(c[:K + 1], arb(0))                          # log columns vanish at zeta = 1
    return ev, dict(Dinf=float(Dinf), D3=float(D3), ns=ns, Ds=ns + 2, npar=K + 1 + len(logs) + int(free),
                    logcoef=[float(v) for v in c[K + 1:]], coef=c)

# ---- zeta rational P_p(u)/Q_q(u), u = 2 zeta - 1, Q = 1 + sum_{j>=1} q_j T_j: SK iterations then damped GN ----
def zrat_at(D, H, L, s, p, q, ns, it_sk=8, it_gn=6):
    z = zeta_arb(D, ns); m = max(p, q); T = [cheb(2 * zz - 1, m) for zz in z]; y = yarb(H, L); sA = [A(si) for si in s]
    Qp = [arb(1)] * len(z)
    for _ in range(it_sk):
        rows = [[T[i][j] / (sA[i] * Qp[i]) for j in range(p + 1)] + [-y[i] * T[i][j] / (sA[i] * Qp[i]) for j in range(1, q + 1)]
                for i in range(len(z))]
        c = ls(rows, [y[i] / (sA[i] * Qp[i]) for i in range(len(z))])
        Qp = [mid(1 + sum((c[p + j] * T[i][j] for j in range(1, q + 1)), arb(0))) for i in range(len(z))]
    def vals(c):
        P = [sum((c[j] * T[i][j] for j in range(p + 1)), arb(0)) for i in range(len(z))]
        Q = [1 + sum((c[p + j] * T[i][j] for j in range(1, q + 1)), arb(0)) for i in range(len(z))]
        return P, Q
    lam = 1e-6; P, Q = vals(c); chi = chi2_of([a / b for a, b in zip(P, Q)], y, s)
    for _ in range(it_gn):
        r = [(P[i] / Q[i] - y[i]) / sA[i] for i in range(len(z))]
        J = [[T[i][j] / (Q[i] * sA[i]) for j in range(p + 1)] + [-P[i] * T[i][j] / (Q[i] * Q[i] * sA[i]) for j in range(1, q + 1)]
             for i in range(len(z))]
        Jm = arb_mat(J); Jt = Jm.transpose(); N = Jt * Jm; g = Jt * arb_mat([[v] for v in r])
        for k in range(N.nrows()): N[k, k] = N[k, k] * (1 + lam)
        dc = msolve(N, g); cn = [mid(c[k] - dc[k, 0]) for k in range(len(c))]
        Pn, Qn = vals(cn); chin = chi2_of([a / b for a, b in zip(Pn, Qn)], y, s)
        if chin < chi: c, P, Q, chi, lam = cn, Pn, Qn, chin, lam / 10
        else: lam *= 100
    return c, chi

def zrat_eval(c, D, p, q, ns):
    z = zeta_arb(D, ns); out = []
    for zz in z:
        T = cheb(2 * zz - 1, max(p, q))
        out.append(sum((c[j] * T[j] for j in range(p + 1)), arb(0)) / (1 + sum((c[p + j] * T[j] for j in range(1, q + 1)), arb(0))))
    return tolist(out)

def fit_zrat(D, H, L, s, pq, ns0=-11.0, free=False):
    p, q = pq
    if free:
        r = minimize_scalar(lambda ns: zrat_at(D, H, L, s, p, q, ns, it_sk=6, it_gn=3)[1], bounds=(-30.0, -4.0),
                            method='bounded', options=dict(xatol=5e-2))
        ns = float(r.x)
    else:
        ns = ns0
    c, _ = zrat_at(D, H, L, s, p, q, ns)
    ev = lambda DD: zrat_eval(c, DD, p, q, ns)
    one = lambda u: float(sum((c[j] * cheb(arb(u), max(p, q))[j] for j in range(p + 1)), arb(0))
                          / (1 + sum((c[p + j] * cheb(arb(u), max(p, q))[j] for j in range(1, q + 1)), arb(0))))
    qc = np.array([1.0] + [float(c[p + j]) for j in range(1, q + 1)])
    zp = (np.polynomial.chebyshev.chebroots(qc) + 1) / 2 if q else np.array([])
    return ev, dict(Dinf=one(-1), D3=one(1), ns=ns, Ds=ns + 2, npar=p + q + 1 + int(free), poles_zeta=zp)
