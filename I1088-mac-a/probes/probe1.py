import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from hpkernel.driver import make_solver
from octo_corrector import load_o, pinned_o, omax, D_of
from pinning import band_coeffs

p = sys.argv[1]
z, meta = load_o(p)
M = meta["M"]; K = len(meta["nodes"])
print(meta["D"], meta["ks"], meta["kc"], meta["kfreeze"], len(meta["segs"]), flush=True)
t = time.time()
s, sp, sq, so = pinned_o(meta, z, threads=2, segs=meta["segs"])
F = so.residual_o(z)
print("pinned residual_o", omax(F), f"{time.time()-t:.1f}s", flush=True)
D = D_of(meta)
sf = make_solver(D, M, nodes=meta["nodes"], kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=2, kfreeze=None)
sf.set_segs(meta["segs"])
t = time.time()
Ff = sf.residual_o(list(z))
print("full residual_o", omax(Ff), f"{time.time()-t:.1f}s", flush=True)
for name, FF in (("pinned", F), ("full", Ff)):
    Fv = np.asarray(FF[0]) + np.asarray(FF[1])
    print(name)
    for b in range(K + 1):
        print(f"  block {b}: " + " ".join(f"{nm} {np.abs(Fv[b*4*M + f*M: b*4*M + (f+1)*M]).max():.2e}" for f, nm in enumerate("pmac")))
    print("  phase row", Fv[-1])
co = band_coeffs(np.asarray(z[0])[:M], np.asarray(z[1])[:M], M, list(range(1, 32, 2)))
print("p1 harmonics |a|+|b|:", " ".join(f"{k}:{abs(a)+abs(b):.1e}" for k, (a, b) in zip(range(1, 32, 2), co)))
