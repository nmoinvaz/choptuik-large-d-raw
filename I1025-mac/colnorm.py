"""M's centre-odd columns (#1025 floor map): small, or nearly dependent? Column norms, singular values of those columns
alone (raw and normalised), and the full M's floor count after normalising them (a lambda-independent change of
variables if the scale is taken at one lambda)."""
import os, sys, json, numpy as np
sys.path.insert(0, os.getcwd())
from dss_ell import DSSEll, NODES_STD
st, D, kc, lam = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
no, ne = S.n_odd, S.n_even
with np.errstate(all="ignore"):
    M = S.mode_matrix(z, lam)
cn = np.linalg.norm(M, axis=0); cmax = cn.max()
C = M[:, :no]
nzr = np.nonzero(np.abs(C).sum(axis=1))[0]
s_raw = np.linalg.svd(C, compute_uv=False); s_nrm = np.linalg.svd(C / cn[:no], compute_uv=False)
print(json.dumps(dict(D=D, kc=kc, lam=lam, n=M.shape[0], col_norm_rel_centre_odd=[float(v) for v in (cn[:no] / cmax)[::5]],
                      rows_touched_by_centre_odd=[int(nzr.min()), int(nzr.max()), int(len(nzr))],
                      sv_centre_odd_raw_rel=[float(v) for v in (s_raw / cmax)[::5]],
                      sv_centre_odd_normalised=[float(v) for v in s_nrm[::5]])), flush=True)
sc = np.ones(M.shape[1]); sc[:no] = cmax / cn[:no]
s1 = np.linalg.svd(M, compute_uv=False); s2 = np.linalg.svd(M * sc[None, :], compute_uv=False)
for tag, s in (("M", s1), ("M with centre-odd columns normalised", s2)):
    print(f"{tag}: below 1e-12 sigma_max {int(np.sum(s < 1e-12 * s[0]))}, below 1e-15 {int(np.sum(s < 1e-15 * s[0]))}, "
          f"smallest five / max {np.array2string(s[-5:] / s[0], precision=2)}", flush=True)
