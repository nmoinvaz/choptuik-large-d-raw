import sys, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
z = np.load("/Users/nathan/Source/choptuik-1025/solver/matter/data/sol_l1kc31L1025_D13.0000.npy")
S = DSSEll(kc=31, nodes=NODES_STD, n=11, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04); S.freeze_from(z, 0.7)
l1 = 2.6841484641099442
P = {}
for d in (0.03, 0.01, 0.003, 0.001):
    with np.errstate(all="ignore"):
        M = S.mode_matrix(z, l1 + d)
    U, s, Vh = np.linalg.svd(M); P[d] = (s / s[0], Vh, U)
    print(f"+{d}: sigma/smax near the V: " + " ".join(f"{v:.2e}" for v in (s / s[0])[(s / s[0] > 1e-10) & (s / s[0] < 2e-7)][::-1][:40]), flush=True)
i = int(np.argmin(abs(np.log(P[0.03][0] / 7.81e-8))))
for a, b in ((0.03, 0.01), (0.01, 0.003), (0.003, 0.001)):
    sa, Va, Ua = P[a]; sb, Vb, Ub = P[b]
    o = np.abs(Vb @ Va[i]); ou = np.abs(Ub.T @ Ua[:, i]); top = np.argsort(o)[::-1][:5]
    print(f"{a}->{b}: V index {i} sigma {sa[i]:.3e}; top right overlaps " + ", ".join(f"{o[j]:.3f}@{sb[j]:.2e}(left {ou[j]:.3f})" for j in top)
          + f"; right weight within top 5 {np.sum(o[top]**2):.3f}", flush=True)
    i = int(top[0])
