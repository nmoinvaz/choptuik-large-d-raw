"""the octo ladder on a converged chain state: must return its horizon data; and from data moved by rel"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from jump import OLadder, D_mp, system
from octo_corrector import load_o, omax, o8

z, meta = load_o(sys.argv[1])
rel = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
D = D_mp(meta)
M, K = meta["M"], len(meta["nodes"])
s = system(meta, D, 2, 13)
lad = OLadder(meta, D, threads=2, verbose=True)
print("rungs", [round(u, 5) for u in lad.us], [round(d, 1) for d in lad.decs], flush=True)
sl = slice(2 * M + 4 * M * K, 4 * M + 4 * M * K)
zz = [np.array(p) for p in z]
if rel:
    rng = np.random.default_rng(1)
    zz[0][sl] = zz[0][sl] * (1 + rel * rng.uniform(0.5, 1, 2 * M) * rng.choice([-1, 1], 2 * M))
    for q in range(1, 8):
        zz[q][sl] = 0.0
t = time.time()
zp, info = lad.project(o8(zz))
print("project", info["ok"], info["s"], "s", flush=True)
d = np.asarray(zp[0][sl]) + np.asarray(zp[1][sl]) - (np.asarray(z[0][sl]) + np.asarray(z[1][sl]))
print("data moved from the state's: m_h", np.abs(d[:M]).max(), "a_h", np.abs(d[M:]).max(), flush=True)
F = s.residual_o(list(zp))
Fv = np.asarray(F[0]) + np.asarray(F[1])
print("max|F| kfreeze 13 after", omax(F), "per block", " ".join(f"{np.abs(Fv[b*4*M:(b+1)*4*M]).max():.1e}" for b in range(K + 1)), flush=True)
for f, nm in enumerate("pmac"):
    print("  horizon", nm, f"{np.abs(Fv[K*4*M + f*M: K*4*M + (f+1)*M]).max():.2e}")
