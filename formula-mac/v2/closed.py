"""Few-parameter physically structured forms (no truncated series): best accuracy each reaches on the real data, with
a self-plant check (the fitted form + the points' noise, refitted from a perturbed start, must return its Dinf to
1e-9 and fit that plant to max |r|/sigma <= 5; otherwise the fit procedure is not trusted and the form is marked).
Unweighted least squares on each range (these forms sit far above the points' errors, so the weights do not matter);
reported: max |residual| on the range, Dinf, and the fitted singularity data. e = 1/n, n = D - 2.
  A  Dinf + A e (1 - e/e_s)^beta                              one branch point at n_s = 1/e_s, exponent beta (4 params+1)
  B  Dinf + A e (1 - e/e_s)^beta (1 - e)^alpha (1 + c e)       both endpoint singularities (Riemann-P-like), 7 params
  C  Dinf + A e 2F1(a, b; c; e/e_s)                            Gauss function with its singular point at n_s, 6 params
  R22, R33  rational [p/q] in e (pole-only), 5 and 7 params
  Z22, Z33  rational [p/q] in zeta(n_s), n_s free, 6 and 8 params (square-root ends at D_s and D = 3)
Ranges: D >= 10; D >= 4; all D (forms without a D = 3 singularity skip 'all'; C, the slow hyp2f1, runs on D >= 10
only with 8 starts, and Z33 with 8 starts, to keep each run under 10 minutes; closed_part1.log holds A-Z22)."""
import numpy as np, warnings
from scipy.optimize import least_squares
from scipy.special import hyp2f1
import common as C, sys
ONLY = sys.argv[1:]            # optional subset of forms, e.g. Z33
warnings.filterwarnings('ignore')
D0, H0, L0, s0, _ = C.data(); y0 = H0 + L0
e = lambda d: 1 / (d - 2)
def fA(d, p): Di, A, es, be = p; x = e(d); return Di + A * x * np.abs(1 - x / es) ** be
def fB(d, p): Di, A, es, be, al, c = p[:6]; x = e(d); return Di + A * x * np.abs(1 - x / es) ** be * np.abs(1 - x) ** al * (1 + c * x)
def fC(d, p): Di, A, a, b, c, es = p; x = e(d); return Di + A * x * hyp2f1(a, b, c, x / es)
def rat(d, p, P, Q, var):
    t = var(d, p); num = sum(p[k] * t ** k for k in range(P + 1)); den = 1 + sum(p[P + k] * t ** k for k in range(1, Q + 1)); return num / den
ve = lambda d, p: e(d)
vz = lambda d, p: C.zeta(d, p[-1])
FORMS = {
    'A': (fA, [1.644, 10.4, -1 / 11, -1.0], ['Dinf', 'A', 'e_s', 'beta'], False),
    'B': (fB, [1.644, 10.4, -1 / 11, -1.0, 0.5, 0.0], ['Dinf', 'A', 'e_s', 'beta', 'alpha', 'c'], True),
    'C': (fC, [1.644, 10.4, 1.0, 1.0, 1.0, -1 / 11], ['Dinf', 'A', 'a', 'b', 'c', 'e_s'], False),
    'R22': ((lambda d, p: rat(d, p, 2, 2, ve)), [1.644, 20, 50, 10, 10], None, False),
    'R33': ((lambda d, p: rat(d, p, 3, 3, ve)), [1.644, 20, 50, 0, 10, 10, 0], None, False),
    'Z22': ((lambda d, p: rat(d, p, 2, 2, vz)), [1.644, 1, 1, 0.1, 0.1, -11.0], None, True),
    'Z33': ((lambda d, p: rat(d, p, 3, 3, vz)), [1.644, 1, 1, 0, 0.1, 0.1, 0, -11.0], None, True),
}
def fit(f, p0, d, y, w=None, starts=30, seed=0):
    rng = np.random.default_rng(seed); best = None; w = np.ones(len(d)) if w is None else w
    for k in range(starts):
        p = np.array(p0, float) * (1 + (0.3 * rng.standard_normal(len(p0)) if k else 0))
        try:
            r = least_squares(lambda q: np.nan_to_num((f(d, q) - y) * w, nan=1e3, posinf=1e3, neginf=-1e3), p,
                              method='lm', max_nfev=20000, xtol=1e-15, ftol=1e-15)
        except Exception:
            continue
        if best is None or r.cost < best.cost: best = r
    return best.x
def dinf(f, p, nm):
    if nm.startswith('Z'): return float(rat(np.array([1e12]), p, int(nm[1]), int(nm[2]), vz)[0])
    return float(f(np.array([1e15]), p)[0])
print(f"{'form':5s} {'range':8s} {'npar':>4s} {'max|res|':>9s} {'at D':>7s} {'Dinf':>14s}  self-plant  parameters")
for nm, (f, p0, names, d3) in FORMS.items():
    if ONLY and nm not in ONLY: continue
    for rnm, m in (('D>=10', D0 >= 10), ('D>=4', D0 >= 4), ('all', D0 > 0)):
        if rnm == 'all' and not d3: continue
        if nm == 'C' and rnm != 'D>=10': continue
        st = 8 if nm in ('C', 'Z33') else 30
        d, y, s = D0[m], y0[m], s0[m]
        p = fit(f, p0, d, y, starts=st); r = f(d, p) - y; i = np.argmax(np.abs(r)); Di = dinf(f, p, nm)
        # self-plant: truth = this fit; noise = the points' errors; refit from the original p0 (perturbed starts)
        yp = f(d, p) + np.random.default_rng(5).normal(0, 1, len(d)) * s
        pp = fit(f, p0, d, yp, starts=st, seed=7); ok = abs(dinf(f, pp, nm) - Di) <= 1e-9 and np.max(np.abs(f(d, pp) - yp)) <= max(5 * s.max(), np.max(np.abs(r)) * 1e-3)
        pr = ' '.join(f'{v:.4g}' for v in p)
        print(f'{nm:5s} {rnm:8s} {len(p):4d} {np.abs(r).max():9.1e} {d[i]:7.2f} {Di:14.10f}  {"ok" if ok else "NOT RECOVERED"}  {pr}', flush=True)
