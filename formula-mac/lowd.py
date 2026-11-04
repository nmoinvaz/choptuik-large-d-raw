# Low D on our double-double points 3.04375 <= D <= 4 (and <= 6): which variable makes Delta smooth? Chebyshev LS in
#   s = sqrt(D - 3); x = D - 3; ln x as an extra column; the Joukowski zeta(n_s); x^p times a polynomial (p scanned).
# Fit on D >= 3.1 and predict 3.04375-3.1 (11 points), and fit on all and report max |res| and Delta(3).
import numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
from jouk import zeta
D, y, s, run = load(); m = D <= 4.0 + 1e-9; D, y, s = D[m], y[m], s[m]
lo = D < 3.1
print(f'{len(D)} points 3.04375-4, {lo.sum()} below 3.1; point errors {s.min():.0e}..{s.max():.0e}')
def cfit(t, y, K, sel, extra=None):
    a, b = 0.0, t[sel].max()
    V = lambda tt: np.hstack([Ch.chebvander((2 * tt - a - b) / (b - a), K)] + ([extra(tt)[:, None]] if extra else []))
    c, *_ = np.linalg.lstsq(V(t[sel]), y[sel], rcond=None)
    return lambda tt: V(np.atleast_1d(np.asarray(tt, float))) @ c
forms = {'s': lambda d: np.sqrt(d - 3), 'x': lambda d: d - 3, 'zeta(-11)': lambda d: 1 - zeta(d, -11.0)}
for nm, tf in forms.items():
    t = tf(D)
    for K in (6, 8, 10, 12, 14):
        e1 = cfit(t, y, K, ~lo); h = np.abs(e1(t[lo]) - y[lo]).max()
        ea = cfit(t, y, K, np.ones(len(D), bool)); r = np.abs(ea(t) - y).max()
        print(f'{nm:10s} K={K:2d}  res(all) {r:.1e}  held 3.04-3.1 {h:.1e}  value at D=3 {float(ea(0.0)[0]):.4f}')
# x^p (polynomial in x), p scanned
x = D - 3
for K in (5, 7, 9):
    best = None
    for p in np.linspace(0.02, 0.6, 59):
        A = np.stack([x ** (p + k) for k in range(K + 1)], 1); c, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = np.abs(A @ c - y).max()
        if best is None or r < best[0]: best = (r, p)
    print(f'x^p poly K={K}: best p {best[1]:.2f}, res {best[0]:.1e}')
