"""sign and log|det| of the mode matrix on a real lambda grid, with M's finiteness (#1025: lambda_1 at k_c 55, D 18)"""
import sys, time, json, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
st, D, kc = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
grid = [float(v) for v in sys.argv[4].split(",")]
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
for l in grid:
    t = time.time()
    with np.errstate(all="ignore"):
        M = S.mode_matrix(z, l)
        fin = bool(np.all(np.isfinite(M)))
        sg, la = np.linalg.slogdet(M) if fin else (np.nan, np.nan)
    print(json.dumps(dict(D=D, kc=kc, lam=l, finite=fin, n_nonfinite=int(np.sum(~np.isfinite(M))),
                          maxabs=float(np.nanmax(np.abs(np.where(np.isfinite(M), M, np.nan)))), sign=float(sg),
                          logabs=float(la), sec=round(time.time() - t, 1))), flush=True)
