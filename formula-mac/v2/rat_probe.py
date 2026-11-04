# Convergence probe for the weighted rational fit in zeta (fixed ns = -11): SK iterations and LM, cost per stage.
import numpy as np, sys
from numpy.polynomial import chebyshev as Ch
from scipy.optimize import least_squares
import common as C
D, H, L, s, run = C.data(); y = H + L
u = 2 * C.zeta(D, -11.0) - 1
for p, q in [(4, 4), (6, 6), (8, 8), (10, 10), (12, 12)]:
    Vp = Ch.chebvander(u, p); Vq = Ch.chebvander(u, q)[:, 1:]
    Qp = np.ones(len(u)); costs = []
    for it in range(30):
        A = np.hstack([Vp, -(y[:, None] * Vq)]) / (s * Qp)[:, None]
        c, *_ = np.linalg.lstsq(A, y / (s * Qp), rcond=None)
        Qp = Ch.chebval(u, np.r_[1.0, c[p + 1:]])
        r = C.res(C.rat_eval(c, u, p, q), H, L) / s; costs.append(np.sum(r ** 2))
    f = lambda cc: C.res(C.rat_eval(cc, u, p, q), H, L) / s
    R = least_squares(f, c, method='lm', xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=20000)
    r = f(R.x); rr = C.res(C.rat_eval(R.x, u, p, q), H, L)
    zp = (C.qzeros(R.x, p, q) + 1) / 2
    inr = [z for z in zp if abs(z.imag) < 1e-6 and 0 <= z.real <= 1]
    print(f'[{p}/{q}] SK cost it1 {costs[0]:.2e} it10 {costs[9]:.2e} it30 {costs[-1]:.2e} | LM {np.sum(r**2):.3e} nfev {R.nfev} '
          f'| max|r|/s {np.abs(r).max():.1e}  hi(D>=8.25) {np.abs(rr[D>=8.25]).max():.1e} lo(D<4) {np.abs(rr[D<4.01]).max():.1e} '
          f'| Dinf {C.rat_eval(R.x, np.array([-1.]), p, q)[0]:.10f} D3 {C.rat_eval(R.x, np.array([1.]), p, q)[0]:.4f} | real poles in [0,1]: {np.round(np.real(inr),4)}', flush=True)
