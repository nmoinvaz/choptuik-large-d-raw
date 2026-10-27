"""T84: how far a single jump in D can go. The full-system residual (kfreeze 13) of a converged state held fixed
(the constant predictor) at D + dD, per block, in the new layout (x85: the pilot's pin7_x85_D73.2707 state, nodes to
0.85) and the old one (T75's pin7_D73.2657, nodes to 0.7). T68's jumps of 2.3 and 4.3 from 67.72 in the old layout
met |F| 1.7e17 and 1.7e27 (comms 2026-10-26 06:30); in the new layout the horizon block responds linearly in dD
(notes/QUAD_DOUBLE.md 12.3, to dD 1e-2). Measured here out to dD 26.7 (D 100).

    python3 jump_resid.py
"""
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import block_norms, load, make_solver  # noqa: E402

R = "/Users/nathan/Source/raw-T84/"
STATES = (("x85", R + "pin7_x85_D73.2707.npz"), ("old 0.7", "/Users/nathan/Source/raw-T75/pin7_D73.2657.npz"))
for name, path in STATES:
    zh, zl, m = load(path)
    D, M = m["D"], m["M"]
    mk = lambda Dx: make_solver(Dx, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=1, kfreeze=13)  # noqa: E731
    s = mk(D)
    segs = s.plan(zh, zl, 1e-32, 0.05)
    print(f"{name}: D {D}, nodes {m['nodes']}, kc {m['kc']} ks {m['ks']}", flush=True)
    for dD in (0.0, 0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0 - D):
        sx = mk(D + dD)
        sx.set_segs(segs)
        Fh, Fl = sx.residual(zh, zl)
        b = block_norms(sx, np.asarray(Fh), np.asarray(Fl))
        fin = np.isfinite(np.asarray(Fh)).all()
        print(f"  dD {dD:6.2f} (D {D + dD:7.3f}): max |F| {max(b):.1e}, blocks " + " ".join(f"{v:.1e}" for v in b)
              + ("" if fin else "  NON-FINITE"), flush=True)
