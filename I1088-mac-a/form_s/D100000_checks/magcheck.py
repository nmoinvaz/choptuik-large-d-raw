"""The exponent-range check at large D (#1088): the held residual of a saved lastnode state once, in double-double, with
Ctx::mutate FS_MAGSTATS (55), whose horizon_mob prints each stored series' smallest nonzero and largest |hi part| to
stderr (this script's caller keeps stderr), and the node data's range (the state's parts) from Python.
Bars: every nonzero magnitude in [1e-280, 1e280], nothing not finite. Controls: --scale 1e250 (the state times 1e250:
the high bar must fire), --ks 4x the formula (the series' tail: the low bar or the zero counts must fire).

    python3 magcheck.py STATE [--ks KS] [--scale S] [--threads T]
"""
import sys

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from form_s import HeldS, held_field, make_solver_s  # noqa: E402
from octo_corrector import load_o  # noqa: E402

args = sys.argv[1:]
path = args[0]
opt = dict(zip(args[1::2], args[2::2]))
z8, meta = load_o(path)
ks = int(opt.get("--ks", meta["ks"]))
scale = float(opt.get("--scale", "1"))
thr = int(opt.get("--threads", "2"))
with mp.workdps(60):
    Dt = mp.mpf(meta["D_str"])
kw = dict(kt=int(meta["kt"]), kc=int(meta["kc"]), ks=ks, threads=thr, segs=meta["segs"], mob=float(meta["hmob"]))
s = make_solver_s(Dt, 32, list(meta["nodes"]), kfreeze=3, **kw)
z = [np.asarray(p) * scale for p in z8]
sh = HeldS(s, 32, 5, held_field(z8, 32))
nz = np.abs(np.concatenate([np.asarray(p) for p in z[:2]]))
nzf = nz[np.isfinite(nz) & (nz > 0)]
print(f"D {float(Dt):g}, ks {ks}, a {float(meta['hmob']):g}, x_l {meta['nodes'][-1]:.6f}, scale {scale:g}: node data "
      f"(the state's two leading parts) min |x| {nzf.min():.3e} max |x| {nzf.max():.3e} zeros {int((nz == 0).sum())}",
      flush=True)
try:
    F = sh.residual_s([np.ascontiguousarray(z[q]) for q in range(2)], 55)
    Fs = np.asarray(F[0]) + np.asarray(F[1])
    print(f"  residual: max |F| {np.abs(Fs).max():.3e}, not finite {int((~np.isfinite(Fs)).sum())}", flush=True)
except BaseException as e:  # hp panics on a NaN pivot
    if isinstance(e, KeyboardInterrupt):
        raise
    print(f"  residual failed: {type(e).__name__}: {e}", flush=True)
