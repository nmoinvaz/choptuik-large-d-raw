"""#1078: how the step plan of a state depends on hmax (tolerance 1e-32 as lowD_gamma.py plans): step count, segments, the largest step, the number of steps above 0.0125 and
0.025. usage: plan_scan.py STATE.npz THREADS HMAX [HMAX ...]  (run from hp/)"""
import sys, os
sys.path.insert(0, os.getcwd())
import numpy as np
from hpkernel.driver import load
import lowD_gamma
from tau_map_gain import nsteps
state, threads, hs = sys.argv[1], int(sys.argv[2]), [float(v) for v in sys.argv[3:]]
zh, zl, meta = load(state)
s, grid = lowD_gamma.build_solver(meta["D"], meta["M"], meta, threads)
for h in hs:
    segs = s.plan(zh, zl, 1e-32, h)
    d = np.concatenate([np.diff(np.asarray(g, float)) for g in segs])
    print(f"hmax {h:g}: {nsteps(segs)} steps in {len(segs)} segments; largest step {np.abs(d).max():.5f}; steps above 0.0125: {int((np.abs(d) > 0.0125).sum())}, above 0.025: {int((np.abs(d) > 0.025).sum())}", flush=True)
