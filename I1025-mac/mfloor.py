"""Is the mode matrix's rounding floor lambda-independent? SVD of M at three lambda on one state."""
import sys, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
st, D, kc, lam1 = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
lams = [lam1, lam1 + 0.5, lam1 + 0.3j]
Ms = []
for l in lams:
    t = time.time()
    M = S.mode_matrix(z, l.real) if isinstance(l, float) else S.mode_matrix_c(z, l, eps=1e-6)
    Ms.append(M)
    print(f"lam {l}: n {M.shape[0]}, built in {time.time() - t:.1f} s", flush=True)
svd = [np.linalg.svd(M) for M in Ms]
for l, (U, s, Vh) in zip(lams, svd):
    nf = int(np.sum(s < 1e-12 * s[0]))
    print(f"lam {l}: sigma_max {s[0]:.3e}, below 1e-12 sigma_max {nf}, smallest {s[-1]:.2e}, "
          f"sigma at the floor's edge {s[-nf-1] if nf < len(s) else np.nan:.2e} / {s[-nf]:.2e}" if nf else
          f"lam {l}: sigma_max {s[0]:.3e}, none below 1e-12 sigma_max, smallest five {s[-5:]}")
    zc = np.abs(Ms[0]).sum(axis=0); zr = np.abs(Ms[0]).sum(axis=1)
print(f"zero columns of M(lam1): {int(np.sum(zc == 0))}, zero rows: {int(np.sum(zr == 0))}")
U0, s0, Vh0 = svd[0]
nf = int(np.sum(s0 < 1e-12 * s0[0]))
if nf:
    Vf, Uf = Vh0[-nf:].conj().T, U0[:, -nf:]
    for l, M in zip(lams[1:], Ms[1:]):
        print(f"floor of M(lam1) applied at lam {l}: |M Vf| / sigma_max {np.linalg.norm(M @ Vf, 2) / s0[0]:.2e}, "
              f"|Uf^H M| / sigma_max {np.linalg.norm(Uf.conj().T @ M, 2) / s0[0]:.2e}")
