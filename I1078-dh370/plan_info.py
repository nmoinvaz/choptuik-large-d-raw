"""#1078: the step plan of a state at hmax 0.05 and at the given hmax (tolerance 1e-32, as lowD_gamma.py plans), the plans' step counts and the state's |F| on each plan
before any polish (max |F| as lowD_gamma.py computes it). usage: plan_info.py STATE.npz HMAX THREADS   (run from hp/, hpkernel importable)"""
import sys, os, time
sys.path.insert(0, os.getcwd())
import numpy as np
from hpkernel.driver import load
import lowD_gamma
from tau_map_gain import nsteps
state, hmax2, threads = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
zh, zl, meta = load(state)
s, grid = lowD_gamma.build_solver(meta["D"], meta["M"], meta, threads)
print(f"{os.path.basename(state)}: D {meta['D']} M {meta['M']} map {grid}; stored plan: {nsteps(meta['segs']) if meta.get('segs') else None} steps")
for h in (0.05, hmax2):
    t = time.time()
    segs = s.plan(zh, zl, 1e-32, h)
    s.set_segs(segs)
    fh, fl = s.residual(zh, zl)
    F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
    print(f"hmax {h}: plan {nsteps(segs)} steps in {len(segs)} segments ({time.time() - t:.1f} s); |F| of the unpolished state on it {F:.3e}", flush=True)
