"""T84: the deflated quad-double Newton (driver.newton_qd with w > 0) on T84's double-double states in the layout
with the last node at 0.85 or 0.8, the full system (kfreeze 13). Control: w = 0 (the undeflated Newton) from the
same state must not converge (notes/QUAD_DOUBLE.md 12.3: it jumps along the nearly singular direction).

    python3 qd_deflated.py STATE.npz [w] [threads] [modes]      (modes: comma list of all, junk, control; default all)
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver, newton_qd, qmax, save_q  # noqa: E402

path = sys.argv[1]
w = int(sys.argv[2]) if len(sys.argv) > 2 else 24
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 4
modes = (sys.argv[4] if len(sys.argv) > 4 else "all").split(",")
z, m = load_q(path)
D, M = m["D"], m["M"]
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
print(f"{os.path.basename(path)}: D {D}, nodes {m['nodes']}, |F| {qmax(s.residual_q(*z)):.2e}, Delta {z[0][-1]:.16f}", flush=True)
out = path[:-4] + "_qd.jsonl"
for mode in modes:
    wi = 0 if mode == "control" else w
    t0 = time.time()
    zq, hist, conv = newton_qd(s, z, tol=1e-50, it_max=14, verbose=True, w=wi, junk=(mode == "junk"))
    f = hist[-1].get("F_new", hist[-1]["F"])
    print(f"{mode} (w {wi}): {'converged' if conv else 'NOT converged'}, |F| {f:.2e}, {len(hist)} steps, {time.time() - t0:.0f} s, "
          f"Delta {zq[0][-1]:.17f} {zq[1][-1]:+.6e} {zq[2][-1]:+.3e}", flush=True)
    with open(out, "a") as fh:
        fh.write(json.dumps(dict(state=os.path.basename(path), D=D, mode=mode, w=wi, conv=conv, F=f, steps=len(hist),
                                 Delta_q=[float(p[-1]) for p in zq], seconds=round(time.time() - t0), hist=hist)) + "\n")
    if conv and wi:
        save_q(path[:-4] + f"_qd_{mode}.npz", zq, dict(m, solver="qd", kfreeze=13))
