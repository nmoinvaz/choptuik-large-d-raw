"""The M 48 plan of chain_dM.py's D 80 solution against the plan resolution_check.py makes at its start (#636)."""
import json
import os
import sys

HP = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a85c4feb2fd2f0829/hp"
sys.path.insert(0, HP)
import numpy as np
import mpmath as mp
import resolution_check as rc
from hpkernel.driver import load_q, make_solver

R = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i636/"
z, m = load_q(R + "T138-win2/chain/anm_pin3_D80.0000.npz")
K = 5
v0 = rc.mp_of(z)
z4 = rc.split4(rc.resample_mp(v0, 32, 48, K))
s = make_solver(mp.mpf("80.0"), 48, nodes=list(m["nodes"]), kt=36, kc=146, ks=130, threads=2, kfreeze=3)
segs_rc = [[float(x) for x in sg] for sg in s.plan(np.asarray(z4[0]), np.asarray(z4[1]), 1e-32, 0.05)]
d = np.load(sys.argv[1])
segs_me = json.loads(str(d["meta"]))["segs"]
print("resolution_check plan steps", [len(sg) - 1 for sg in segs_rc], "chain_dM plan steps", [len(sg) - 1 for sg in segs_me])
same = len(segs_rc) == len(segs_me) and all(len(a) == len(b) and all(x == y for x, y in zip(a, b)) for a, b in zip(segs_rc, segs_me))
print("identical" if same else "DIFFERENT",
      max((abs(x - y) for a, b in zip(segs_rc, segs_me) for x, y in zip(a, b)), default=None))
