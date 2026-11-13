#!/usr/bin/env python3
"""#597: hp/modecount_smooth.py's statistic at steps of k ulps instead of one. The matrix is assembled at Re lambda,
k f64 ulps up and 2k ulps up (CSolver.mode_matrix), and the entries with |d_2k - 2 d_k| > |d_k| / 2 are counted, for
each k given. If an entry's non-linearity is evaluation noise of a fixed size, its share falls as k grows (the change
grows like k, the noise does not); a step in how lambda enters would not fall that way.

    cd hp && python3 smooth_k597.py STATE M KF|none RE IM K1,K2,...
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
from modecount_common import setup  # noqa: E402

path, M, re0, im0 = sys.argv[1], int(sys.argv[2]), float(sys.argv[4]), float(sys.argv[5])
kf = None if sys.argv[3] == "none" else int(sys.argv[3])
ks = [int(x) for x in sys.argv[6].split(",")]
st = setup(path, M=M, threads=4, kf=kf, fmax=1e-15, log=lambda *a: None)
blk = 4 * M


def mat(r):
    rh, rl, ih, il = st.c.mode_matrix(st.zh, st.zl, r, im0)
    return tuple(np.asarray(x) for x in (rh, rl, ih, il))


def diff(A, B):
    return ((B[0] - A[0]) + (B[1] - A[1])) + 1j * ((B[2] - A[2]) + (B[3] - A[3]))


def up(x, k):
    for _ in range(k):
        x = float(np.nextafter(x, np.inf))
    return x


A0 = mat(re0)
scale = np.abs(A0[0] + 1j * A0[2])
print(f"{os.path.basename(path)} at {re0}{im0:+}i, M {M}, kf {kf}, n {scale.shape[0]}; ulp of Re {np.spacing(re0):.3e}")
for k in ks:
    d1, d2 = diff(A0, mat(up(re0, k))), diff(A0, mat(up(re0, 2 * k)))
    mask = np.abs(d1) > 1e-30 * (scale + 1e-300)
    rel = np.abs(d2 - 2 * d1) / np.maximum(np.abs(d1), 1e-300)
    bad = mask & (rel > 0.5)
    rows = np.nonzero(bad)[0]
    nb = (scale.shape[0] + blk - 1) // blk
    print(f"  k {k:6d}: changed {int(mask.sum())}, non-linear {int(bad.sum())} "
          f"({100 * bad.sum() / max(mask.sum(), 1):.3g}%), by row block {np.bincount(rows // blk, minlength=nb).tolist()}; "
          f"median |d_2k - 2 d_k| / |d_k| {np.median(rel[mask]):.2e}", flush=True)
