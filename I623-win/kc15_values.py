#!/usr/bin/env python3
"""#623: F and the constraint of the four k_c = 15 seeds, evaluated the way sigdss_run.py's refine does (SigDSS at kc 15, frozen with kappa 0.5, no Newton step).
usage: OPENBLAS_NUM_THREADS=1 python kc15_values.py        (writes kc15_values.json beside it)
The seeds are rows 0, 1, 2, 4 of data/sigdss_d4eta15.npz in the worktree's solver/matter (eta = inf, 10, 5, 2), D = 4, eps = 1/eta."""
import json
import os
import sys

import numpy as np

MATTER = r"C:\Users\nathan\Source\choptuik-i623\solver\matter"
sys.path.insert(0, MATTER)
from sigdss_solver import NODES_STD, SigDSS  # noqa: E402

D, KAPPA = 4.0, 0.5
d = np.load(os.path.join(MATTER, "data", "sigdss_d4eta15.npz"))
out = {}
for i, (e, eps) in [(0, ("inf", 0.0)), (1, ("10.0000", 0.1)), (2, ("5.0000", 0.2)), (4, ("2.0000", 0.5))]:
    z = d["Z"][i]
    S = SigDSS(kc=15, nodes=NODES_STD, n=D - 2, eps=eps, Delta_ref=z[-1], Ks=16, u0=0.01, N=None)
    S.freeze_from(z, KAPPA)
    F = float(np.linalg.norm(S.residual(z[None, :])[0]))
    out[e] = dict(eps=eps, Delta=float(z[-1]), F=F, constraint=float(S.constraint(z)), N=S.N, row=i, par=float(d["v"][i]))
    print(e, out[e], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kc15_values.json"), "w"), indent=1)
