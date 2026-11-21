#!/usr/bin/env python3
"""resid1067.py THREADS CKPT [--plant P]: max |F| of a saved lowD_dd.py checkpoint at its own step plan (as dh170's ref/resid1014.py, which this is a copy of), with the planted control scaled to the checkpoint:
the as-saved max|F| X, then max|F| after P is added to one low part (index size // 2) of the vector. dh170's control planted a fixed 1e-20, which a checkpoint with max|F| above 1e-20 cannot show (after call 1 at
M 512 the checkpoint's max|F| is 9.6e-13); here P defaults to 1e-20 and run1067_s1.py passes 1e3 times the as-saved max|F| from a first call without --plant. Prints 'as saved: max|F| X' and 'planted P: max|F| Y'."""
import sys

import numpy as np

from hpkernel.driver import load, make_solver

threads = int(sys.argv[1])
ckpt = sys.argv[2]
plant = float(sys.argv[sys.argv.index("--plant") + 1]) if "--plant" in sys.argv else None   # --plant 0 evaluates the planted case with nothing planted
zh, zl, m = load(ckpt)
s = make_solver(m["D"], m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads)
s.set_segs(m["segs"])
zh, zl = np.array(zh), np.array(zl)
for tag, dz in (("as saved", 0.0), (f"planted {plant:g}" if plant is not None else "planted none", plant or 0.0)):
    if tag != "as saved" and plant is None:
        continue
    zl2 = zl.copy()
    if dz:
        zl2[zl.size // 2] += dz
    fh, fl = s.residual(zh, zl2)
    F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
    print(f"{ckpt.split('/')[-1]} {tag}: max|F| {F:.3e}  Delta {zh[-1]!r} {zl[-1]!r}", flush=True)
