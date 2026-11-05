# Shared pieces for formula/v2: data (cleaned once, the same grid for plants and real data), variable maps, weighted
# linear (Chebyshev) and rational least squares. Values are kept as hi + lo; residuals are (model - hi) - lo.
import csv, sys, numpy as np
from numpy.polynomial import chebyshev as Ch
from scipy.optimize import least_squares
sys.path.insert(0, '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/formula')
from data import load as load0           # noqa: E402  (previous agent's loader, read and kept)
R = '/Users/nathan/Source/choptuik-large-d/hp/data/'
DINF = 1.643893746                       # README value, for display only

def load_hl():
    """Same rows as data.load, but values as (hi, lo) pairs."""
    D, y, s, run = load0()
    hi = {}; lo = {}
    for r in csv.DictReader(open(R + 'delta_dd.csv')):
        if 'unresolved' in r['run']: continue
        k = round(float(r['D']), 6); hi[k] = float(r['Delta_hi']); lo[k] = float(r['Delta_lo'])
    for r in csv.DictReader(open(R + 'delta_dd_lowD.csv')):
        if r['best'] == '1' and r['resolved'] == '1':
            k = round(float(r['D']), 6)
            if k not in hi: hi[k] = float(r['Delta_hi']); lo[k] = float(r['Delta_lo'])
    H = np.array([hi[d] for d in D]); L = np.array([lo[d] for d in D])
    assert np.allclose(H + L, y, rtol=0, atol=1e-15)
    return D, H, L, s, run

def thin_m48():
    """The unresolved M = 48 rows 4.25-8.2 (not in the fits): value and an error estimate, the M48 -> 64 change
    interpolated in log10 against D from the four D where it is measured (4: 2.6e-7, 5: 8.7e-12, 6: 3.0e-14,
    8: 9.5e-21)."""
    kD = np.array([4.0, 5.0, 6.0, 8.0]); kE = np.log10([2.6e-7, 8.7e-12, 3.0e-14, 9.5e-21])
    out = []
    for r in csv.DictReader(open(R + 'delta_dd_lowD.csv')):
        d = float(r['D'])
        if r['M'] == '48' and r['resolved'] == '0' and 4.0 < d < 8.25 and d not in (5.0, 6.0, 8.0):
            e = 10 ** np.interp(d, kD, kE); out.append((d, float(r['Delta_hi']) + float(r['Delta_lo']), max(e, 1e-15)))
    a = np.array(out); return a[:, 0], a[:, 1], a[:, 2]

def zeta(D, ns):
    """Joukowski variable of the n-plane cut [ns, 1] (n = D - 2): 0 at D = inf, 1 at D = 3, -1 at D = ns + 2."""
    n = np.asarray(D, float) - 2.0; u = (2 * n - (1 + ns)) / (1 - ns)
    return u - np.sqrt(u * u - 1)

def w1(D, ns):
    """One cut, e <= 1/ns (e = 1/n), onto the disc; 0 at D = inf."""
    q = np.sqrt(1 - ns / (np.asarray(D, float) - 2)); return (q - 1) / (q + 1)

eps = lambda D: 1.0 / (np.asarray(D, float) - 2.0)

def clean_grid(D, y, s, thr=1e-15, dmin=10.0):
    """Drop D >= dmin points whose residual from a smooth fit sits > thr off the median of its four neighbours (the
    rule of hp/dd_fits_mp.clean; here a degree-18 Chebyshev fit in 1/D of the D >= dmin points only, unweighted)."""
    m = D >= dmin; t = 1 / D[m]; a, b = t.min(), t.max(); V = Ch.chebvander((2 * t - a - b) / (b - a), 18)
    c, *_ = np.linalg.lstsq(V, y[m], rcond=None); r = V @ c - y[m]
    keep = np.ones(len(D), bool); idx = np.where(m)[0]
    for j, i in enumerate(idx):
        nb = np.r_[r[max(0, j - 2):j], r[j + 1:j + 3]]
        if abs(r[j] - np.median(nb)) > thr: keep[i] = False
    return keep

def data(clean=True):
    """All points; with clean, the 27 points hp/dd_fits_mp.clean drops (60 digits, D >= 10; cached by mkclean.py)."""
    D, H, L, s, run = load_hl()
    if clean:
        import json, os
        drop = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clean_drop.json')))['drop'])
        k = np.array([round(d, 6) not in drop for d in D]); D, H, L, s = D[k], H[k], L[k], s[k]
        run = [r for r, kk in zip(run, k) if kk]
    return D, H, L, s, run

# ---- linear: polynomial (Chebyshev) in a variable t on a fixed interval [a, b], weighted by 1/sigma ----
def lin_fit(t, H, L, s, K, a, b, extra=None):
    """extra: list of functions of the row index set -> extra columns (already evaluated arrays aligned with t)."""
    u = (2 * t - a - b) / (b - a); V = Ch.chebvander(u, K)
    if extra is not None: V = np.hstack([V, np.column_stack(extra)])
    W = V / s[:, None]
    c, *_ = np.linalg.lstsq(W, H / s, rcond=None)
    c2, *_ = np.linalg.lstsq(W, (H - V @ c + L) / s, rcond=None)        # one refinement step on the hi + lo residual
    return c + c2

def lin_eval(c, t, K, a, b, extra=None):
    u = (2 * np.asarray(t, float) - a - b) / (b - a); V = Ch.chebvander(u, K)
    if extra is not None: V = np.hstack([V, np.column_stack(extra)])
    return V @ c

def res(model_vals, H, L):
    if isinstance(model_vals, tuple):                # (hi, lo) from the arb fits
        return (model_vals[0] - H) + (model_vals[1] - L)
    return (model_vals - H) - L

# ---- rational P_p(u)/Q_q(u) in a Chebyshev variable u, Q = 1 + sum_{j>=1} q_j T_j(u) ----
def rat_eval(c, u, p, q):
    P = Ch.chebval(u, c[:p + 1]); Q = Ch.chebval(u, np.r_[1.0, c[p + 1:]]) if q else 1.0
    return P / Q

def rat_fit(u, H, L, s, p, q, iters=8, c0=None):
    """Sanathanan-Koerner iterations from the linearised problem, then Levenberg-Marquardt on (P/Q - y)/sigma."""
    y = H + L
    Vp = Ch.chebvander(u, p); Vq = Ch.chebvander(u, q)[:, 1:] if q else np.zeros((len(u), 0))
    Qprev = np.ones(len(u)); c = c0
    if c is None:
        for _ in range(iters):
            A = np.hstack([Vp, -(y[:, None] * Vq)]) / (s * Qprev)[:, None]
            c, *_ = np.linalg.lstsq(A, y / (s * Qprev), rcond=None)
            Qprev = Ch.chebval(u, np.r_[1.0, c[p + 1:]]) if q else np.ones(len(u))
    f = lambda cc: res(rat_eval(cc, u, p, q), H, L) / s
    r = least_squares(f, c, method='lm', xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    return r.x

def qzeros(c, p, q):
    """Zeros of Q in the Chebyshev variable u (poles of the rational form)."""
    if not q: return np.array([])
    return Ch.chebroots(np.r_[1.0, c[p + 1:]])
