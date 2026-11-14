"""#780: at D 20.04's largest phase difference, which part differs: the light-cone block or the LU.
A_d is complex_imag.py's matrix (double light-cone block H_d); A_h is A_d with complex_imag_dd's H (horizon_dd).
ln det by scipy's double LU and by complex_imag_dd's double-double banded LU."""
import sys, math
import numpy as np
import scipy.linalg as sl
sys.path.insert(0, sys.argv[1])
import complex_imag as ci
import complex_imag_dd as cd
import ddnp as dd
bg = ci.Background(sys.argv[2], ks_series=100)
tf = ci.TestField(bg, None)                        # rtol 1e-11, as the double counts
st = cd.DDState(bg)
M, L = bg.M, len(bg.X)
def lu_double(A):
    lu, piv = sl.lu_factor(A)
    d = np.diag(lu)
    v = np.sum(np.log(np.abs(d))) + 1j * (np.sum(np.angle(d)) + np.pi * int(np.sum(piv != np.arange(len(piv)))))
    return complex(v.real, math.remainder(v.imag, 2 * math.pi))
def lu_ddp(A):
    _, _, v = cd.lu_factor(dd.from_complex(A), lb=3 * M, ub=3 * M)
    return complex(v.real, math.remainder(v.imag, 2 * math.pi))
for s in sys.argv[3:]:
    lam = complex(s)
    A_d = tf.matrix(lam)
    H_d = tf.horizon(lam, bg.X[-1])
    H_h, tail = cd.horizon_dd(st, bg, lam, bg.X[-1])
    H_h = H_h.to_complex()
    r0 = 2 * M * L
    A_h = A_d.copy()
    A_h[r0:r0 + 2 * M, M + 2 * M * L:] = H_h
    v = {k: f(A) for k, f, A in (("d_dLU", lu_double, A_d), ("h_dLU", lu_double, A_h), ("d_ddLU", lu_ddp, A_d),
                                  ("h_ddLU", lu_ddp, A_h))}
    ph = lambda a, b: math.remainder(a.imag - b.imag, 2 * math.pi)
    print("lam %s: |H_d - H_h| / max|H_h| = %.1e (largest relative entry difference %.1e); phase of ln det:" % (
        lam, np.max(np.abs(H_d - H_h)) / np.max(np.abs(H_h)),
        np.max(np.abs(H_d - H_h) / np.maximum(np.abs(H_h), 1e-300 + 1e-12 * np.max(np.abs(H_h))))))
    print("   light-cone block (double LU) %+.2e rad, (double-double LU) %+.2e rad; LU (double H) %+.2e rad, "
          "(double-double H) %+.2e rad; both %+.2e rad" % (
              ph(v["h_dLU"], v["d_dLU"]), ph(v["h_ddLU"], v["d_ddLU"]), ph(v["d_ddLU"], v["d_dLU"]),
              ph(v["h_ddLU"], v["h_dLU"]), ph(v["h_ddLU"], v["d_dLU"])), flush=True)
