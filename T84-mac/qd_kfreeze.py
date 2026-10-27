"""T84: the plain quad-double Newton on the system with p1's harmonics above KF pinned to zero (kfreeze KF), from a
state whose harmonics above KF are zeroed (as scan_hp's freeze_p1). The full system (kfreeze 13) is nearly degenerate
past D 73 (qd_weak.py, qd_deflated.py); the pinned double-double system is not. Prints Delta and saves the state.

    python3 qd_kfreeze.py STATE.npz KF [threads]
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver, newton_qd, plow_odd, qmax, save_q  # noqa: E402

path, kf = sys.argv[1], int(sys.argv[2])
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
lo, lo2 = plow_odd(M, kf)
P = lo + lo2
z = list(z)
z[0] = z[0].copy(); z[0][:M] = P @ (z[0][:M] + z[1][:M] + z[2][:M] + z[3][:M])
for q in (1, 2, 3):
    z[q] = z[q].copy(); z[q][:M] = 0.0
z = tuple(np.ascontiguousarray(p) for p in z)
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=kf)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
print(f"{os.path.basename(path)}: D {D}, nodes {m['nodes']}, kfreeze {kf}: start |F| {qmax(s.residual_q(*z)):.2e}, Delta {z[0][-1]:.16f}", flush=True)
t0 = time.time()
zq, hist, conv = newton_qd(s, z, tol=1e-50, it_max=14, verbose=True)
f = hist[-1].get("F_new", hist[-1]["F"])
print(f"kfreeze {kf}: {'converged' if conv else 'NOT converged'}, |F| {f:.2e}, {len(hist)} steps, {time.time() - t0:.0f} s, "
      f"Delta {zq[0][-1]:.17f} {zq[1][-1]:+.6e} {zq[2][-1]:+.3e} {zq[3][-1]:+.3e}", flush=True)
with open(path[:-4] + f"_kf{kf}.jsonl", "a") as fh:
    fh.write(json.dumps(dict(state=os.path.basename(path), D=D, kfreeze=kf, conv=conv, F=f, steps=len(hist),
                             Delta_q=[float(p[-1]) for p in zq], seconds=round(time.time() - t0), hist=hist)) + "\n")
if conv:
    save_q(path[:-4] + f"_kf{kf}.npz", zq, dict(m, solver="qd", kfreeze=kf))
