"""How inconsistent may a last node be for the u0 rung to project it? The chain's state at D 245.5586 with its last
node moved by eps (relative, the smooth tau profile 1 + 0.5 cos theta, all four fields, signs + - + -), then
OLadder.rung at u0 from the state's own horizon data (no inner rungs). Pass for a size: the rung's |R| falls below 1e-26
(the quad-double block LU's floor is about 2e-29 there, ladtest3.log). Prints |R| at each step.

    python3 u0_tolerance.py STATE.npz EPS1,EPS2,...
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from jump import OLadder, D_mp
from octo_corrector import load_o, o8
from multidouble import od_axpy

z, meta = load_o(sys.argv[1])
D = D_mp(meta)
M, K = meta["M"], len(meta["nodes"])
lad = OLadder(meta, D, threads=2)
o = lad.rs.off
nk = o["node"](K - 1)
sl_ = slice(o["mh"], o["mh"] + 2 * M)
th = np.pi * np.arange(M) / M
prof = 1 + 0.5 * np.cos(th)
zv = np.asarray(z[0]) + np.asarray(z[1])
zero = np.zeros(len(zv))
d0 = [np.ascontiguousarray(np.array(np.asarray(p)[sl_])) for p in z]
for eps in [float(x) for x in sys.argv[2].split(",")]:
    pert = np.zeros(len(zv))
    for f, sg in zip(range(4), (1, -1, 1, -1)):
        sl = slice(nk + f * M, nk + (f + 1) * M)
        pert[sl] = sg * eps * prof * np.abs(zv[sl])
    zp = o8(od_axpy(1.0, pert, *([zero] * 7), *z))
    target = [np.array(np.asarray(p)[nk:nk + 4 * M]) for p in zp]
    t = time.time()
    d, h, ok = lad.rung(lad.us[-1], zp, target, d0)
    print(f"node moved {eps:.0e}: |R| " + " -> ".join(f"{x:.2e}" for x in h) +
          f"  {'PASS' if h[-1] < 1e-26 else 'FAIL'} ({time.time() - t:.0f} s)", flush=True)
