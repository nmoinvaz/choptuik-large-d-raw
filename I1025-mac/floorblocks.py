"""M's floor singular vectors (sigma < tau sigma_max) by shooting block: input weight per unknown group (centre, node k,
outer) and output weight per block row (0 = centre -> node 0, k = node k-1 -> k, last = outer -> node K-1) (#1025)"""
import os, sys, json, numpy as np
sys.path.insert(0, os.getcwd())
from dss_ell import DSSEll, NODES_STD
st, D, kc, lam = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
tau = float(sys.argv[5]) if len(sys.argv) > 5 else 1e-15
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
sizes, K, L = S.layout()
no, ne = S.n_odd, S.n_even
blk = 3 * no + 2 * ne
with np.errstate(all="ignore"):
    M = S.mode_matrix(z, lam)
U, s, Vh = np.linalg.svd(M)
k = int(np.sum(s < tau * s[0]))
wc = (Vh[-k:] ** 2).sum(axis=0) / k; wr = (U[:, -k:] ** 2).sum(axis=1) / k
cg = {"centre": wc[:no + ne].sum()}
for i in range(K):
    cg[f"node{i}"] = wc[no + ne + blk * i: no + ne + blk * (i + 1)].sum()
cg["outer"] = wc[no + ne + blk * K:].sum()
rg = {f"block{b}": wr[blk * b: blk * (b + 1)].sum() for b in range(K + 1)}
print(json.dumps(dict(D=D, kc=kc, lam=lam, n_floor=k, input_by_group={a: round(float(v), 4) for a, v in cg.items() if v > 1e-4},
                      output_by_block={a: round(float(v), 4) for a, v in rg.items() if v > 1e-4})), flush=True)
