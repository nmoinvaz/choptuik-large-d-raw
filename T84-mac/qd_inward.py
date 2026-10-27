"""T84: the two-radius horizon treatment that the kernel already has (Ctx::match_node: segments beyond it integrate
inward from the horizon side), on T75's frontier state. Nodes 0.3..0.7 plus 0.85 and 0.95, matched at 0.7: the horizon
series is summed at u = 0.05, where it converges for any nearby data, and integrated inward to 0.7. Measures the
blocks' response to D with the state held (as blocks_dD.py: 2.1e-2 at dD 1e-8 and 3.8e15 at 1e-4 in the 0.7 layout)
and runs the plain quad-double Newton at D (full system, kfreeze 13), which stalls in every other layout.

    python3 qd_inward.py STATE.npz [threads] [extra nodes, default 0.85,0.95]
"""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import block_norms, load_q, make_solver, newton_qd, qmax, renode, save_q  # noqa: E402

path = sys.argv[1]
threads = int(sys.argv[2]) if len(sys.argv) > 2 else 4
extra = [float(v) for v in (sys.argv[3] if len(sys.argv) > 3 else "0.85,0.95").split(",")]
z, m = load_q(path)
D, M, old = m["D"], m["M"], list(m["nodes"])
kw = dict(kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s_old = make_solver(D, M, nodes=old, **kw)
s_old.set_segs(s_old.plan(z[0], z[1], 1e-32, 0.05))
print(f"{os.path.basename(path)}: D {D}, old layout {old}: |F| {qmax(s_old.residual_q(*z)):.2e}", flush=True)
new = old + extra
match = len(old) - 1
zh, zl = renode(s_old, z[0], z[1], old, new, M)
nh = 2 * M + 4 * M * len(old)
low = [np.concatenate([p[:nh], np.zeros(4 * M * len(extra)), p[nh:]]) for p in (z[2], z[3])]
zn = tuple(np.ascontiguousarray(p) for p in (zh, zl, *low))
s = make_solver(D, M, nodes=new, match_node=match, **kw)
s.set_segs(s.plan(zn[0], zn[1], 1e-32, 0.05))
segs = s.get_segs()
F = s.residual_q(*zn)
print(f"inward layout {new}, matched at node {match} (x {new[match]}), u0 {1 - new[-1]:.2f}: |F| {qmax(F):.2e}, blocks "
      + " ".join(f"{v:.1e}" for v in block_norms(s, F[0], F[1])), flush=True)
for h in (1e-8, 1e-6, 1e-4, 1e-2):
    sx = make_solver(D + h, M, nodes=new, match_node=match, **kw)
    sx.set_segs(segs)
    Fx = sx.residual_q(*zn)
    print(f"  dD {h:.0e}: max |F| {qmax(Fx):.1e}, blocks " + " ".join(f"{v:.1e}" for v in block_norms(sx, Fx[0], Fx[1])), flush=True)
t0 = time.time()
zq, hist, conv = newton_qd(s, zn, tol=1e-50, it_max=10, verbose=True)
f = hist[-1].get("F_new", hist[-1]["F"])
print(f"inward: {'converged' if conv else 'NOT converged'}, |F| {f:.2e}, {len(hist)} steps, {time.time() - t0:.0f} s, "
      f"Delta {zq[0][-1]:.17f} {zq[1][-1]:+.6e} {zq[2][-1]:+.3e}; old layout's Delta {z[0][-1]:.17f} {z[1][-1]:+.6e}", flush=True)
tag = "_".join(f"{v:g}" for v in extra)
with open(path[:-4] + f"_inward{tag}.jsonl", "a") as fh:
    fh.write(json.dumps(dict(state=os.path.basename(path), D=D, nodes=new, match_node=match, conv=conv, F=f, steps=len(hist),
                             Delta_q=[float(p[-1]) for p in zq], seconds=round(time.time() - t0), hist=hist)) + "\n")
if conv:
    save_q(path[:-4] + f"_inward{tag}.npz", zq, dict(m, nodes=new, match_node=match, solver="qd", kfreeze=13))
