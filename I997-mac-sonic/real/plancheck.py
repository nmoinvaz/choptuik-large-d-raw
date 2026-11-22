import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-lowd-sonic/solver/lowd_sonic")
sys.path.insert(0, "/Users/nathan/Source/choptuik-lowd-sonic/hp")
from hybrid import Hybrid
from hpkernel.driver import load
zh, zl, meta = load(sys.argv[1])
M, nodes, D = meta["M"], meta["nodes"], meta["D"]
phi = np.load(sys.argv[2])
segs = meta["segs"]
for label, sp in (("stored plan", (1, 1)), ("split 2/4", (2, 4)), ("split 4/8", (4, 8))):
    hy = Hybrid(D, M, nodes, meta["kt"], meta["kc"], meta["ks"], segs, (0.01, 0.02), phi, 4, 1.0)
    if sp != (1, 1):
        hy.split(*sp)
    t = time.time()
    Fh, Fl = hy.s.residual(zh, zl)
    bl = hy.blocks(np.asarray(Fh))
    bl[hy.ib] = float("nan")
    print(f"{label}: steps outside band {sum(len(q)-1 for i,q in enumerate(hy.segs) if i != hy.ia)}, {time.time()-t:.0f}s; hp blocks:", " ".join(f"{v:.1e}" for v in bl), flush=True)
