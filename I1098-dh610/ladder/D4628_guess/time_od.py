"""times form S's octo-double residual at a saved state with ks overridden (the serial horizon block's cost)

    python3 time_od.py HP_DIR STATE KS THREADS
"""
import sys, time
hp_dir, path, ks, thr = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, hp_dir)
import mpmath as mp, numpy as np
import form_s
from octo_corrector import load_o
z8, m = load_o(path)
with mp.workdps(60):
    D = mp.mpf(m["D_str"])
s = form_s.make_solver_s(D, int(m["M"]), list(m["nodes"]), kt=int(m.get("kt", 36)), kc=int(m["kc"]), ks=ks, threads=thr,
                         kfreeze=13, segs=m["segs"], mob=float(m["hmob"]))
t0 = time.time()
F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(8)])
print(f"{path.split('/ladder/')[-1]}: x_l {m['nodes'][-1]:.7f}, ks {ks}: od max |F| "
      f"{np.abs(np.asarray(F[0]) + np.asarray(F[1])).max():.3e} ({time.time() - t0:.1f} s)", flush=True)
