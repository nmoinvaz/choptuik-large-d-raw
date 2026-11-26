"""#1099: the octo-double residual (HP_EXACT_RECIP=1, the exact reciprocals) at recip_check's D 300 and D 1000 states with
the hpkernel on PYTHONPATH, saved for a bit-for-bit comparison of two builds: OUT.npz holds each state's eight part
arrays and the residual with every Taylor step halved."""
import os
import sys

import numpy as np

os.environ["HP_EXACT_RECIP"] = os.environ.get("RECIP_BITS_EXACT", "1")
import hpkernel  # noqa: E402
import form_s  # noqa: E402
from mpmath import mp  # noqa: E402
from octo_corrector import load_o  # noqa: E402
from recip_check import halve  # noqa: E402

print("hpkernel", hpkernel.__file__, flush=True)
out = {}
for tag, path in (("d300", sys.argv[2]), ("d1000", sys.argv[3])):
    z8, meta = load_o(path)
    with mp.workdps(60):
        D = mp.mpf(meta["D_str"])
    for name, segs in (("", meta["segs"]), ("_halved", [halve(g) for g in meta["segs"]])):
        kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=4, segs=segs,
                  mob=float(meta.get("hmob", 0.0) or 0.0))
        s = form_s.make_solver_s(D, int(meta["M"]), list(meta["nodes"]), kfreeze=13, **kw)
        F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(8)])
        out[tag + name] = np.array([np.asarray(f) for f in F])
        print(tag + name, "max |F|", float(np.abs(out[tag + name][0]).max()), flush=True)
np.savez(sys.argv[1], **out)
