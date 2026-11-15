#!/usr/bin/env python3
"""#800 (the coordinator), second part: the tail's contribution F(ks 250, w 1) - F(w 0) at t0's base in octo-double and
in quad-double on anm_run's five-node solver, and horizon_radius's two-node H at ks 250 and at ks 130 on this build."""
import sys
import mpmath as mp
import numpy as np
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-800/hp")
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o, o8  # noqa: E402
import horizon_radius as H  # noqa: E402

P = "/home/nathan/Source/choptuik-large-d-raw/I800-dh370/t0/base_pin3_D245.1366.npz"
z8, m = load_o(P)
D, M = mp.mpf(m["D_str"]), int(m["M"])
L = len(z8[0]); Kb = (L - 1) // (4 * M) - 1
def mk(ks, w, fr):
    s = make_solver(D, M, nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=ks, threads=1, kfreeze=3,
                    horizon_alpha=0, ks_w=w, ks_w_from=fr)
    s.set_segs(m["segs"])
    return s
z4 = [np.ascontiguousarray(np.asarray(p)) for p in z8[:4]]
for prec in ("qd", "od"):
    F = {}
    for w in (0.0, 1.0):
        s = mk(250, w, 131)
        F[w] = s.residual_q(*z4) if prec == "qd" else o8(s.residual_o(list(o8(z8))))
    d = np.abs((np.asarray(F[1.0][0]) - np.asarray(F[0.0][0])) + (np.asarray(F[1.0][1]) - np.asarray(F[0.0][1])))
    i = int(np.argmax(d))
    print(f"{prec} five-node: max |F(w 1) - F(w 0)| {d.max():.3e} at row {i} (block {i // (4 * M)}, field {(i % (4 * M)) // M}); "
          f"horizon block {d[Kb * 4 * M:].max():.3e}, other blocks {d[:Kb * 4 * M].max():.3e}", flush=True)
for ks in (130, 250):
    mm = dict(m); mm["ks"] = ks
    sr = H.Series([np.asarray(p) for p in z8], mm, threads=1)
    b, Hr = sr.terms("qd", ks)
    t = np.abs(b).max(axis=(1, 2))
    print(f"two-node qd at ks {ks}: H {dict(zip(H.FIELDS, [f'{x:.2e}' for x in Hr]))}, sum of t_k over 131..{ks} "
          f"{t[131:].sum() if ks > 130 else 0:.3e}, max t_k past 130 {t[131:].max() if ks > 130 else 0:.3e}", flush=True)
