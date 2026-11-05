# Candidate representations of Delta(D), each a fit routine fit_X(D, H, L, s, choice) -> (ev, info); info has Dinf,
# D3 (or None), and the fitted singularity data. The same routines serve the plants (planted.py) and the real data.
import numpy as np
from numpy.polynomial import chebyshev as Ch
from scipy.optimize import least_squares, minimize_scalar
import common as C

EPS_MAX = 0.5                                     # e = 1/n on D >= 4

# ---- E: rational in e = 1/n (pole-only family of the README formula), fitted on D >= 4 ----
def fit_eps_rat(D, H, L, s, pq):
    p, q = pq; sel = D >= 4.0 - 1e-12
    u = lambda DD: 2 * C.eps(DD) / EPS_MAX - 1
    c = C.rat_fit(u(D[sel]), H[sel], L[sel], s[sel], p, q)
    ev = lambda DD: C.rat_eval(c, u(DD), p, q)
    poles = C.qzeros(c, p, q); e_p = (poles + 1) * EPS_MAX / 2
    with np.errstate(divide='ignore'):
        Dp = 2 + 1 / e_p
    return ev, dict(Dinf=float(C.rat_eval(c, np.array([-1.0]), p, q)[0]),
                    D3=float(C.rat_eval(c, np.array([3.0]), p, q)[0]), poles_D=Dp, npar=p + q + 1)

# ---- Z: rational in the Joukowski zeta of the n-plane cut [ns, 1], ns free (joint Levenberg-Marquardt) ----
def _zrat_at(D, H, L, s, p, q, ns):
    u = 2 * C.zeta(D, ns) - 1; c = C.rat_fit(u, H, L, s, p, q)
    return c, float(np.sum((C.res(C.rat_eval(c, u, p, q), H, L) / s) ** 2))

def fit_zeta_rat(D, H, L, s, pq, ns0=-11.0, free=True):
    """ns free: bounded scalar minimisation of the inner rational fit's chi2 over ns in [-40, -3]."""
    p, q = pq
    if free:
        r = minimize_scalar(lambda ns: _zrat_at(D, H, L, s, p, q, ns)[1], bounds=(-40.0, -3.0), method='bounded',
                            options=dict(xatol=1e-2))
        ns = float(r.x)
    else:
        ns = ns0
    c, _ = _zrat_at(D, H, L, s, p, q, ns)
    ev = lambda DD: C.rat_eval(c, 2 * C.zeta(DD, ns) - 1, p, q)
    z_p = (C.qzeros(c, p, q) + 1) / 2                 # poles in zeta
    return ev, dict(Dinf=float(C.rat_eval(c, np.array([-1.0]), p, q)[0]), D3=float(C.rat_eval(c, np.array([1.0]), p, q)[0]),
                    ns=float(ns), Ds=float(ns + 2), poles_zeta=z_p, npar=p + q + 1 + int(free))

# ---- P: polynomial in zeta (equivalently a dispersion integral over [ns, 1] with a Chebyshev-U density) ----
def _zpoly(D, H, L, s, K, ns):
    t = C.zeta(D, ns); c = C.lin_fit(t, H, L, s, K, 0.0, 1.0)
    return c, float(np.sum((C.res(C.lin_eval(c, t, K, 0.0, 1.0), H, L) / s) ** 2))

def fit_zeta_poly(D, H, L, s, K, ns0=-11.0, free=False):
    if free:
        r = minimize_scalar(lambda ns: _zpoly(D, H, L, s, K, ns)[1], bounds=(-40.0, -3.0), method='bounded',
                            options=dict(xatol=1e-3))
        ns = float(r.x)
    else:
        ns = ns0
    c, _ = _zpoly(D, H, L, s, K, ns)
    ev = lambda DD: C.lin_eval(c, C.zeta(DD, ns), K, 0.0, 1.0)
    return ev, dict(Dinf=float(C.lin_eval(c, np.array([0.0]), K, 0.0, 1.0)[0]),
                    D3=float(C.lin_eval(c, np.array([1.0]), K, 0.0, 1.0)[0]), ns=ns, Ds=ns + 2, npar=K + 1 + int(free), coef=c)

# ---- N: polynomial in 1/n (the plain series, reference for the held-out diagnostic), D >= 10 ----
def fit_n_poly(D, H, L, s, K, dmin=10.0):
    sel = D >= dmin; t = C.eps(D[sel]); a, b = 0.0, 1 / (dmin - 2)
    c = C.lin_fit(t, H[sel], L[sel], s[sel], K, a, b)
    ev = lambda DD: C.lin_eval(c, C.eps(DD), K, a, b)
    return ev, dict(Dinf=float(C.lin_eval(c, np.array([0.0]), K, a, b)[0]), D3=None, npar=K + 1)

