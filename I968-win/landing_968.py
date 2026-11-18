#!/usr/bin/env python3
"""#968 (win): a check on rt_perturb --along with the real samples. Moving C along the line to A by delta = max|A - C| / max|C| (in double-double, from rt_perturb's own functions) must land on A:
max|z' - z_A| / max|z| far below the distance itself (1.7e-20), at the rounding of the double vector p = delta max|z| r (about 1e-16 of the distance) and the dd resolution (1e-32).
Also the move at the three delta of the runs: the cosine of z' - z_C with z_A - z_C (1 by construction, a check of the file), and max|z' - z_A| for the delta past a.

usage: python -I landing_968.py       (venv-t151 python, from this folder)"""
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-i968\solver\rt")
import rt_perturb as P

HERE = os.path.dirname(os.path.abspath(__file__))
C = r"C:\Users\nathan\Source\choptuik-large-d-raw\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"
A = r"C:\Users\nathan\Source\choptuik-large-d-raw\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz"
c, a = np.load(C), np.load(A)
zh, zl = np.asarray(c["zh"], float), np.asarray(c["zl"], float)
oh, ol = np.asarray(a["zh"], float), np.asarray(a["zl"], float)
scale = float(np.abs(zh + zl).max())
dist = P.realised(zh, zl, oh, ol)
print(f"max|z_C| {scale:.6e}, max|z_A - z_C| / max|z| {dist:.6e} (max-norm {dist * scale:.4e})")
nh, nl = P.move(zh, zl, dist, 977, along=(oh, ol))
land = P.realised(oh, ol, nh, nl)
print(f"delta = {dist:.6e} (the distance): max|z' - z_A| / max|z| {land:.3e}, {land / dist:.1e} of the distance")
dh, dl = P.dd_add(oh, ol, -zh, -zl)
d0 = dh + dl
for dstr in ("1e-20", "1e-19", "1e-18"):
    s = np.load(os.path.join(HERE, "states", f"c_along_d{dstr}.npz"))
    sh, sl = np.asarray(s["zh"], float), np.asarray(s["zl"], float)
    qh, ql = P.dd_add(sh, sl, -zh, -zl)
    q = qh + ql
    cos = float(q @ d0 / (np.linalg.norm(q) * np.linalg.norm(d0)))
    past = P.realised(oh, ol, sh, sl)
    print(f"c_along_d{dstr}: realised {P.realised(zh, zl, sh, sl):.6e}, cosine of the move with z_A - z_C {cos:.12f}, max|z' - z_A| / max|z| {past:.4e}")
