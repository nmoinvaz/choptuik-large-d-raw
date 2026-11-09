"""Control for the D = 30 M = 48 no-cut layout: the M 32 state resampled to M = 48 as setup does, with a node added at
0.15 (modecount_common.add_node), re-converged as setup does (Newton, then Levenberg-Marquardt); prints |F|, Delta and
the series truncations, and saves the state to argv[2]."""
import sys, time
import numpy as np
WT = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a92db8e6b268598e4/hp"
sys.path.insert(0, WT)
import modecount_common as mc
from hpkernel.driver import load, save, newton_solve, lm_solve
zh, zl, meta = load(sys.argv[1])
M = 48
zh, zl, meta = mc.resample_state(zh, zl, meta, M, None)
s = mc.build_solver(meta, zh, zl, M, None)
zh, zl, meta = mc.add_node(s, zh, zl, meta, 0)
s = mc.build_solver(meta, zh, zl, M, None)
F = mc.resid(s, zh, zl)
print(f"nodes {meta['nodes']}: |F| {F:.2e}; truncations " + mc.tails_text([mc.series_tail(s, zh, zl, meta, w) for w in (0, 1)]), flush=True)
t = time.time()
zh, zl, hist = newton_solve(s, zh, zl, tol=1e-24, it_max=12, verbose=True)
F = mc.resid(s, zh, zl)
print(f"after Newton |F| {F:.2e} ({time.time() - t:.0f} s)", flush=True)
if F > 1e-24:
    zh, zl, hist = lm_solve(s, zh, zl, tol=1e-27, it_max=20, verbose=True, newton_after=1e-22)
    F = mc.resid(s, zh, zl)
    print(f"after LM |F| {F:.2e} ({time.time() - t:.0f} s)", flush=True)
print(f"Delta {zh[-1]!r} {zl[-1]:+.3e}; truncations " + mc.tails_text([mc.series_tail(s, zh, zl, meta, w) for w in (0, 1)]), flush=True)
save(sys.argv[2], zh, zl, dict(meta, F=F))
