import sys, os, json, time, numpy as np
WTM = "/Users/nathan/Source/choptuik-ell1-speed/solver/matter"
sys.path.insert(0, WTM); os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
import multidouble as md, ell_ddm
recf, st, D, lam = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
z = np.load(st)
S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
print("N", S.N, "n_odd", S.n_odd, "n_even", S.n_even, "steps", sum(steps.values()), steps, flush=True)
blocks, offs = S._block_list()
S.lam = lam; h = 1e-20
for b in (0, 1, 12):
    c0, nf, fun, tgt = blocks[b]
    t0 = time.time()
    X = np.repeat(z[None, c0:c0 + nf], nf + 1, axis=0).astype(complex)
    X[1:] += 1j * h * np.eye(nf)
    om = np.full(nf + 1, 2 * np.pi / z[-1], dtype=complex)
    if b == 12:
        t1 = time.time()
        Sx = S.ssh_series(S.phys(X[:, :S.n_odd], "odd"), S.phys(X[:, S.n_odd:S.n_odd + S.n_even], "even"), S.phys(X[:, S.n_odd + S.n_even:], "odd"), om)
        print(f"  block 12 ssh_series {time.time() - t1:.1f} s", flush=True)
    R = S.tospec(fun(X, om))
    print(f"block {b}: nf {nf}, {time.time() - t0:.1f} s (steps {list(steps.values())[b]})", flush=True)
S.lam = 0.0
t0 = time.time(); E = ell_ddm.DDEll(S); print(f"DDEll init {time.time() - t0:.1f} s", flush=True)
t0 = time.time(); Md = E.mode_matrix(z, lam, only=[12]); print(f"dd block 12 {time.time() - t0:.1f} s", flush=True)
nv = S.layout()[2] - 1
rng = np.random.default_rng(0); H = rng.standard_normal((nv, nv)); Hl = np.zeros_like(H)
t0 = time.time(); md.dd_logdet(H, Hl, True); print(f"dd_logdet n {nv}: {time.time() - t0:.1f} s", flush=True)
t0 = time.time(); np.linalg.slogdet(H); print(f"slogdet n {nv}: {time.time() - t0:.1f} s", flush=True)
