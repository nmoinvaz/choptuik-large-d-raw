#!/usr/bin/env python3
"""Which rows of residual_jet_q (and residual_jet, dd) differ between two builds, at xsolve_bits.py's first state and
its jet (z, z / 1000), 2 orders.

    PYTHONPATH=<site> python3 jetq_rows.py HPDIR RAWDIR OUT.npz
    python3 jetq_rows.py cmp A.npz B.npz
"""
import os
import sys

import numpy as np

if sys.argv[1] == "cmp":
    A, B = np.load(sys.argv[2]), np.load(sys.argv[3])
    for k in A.files:
        a, b = A[k], B[k]
        rows = np.nonzero((a.view(np.uint64) != b.view(np.uint64)).reshape(-1, a.shape[-1]).any(axis=0))[0]
        print(k, a.shape, "differing rows:", rows[:20], "count", len(rows))
    sys.exit(0)
hp, raw, out = sys.argv[1:4]
sys.path.insert(0, hp)
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o  # noqa: E402
z8, m = load_o(os.path.join(raw, "anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz"))
z8 = [np.ascontiguousarray(np.array(p, dtype=float)) for p in z8]
z4 = z8[:4]
D = m.get("D_str", repr(float(m["D"])))
s = make_solver(D, int(m["M"]), nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130),
                threads=2, kfreeze=m.get("kfreeze", 3))
s.set_segs(s.plan(z4[0], z4[1], 1e-32, 0.05))
jq = s.residual_jet_q([tuple(z4), tuple(p / 1000 for p in z4)], 2)
jq9 = s.residual_jet_q([tuple(z4), tuple(p / 1000 for p in z4)], 2, mutate=9)
jd = s.residual_jet([z4[0], z4[0] / 1000], [z4[1], z4[1] / 1000], 2)
np.savez(out, jq=np.array(jq), jq9=np.array(jq9), jd=np.array(jd))
print("wrote", out)
