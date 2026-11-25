import sys, time, cProfile, pstats, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-ell1-speed/solver/matter")
import ell_fastm, ell_ddm, ell_fastdd, ddnp as dd
from ell_ddm import DT
S, z, rec, same, msg = ell_fastm.load_system(sys.argv[1], sys.argv[2], float(sys.argv[3]))
E = ell_ddm.DDEll(S); E.om = 2 * np.pi / z[-1]
blocks, offs = S._block_list(); c0, nf, fun, tgt = blocks[11]
no, ne = S.n_odd, S.n_even; cut = np.cumsum([0, no, no, ne, ne, no])
X = z[c0:c0 + nf]
s = [DT(dd.R(X[None, cut[f]:cut[f + 1]].copy())) for f in range(5)]
dc = dd.R(np.random.default_rng(0).standard_normal((311, nf)))
for mixed in (False,):
    J = ell_fastdd.DDJac(E, mixed)
    J.stage(0.93, s, dc, 0.49)
    pr = cProfile.Profile(); pr.enable(); t0 = time.time()
    for _ in range(4):
        J.stage(0.93, s, dc, 0.49)
    print(f"mixed {mixed}: {(time.time() - t0) / 4 * 1e3:.0f} ms per stage", flush=True)
    pr.disable(); pstats.Stats(pr).sort_stats("tottime").print_stats(10)
# ell_ddm's own stage cost on dual numbers with nf = 311 tangents
t = [DT(x.v, dd.R(np.random.default_rng(1).standard_normal((311, x.v.shape[1])))) for x in s]
E.lam = 0.49
E.rhs(0.93, t)
t0 = time.time()
for _ in range(4):
    E.rhs(0.93, t)
print(f"ell_ddm rhs on 311 dual tangents: {(time.time() - t0) / 4 * 1e3:.0f} ms per stage", flush=True)
