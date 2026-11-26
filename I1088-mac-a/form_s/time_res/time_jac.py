"""Time one double-double Newton step (qj_step: the dd Jacobian and its solve) of form S's held system on a saved
lastnode state at each horizon order ks given, and the step's Delta component (#1088 cost of ks)."""
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import HeldS, held_field, make_solver_s, qj_step  # noqa: E402
from octo_corrector import load_o  # noqa: E402

path, kss, thr = sys.argv[1], [int(k) for k in sys.argv[2].split(",")], int(sys.argv[3])
z8, meta = load_o(path)
with mp.workdps(60):
    Dt = mp.mpf(meta["D_str"])
for ks in kss:
    kw = dict(kt=int(meta["kt"]), kc=int(meta["kc"]), ks=ks, threads=thr, segs=meta["segs"], mob=float(meta["hmob"]))
    s = make_solver_s(Dt, 32, list(meta["nodes"]), kfreeze=3, **kw)
    sh = HeldS(s, 32, 5, held_field(z8, 32))
    t0 = time.time()
    F = sh.residual_s([np.ascontiguousarray(z8[q]) for q in range(2)])
    t1 = time.time()
    d, gain = qj_step(sh, z8, F, gain=True, parts=2)
    t2 = time.time()
    print(f"D {float(Dt):g} ks {ks}: dd residual {t1 - t0:.1f} s, dd step (J, solves) {t2 - t1:.1f} s, step's dDelta "
          f"{float(np.asarray(d[0])[-1]):+.3e}, gain {gain:.3e}", flush=True)
