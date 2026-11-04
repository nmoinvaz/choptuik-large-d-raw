# Low-D structure test on our DD points 3.04375-4: the polynomial in s plus log columns s^j ln s (j = jmin..jmax), and
# a power-series in s with a free leading power, s^q P(s). Same held-out split as lowd.py.
import numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
D, y, sg, run = load(); m = D <= 4.0 + 1e-9; D, y = D[m], y[m]; lo = D < 3.1
s = np.sqrt(D - 3)
def basis(s, K, logs):
    cols = [Ch.chebvander(2 * s - 1, K)]
    for j in logs: cols.append((s ** j * np.log(s))[:, None])
    return np.hstack(cols)
def run_(K, logs):
    A = basis(s, K, logs)
    c1, *_ = np.linalg.lstsq(A[~lo], y[~lo], rcond=None); h = np.abs(A[lo] @ c1 - y[lo]).max()
    c, *_ = np.linalg.lstsq(A, y, rcond=None); r = np.abs(A @ c - y).max()
    v3 = Ch.chebval(-1.0, c[:K + 1])                      # s = 0: the log columns vanish when j >= 1
    return r, h, v3, len(c)
for logs in ([], [2], [1, 2], [2, 4], [1, 2, 3], [2, 3, 4]):
    for K in (6, 8, 10):
        r, h, v3, npar = run_(K, logs)
        print(f'poly s deg {K:2d} + s^j ln s, j={logs}: {npar:2d} params  res {r:.1e}  held 3.04-3.1 {h:.1e}  Delta(3) {v3:.4f}')
