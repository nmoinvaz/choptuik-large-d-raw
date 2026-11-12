#!/usr/bin/env python3
"""#525: the state at D 215.1312 reached by two steps of a = -0.5 down from crawlG D 216.1312 (this task) against crawlB2's D 215.1312 (reached by a step of +0.1 from I19-win2's D 215.0312, the chain crawlG was built on).
usage: python compare_215_525.py [--mutate]        (run from I525-win2; needs mpmath)
Both states are sums of their eight parts (zh, zl, z2..z7), each part added as an exact double. Reports the difference of Delta (the last entry) and the largest entry difference, absolute and relative to the
largest entry. --mutate compares against the D 215.6312 state of this task instead, which must differ by far more (exit 1 when the two states differ by more than 1e-6 relative; the mutated comparison must exit 1)."""
import os, sys
import numpy as np
from mpmath import mp, mpf
mp.prec = 400
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "down", "anm_pin3_D215.1312.npz")
B = os.path.join(HERE, "..", "I461-win2", "crawlB2", "anm_pin3_D215.1312.npz")
if "--mutate" in sys.argv:
    B = os.path.join(HERE, "down", "anm_pin3_D215.6312.npz")
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")


def vec(path):
    d = np.load(path, allow_pickle=True)
    n = len(d["zh"])
    return [sum((mpf(float(d[k][i])) for k in PARTS if k in d.files), mpf(0)) for i in range(n)]


a, b = vec(A), vec(B)
diff = [abs(x - y) for x, y in zip(a, b)]
big = max(abs(x) for x in a)
dmax = max(diff)
print(f"{os.path.basename(os.path.dirname(A))}/{os.path.basename(A)} against {os.path.basename(os.path.dirname(B))}/{os.path.basename(B)}")
print(f"Delta {mp.nstr(a[-1], 25)} against {mp.nstr(b[-1], 25)}, difference {mp.nstr(a[-1] - b[-1], 5)}")
print(f"largest entry {mp.nstr(big, 6)}, largest entry difference {mp.nstr(dmax, 5)} (relative {mp.nstr(dmax / big, 5)}) at index {diff.index(dmax)} of {len(a)}")
bad = dmax / big > mpf("1e-6")
print("states differ" if bad else "states agree to 1e-6 relative")
sys.exit(1 if bad else 0)
