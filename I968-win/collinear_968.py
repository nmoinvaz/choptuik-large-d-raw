#!/usr/bin/env python3
"""#968 (win): read-only, no run. Are the K = 0 root samples a, b, c of D 40.020065 (32 x 121) collinear? From the stored double-double states (zh + zl), the differences z_a - z_c and z_b - z_c are
formed in double-double (rt_perturb.dd_add), then the cosine of the two (2-norm), and the part of z_b - z_c off the line through c and a (its relative 2-norm and max-norm).
usage: python -I collinear_968.py     (venv-t151 python)"""
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-i968\solver\rt")
import rt_perturb as P

R = r"C:\Users\nathan\Source\choptuik-large-d-raw"
F = {"a": R + r"\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz",
     "b": R + r"\I701-win\solves\k0b_D40_mutnorows_D40.0201_32x121.npz",
     "c": R + r"\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"}
Z = {}
for k, p in F.items():
    d = np.load(p)
    Z[k] = (np.asarray(d["zh"], float), np.asarray(d["zl"], float))
scale = float(np.abs(Z["c"][0] + Z["c"][1]).max())


def diff(x, y):
    h, l = P.dd_add(Z[x][0], Z[x][1], -Z[y][0], -Z[y][1])
    return h + l


ac, bc, ab = diff("a", "c"), diff("b", "c"), diff("a", "b")
for nm, v in (("a - c", ac), ("b - c", bc), ("a - b", ab)):
    print(f"max|{nm}| / max|z| {np.abs(v).max() / scale:.4e}, 2-norm / max|z| {np.linalg.norm(v) / scale:.4e}")
cos = float(ac @ bc / (np.linalg.norm(ac) * np.linalg.norm(bc)))
t = float(bc @ ac / (ac @ ac))
off = bc - t * ac
print(f"cosine of (a - c) and (b - c): {cos:.12f}; b - c = {t:.6f} (a - c) + off, off 2-norm / (b - c) 2-norm {np.linalg.norm(off) / np.linalg.norm(bc):.4e}, max-norm / (b - c) max-norm {np.abs(off).max() / np.abs(bc).max():.4e}")
