"""Diagnostic: det M at real lambda on a state with its layout changed, without the setup gate.
argv: STATE kf mode lams; mode 'drop_last' removes the last node (state unchanged elsewhere, not re-converged),
'add_outer' adds a node at half the last node's distance to the horizon and re-converges (Newton, then LM)."""
import sys, time
import numpy as np
WT = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a92db8e6b268598e4/hp"
sys.path.insert(0, WT)
import modecount_common as mc
from hpkernel.driver import load, newton_solve, lm_solve
path, kf, mode = sys.argv[1], (None if sys.argv[2] == "none" else int(sys.argv[2])), sys.argv[3]
lams = [float(v) for v in sys.argv[4].split(",")]
zh, zl, meta = load(path)
M, nodes = meta["M"], list(meta["nodes"])
K = len(nodes)
if mode == "drop_last":
    o = 2 * M + 4 * M * (K - 1)
    zh = np.concatenate([zh[:o], zh[o + 4 * M:]])
    zl = np.concatenate([zl[:o], zl[o + 4 * M:]])
    meta = dict(meta, nodes=nodes[:-1])
elif mode == "add_outer":
    s = mc.build_solver(meta, zh, zl, M, kf)
    zh, zl, meta = mc.add_node(s, zh, zl, meta, 1)
s, c = mc.build_pair(meta, zh, zl, M, kf)
F = mc.resid(s, zh, zl)
print(f"{mode}: M {M} nodes {meta['nodes']} |F| {F:.2e}; " + mc.tails_text([mc.series_tail(s, zh, zl, meta, w) for w in (0, 1)]), flush=True)
if mode == "add_outer" and F > 1e-22:
    zh, zl, _ = newton_solve(s, zh, zl, tol=1e-24, it_max=8, verbose=True)
    F = mc.resid(s, zh, zl)
    if F > 1e-22:
        zh, zl, _ = lm_solve(s, zh, zl, tol=1e-27, it_max=10, verbose=True, newton_after=1e-22)
        F = mc.resid(s, zh, zl)
    print(f"  re-converged |F| {F:.2e}", flush=True)
zh, zl = np.ascontiguousarray(zh), np.ascontiguousarray(zl)
for lam in lams:
    t = time.time()
    r = s.mode_det(zh, zl, lam, 0.0)
    t1 = time.time() - t
    t = time.time()
    q = c.mode_det(zh, zl, lam, 0.0)
    print(f"  lam {lam}: hpkernel {r} ({t1:.0f} s)\n            cx {q} ({time.time() - t:.0f} s)", flush=True)
