#!/usr/bin/env python3
"""#1014: a state's max |F| on a step plan other than its stored one, and the plan the lowD_dd.py planner (tol_step 1e-32, hmax 0.05) gives it.

    plan_resid1014.py THREADS STATE [--replan | --plan-from CKPT] [--mutate]
      --replan          plan the state itself with s.plan(zh, zl, 1e-32, 0.05) (lowD_dd.py's defaults), print the number of steps and max|F| on that plan
      --plan-from CKPT  use CKPT's stored plan (M may differ: the plan lists steps along x)
      neither           the stored plan (the control: reproduces resid1014.py)
      --mutate          also plant +1e-20 in one low part (must read 1.0e-20: the check can fail)
Controls, written before the runs: my after-call-4 state on its stored plan reads 1.420e-27 (4388 steps), and replanned reads the same plan size 4388 (the planner
reproduces lowD_dd.py's own plan) and about 1.4e-27."""
import sys

import numpy as np

from hpkernel.driver import load, make_solver

threads = int(sys.argv[1])
state = sys.argv[2]
zh, zl, m = load(state)
s = make_solver(m["D"], m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads)
zh, zl = np.array(zh), np.array(zl)
if "--replan" in sys.argv:
    segs = s.plan(zh, zl, 1e-32, 0.05)
    how = "replanned (tol_step 1e-32, hmax 0.05)"
elif "--plan-from" in sys.argv:
    ck = sys.argv[sys.argv.index("--plan-from") + 1]
    segs = load(ck)[2]["segs"]
    how = f"plan of {ck.split('/')[-1]}"
else:
    segs = m["segs"]
    how = "stored plan"
s.set_segs(segs)
steps = sum(len(g) - 1 for g in s.get_segs())
for tag, dz in (("as is", 0.0), ("+1e-20 planted", 1e-20)):
    if dz and "--mutate" not in sys.argv:
        continue
    zl2 = zl.copy()
    if dz:
        zl2[zl.size // 2] += dz
    fh, fl = s.residual(zh, zl2)
    F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
    print(f"{state.split('/')[-1]} M {m['M']} on the {how}, {steps} steps, {tag}: max|F| {F:.3e}", flush=True)
