"""A saved form-S state's octo-double residual (the full system, kfreeze 13 unless given), all eight parts, saved as npz
for comparing two builds' bits on one state (#1098); prints max |F| and, with a second file, the largest difference.

    python3 dump_residual.py HP_DIR STATE OUT.npz [OTHER.npz] [KFREEZE]
"""
import sys

import numpy as np

hp_dir, path, out = sys.argv[1:4]
other = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4].endswith(".npz") else None
kf = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 13
sys.path.insert(0, hp_dir)
from mpmath import mp  # noqa: E402

import form_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

z8, meta = load_o(path)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), ks=int(meta["ks"]), threads=2, segs=meta["segs"],
          mob=float(meta.get("hmob", 0.0) or 0.0))
s = form_s.make_solver_s(D, int(meta["M"]), list(meta["nodes"]), kfreeze=kf, **kw)
F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(8)])
parts = np.array([np.asarray(f) for f in F])
np.savez(out, parts=parts, kernel=str(form_s.kernel_info()))
Fs = parts[0] + parts[1]
line = f"D {float(D):g}: od max |F| {np.abs(Fs).max():.6e} ({form_s.kernel_info()})"
if other:
    o = np.load(other)["parts"]
    with mp.workdps(160):
        d = max(abs(mp.fsum(mp.mpf(float(parts[q][i])) for q in range(8)) - mp.fsum(mp.mpf(float(o[q][i])) for q in range(8)))
                for i in range(parts.shape[1]))
    bits = int(np.sum(parts != o))
    line += f"; against {other}: max |F - F_other| {mp.nstr(d, 4)}, parts differing {bits} of {parts.size}"
print(line, flush=True)
