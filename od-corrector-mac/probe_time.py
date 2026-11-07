import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q, qmax
from reseed import pinned
raw = "/Users/nathan/Source/choptuik-large-d-raw"
z4, meta = load_q(os.path.join(raw, sys.argv[1]))
D = mp.mpf(meta["D_str"])
s, sp, sq = pinned(meta, D, z4, threads=3)
print("L", len(z4[0]), "M", meta["M"], "nodes", len(meta["nodes"]), "kfreeze", meta["kfreeze"], "segs", len(s.get_segs()))
print("|c| max", float(np.abs(sp.ch).max()), "nonzero", int((sp.ch != 0).sum()))
t = time.time(); F = sq.residual_q(*z4); print("residual_q", round(time.time() - t, 1), "s, max", qmax(F))
z8 = [np.ascontiguousarray(p) for p in z4] + [np.zeros(len(z4[0]))] * 4
t = time.time(); F8 = s.residual_o(z8); print("residual_o", round(time.time() - t, 1), "s")
t = time.time(); st = sq.newton_q(*z4); print("newton_q", round(time.time() - t, 1), "s", s.step_timing(), "piv", st[6], st[7])
t = time.time(); so = s.newton_o(z8); print("newton_o", round(time.time() - t, 1), "s", s.step_timing(), "piv", so[3], so[4])
