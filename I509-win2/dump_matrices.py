#!/usr/bin/env python3
"""#509: dump the complex mode matrix at the two check points of October's cache from one build of modecount_cx (the old DotAcc dtau_c, or today's).
usage: python dump_matrices.py HP_DIR CX_BUILD_DIR TAG OUTDIR
  HP_DIR        the hp directory of the worktree (modecount_common.py, hpkernel is the venv's)
  CX_BUILD_DIR  a directory with modecount_cx.cp312-win_amd64.pyd (cxbuild_old = the revert of dtau_c, cxbuild_new = today's)
  TAG           'old' or 'new' (file names)
Writes OUTDIR/mat_<TAG>_p<k>.npz with re_hi, re_lo, im_hi, im_lo (the (L-1, L-1) arrays of CSolver.mode_matrix at lambda = lr + i li, k = 1, 2) and det = (ln|det|, arg, min|u|, max|u|)
from CSolver.mode_det at the same point (the code's own LU), and prints them."""
import json, os, sys
import numpy as np

hp_dir, cxdir, tag, out = sys.argv[1:5]
RAW = "D:/choptuik-large-d-raw"
S = f"{RAW}/I250-mac/states/modecount_state_D30.0688_M48_october.npz"
PTS = [(4.267, 0.9740000000000001), (3.94364216362105, 1.1900607986722187)]
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402  (puts hp/modecount_cx/build on sys.path)
sys.path.insert(0, cxdir)
sys.modules.pop("modecount_cx", None)
st = mc.setup(S, M=None, kf=None, fmax=1e-15)
import modecount_cx  # noqa: E402
print("modecount_cx from", modecount_cx.__file__, flush=True)
assert os.path.dirname(os.path.abspath(modecount_cx.__file__)) == os.path.abspath(cxdir), "wrong build"
os.makedirs(out, exist_ok=True)
for k, (lr, li) in enumerate(PTS, 1):
    d = st.c.mode_det(st.zh, st.zl, float(lr), float(li))
    rh, rl, ih, il = st.c.mode_matrix(st.zh, st.zl, float(lr), float(li))
    p = os.path.join(out, f"mat_{tag}_p{k}.npz")
    np.savez(p, re_hi=rh, re_lo=rl, im_hi=ih, im_lo=il, det=np.array(d), lam=np.array([lr, li]))
    print(f"{tag} point {k} ({lr}, {li}): n {rh.shape[0]}, mode_det {d[0]!r} {d[1]!r} min|u| {d[2]:.3e} max|u| {d[3]:.3e}; saved {p}", flush=True)
