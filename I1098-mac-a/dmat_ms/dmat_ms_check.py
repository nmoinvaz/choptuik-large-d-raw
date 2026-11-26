"""hp's d/dtheta operator against the 120-digit one (multishoot PR #67's reference, scripts/dmat_mp: D at 120 digits split
greedily into f64 parts) in one residual (#1098): the octo-double residual of a state with hp's remainders c (from
80-digit values, form_s.dmat_corr) and again with c' = RN(D_120 - hi - lo) (hi, lo hp's), so that hi + lo + c' is the
120-digit D to f64 rounding of c', as multishoot's hi + lo + c is. Reported: max |F' - F| and the first-order move of
the converged Delta, -g . (F' - F) with g = J^-T e_Delta (the quad-double Jacobian solved in quad-double, as gainq.py).

    python3 dmat_ms_check.py STATE [--kfreeze 13] [--threads 4]
"""
import sys
import time

import numpy as np
from mpmath import mp
from multidouble import QDLu

import form_s
import hpkernel.driver as drv
from octo_corrector import load_o


def c120(M, hi, lo, parity):
    out = np.zeros((M, M))
    with mp.workdps(120):
        N = 2 * M
        for i in range(M):
            for j in range(M):
                v = mp.mpf(0)
                for jj, sgn in ((j, 1), (j + M, -1 if parity == "odd" else 1)):
                    if jj != i:
                        v += sgn * mp.mpf(0.5) * (-1) ** (i - jj) * mp.cot((i - jj) * mp.pi / N)
                out[i, j] = float(v - mp.mpf(float(hi[i, j])) - mp.mpf(float(lo[i, j])))
    return out


def fsum8(F, i):
    return mp.fsum(mp.mpf(float(F[q][i])) for q in range(8))


args = sys.argv[1:]
opt = dict(zip(args[1::2], args[2::2]))
kf, thr = int(opt.get("--kfreeze", "13")), int(opt.get("--threads", "4"))
z8, meta = load_o(args[0])
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
M = int(meta["M"])
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=thr, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
t0 = time.time()
s = form_s.make_solver_s(D, M, list(meta["nodes"]), kfreeze=kf, **kw)
assert form_s._DMAT_STATE["applied"], "this hpkernel applies no remainders"
zz = [np.ascontiguousarray(z8[q]) for q in range(8)]
F1 = [np.asarray(f) for f in s.residual_s(zz)]
oh, ol = drv.dmat_odd(M)
eh, el = form_s.dmat_even(M)
co, ce = form_s.dmat_corr(M)
co2, ce2 = c120(M, np.asarray(oh), np.asarray(ol), "odd"), c120(M, np.asarray(eh), np.asarray(el), "even")
print(f"M {M}: max |c' - c| odd {np.abs(co2 - co).max():.3e}, even {np.abs(ce2 - ce).max():.3e}; "
      f"max |c| odd {np.abs(co).max():.3e}", flush=True)
s.set_dmat_corr(np.ascontiguousarray(co2), np.ascontiguousarray(ce2))
F2 = [np.asarray(f) for f in s.residual_s(zz)]
L = len(F1[0])
mp.dps = 120
dF = [fsum8(F2, i) - fsum8(F1, i) for i in range(L)]
nF1 = max(abs(fsum8(F1, i)) for i in range(L))
J = s.jacobian_s([zz[q] for q in range(4)])
eD = np.zeros(L)
eD[-1] = 1.0
gq = QDLu(*[np.ascontiguousarray(np.asarray(J[q]).T) for q in range(4)]).solve(eD, np.zeros(L), np.zeros(L), np.zeros(L))
g = [mp.mpf(float(gq[0][i])) + mp.mpf(float(gq[1][i])) for i in range(L)]
dD = -mp.fsum(g[i] * dF[i] for i in range(L))
print(f"D {float(D):g} (kfreeze {kf}): od max |F| {mp.nstr(nF1, 4)}; with the 120-digit operator max |F' - F| "
      f"{mp.nstr(max(abs(v) for v in dF), 4)}; first-order move of Delta -g.(F' - F) {mp.nstr(dD, 4)}; "
      f"gain {mp.nstr(mp.fsum(abs(v) for v in g), 4)} ({time.time() - t0:.0f} s)", flush=True)
# the control: c' moved by 2^-20 of hi + lo's own rounding (c'(1 + 2^-20)) must move Delta in proportion
s.set_dmat_corr(np.ascontiguousarray(co2 * (1 + 2.0 ** -20)), np.ascontiguousarray(ce2 * (1 + 2.0 ** -20)))
F3 = [np.asarray(f) for f in s.residual_s(zz)]
dF3 = [fsum8(F3, i) - fsum8(F2, i) for i in range(L)]
dD3 = -mp.fsum(g[i] * dF3[i] for i in range(L))
print(f"control (c' x (1 + 2^-20)): max |dF| {mp.nstr(max(abs(v) for v in dF3), 4)}, Delta's move {mp.nstr(dD3, 4)} "
      f"(about 2^-20 of the double-double term, -2.2e-32 at D 300: about 2e-38)", flush=True)
