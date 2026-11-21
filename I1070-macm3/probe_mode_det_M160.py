# #1070 macm3b: a probe, not a run. Does Solver.mode_det accept the M 160 state? The calls of hp/lowD_gamma.py without the polish; no output file.
# Run from the worktree's hp/: ~/Source/venv-macm3-1058b/bin/python -I probe_mode_det_M160.py
import sys, os, time
sys.path.insert(0, os.getcwd())
from hpkernel.driver import load, make_solver
f = os.path.expanduser("~/Source/choptuik-large-d-raw-749p/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz")
zh, zl, meta = load(f); t = time.time()
s = make_solver(meta["D"], meta["M"], nodes=meta["nodes"], kt=meta.get("kt", 36), kc=meta.get("kc", 60), ks=meta.get("ks", 100), threads=2)
s.set_segs(s.plan(zh, zl, 1e-32, 0.05))
try:
    print(s.mode_det(zh, zl, 4.397784106690153, 0.0))
except Exception as e:
    print(type(e).__name__, e, f"({time.time()-t:.1f} s)")
