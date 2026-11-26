"""The B slaving's refinement count against the residual (#1098: is the D 300 last-segment term its floor?): the
full system's octo-double residual (kfreeze 13) of a saved state under the environment's HP_SLAVE_REFINE_OD (set by the
caller; read once per process), its max |F| per block and the largest change against a reference residual file if
given (the default count's), saved as npz for the comparison.

    HP_SLAVE_REFINE_OD=N python3 refine_test.py STATE OUT.npz [REF.npz]
"""
import os
import sys

import numpy as np

sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-1088a/hp")
from mpmath import mp  # noqa: E402

from form_s import blocks_s, make_solver_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

path, out = sys.argv[1], sys.argv[2]
ref = sys.argv[3] if len(sys.argv) > 3 else None
z8, meta = load_o(path)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
M = int(meta["M"])
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=2, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
s = make_solver_s(D, M, list(meta["nodes"]), kfreeze=13, **kw)
F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(8)])
Fh, Fl = np.asarray(F[0]), np.asarray(F[1])
np.savez(out, hi=Fh, lo=Fl)
line = (f"D {float(D):g} HP_SLAVE_REFINE_OD={os.environ.get('HP_SLAVE_REFINE_OD', '(default 4)')}: od max |F| "
        f"{float(np.abs(Fh + Fl).max()):.3e}, blocks " + " ".join(f"{b:.1e}" for b in blocks_s(F, M, len(meta['nodes']))))
if ref:
    r = np.load(ref)
    d = (Fh - r["hi"]) + (Fl - r["lo"])
    line += f"; max |F - F_ref| {float(np.abs(d).max()):.3e} at row {int(np.argmax(np.abs(d)))}"
print(line, flush=True)
