#!/usr/bin/env python3
"""#1014 step C: my lifted M 320 state (states/lowD1014_D3.0475_M320.npz) with its stored 4388-step plan replaced by the planner's own plan on the converged state
(s.plan(zh, zl, 1e-32, 0.05): lowD_dd.py's defaults), saved as states/lowD1014_D3.0475_M320_plan1820.npz. The vector is untouched.
Checks (written before the run): the plan has 1820 steps (plan_resid1014.py's replan), max|F| on it is 1.420e-27 as on the 4388-step plan, the vector is byte-identical,
and the meta keeps every other key. --mutate: scale the saved vector's last unknown by 1+1e-9 and the |F| check must fail (exit 1)."""
import json
import os
import sys

import numpy as np

from hpkernel.driver import load, make_solver, save

HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, "states/lowD1014_D3.0475_M320.npz")
dst = os.path.join(HERE, "states/lowD1014_D3.0475_M320_plan1820" + ("_MUT" if "--mutate" in sys.argv else "") + ".npz")      # --mutate never touches the real file
zh, zl, m = load(src)
s = make_solver(m["D"], m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=3)
zh, zl = np.array(zh), np.array(zl)
s.set_segs(s.plan(zh, zl, 1e-32, 0.05))
segs = [[float(x) for x in g] for g in s.get_segs()]
steps = sum(len(g) - 1 for g in segs)
m2 = dict(m)
m2["segs"] = segs
if "--mutate" in sys.argv:
    zh = zh.copy()
    zh[-1] *= 1 + 1e-9
save(dst, zh, zl, m2)
zh2, zl2, m3 = load(dst)
s.set_segs(m3["segs"])
fh, fl = s.residual(np.array(zh2), np.array(zl2))
F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
same = np.array_equal(zh2, np.load(src)["zh"]) and np.array_equal(zl2, np.load(src)["zl"])
keys = set(m3) == set(m)
ok = steps == 1820 and abs(F - 1.420e-27) < 5e-30 and same and keys
print(f"plan {steps} steps, max|F| {F:.3e}, vector identical {same}, meta keys kept {keys}: {'pass' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
