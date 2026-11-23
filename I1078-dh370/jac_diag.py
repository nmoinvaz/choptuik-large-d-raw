"""#1078, t5's order (comment of 23:40 UTC, check 1): the background Jacobian of a state: one Newton step (dd, its LU's pivot range), and the 200 smallest pivots of the equilibrated float64 LU of the dense Jacobian with their unknowns.

    cd hp && python3 jac_diag.py STATE.npz OUT.jsonl [--threads=4] [--hmax=0.05] [--small=200]

One Newton step (driver.newton_step, jac "dd": s.newton, the step dz = -J^-1 F and the LU's pivot range pmin, pmax), then Solver.jacobian (the dense (L, L) Jacobian, hi and lo, L = 4M(K+1) + 1: the last column is Delta,
the last row the phase row), then mode_scale.scaled_det on it: Ruiz equilibration by powers of two, float64 LU with row interchanges, the smallest pivots with their column index (small_map: index 8448 = Delta). The
state is not changed (the step is not applied)."""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.getcwd())
import lowD_gamma as LG  # noqa: E402
import mode_scale as MS  # noqa: E402
from hpkernel.driver import load, newton_step  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
o = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
state, out = args[0], args[1]
zh, zl, meta = load(state)
D, M = meta["D"], meta["M"]
s, grid = LG.build_solver(D, M, meta, int(o.get("threads", 4)))
s.set_segs(s.plan(zh, zl, 1e-32, float(o.get("hmax", 0.05))))
Fh, Fl = s.residual(zh, zl)
F0 = float(np.abs(np.asarray(Fh) + np.asarray(Fl)).max())
t = time.time()
dh, dl, Fh, Fl, pmin, pmax, info = newton_step(s, zh, zl)
dz = float(np.abs(np.asarray(dh) + np.asarray(dl)).max())
dDelta = float(dh[-1] + dl[-1])
print(f"{os.path.basename(state)}: D {D} M {M} map {grid}; |F| {F0:.3e}; one dd Newton step: |dz| {dz:.3e}, dDelta {dDelta:+.3e}, LU pivots {pmin:.3e} .. {pmax:.3e} "
      f"(ratio {pmin / pmax:.1e}), {time.time() - t:.0f} s", flush=True)
t = time.time()
Jh, Jl = s.jacobian(zh, zl)
n = np.asarray(Jh).shape[0]
d = MS.scaled_det(np.asarray(Jh), np.asarray(Jl), small=int(o.get("small", 200)))
row = dict(D=D, M=M, state=os.path.basename(state), map=grid, n=n, F=F0, dz=dz, dDelta=dDelta, newton_pmin=float(pmin), newton_pmax=float(pmax), sec_jac=round(time.time() - t, 1), **d)
with open(out, "a") as fh:
    fh.write(json.dumps(row) + "\n")
print(f"dense Jacobian n {n}: scaled float64 pivots {d['pmin']:.3e} .. {d['pmax']:.3e} (ratio {d['ratio']:.1e}); unscaled {d['pmin_unscaled']:.3e} .. {d['pmax_unscaled']:.3e} (ratio {d['ratio_unscaled']:.1e}); "
      f"the {len(d['small'])} smallest scaled pivots span {abs(d['small'][0][1]):.3e} .. {abs(d['small'][-1][1]):.3e}; {row['sec_jac']} s", flush=True)
