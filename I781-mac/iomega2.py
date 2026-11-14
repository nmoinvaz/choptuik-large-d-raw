"""D near lambda = i omega with the unchanged code, and D(i omega) itself with the integrator's absolute tolerance
raised from 1e-19 to 1e-16 for this point only (#781, setting A, N 160)"""
import sys, time, math
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, sys.argv[1])
import css_inf_jump as m
P = m.Problem(N=160)
x, j = P.select(log=lambda s: None)
w = 1j * P.om
for eps in (0.1, 0.01, 0.001, 0.0001, 0.001j, -0.001):
    t = time.time()
    d = P.det(w + eps)
    print('lam = i omega + %-8s D %+.6e %+.6ei |D| %.3e |D|/|eps| %.4e (%.1fs)' % (
        eps, d.real, d.imag, abs(d), abs(d) / abs(eps), time.time() - t), flush=True)
def path_integrate_atol(rhs, y0, r0, r1, alpha, rtol, atol=1e-16):
    e = np.exp(1j * alpha)
    s1 = solve_ivp(lambda r, y: e * rhs(r * e, y), (r0, r1), y0, method="DOP853", rtol=rtol, atol=atol)
    s2 = solve_ivp(lambda p, y: 1j * r1 * np.exp(1j * p) * rhs(r1 * np.exp(1j * p), y), (alpha, 0.0), s1.y[:, -1],
                   method="DOP853", rtol=rtol, atol=atol)
    return s2.y[:, -1], s1.nfev + s2.nfev
for lam in (w, w + 0.001, 2.0):
    m.path_integrate = path_integrate_atol
    t = time.time()
    d = P.det(lam)
    print('atol 1e-16: lam %-28s D %+.6e %+.6ei |D| %.3e (%.1fs, nfev %d)' % (
        lam, d.real, d.imag, abs(d), time.time() - t, P.last['nfev']), flush=True)
