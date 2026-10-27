import sys, numpy as np
from hpkernel.driver import load_q, make_solver, block_norms
zs, meta = load_q(sys.argv[1]); D, M = meta["D"], meta["M"]
mk = lambda Dx, ks=meta["ks"]: make_solver(Dx, M, nodes=list(meta["nodes"]), kt=meta["kt"], kc=meta["kc"], ks=ks, threads=6, kfreeze=13)
s = mk(D); segs = s.plan(zs[0], zs[1], 1e-32, 0.05)
for ks in (meta["ks"], 160, 200):
    for h in (0.0, 1e-8, 1e-6, 1e-4):
        sx = mk(D + h, ks); sx.set_segs(segs)
        F = sx.residual_q(*zs)
        print(f"ks {ks} h {h:.0e}: blocks " + " ".join(f"{v:.1e}" for v in block_norms(sx, F[0], F[1])), flush=True)
    print("horizon series tail at D (ks %d):" % ks, end=" ")
    sx = mk(D, ks); sx.set_segs(segs)
    hh, hl = sx.series(zs[0], zs[1], 1)
    c = np.abs((hh + hl).reshape(-1, 4, M)).max(axis=(1, 2)); u0 = 1 - meta["nodes"][-1]
    print(" ".join(f"{k}:{c[k] * u0**k:.1e}" for k in range(0, len(c), max(1, len(c) // 10))), flush=True)
