"""Discretization of the fine-mesh held system at a converged state (#1088): the held residual (octo-double) with every
Taylor step halved, with ks + 100, and with kc + 30, each one's first-order dDelta -e_Delta^T J^-1 dF (J the sparse
float64 Jacobian at the state). If one of them moves Delta by ~1e-9..1e-8, the fine mesh's D 2200 and 2828 offsets from
Track C are its truncation.

    python3 finedisc.py STATE.npz THREADS
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
import scipy.sparse.linalg as spl
from form_s import make_solver_s, HeldS, held_field, blocks_s
from form_s_fine import sparse_jacobian
from octo_corrector import load_o
from multidouble import od_axpy

path, thr = sys.argv[1], int(sys.argv[2])
z8, meta = load_o(path)
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
h8 = held_field(z8, M)
kw = dict(kt=meta["kt"], threads=thr, mob=meta.get("hmob", 0.0), kfreeze=3)


def held(kc, ks, segs):
    return HeldS(make_solver_s(D, M, nodes, kc=kc, ks=ks, segs=segs, **kw), M, K, h8)


t0 = time.time()
base = held(meta["kc"], meta["ks"], meta["segs"])
zz = [np.ascontiguousarray(p) for p in z8]
F0 = base.residual_s(zz)
L = len(zz[0])
J = sparse_jacobian(base.s, z8, K, L)
lu = spl.splu(J.tocsc(), permc_spec="COLAMD")
eD = np.zeros(L)
eD[-1] = 1.0
g = lu.solve(eD, trans="T")
print(f"{path.split('/')[-1]}: D {float(D):g}, K {K}, gain {np.abs(g).sum():.2e} ({time.time() - t0:.0f} s)", flush=True)
fine = [[s[0]] + [v for a, b in zip(s[:-1], s[1:]) for v in (0.5 * (a + b), b)] for s in meta["segs"]]
for nm, kc, ks, segs in (("steps halved", meta["kc"], meta["ks"], fine), ("ks + 100", meta["kc"], meta["ks"] + 100, meta["segs"]),
                         ("kc + 30", meta["kc"] + 30, meta["ks"], meta["segs"])):
    t0 = time.time()
    F = held(kc, ks, segs).residual_s(zz)
    dF = np.asarray(od_axpy(-1.0, *[np.ascontiguousarray(np.asarray(f)) for f in F0], *[np.ascontiguousarray(np.asarray(f)) for f in F])[0])
    b = blocks_s([dF, np.zeros(L)], M, K)
    worst = int(np.argmax(b[:K + 1]))
    print(f"  {nm}: max |dF| {np.abs(dF).max():.3e} (block {worst} of {K}), first-order dDelta {-(g @ dF):+.3e} "
          f"({time.time() - t0:.0f} s)", flush=True)
