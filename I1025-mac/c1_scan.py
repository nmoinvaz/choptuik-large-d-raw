import sys, os, json, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
from dss_ell import DSSEll, NODES_STD
z = np.load("/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy")
S = DSSEll(kc=55, nodes=NODES_STD, n=14, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04); S.freeze_from(z, 0.7)
for l in [2.24250, 2.24254, 2.24258, 2.24262, 2.24266, 2.2426280416106374, 2.2426280416106374]:
    with np.errstate(all="ignore"):
        s, ld = np.linalg.slogdet(S.mode_matrix(z, l))
    print(json.dumps(dict(D=16, kc=55, u0=0.04, lam=l, sign=float(s), ln=float(ld))), flush=True)
