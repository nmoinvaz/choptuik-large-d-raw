import sys, os, json, time, cProfile, pstats, numpy as np
WTM = "/Users/nathan/Source/choptuik-ell1-speed/solver/matter"
sys.path.insert(0, WTM); os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
recf, st, D, lam = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
z = np.load(st)
S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
print("N", S.N, "n_odd", S.n_odd, "n_even", S.n_even, "steps", sum(steps.values()), steps, flush=True)
blocks, offs = S._block_list()
# time per block
S.lam = lam
h = 1e-20
for b, (c0, nf, fun, tgt) in enumerate(blocks):
    t0 = time.time()
    X = np.repeat(z[None, c0:c0 + nf], nf + 1, axis=0).astype(complex)
    X[1:] += 1j * h * np.eye(nf)
    om = np.full(nf + 1, 2 * np.pi / z[-1], dtype=complex)
    if b in (1, 12):
        pr = cProfile.Profile(); pr.enable()
    R = S.tospec(fun(X, om))
    if b in (1, 12):
        pr.disable(); pstats.Stats(pr).sort_stats("tottime").print_stats(12)
    print(f"block {b}: nf {nf}, {time.time() - t0:.2f} s", flush=True)
S.lam = 0.0
