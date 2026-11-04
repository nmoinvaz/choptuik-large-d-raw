# Is the float64 weighted LS of the zeta polynomial accurate? cond(W), and chi2 from numpy lstsq (default rcond),
# lstsq without truncation, and an mpmath QR at 40 digits, for K = 24, 28, 32 at ns = -11, on the real data.
import numpy as np, mpmath as mp, time
from numpy.polynomial import chebyshev as Ch
import common as C
D, H, L, s, run = C.data(); y = H + L
t = C.zeta(D, -11.0); u = 2 * t - 1
mp.mp.dps = 40
for K in (24, 28, 32):
    V = Ch.chebvander(u, K); W = V / s[:, None]; b = y / s
    sv = np.linalg.svd(W, compute_uv=False)
    c1, *_ = np.linalg.lstsq(W, b, rcond=None)
    c2, *_ = np.linalg.lstsq(W, b, rcond=1e-30)
    cl = C.lin_fit(t, H, L, s, K, 0.0, 1.0)
    chi = lambda c: np.sum((C.res(V @ c, H, L) / s) ** 2)
    T0 = time.time()
    Wm = mp.matrix(W.tolist()); bm = mp.matrix([mp.mpf(h) / mp.mpf(si) + mp.mpf(l) / mp.mpf(si) for h, l, si in zip(H, L, s)])
    cm = mp.qr_solve(Wm, bm)[0]; cmf = np.array([float(v) for v in cm])
    # chi2 in mp
    r = Wm * cm - bm; chim = float(sum(v ** 2 for v in r))
    print(f'K={K}: cond {sv[0] / sv[-1]:.1e}  chi2 lstsq {chi(c1):.3e}  no-trunc {chi(c2):.3e}  lin_fit {chi(cl):.3e}  mp {chim:.3e}'
          f'  Dinf mp {float(sum(cm[k] * (-1) ** k for k in range(K + 1))):.12f} D3 mp {float(sum(cm)):.5f} ({time.time() - T0:.0f} s)', flush=True)
