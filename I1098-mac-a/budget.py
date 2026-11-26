"""Per-point error budget of a full form-S solve (#1098 part 1): re-solve the FULL system (kfreeze 13) from a saved full
state with one discretization parameter changed, and report Delta's change against the same solve at the state's own
discretization (the baseline), each converged by Newton with the given Jacobian mode and residual precision.

    python3 budget.py STATE VARIANT [--jac qq] [--res od] [--tol 1e-48] [--threads 2]
    VARIANT: base | steps2 (every Taylor step halved) | ks+N | kc+N | kt+N
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import make_solver_s, newton_o_s  # noqa: E402
from octo_corrector import delta_digits, load_o  # noqa: E402

args = sys.argv[1:]
path, var = args[0], args[1]
opt = dict(zip(args[2::2], args[3::2]))
jac, res, tol, thr = opt.get("--jac", "qq"), opt.get("--res", "od"), float(opt.get("--tol", "1e-48")), int(opt.get("--threads", "2"))
z8, meta = load_o(path)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=thr, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
if var == "steps2":
    kw["segs"] = [[g[0]] + [v for a, b in zip(g[:-1], g[1:]) for v in (0.5 * (a + b), b)] for g in meta["segs"]]
elif var != "base":
    name, n = var.split("+")
    kw[name] += int(n)
s = make_solver_s(D, int(meta["M"]), list(meta["nodes"]), kfreeze=13, **kw)
t0 = time.time()
z, conv, recs = newton_o_s(s, z8, tol, 6, 6, None, verbose=False, jac=jac, res=res)
F = s.residual_s([np.ascontiguousarray(z[q]) for q in range(8)])
nF = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
d0, d1 = delta_digits(z8, 40), delta_digits(z, 40)
with mp.workdps(60):
    dd = float(mp.mpf(d1) - mp.mpf(d0))
steps = [f"{r['F']:.1e}->{r['F_new']:.1e}" for r in recs]
print(json.dumps(dict(D=meta["D_str"], variant=var, kt=kw["kt"], kc=kw["kc"], ks=kw["ks"],
                      taylor_steps=sum(len(g) - 1 for g in kw["segs"]), mob=kw["mob"], jac=jac, res=res,
                      converged=bool(conv), steps=steps, F_od=nF, gain=recs[-1].get("gain") if recs else None,
                      Delta=d1, dDelta_vs_state=dd, s=round(time.time() - t0, 1))), flush=True)
