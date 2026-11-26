"""The held form-S solve from a guess, step by step (#1098 continuation diagnostic): kfreeze k0 - 2 with p1's harmonics
k0..kmax held at the guess's own values, newton_o_s verbose with the given Jacobian mode and residual.

    python3 heldsolve.py STATE [--k0 5] [--kmax 25] [--jac qd] [--res od] [--tol 1e-48] [--it 10] [--threads 2] [--save OUT]
"""
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import HeldS, make_solver_s, newton_o_s  # noqa: E402
from octo_corrector import delta_digits, load_o, save_o  # noqa: E402
from pinning import band_coeffs, band_field  # noqa: E402

args = sys.argv[1:]
path = args[0]
opt = dict(zip(args[1::2], args[2::2]))
k0, kmax = int(opt.get("--k0", "5")), int(opt.get("--kmax", "25"))
jac, res, tol, it, thr = opt.get("--jac", "qd"), opt.get("--res", "od"), float(opt.get("--tol", "1e-48")), int(opt.get("--it", "10")), int(opt.get("--threads", "2"))
z8, meta = load_o(path)
M, K = int(meta["M"]), len(meta["nodes"])
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=thr, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
held = list(range(k0, kmax + 1, 2))
co = band_coeffs(np.asarray(z8[0])[:M], np.asarray(z8[1])[:M], M, held, exact=True, rest=[np.asarray(p)[:M] for p in z8[2:]])
s = HeldS(make_solver_s(D, M, list(meta["nodes"]), kfreeze=k0 - 2, **kw), M, K, band_field(co, held, M, parts=8))
t0 = time.time()
z, conv, recs = newton_o_s(s, z8, tol, it, 8, None, verbose=True, jac=jac, res=res)
print(f"converged {conv} in {len(recs)} steps ({time.time() - t0:.0f} s); Delta {delta_digits(z, 40)}", flush=True)
if "--save" in opt:
    save_o(opt["--save"], z, dict(meta, kfreeze=k0 - 2, held_harmonics=held))
