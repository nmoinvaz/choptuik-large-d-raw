"""Delta's gain sum |J^-T e_Delta| of a saved state's system (#1098's residual bound), with J the quad-double Jacobian
solved in quad-double (QDLu) and, for comparison, in double-double: the full system (kfreeze 13, or --kfreeze K)
without held values. With the octo-double residual, gain max |F| is Delta's first-order error bound.

    python3 gainq.py STATE [--kfreeze 13] [--threads 2]
"""
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402
from multidouble import QDLu, dd_solve  # noqa: E402

from form_s import make_solver_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

args = sys.argv[1:]
path = args[0]
opt = dict(zip(args[1::2], args[2::2]))
kf, thr = int(opt.get("--kfreeze", "13")), int(opt.get("--threads", "2"))
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
gd = np.asarray(dd_solve(np.ascontiguousarray(np.asarray(J[0]).T), np.ascontiguousarray(np.asarray(J[1]).T), eD, np.zeros(L))[0])
print(f"D {float(D):g} (kfreeze {kf}): od max |F| {nF:.3e}; Delta's gain {np.abs(g).sum():.4e} (qd solve), "
      f"{np.abs(gd).sum():.4e} (dd solve); first-order bound {np.abs(g).sum() * nF:.2e}; largest |g| entries at rows "
      f"{list(np.argsort(-np.abs(g))[:5])} ({time.time() - t0:.0f} s)", flush=True)
