"""#1104 winb: the step count freeze_from gives for my k_c 143 D 23.0 state at kappa 0.7 (the record's 4705) and at kappa 0.5 (t5's bar 6587 +- 132); read-only, one call each. usage: steps_check_1104.py STATE REC WTM"""
import json, os, sys, time
st, recf, wtm = sys.argv[1:4]
sys.path.insert(0, wtm); os.chdir(wtm)
import numpy as np
from dss_ell import DSSEll, NODES_STD
rec = [json.loads(x) for x in open(recf) if x.strip()][-1]
z = np.load(st)
S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=rec["D"] - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
for kap in (0.7, 0.5):
    t0 = time.time(); n = sum(S.freeze_from(z, kap).values())
    print(f"kappa {kap}: steps {n} ({time.time() - t0:.1f} s)")
