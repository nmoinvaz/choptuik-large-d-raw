"""Time form S's held residual in double-, quad- and octo-double on a saved lastnode guess (#1088 cost estimate)."""
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import HeldS, held_field, make_solver_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

path, parts_list, thr = sys.argv[1], [int(p) for p in sys.argv[2].split(",")], int(sys.argv[3])
z8, meta = load_o(path)
with mp.workdps(60):
    Dt = mp.mpf(meta["D_str"])
kw = dict(kt=int(meta["kt"]), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=thr, segs=meta["segs"], mob=float(meta["hmob"]))
t0 = time.time()
s = make_solver_s(Dt, 32, list(meta["nodes"]), kfreeze=3, **kw)
sh = HeldS(s, 32, 5, held_field(z8, 32))
print(f"D {float(Dt):g} ks {meta['ks']}: setup {time.time() - t0:.1f} s", flush=True)
for p in parts_list:
    t0 = time.time()
    F = sh.residual_s([np.ascontiguousarray(z8[q]) for q in range(p)])
    nF = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
    print(f"  {p} parts: max |F| {nF:.3e}, {time.time() - t0:.1f} s", flush=True)
