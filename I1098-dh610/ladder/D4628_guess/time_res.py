"""times form S's residual (dd, qd, od) and form A's plan at a saved state's layout"""
import sys, time
hp_dir, path, thr = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, hp_dir)
import mpmath as mp, numpy as np
import form_s
from octo_corrector import load_o
z8, m = load_o(path)
with mp.workdps(60):
    D = mp.mpf(m["D_str"])
kw = dict(kt=int(m.get("kt", 36)), kc=int(m["kc"]), ks=int(m["ks"]), threads=thr, segs=m["segs"], mob=float(m["hmob"]))
s = form_s.make_solver_s(D, int(m["M"]), list(m["nodes"]), kfreeze=13, **kw)
for parts in (2, 4, 8):
    t0 = time.time()
    F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(parts)])
    print(f"{parts} parts: max |F| {np.abs(np.asarray(F[0]) + np.asarray(F[1])).max():.3e} ({time.time() - t0:.1f} s)", flush=True)
