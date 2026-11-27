"""#1101 R1 pre-start check: the RK4 step count ell_refine.py's first freeze_from gives for the k_c 127 D 23.0 state at kappa 0.7 (must be 4179, the record's), 0.5 (R1: 5851 +- 2%), 0.35 (R2: 8358 +- 2%),
and 0.6 (a control that must fall outside the R1 range). Same constructor as ell_refine.py's mk(); run from solver/matter of the scan worktree."""
import sys, os, json, time
import numpy as np
HERE = os.getcwd(); sys.path.insert(0, HERE)
from dss_ell import DSSEll, NODES_STD
D, KC = 23.0, 127
z0 = np.load(os.path.join(HERE, "data", f"sol_l1kc127wind23_D{D:.4f}.npy"))
S = DSSEll(kc=KC, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z0[-1], Ks=30, u0=0.04, rk=1)
res = {}
for kap in (0.7, 0.5, 0.35, 0.6):
    t0 = time.time(); st = S.freeze_from(z0, kap); res[kap] = int(sum(st.values()))
    print(f"kappa {kap}: steps {res[kap]} ({time.time() - t0:.1f} s)", flush=True)
ok = res[0.7] == 4179 and 5734 <= res[0.5] <= 5968 and 8190 <= res[0.35] <= 8525 and not (5734 <= res[0.6] <= 5968)
print("PASS" if ok else "FAIL", "(0.7 == 4179; 0.5 in 5734-5968; 0.35 in 8190-8525; the 0.6 control outside the 0.5 range)")
sys.exit(0 if ok else 1)