# ---- W: polynomial in w1(ns) (one square-root cut at ns, nothing at D = 3), D >= 10 ----
def fit_w1_poly(D, H, L, s, K, ns=-11.0, dmin=10.0):
    sel = D >= dmin; t = C.w1(D[sel], ns); a, b = float(C.w1(np.array([dmin]), ns)[0]), 0.0
    a, b = min(a, b), max(a, b)
    c = C.lin_fit(t, H[sel], L[sel], s[sel], K, a, b)
    ev = lambda DD: C.lin_eval(c, C.w1(DD, ns), K, a, b)
    return ev, dict(Dinf=float(C.lin_eval(c, np.array([0.0]), K, a, b)[0]), D3=None, ns=ns, npar=K + 1)

# ---- zeta polynomial plus D = 3 log columns (1 - zeta)^j ln(1 - zeta), j in logs ----
def fit_zeta_log(D, H, L, s, choice, ns=-11.0):
    K, logs = choice; t = C.zeta(D, ns)
    ex = lambda tt: [(1 - tt) ** j * np.log(1 - tt) for j in logs]
    c = C.lin_fit(t, H, L, s, K, 0.0, 1.0, extra=ex(t))
    ev = lambda DD: C.lin_eval(c, C.zeta(DD, ns), K, 0.0, 1.0, extra=ex(C.zeta(DD, ns)))
    return ev, dict(Dinf=float(ev(np.array([1e12]))[0]), D3=float(C.lin_eval(c[:K + 1], np.array([1.0]), K, 0.0, 1.0)[0]),
                    ns=ns, npar=K + 1 + len(logs), logcoef=c[K + 1:])

import arbfit as AF
def fit_zeta_poly_arb(D, H, L, s, K, ns0=-11.0, free=False): return AF.fit_zpoly(D, H, L, s, K, ns0=ns0, free=free)
def fit_zeta_rat_arb(D, H, L, s, pq, ns0=-11.0): return AF.fit_zrat(D, H, L, s, pq, ns0=ns0)
def fit_zeta_log_arb(D, H, L, s, choice, ns0=-11.0): return AF.fit_zpoly(D, H, L, s, choice[0], ns0=ns0, logs=choice[1])

DMIN = {fit_zeta_poly_arb: 0.0, fit_zeta_rat_arb: 0.0, fit_zeta_log_arb: 0.0, fit_eps_rat: 4.0, fit_zeta_rat: 0.0, fit_zeta_poly: 0.0, fit_n_poly: 10.0, fit_w1_poly: 10.0, fit_zeta_log: 0.0}

# ---- the held-out splits (frozen) ----
def splits(D):
    return {'full': np.ones(len(D), bool), 'H1': D <= 45.0, 'H2': D >= 3.1, 'H3': ~((D > 4.0 + 1e-9) & (D < 8.25 - 1e-9))}

def evaluate(fitfun, D, H, L, s, choice, thin=None, need=None, **kw):
    """Run one fit choice through the frozen splits, on the form's own domain D >= DMIN. Returns dict: full residual
    (max |r|/s, max |r| on D >= 8.25 and on D < 4.01, chi2/dof), Dinf, D3, singularity info (from the full fit), and
    held-out maxima: H1 on D > 45, H2 on D < 3.1, H3 on D = 5, 6, 8 and on the M48 thin points (thin = (D, value,
    err) or None). H2 needs a domain reaching below 3.1 and H3 one reaching D = 4."""
    dm = DMIN[fitfun]; dom = D >= dm - 1e-12; D, H, L, s = D[dom], H[dom], L[dom], s[dom]
    if need is None:
        need = ['full', 'H1'] + (['H2'] if dm < 3.1 else []) + (['H3'] if dm <= 4.0 else [])
    out = {}; sp = splits(D)
    for nm in need:
        m = sp[nm]
        try:
            ev, info = fitfun(D[m], H[m], L[m], s[m], choice, **kw)
        except Exception as e:                    # a fit that fails is recorded, not hidden
            out[nm] = dict(error=repr(e)); continue
        if nm == 'full':
            r = C.res(ev(D), H, L); lo = D < 4.01
            out['full'] = dict(maxrs=float(np.max(np.abs(r / s))), maxr_hi=float(np.max(np.abs(r[D >= 8.25]))),
                               maxr_lo=float(np.max(np.abs(r[lo]))) if lo.any() else None,
                               chi2dof=float(np.sum((r / s) ** 2) / max(1, len(D) - info['npar'])),
                               **{k: v for k, v in info.items() if k != 'coef'})
        else:
            h = ~m; r = C.res(ev(D[h]), H[h], L[h])
            d = dict(max=float(np.max(np.abs(r))), maxrs=float(np.max(np.abs(r / s[h]))), Dinf=info['Dinf'],
                     D3=info.get('D3'), ns=info.get('ns'))
            if nm == 'H3' and thin is not None:
                rt = C.res(ev(thin[0]), thin[1], np.zeros(len(thin[1]))); d['thin_max'] = float(np.max(np.abs(rt))); d['thin_maxrs'] = float(np.max(np.abs(rt / thin[2])))
            out[nm] = d
    return out
