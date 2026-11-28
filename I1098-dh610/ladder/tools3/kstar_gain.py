"""Delta's gain sum |J^-T e_Delta| of a saved state's system at kfreeze K (#1098's residual bound at k*), with J the
quad-double Jacobian solved in quad-double (multidouble's QDLu) and, for comparison, in double-double; the system is
form S at kfreeze K without held values (the target system of release_ls at kmax K). With the octo-double residual,
gain x max |F| is Delta's first-order error bound. The same computation as I1098-dh610's gainq.py; form_s and hpkernel
come from PYTHONPATH (SITE:HP).

    python3 kstar_gain.py STATE [--kfreeze 15] [--threads 2]

The last line reads "gain_qd G F_od F" for the scripts that call it.
"""
import sys
import time

import numpy as np
from mpmath import mp
from multidouble import QDLu, dd_solve

from form_s import make_solver_s
from octo_corrector import load_o

args = sys.argv[1:]
path = args[0]
opt = dict(zip(args[1::2], args[2::2]))
kf, thr = int(opt.get("--kfreeze", "15")), int(opt.get("--threads", "2"))
z8, meta = load_o(path)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=thr, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
s = make_solver_s(D, int(meta["M"]), list(meta["nodes"]), kfreeze=kf, **kw)
t0 = time.time()
F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(8)])
nF = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
J = s.jacobian_s([np.ascontiguousarray(z8[q]) for q in range(4)])
L = s.size_s
eD = np.zeros(L)
eD[-1] = 1.0
gq = QDLu(*[np.ascontiguousarray(np.asarray(J[q]).T) for q in range(4)]).solve(eD, np.zeros(L), np.zeros(L), np.zeros(L))
g = np.asarray(gq[0]) + np.asarray(gq[1])
gd = np.asarray(dd_solve(np.ascontiguousarray(np.asarray(J[0]).T), np.ascontiguousarray(np.asarray(J[1]).T), eD,
                         np.zeros(L))[0])
G = float(np.abs(g).sum())
print(f"D {float(D):g} (kfreeze {kf}): od max |F| {nF:.3e}; Delta's gain {G:.4e} (qd solve), {np.abs(gd).sum():.4e} "
      f"(dd solve); first-order bound {G * nF:.2e} ({time.time() - t0:.0f} s)", flush=True)
print(f"gain_qd {G:.6e} F_od {nF:.6e}", flush=True)
