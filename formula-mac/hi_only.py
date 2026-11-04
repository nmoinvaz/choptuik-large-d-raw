# D >= 10 only (the dd_fits_mp range): polynomial in 1/n against polynomial in the Joukowski zeta(n_s), same data,
# float64 Chebyshev least squares (unweighted, as dd_fits_mp). Fit on 10-45, held out 45-67.77; and fit on all 10-67.77.
import numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
from jouk import zeta, DINF
D, y, s, run = load()
m = D >= 10; D, y = D[m], y[m]
def pfit(t, y, K, tf):
    a, b = t[tf].min(), t[tf].max(); V = Ch.chebvander((2 * t[tf] - a - b) / (b - a), K)
    c, *_ = np.linalg.lstsq(V, y[tf], rcond=None)
    return lambda tt: Ch.chebval((2 * np.asarray(tt) - a - b) / (b - a), c)
fitm = D <= 45; hold = ~fitm
vars_ = [('1/n', lambda d: 1 / (d - 2))] + [(f'zeta ns={ns:g}', (lambda ns: lambda d: zeta(d, ns))(ns)) for ns in (-7, -9, -11, -13, -16)]
print(f'{len(D)} points D >= 10; columns: K, max|res| all-fit, limit - {DINF} (all), held-out max 45-67.77 (fit <= 45), limit (fit <= 45) - Dinf')
for nm, tf in vars_:
    t = tf(D)
    for K in (8, 10, 12, 14, 16, 18):
        e_all = pfit(t, y, K, np.ones(len(D), bool)); r = np.abs(e_all(t) - y).max()
        e45 = pfit(t, y, K, fitm); h = np.abs(e45(t[hold]) - y[hold]).max()
        print(f'{nm:13s} K={K:2d}  res {r:8.1e}  lim {float(e_all(0.0)) - DINF:+9.1e}  held {h:8.1e}  lim45 {float(e45(0.0)) - DINF:+9.1e}')
