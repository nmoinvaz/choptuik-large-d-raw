"""Where do M's rounding-floor singular directions live (#1025)? SVD of M at two lambda; the right (input) and left
(output) singular vectors with sigma < tau sigma_max, their weight by field and by coefficient index within a field's
block, and the principal angles between the two lambdas' floor subspaces."""
import sys, json, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD, PAR
st, D, kc = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
lams = [float(v) for v in sys.argv[4].split(",")]
tau = float(sys.argv[5]) if len(sys.argv) > 5 else 1e-15
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
sizes, K, L = S.layout()
no, ne = S.n_odd, S.n_even
names = ["c.odd", "c.even"] + [f"{f}" for i in range(K) for f in ("p", "m", "a", "c", "q")] + ["s.odd", "s.even", "s.odd2"]
offs = np.concatenate([[0], np.cumsum(sizes)])
col_field = np.concatenate([[names[i]] * sizes[i] for i in range(len(sizes))])
col_pos = np.concatenate([np.arange(sizes[i]) / sizes[i] for i in range(len(sizes))])
blk = 3 * no + 2 * ne
rcut = np.cumsum([0, no, no, ne, ne, no])
row_field = np.array([("p", "m", "a", "c", "q")[np.searchsorted(rcut, j % blk, side="right") - 1] for j in range(sizes and (L - 1))])
row_pos = np.array([((j % blk) - rcut[np.searchsorted(rcut, j % blk, side="right") - 1]) /
                    (rcut[np.searchsorted(rcut, j % blk, side="right")] - rcut[np.searchsorted(rcut, j % blk, side="right") - 1])
                    for j in range(L - 1)])
print(f"n_odd {no}, n_even {ne}, K {K}, n {L - 1}")
sub = {}
for l in lams:
    with np.errstate(all="ignore"):
        M = S.mode_matrix(z, l)
    U, s, Vh = np.linalg.svd(M)
    k = int(np.sum(s < tau * s[0]))
    V, Uf = Vh[-k:].T, U[:, -k:]
    sub[l] = (V, Uf)
    wc = (V ** 2).sum(axis=1) / k; wr = (Uf ** 2).sum(axis=1) / k
    byf = lambda w, f: {n: round(float(w[f == n].sum()), 4) for n in sorted(set(f)) if w[f == n].sum() > 1e-3}
    hi_c = float(wc[col_pos >= 0.8].sum()); hi_r = float(wr[row_pos >= 0.8].sum())
    print(json.dumps(dict(lam=l, n_floor=k, tau=tau, sigma_rel=[float(v / s[0]) for v in s[-k:][::-1][:3]] + [float(s[-k - 1] / s[0])],
                          input_weight_by_field=byf(wc, col_field), input_weight_top20pct_coeffs=round(hi_c, 4),
                          output_weight_by_field=byf(wr, row_field), output_weight_top20pct_coeffs=round(hi_r, 4))), flush=True)
if len(lams) > 1:
    (V0, U0), (V1, U1) = sub[lams[0]], sub[lams[1]]
    k = min(V0.shape[1], V1.shape[1])
    cr = np.linalg.svd(V0.T @ V1, compute_uv=False); cl = np.linalg.svd(U0.T @ U1, compute_uv=False)
    print(f"principal cosines between the floors at lam {lams[0]} and {lams[1]}: right min {cr.min():.3e} "
          f"(of {len(cr)}; below 0.99: {int(np.sum(cr < 0.99))}), left min {cl.min():.3e} (below 0.99: {int(np.sum(cl < 0.99))})")
