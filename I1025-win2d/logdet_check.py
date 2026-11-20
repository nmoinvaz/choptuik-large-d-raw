#!/usr/bin/env python3
"""#1025 preparation check (coordinator's hc 2026-11-20): multidouble 5.1.0's dd_logdet on a planted 200 x 200 matrix.
    python logdet_check.py [--mutate=lnd]
A = Q diag(d) Q^T, d known with 3 negative entries: sign -1 and ln|det| = sum ln|d_i| within 1e-12; the control with one row
negated must flip the sign. Information: the matrix as stored (python-flint, exact entries), par=True, qd_logdet."""
import sys, json, time
import numpy as np
import mpmath as mp
import flint
import multidouble as md

mutate = "--mutate=lnd" in sys.argv
n, seed, bar = 200, 20261120, 1e-12
g = np.random.default_rng(seed)
Q = np.linalg.qr(g.standard_normal((n, n)))[0]
u = g.uniform(-0.7, 0.7, n)
neg = np.sort(g.choice(n, 3, replace=False))
sgn = np.ones(n); sgn[neg] = -1.0
d = sgn * np.exp(u)
A = Q @ np.diag(d) @ Q.T
mp.mp.dps = 50
dexp = d.copy()
if mutate:
    dexp[0] *= 1 + 1e-9
exact = sum(mp.log(abs(mp.mpf(float(x)))) for x in dexp)
exp_sign = -1.0 if int(np.sum(dexp < 0)) % 2 else 1.0
print(f"multidouble {md.__file__}; numpy {np.__version__}; python-flint {flint.__version__}; n {n}, seed {seed}; negative d at {neg.tolist()}; "
      f"|d| in [{np.abs(d).min():.4f}, {np.abs(d).max():.4f}]; planted sign {exp_sign:+.0f}, sum ln|d_i| = {mp.nstr(exact, 25)}"
      + ("; --mutate=lnd" if mutate else ""), flush=True)
t = time.perf_counter(); s1, ln1, mn1, mx1 = md.dd_logdet(A, np.zeros_like(A)); t1 = time.perf_counter() - t
print(f"dd_logdet: sign {s1:+.0f}, ln|det| {ln1!r}, min|u_kk| {mn1:.4e}, max|u_kk| {mx1:.4e}, {t1:.2f} s", flush=True)
err = float(abs(mp.mpf(ln1) - exact))
Ac = A.copy(); Ac[0] = -Ac[0]
sc, lnc, _, _ = md.dd_logdet(Ac, np.zeros_like(Ac))
print(f"control (row 0 negated): sign {sc:+.0f}, ln|det| {lnc!r}, |ln diff| from the unnegated {abs(lnc - ln1):.3e}", flush=True)
# information
flint.ctx.prec = 600
M = flint.arb_mat(n, n, [flint.arb(float(x)) for x in A.ravel()])
det = M.det()
fs = 1.0 if det.lower() > 0 else (-1.0 if det.upper() < 0 else 0.0)
fl = abs(det).log()
fln = mp.mpf(fl.mid().str(40, radius=False))
print(f"info: stored matrix by python-flint (600 bits): sign {fs:+.0f}, ln|det| {mp.nstr(fln, 25)} (ball radius {fl.rad().str(3)})", flush=True)
print(f"info: dd_logdet - stored {float(mp.mpf(ln1) - fln):+.3e}; planted - stored {float(exact - fln):+.3e} (the rounding in forming A in float64, with Q's departure from orthogonality)", flush=True)
s2, ln2, _, _ = md.dd_logdet(A, np.zeros_like(A), par=True)
print(f"info: par=True: sign {s2:+.0f}, ln|det| {ln2!r}, same bits as par=False: {ln2 == ln1 and s2 == s1}", flush=True)
z = np.zeros_like(A)
sq, lnq, _, _ = md.qd_logdet(A, z, z, z)
print(f"info: qd_logdet: sign {sq:+.0f}, ln|det| {lnq!r}, minus dd_logdet {lnq - ln1:+.3e}, minus planted {float(mp.mpf(lnq) - exact):+.3e}", flush=True)
ok_sign = s1 == exp_sign == -1.0
ok_ln = err <= bar
ok_ctrl = sc == -s1 and abs(lnc - ln1) <= bar
print(f"1. sign {'PASS' if ok_sign else 'FAIL'}: dd_logdet {s1:+.0f}, planted {exp_sign:+.0f}", flush=True)
print(f"2. ln|det| {'PASS' if ok_ln else 'FAIL'}: |dd_logdet - sum ln|d_i|| = {err:.3e} (bar {bar:g})", flush=True)
print(f"3. control {'PASS' if ok_ctrl else 'FAIL'}: row 0 negated gives sign {sc:+.0f} (must be {-s1:+.0f}), ln|det| moved {abs(lnc - ln1):.3e}", flush=True)
print(f"logdet_check: {'PASS' if (ok_sign and ok_ln and ok_ctrl) else 'FAIL'}", flush=True)
sys.exit(0 if (ok_sign and ok_ln and ok_ctrl) else 1)
