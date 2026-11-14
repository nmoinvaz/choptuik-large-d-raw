"""det M with the last segment(s) cut into nsub pieces (extra matching points; det unchanged in exact arithmetic),
double DOP853 propagators at two rtol, determinant by the double-double banded LU of complex_imag_dd.py"""
import sys, time, math, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci, complex_imag_dd as cd, ddnp as dd
from ddnp import R, C
bg = ci.Background(sys.argv[1])
nsubs = [int(v) for v in sys.argv[2].split(',')]
lam = complex(sys.argv[3]) if len(sys.argv) > 3 else 1.3 + 0.4j
M = bg.M
def matrix(tf, nsub, nlast=2):
    L = len(bg.X)
    # matching points: nodes, with the last nlast segments cut into nsub pieces
    pts = [bg.X[0]]
    segi = []
    si = 1 if bg.pre else 0
    for b in range(1, L):
        x0, x1, seg = bg.segs[si + b - 1]
        k = nsub if b >= L - nlast else 1
        for j in range(1, k + 1):
            pts.append(x0 + (x1 - x0) * j / k if j < k else x1)
            segi.append(seg)
    Lp = len(pts)
    N = 2 * M * (Lp + 1)
    A = np.zeros((N, N), complex)
    I2 = np.eye(2 * M)
    Cm = tf.centre(lam, bg.xs)
    if bg.pre:
        x0, x1, seg = bg.segs[0]
        Cm = tf.propagate(seg, x0, x1, Cm, lam)
    A[0:2 * M, 0:M] = Cm
    A[0:2 * M, M:3 * M] = -I2
    for b in range(1, Lp):
        Phi = tf.propagate(segi[b - 1], pts[b - 1], pts[b], I2.astype(complex), lam)
        r0 = 2 * M * b
        A[r0:r0 + 2 * M, M + 2 * M * (b - 1):M + 2 * M * b] = Phi
        A[r0:r0 + 2 * M, M + 2 * M * b:M + 2 * M * (b + 1)] = -I2
    H = tf.horizon(lam, bg.X[-1])
    r0 = 2 * M * Lp
    A[r0:r0 + 2 * M, M + 2 * M * (Lp - 1):M + 2 * M * Lp] = -I2
    A[r0:r0 + 2 * M, M + 2 * M * Lp:] = H
    return A
for nsub in nsubs:
    res = {}
    for rt in (1e-11, 1e-13):
        tf = ci.TestField(bg, rtol=rt)
        t = time.time()
        A = matrix(tf, nsub)
        t1 = time.time()
        _, _, v = cd.lu_factor(dd.from_complex(A), lb=3 * M, ub=3 * M)
        res[rt] = v
        print('nsub %d rtol %g: N %d ln det %s (matrix %.1fs, dd LU %.1fs)' % (nsub, rt, A.shape[0], v, t1 - t, time.time() - t1), flush=True)
    d = res[1e-11] - res[1e-13]
    print('nsub %d: rtol 1e-11 - 1e-13: dln|det| %.2e dphase %.2e' % (nsub, d.real, math.remainder(d.imag, 2 * math.pi)), flush=True)
