#!/usr/bin/env python3
"""#800 (the coordinator), third part: does the octo-double residual of t0's base depend on what the process ran
before? diag800.py (od only) read the horizon block at w 0 as 3.1e29 and the tail as 6.4e60; diag800b.py (qd first)
read the tail as 1.3e-17. Order here: od at w 0 and w 1 on fresh solvers, then one qd residual, then od again on fresh
solvers, then od again on the first solvers. Raw (unpinned) max |F| of the horizon block and of the rest."""
import sys
import mpmath as mp
import numpy as np
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-800/hp")
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o, o8  # noqa: E402

P = "/home/nathan/Source/choptuik-large-d-raw/I800-dh370/t0/base_pin3_D245.1366.npz"
z8, m = load_o(P)
D, M = mp.mpf(m["D_str"]), int(m["M"])
L = len(z8[0]); Kb = (L - 1) // (4 * M) - 1
z4 = [np.ascontiguousarray(np.asarray(p)) for p in z8[:4]]
def mk(ks=250, w=0.0, fr=131):
    s = make_solver(D, M, nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=ks, threads=1, kfreeze=3,
                    horizon_alpha=0, ks_w=w, ks_w_from=fr)
    s.set_segs(m["segs"])
    return s
def show(tag, F):
    f = np.abs(np.asarray(F[0]) + np.asarray(F[1]))
    print(f"{tag}: horizon block max {f[Kb * 4 * M:].max():.3e}, other blocks {f[:Kb * 4 * M].max():.3e}", flush=True)
    return f
a0, a1 = mk(w=0.0), mk(w=1.0)
f0 = show("1 od fresh w 0", o8(a0.residual_o(list(o8(z8)))))
f1 = show("2 od fresh w 1", o8(a1.residual_o(list(o8(z8)))))
show("3 qd fresh w 0", a0.residual_q(*z4) if False else mk(w=0.0).residual_q(*z4))
f0b = show("4 od fresh w 0 after qd", o8(mk(w=0.0).residual_o(list(o8(z8)))))
f1b = show("5 od fresh w 1 after qd", o8(mk(w=1.0).residual_o(list(o8(z8)))))
show("6 od first solver w 0 again", o8(a0.residual_o(list(o8(z8)))))
show("7 od fresh w 0 twice", o8(mk(w=0.0).residual_o(list(o8(z8)))))
print(f"tail before qd {np.abs(f1 - f0).max():.3e}, after {np.abs(f1b - f0b).max():.3e}; "
      f"od w 0 before and after qd differ by {np.abs(f0 - f0b).max():.3e}", flush=True)
