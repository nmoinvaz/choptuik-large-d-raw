# Dry run (float64) of a planted-truth test for the conformal-map fit, on the real D >= 10 grid, noise 1e-15, fixed seed.
# Plants with a known limit L:
#   R   the README rational formula (poles at D = -3.24, -11.01; no branch point), L = a0
#   S9  R + 0.05 (sqrt(1 - e/e9) - 1 - e/(2 e9)) ... a square-root branch at D = -9 (the map's assumed cut), L = a0
#   S6  the same branch at D = -6 (misplaced against the assumed n_s = -11)
#   C   R + 1e-3 Re[t^3/(1 - t/ts)], t = 1/D, ts = 0.06 e^{2 pi i/3} (planted_dinf T3, complex pair near the data)
# Each plant: fit on 10-45, held-out max on 45-60.1, and limit - L, for 1/D (K 16) and w1(-11) (K 12, 14).
import numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
from poles import a, b
D, y, s, run = load(); D = D[(D >= 10) & (D <= 60.1)]
rng = np.random.default_rng(1)
rat = lambda d: np.polyval(a[::-1], 1 / (d - 2)) / np.polyval(b[::-1], 1 / (d - 2))
def br(d, Ds):
    e, es = 1 / (d - 2), 1 / (Ds - 2); q = np.sqrt(1 - e / es); return q - 1 + e / (2 * es)
ts = 0.06 * np.exp(2j * np.pi / 3)
plants = {'R': lambda d: rat(d), 'S9': lambda d: rat(d) + 0.05 * br(d, -9.0), 'S6': lambda d: rat(d) + 0.05 * br(d, -6.0),
          'C': lambda d: rat(d) + 1e-3 * np.real((1 / d) ** 3 / (1 - (1 / d) / ts))}
L = a[0]
def pfit(t, y, K, sel):
    lo, hi = t[sel].min(), t[sel].max(); V = Ch.chebvander((2 * t[sel] - lo - hi) / (hi - lo), K)
    c, *_ = np.linalg.lstsq(V, y[sel], rcond=None); return lambda tt: Ch.chebval((2 * np.asarray(tt) - lo - hi) / (hi - lo), c)
w1 = lambda d, ns: (lambda q: (q - 1) / (q + 1))(np.sqrt(1 - ns / (d - 2)))
models = [('1/D K16', lambda d: 1 / d, 16), ('w1(-11) K12', lambda d: w1(d, -11.0), 12), ('w1(-11) K14', lambda d: w1(d, -11.0), 14)]
fitm = D <= 45; hold = ~fitm
for pn, pf in plants.items():
    yy = pf(D) + rng.normal(0, 1e-15, len(D))
    out = []
    for mn, tf, K in models:
        t = tf(D); ev = pfit(t, yy, K, fitm)
        out.append(f'{mn}: held {np.abs(ev(t[hold]) - yy[hold]).max():.0e} lim-L {float(ev(0.0)) - L:+.0e}')
    print(f'{pn:3s} ' + ' | '.join(out))
