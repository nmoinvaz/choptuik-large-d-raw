"""scratch: the f64 leading part of the octo-double Jacobian at a stored state, as near_null.py forms the system"""
import os
import sys
import time

import numpy as np

HP = sys.argv[1]
sys.path.insert(0, HP)
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o  # noqa: E402

raw, st, out = sys.argv[2:5]
z, m = load_o(os.path.join(raw, st))
z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
M, nodes = int(m["M"]), list(m["nodes"])
D = m.get("D_str", repr(float(m["D"])))
s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130),
                threads=2, kfreeze=int(m.get("kfreeze", 3)))
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
t0 = time.time()
J = [np.asarray(p) for p in s.jacobian_o(z)]
print(f"jacobian_o {time.time() - t0:.0f} s, L {len(z[0])}, M {M}, nodes {nodes}", flush=True)
np.savez(out, J0=J[0], J1=J[1], M=M, K=len(nodes))
