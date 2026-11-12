"""Residual of a stored state under near_null's system (re-planned, no held offset) and the base polish's (stored plan,
held offset at the state's own coefficients), by block. Scratch probe for #501."""
import os
import sys
import time

import numpy as np

HP = sys.argv[1]
sys.path.insert(0, HP)
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o  # noqa: E402
from renode_o import blocks, fmax, pinned  # noqa: E402

raw, st = sys.argv[2], sys.argv[3]
z, m = load_o(os.path.join(raw, st))
z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
M, nodes = int(m["M"]), list(m["nodes"])
D = m.get("D_str", repr(float(m["D"])))
kf = int(m.get("kfreeze", 3))
s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2, kfreeze=kf)
t = time.time()
plan = s.plan(z[0], z[1], 1e-32, 0.05)
print(f"re-plan {sum(len(g) - 1 for g in plan)} steps ({time.time() - t:.0f} s); stored {sum(len(g) - 1 for g in m['segs'])}", flush=True)
same = len(plan) == len(m["segs"]) and all(len(a) == len(b) and np.allclose(a, b, rtol=0, atol=0) for a, b in zip(plan, m["segs"]))
print("re-plan equals the stored plan:", same, flush=True)
for name, segs in (("near_null plan", plan), ("stored plan", m["segs"])):
    s.set_segs(segs)
    for held in (False, True):
        t = time.time()
        F = pinned(s, z, M, kf).residual_o(z) if held else s.residual_o(z)
        b = blocks(F, M, len(nodes), kf)
        print(f"{name}, {'held offset' if held else 'bare'}: max|F| {fmax(F):.2e} ({time.time() - t:.0f} s); "
              + "; ".join(f"{k} {v:.2e}" for k, v in b.items()), flush=True)
