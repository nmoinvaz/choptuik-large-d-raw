"""The full system (kfreeze 13: harmonics 1-13 free) at a held fine-mesh solution (#1088): its octo-double residual and
the first-order Delta change -e_Delta^T J^-1 F with J its sparse float64 Jacobian (form_s_fine.sparse_jacobian,
SuperLU), and the same at the old layout's held solution when given, to tell the held system's layout dependence from
the fine mesh's own error.

    python3 fullcheck.py STATE.npz THREADS
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
import scipy.sparse.linalg as spl
from form_s import make_solver_s
from form_s_fine import sparse_jacobian
from octo_corrector import load_o

for path in sys.argv[2:]:
    pass
path, thr = sys.argv[1], int(sys.argv[2])
z8, meta = load_o(path)
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
t0 = time.time()
s = make_solver_s(D, M, nodes, kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr, segs=meta["segs"],
                  mob=meta.get("hmob", 0.0), kfreeze=13)
L = s.size_s
F = s.residual_s([np.ascontiguousarray(p) for p in z8])
Fv = np.asarray(F[0]) + np.asarray(F[1])
J = sparse_jacobian(s, z8, K, L)
lu = spl.splu(J.tocsc(), permc_spec="COLAMD")
eD = np.zeros(L)
eD[-1] = 1.0
g = lu.solve(eD, trans="T")
dD = -(g @ Fv)
dz = -lu.solve(Fv)
print(f"{path.split('/')[-1]}: D {float(D):g}, K {K}; the full system's max |F| {np.abs(Fv).max():.3e}, first-order dDelta "
      f"{dD:+.4e} (gain {np.abs(g).sum():.2e}); the full Newton step's dDelta {dz[-1]:+.4e}, |dz| {np.abs(dz).max():.2e} "
      f"({time.time() - t0:.0f} s)", flush=True)
