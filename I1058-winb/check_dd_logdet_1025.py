#!/usr/bin/env python3
"""#1025 (win): the coordinator's planted check of multidouble.dd_logdet in venv-md510 (multidouble 5.1.0, commit 8c4360ac).
A = Q diag(d) Q^T, n = 200, Q from a QR of a seeded normal matrix, d known with 3 negative entries, so det A = det(Q)^2 prod d with det(Q)^2 = 1 up to rounding:
the exact values are sign -1 and ln|det| = sum ln|d_i| (mpmath, 50 digits). Pass: dd_logdet's sign is -1 and |ln|det| - exact| <= 1e-12.
Control: the same matrix with one row negated; its sign must flip (+1), ln|det| unchanged within 1e-12.
Extras (not criteria): mpmath's own ln|det| of the stored float64 matrix, qd_logdet, par=True against par=False bit for bit.
Run from any folder with venv-md510's python; writes JSON to the path given as argv[1]."""
import importlib.metadata as md, json, sys, time
import numpy as np, mpmath, multidouble
mpmath.mp.dps = 50
n = 200
rng = np.random.default_rng(1025)
Q, R = np.linalg.qr(rng.standard_normal((n, n)))
Q = Q * np.sign(np.diag(R))
mag = np.exp(rng.uniform(np.log(0.9), np.log(1.11), n))          # |d_i| in [0.9, 1.11]: the documented rounding bound n 2^-53 (1 + sum |ln|u||) is under 5e-13
neg = rng.choice(n, 3, replace=False)
d = mag.copy(); d[neg] *= -1
A = (Q * d) @ Q.T
exact_sign = -1.0 if (d < 0).sum() % 2 else 1.0
exact_ln = float(sum(mpmath.log(abs(mpmath.mpf(float(x)))) for x in d))
zero = np.zeros_like(A)
out = dict(n=n, multidouble=md.version("multidouble"), numpy=np.__version__, mpmath=mpmath.__version__, neg_idx=[int(i) for i in sorted(neg)],
           n_negative=int((d < 0).sum()), exact_sign=exact_sign, exact_ln=exact_ln, cond_A=float(np.linalg.cond(A)), orth_err=float(np.abs(Q.T @ Q - np.eye(n)).max()))
t = time.time(); s, ln, umin, umax = multidouble.dd_logdet(A, zero); out["dd_seconds"] = time.time() - t
out.update(dd_sign=s, dd_ln=ln, dd_minu=umin, dd_maxu=umax, dd_ln_err=ln - exact_ln, dd_sign_ok=(s == exact_sign), dd_ln_ok=(abs(ln - exact_ln) <= 1e-12))
A2 = A.copy(); A2[17, :] *= -1.0
s2, ln2, _, _ = multidouble.dd_logdet(A2, zero)
out.update(ctrl_sign=s2, ctrl_ln=ln2, ctrl_ln_diff=ln2 - ln, ctrl_flipped=(s2 == -s), ctrl_ln_ok=(abs(ln2 - ln) <= 1e-12))
sp, lnp, _, _ = multidouble.dd_logdet(A, zero, par=True)
out.update(par_same_bits=(sp == s and lnp == ln))
z = zero
sq, lnq, uq0, uq1 = multidouble.qd_logdet(A, z, z, z)
out.update(qd_sign=sq, qd_ln=lnq, qd_ln_err=lnq - exact_ln, qd_sign_ok=(sq == exact_sign), qd_ln_ok=(abs(lnq - exact_ln) <= 1e-12), qd_minus_dd=lnq - ln)
t = time.time()
M = mpmath.matrix(A.tolist()); det = mpmath.det(M)
out.update(mp_det_seconds=time.time() - t, mp_sign=float(mpmath.sign(det)), mp_ln=float(mpmath.log(abs(det))), dd_minus_mp=ln - float(mpmath.log(abs(det))))
out["PASS"] = bool(out["dd_sign_ok"] and out["dd_ln_ok"] and out["ctrl_flipped"] and out["ctrl_ln_ok"])
json.dump(out, open(sys.argv[1], "w"), indent=1)
for k, v in out.items():
    print(f"{k}: {v!r}")
print("PASS" if out["PASS"] else "FAIL")
