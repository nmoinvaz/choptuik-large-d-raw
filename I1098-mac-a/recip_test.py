"""The horizon series' 1/k in dd against lane precision (Ctx::exact_recip, #1098): a saved state's od residual with
exact_recip 0 (what form S has used) and 1, per block, and their difference.

    python3 recip_test.py STATE [KFREEZE]
"""
import sys

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import blocks_s, make_solver_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

z8, meta = load_o(sys.argv[1])
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
M = int(meta["M"])
kf = int(sys.argv[2]) if len(sys.argv) > 2 else 13
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=2, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
Fs = []
for mode in (0, 1):
    s = make_solver_s(D, M, list(meta["nodes"]), kfreeze=kf, **kw)
    s.set_exact_recip(mode, 0)
    F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(8)])
    Fs.append(np.asarray(F[0]) + np.asarray(F[1]))
    print(f"D {float(D):g} mob {kw['mob']:g} exact_recip {mode}: od max |F| {np.abs(Fs[-1]).max():.3e}, blocks "
          + " ".join(f"{b:.1e}" for b in blocks_s(F, M, len(meta["nodes"]))), flush=True)
d = Fs[1] - Fs[0]
print(f"  max |F1 - F0| {np.abs(d).max():.3e} at row {int(np.argmax(np.abs(d)))}", flush=True)
