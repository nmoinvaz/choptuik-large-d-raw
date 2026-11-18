"""#975: the zero of m7_outer.py --local with more digits (same arithmetic, copied from its local()), plus the distance to a
reference.   python zero_digits.py TAG     (run from this folder; reads the m7_outer command from logs/m7_outer_win2_TAG.txt)"""
import os, sys
import numpy as np
sys.path.insert(0, os.environ.get("RUN_SRC", "D:/choptuik-i962/solver/inner_stokes"))
import m7_outer
tag = sys.argv[1]
cmd = [l for l in open(os.path.join("logs", f"m7_outer_win2_{tag}.txt"), encoding="utf-8") if l.startswith("$ ")][0][2:].split()
args = cmd[cmd.index("--local") + 1:]
k = args.index("--")
cen = [m7_outer.point(f, True) for f in args[:k]]
offs = [m7_outer.point(f, True) for f in args[k + 1:]]
good = [c for c in cen if c[3] < 1e-6]
if not good or any(o[3] >= 1e-6 for o in offs):
    sys.exit("not enough solves with |r_3| < 1e-6 (the refusal of m7_outer.py --local)")
p0 = good[0][1]; R = np.array([c[2] for c in good]); r0 = R.mean(axis=0)
(_, pa, ra, _), (_, pw, rw, _) = offs
J = np.column_stack([(ra - r0) / (pa[0] - p0[0]), (rw - r0) / (pw[1] - p0[1])])
z = p0 + (-np.linalg.solve(J, r0))
print(f"{tag}: zero A {z[0]:.9f}, w/w_inf {z[1]:.9f}")
for name, ref in (("(2.71922, 1.000022)", (2.71922, 1.000022)), ("rpi5 Job 0 (2.719236, 1.000028)", (2.719236, 1.000028)),
                  ("rpi5 Job A (2.719326, 1.000042)", (2.719326, 1.000042))):
    print(f"  minus {name}: dA {z[0] - ref[0]:+.3e}, dw {z[1] - ref[1]:+.3e}")
