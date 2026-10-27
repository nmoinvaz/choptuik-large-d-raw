"""T84: the full-system Delta from a pinned quad-double solution: the residual of the full system (kfreeze 13) at the
pinned solution and one full-system Newton step from it, in quad-double, whose Delta component is the linearised
correction (T75's dDelta_pin, there in double-double); Delta_full1 = Delta_pinned + that. The step is not taken
(the full system's basin is closed there); the correction's error is about c |dz|^2 x dDelta/dF.

    python3 qd_fullcorr.py STATE_qd.npz [threads]
"""
import json
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver, qmax  # noqa: E402

path = sys.argv[1]
threads = int(sys.argv[2]) if len(sys.argv) > 2 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
st = s.newton_q(*z)
f = qmax(st[4:6])
dd = [float(st[q][-1]) for q in range(4)]
corr = dd[0] + dd[1]
full1 = (z[0][-1] + dd[0], z[1][-1] + dd[1])
print(f"{os.path.basename(path)}: D {D}, pin {m.get('pin')}: full-system |F| {f:.2e}, |dz| {np.abs(st[0]).max():.1e}, pivots {st[6]:.1e}..{st[7]:.1e}")
print(f"  Delta_pinned {z[0][-1]:.17f} {z[1][-1]:+.6e} {z[2][-1]:+.3e}")
print(f"  correction   {dd[0]:+.6e} {dd[1]:+.3e} {dd[2]:+.3e} {dd[3]:+.3e}")
print(f"  Delta_full1  {full1[0]:.17f} {full1[1]:+.6e}   (quadratic error about {0.3 * float(np.abs(st[0]).max()) ** 2 * 1e11:.1e})", flush=True)
with open(path[:-4] + "_fullcorr.jsonl", "a") as fh:
    fh.write(json.dumps(dict(state=os.path.basename(path), D=D, pin=m.get("pin"), F_full=f, dz=float(np.abs(st[0]).max()),
                             piv=[st[6], st[7]], Delta_pinned_q=[float(p[-1]) for p in z], correction_q=dd)) + "\n")
