#!/usr/bin/env python3
"""#1014 step B2: the planner's step count at several (tol_step, hmax), for choosing a plan of at least 4388 steps (coordinator's hc, 2026-11-20 about 06:50 UTC).

    plan_sweep1014.py THREADS STATE TOL:HMAX [TOL:HMAX ...]      prints the number of steps of s.plan(zh, zl, TOL, HMAX) for each pair, and max|F| on it
Control, written before the run: the pair 1e-32:0.05 must reproduce plan_resid1014.py --replan (T82-win M 384 state: 2638 steps, max|F| 2.252e-22)."""
import sys
import time

import numpy as np

from hpkernel.driver import load, make_solver

threads, state = int(sys.argv[1]), sys.argv[2]
zh, zl, m = load(state)
s = make_solver(m["D"], m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads)
zh, zl = np.array(zh), np.array(zl)
for pair in sys.argv[3:]:
    tol, hmax = (float(x) for x in pair.split(":"))
    t = time.time()
    s.set_segs(s.plan(zh, zl, tol, hmax))
    segs = s.get_segs()
    steps = sum(len(g) - 1 for g in segs)
    fh, fl = s.residual(zh, zl)
    F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
    print(f"{state.split('/')[-1]} M {m['M']} tol_step {tol:g} hmax {hmax:g}: {steps} steps, max|F| {F:.3e}, {time.time() - t:.0f} s", flush=True)
