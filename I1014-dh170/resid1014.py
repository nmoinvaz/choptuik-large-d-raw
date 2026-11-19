#!/usr/bin/env python3
"""#1014: max |F| of saved M 320 checkpoints, the residual lowD_dd.py's Newton prints, at the checkpoint's own step plan.
    resid1014.py THREADS CKPT... [--mutate]
Controls (written before the run): the after_call3 checkpoint must give the 2.22e-27 that Newton call 4 printed as its start |F|
(within 1%); a planted 1e-20 in one low part of the after_call4 state must raise its |F| above 1e-26 (the check can fail)."""
import json
import sys

import numpy as np

from hpkernel.driver import load, make_solver  # noqa: E402

threads = int(sys.argv[1])
files = [a for a in sys.argv[2:] if not a.startswith("--")]
mut = "--mutate" in sys.argv
out = {}
s = None
for f in files:
    zh, zl, m = load(f)
    if s is None:
        s = make_solver(m["D"], m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads)
    s.set_segs(m["segs"])
    zh, zl = np.array(zh), np.array(zl)
    for tag, dz in (("", 0.0), ("+1e-20", 1e-20)):
        if tag and not mut:
            continue
        zl2 = zl.copy()
        if tag:
            zl2[zl.size // 2] += dz
        fh, fl = s.residual(zh, zl2)
        F = float(np.abs(np.asarray(fh) + np.asarray(fl)).max())
        print(f"{f.split('/')[-1]} {tag or 'as saved'}: max|F| {F:.3e}  Delta {zh[-1]!r} {zl[-1]!r}", flush=True)
        out[f.split("/")[-1] + tag] = F
json.dump(out, open("resid1014.json", "w"), indent=1)
