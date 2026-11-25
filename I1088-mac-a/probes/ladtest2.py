"""debug the u0 rung: residual of the state's own data on the rung solver, targets' accuracy"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from jump import OLadder, D_mp
from octo_corrector import load_o, o8
from reseed import res_rows

z, meta = load_o(sys.argv[1])
D = D_mp(meta)
M, K = meta["M"], len(meta["nodes"])
lad = OLadder(meta, D, threads=2, verbose=True)
o, a = lad.rs.off, lad.rs.aoff
sl_ = slice(o["mh"], o["mh"] + 2 * M)
d0 = [np.array(np.asarray(p)[sl_]) for p in z]
nk = o["node"](K - 1)
for u in lad.us:
    s = lad.rs.rung_solver(u)
    rows = lad.rs.rung_rows()
    print("u", u, "solver nodes", (lad.rs.nodes[0], 1 - u), flush=True)
tg = lad.targets(z)
# the state's own data at each rung against the targets
for u in lad.us:
    s = lad.rs.rung_solver(u)
    rows = lad.rs.rung_rows()
    cols = np.r_[a["mh"]:a["mh"] + 2 * M]
    base = [np.zeros(a["L"]) for _ in range(8)]
    for q in range(8):
        zq = np.asarray(z[q])
        base[q][:2 * M] = zq[:2 * M]
        base[q][a["node"](0):a["node"](1)] = zq[o["node"](0):o["node"](1)]
        base[q][a["node"](1):a["node"](1) + 4 * M] = tg[u][q]
        base[q][-1] = zq[-1]
        base[q][cols] = d0[q]
    R = res_rows(s, [np.ascontiguousarray(b) for b in base], rows)
    Rv = np.asarray(R[0]) + np.asarray(R[1])
    print(f"u {u:.5f}: state's data |R| m {np.abs(Rv[:M]).max():.2e} a {np.abs(Rv[M:]).max():.2e}", flush=True)
    # all rows of the horizon block
    Rall = res_rows(s, [np.ascontiguousarray(b) for b in base], np.r_[8 * M:12 * M])
    Ra = np.asarray(Rall[0]) + np.asarray(Rall[1])
    print("    rows p m a c:", " ".join(f"{np.abs(Ra[f*M:(f+1)*M]).max():.2e}" for f in range(4)), flush=True)
