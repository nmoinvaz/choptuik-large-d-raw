# One fit over every DD point 3.04375-67.77 (weights 1/err): absolute residuals by range, for zeta(n_s) and w1(n_s).
import numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
from jouk import zeta, DINF
D, y, s, run = load()
w1 = lambda d, ns: (lambda q: (q - 1) / (q + 1))(np.sqrt(1 - ns / (d - 2)))
def wfit(t, K):
    lo, hi = t.min(), t.max(); V = Ch.chebvander((2 * t - lo - hi) / (hi - lo), K)
    c, *_ = np.linalg.lstsq(V / s[:, None], y / s, rcond=None)
    return lambda tt: Ch.chebval((2 * np.asarray(tt) - lo - hi) / (hi - lo), c)
rngs = [(3.0, 3.1), (3.1, 3.5), (3.5, 4.01), (4.01, 8.3), (8.3, 30), (30, 68)]
for nm, tf in [('zeta(-11)', lambda d: zeta(d, -11.0)), ('zeta(-13)', lambda d: zeta(d, -13.0)), ('w1(-11)', lambda d: w1(d, -11.0))]:
    t = tf(D)
    for K in (20, 24, 28, 32):
        ev = wfit(t, K); r = np.abs(ev(t) - y)
        print(f'{nm:9s} K={K}: ' + '  '.join(f'{a:g}-{b:g}: {r[(D >= a) & (D < b)].max():.0e}' for a, b in rngs)
              + f'   lim-Dinf {float(ev(tf(1e12))) - DINF:+.0e}')
print('point errors by range: ' + '  '.join(f'{a:g}-{b:g}: {s[(D >= a) & (D < b)].max():.0e}' for a, b in rngs))
