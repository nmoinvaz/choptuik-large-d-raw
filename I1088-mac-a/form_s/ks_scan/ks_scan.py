"""The held form-S residual of a saved lastnode state at each horizon order ks given (#1088's ks reduction): its max |F|,
its horizon block, and the largest change of any row against the residual at the last (reference) ks, in the given
part count (2 dd, 4 qd), with the time of each evaluation.

    python3 ks_scan.py STATE KS1,KS2,...,KSREF PARTS THREADS
"""
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import HeldS, blocks_s, held_field, make_solver_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

path, kss, parts, thr = sys.argv[1], [int(k) for k in sys.argv[2].split(",")], int(sys.argv[3]), int(sys.argv[4])
z8, meta = load_o(path)
with mp.workdps(60):
    Dt = mp.mpf(meta["D_str"])
n = float(Dt) - 2
print(f"D {float(Dt):g} (n/2 = {n / 2:.0f}), state {path.split('/')[-1]} (its ks {meta['ks']}), {parts} parts", flush=True)
res = {}
for ks in kss:
    kw = dict(kt=int(meta["kt"]), kc=int(meta["kc"]), ks=ks, threads=thr, segs=meta["segs"], mob=float(meta["hmob"]))
    s = make_solver_s(Dt, 32, list(meta["nodes"]), kfreeze=3, **kw)
    sh = HeldS(s, 32, 5, held_field(z8, 32))
    t0 = time.time()
    F = sh.residual_s([np.ascontiguousarray(z8[q]) for q in range(parts)])
    res[ks] = (np.asarray(F[0]), np.asarray(F[1]), time.time() - t0, blocks_s(F, 32, 5))
ref = kss[-1]
for ks in kss:
    Fh, Fl, ts, b = res[ks]
    d = float(np.abs((Fh - res[ref][0]) + (Fl - res[ref][1])).max())
    print(f"  ks {ks:6d} ({ks / n:.3f} n): max |F| {float(np.abs(Fh + Fl).max()):.3e}, horizon block {b[5]:.3e}, "
          f"max |F - F(ks {ref})| {d:.3e} ({ts:.1f} s)", flush=True)
