"""unit check of OLadder.rung at u0: the state's own data moved along a_h by rel, the rung's Newton must return"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from jump import OLadder, D_mp
from octo_corrector import load_o, o8
from multidouble import od_axpy

z, meta = load_o(sys.argv[1])
D = D_mp(meta)
M, K = meta["M"], len(meta["nodes"])
lad = OLadder(meta, D, threads=2, verbose=True)
o = lad.rs.off
sl_ = slice(o["mh"], o["mh"] + 2 * M)
nk = o["node"](K - 1)
u0 = lad.us[-1]
target = [np.array(np.asarray(p)[nk:nk + 4 * M]) for p in z]
d0 = [np.ascontiguousarray(np.array(np.asarray(p)[sl_])) for p in z]
rng = np.random.default_rng(1)
for rel in [float(x) for x in sys.argv[2].split(",")]:
    pert = np.zeros(2 * M)
    pert[M:] = rel * rng.uniform(0.5, 1, M) * rng.choice([-1, 1], M)
    zero = np.zeros(2 * M)
    d = [np.ascontiguousarray(np.asarray(p)) for p in od_axpy(1.0, pert, *([zero] * 7), *d0)]
    t = time.time()
    dn, h, ok = lad.rung(u0, z, target, d)
    diff = np.asarray(dn[0]) + np.asarray(dn[1]) - (d0[0] + d0[1])
    print(f"a_h moved {rel:.0e}: |R| " + " -> ".join(f"{x:.2e}" for x in h) + f"  ({time.time() - t:.1f} s), data off by {np.abs(diff).max():.1e}", flush=True)
