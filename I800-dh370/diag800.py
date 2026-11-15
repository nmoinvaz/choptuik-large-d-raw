#!/usr/bin/env python3
"""#800 (the coordinator): where the rung w = 1/64's start max|F| 9.4e44 comes from. The octo-double residual of t0's
base (ks 250, converged at w = 0 from order 131) on wip/i800's build, unpinned, with the solver made as anm_run makes
it (its stored plan), for several (ks_w, ks_w_from). Printed per case: max |F| over all rows, its row and block, the
horizon block's max, and max |F(case) - F(w 0)|. horizon_radius.py (main) reads the full tail at this base as 1.3e-17
in the m rows, so w = 1 must lie near that and w = 1/64 near 1/64 of it, if the weighting is right."""
import sys
import mpmath as mp
import numpy as np
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-800/hp")
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o, o8  # noqa: E402

P = "/home/nathan/Source/choptuik-large-d-raw/I800-dh370/t0/base_pin3_D245.1366.npz"
z8, m = load_o(P)
D, M = mp.mpf(m["D_str"]), int(m["M"])
print(f"t0 base: D {m['D_str']}, M {M}, ks {m.get('ks')}, ks_w {m.get('ks_w')}, ks_w_from {m.get('ks_w_from')}, "
      f"plan {sum(len(s) - 1 for s in m['segs'])} steps")
L = len(z8[0]); Kb = (L - 1) // (4 * M) - 1
cases = [(250, 0.0, 131), (250, 1 / 64, 131), (250, 1.0, 131), (250, 0.5, 131), (250, 1 / 64, 0), (130, 1.0, 0)]
F0 = None
for ks, w, fr in cases:
    s = make_solver(D, M, nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=ks, threads=1, kfreeze=3,
                    horizon_alpha=0, ks_w=w, ks_w_from=fr)
    s.set_segs(m["segs"])
    F = o8(s.residual_o(list(o8(z8))))
    f = np.abs(np.asarray(F[0]) + np.asarray(F[1]))
    i = int(np.argmax(f)); blk = i // (4 * M)
    h = f[Kb * 4 * M:(Kb + 1) * 4 * M].max()
    d = ""
    if (ks, w, fr) == (250, 0.0, 131):
        F0 = f.copy(); Fs0 = F
    elif ks == 250:
        dd = np.abs((np.asarray(F[0]) - np.asarray(Fs0[0])) + (np.asarray(F[1]) - np.asarray(Fs0[1])))
        d = f", max |F - F(w 0)| {dd.max():.3e} at row {int(np.argmax(dd))}"
    print(f"ks {ks} ks_w {w:.6g} from {fr}: max|F| {f.max():.3e} at row {i} (block {blk} of {Kb + 1}, field {(i % (4 * M)) // M}), "
          f"horizon block max {h:.3e}{d}", flush=True)
