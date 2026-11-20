"""Does a lambda-independent equilibration (Ruiz, from M at a reference lambda) remove M's ill-conditioning?"""
import sys, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
st, D, kc, lam1 = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
lams = [lam1 + 0.5, lam1, lam1 - 0.4, lam1 + 0.3j, lam1 + 1.0j]
Ms = [S.mode_matrix(z, l.real) if isinstance(l, float) else S.mode_matrix_c(z, l, eps=1e-6) for l in lams]
A = np.abs(Ms[0]); dr = np.ones(A.shape[0]); dc = np.ones(A.shape[1])
for _ in range(30):                                   # Ruiz: rows and columns to unit max-norm
    B = dr[:, None] * A * dc[None, :]
    dr /= np.sqrt(B.max(axis=1)); B = dr[:, None] * A * dc[None, :]; dc /= np.sqrt(B.max(axis=0))
print(f"row scales {dr.min():.2e}..{dr.max():.2e}, column scales {dc.min():.2e}..{dc.max():.2e}")
for l, M in zip(lams, Ms):
    s = np.linalg.svd(M, compute_uv=False); ss = np.linalg.svd(dr[:, None] * M * dc[None, :], compute_uv=False)
    print(f"lam {l}: cond {s[0] / s[-1]:.2e}, smallest 4 / max {np.array2string(s[-4:] / s[0], precision=2)}; "
          f"scaled cond {ss[0] / ss[-1]:.2e}, smallest 4 / max {np.array2string(ss[-4:] / ss[0], precision=2)}", flush=True)
