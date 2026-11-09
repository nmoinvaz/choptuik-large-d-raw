import os, sys, glob
import numpy as np
WT = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a92db8e6b268598e4/hp"
sys.path.insert(0, WT)
from hpkernel.driver import load
import modecount_common as mc
paths = sys.argv[1:]
worst = 0
for p in paths:
    zh, zl, meta = load(p)
    s = mc.build_solver(meta, zh, zl, meta["M"], None)
    t = [mc.series_tail(s, zh, zl, meta, w) for w in (0, 1)]
    w = max(x["tail"] for x in t)
    worst = max(worst, w)
    print(f"{os.path.basename(p):46s} D {meta['D']:8.4f} M {meta['M']:3d} nodes {meta['nodes'][0]:g}..{meta['nodes'][-1]:g} "
          f"kc {meta['kc']} ks {meta['ks']}: centre {t[0]['tail']:.1e} (r {t[0]['radius']:.3f}) horizon {t[1]['tail']:.1e} "
          f"(r {t[1]['radius']:.3f})  {'ok' if w <= mc.SERIES_TAIL else 'GATE FIRES'}", flush=True)
print(f"worst {worst:.1e}")
