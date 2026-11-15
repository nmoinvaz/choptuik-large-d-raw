#!/usr/bin/env python3
"""#817: the exact eight-part Delta of #713's planted truth and of each arm's final state, against the two references.

    python3 -I delta_ref817.py TRUTH.npz [ARM.npz ...]

Delta of a state is the sum of the last entry of its eight parts (zh, zl, z2 .. z7), each taken as the exact double and
summed in mpmath at 60 digits, as report_608r.py's delta() does. The two references are the truth's Delta and the truth's
Delta minus 2.0184e-11 (the offset of the #817 comment of 2026-11-15). Prints no verdict on Delta."""
import sys

import numpy as np
from mpmath import mp, mpf

mp.dps = 60
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
OFFSET = mpf("2.0184e-11")


def delta(path):
    z = np.load(path, allow_pickle=False)
    missing = [k for k in PARTS if k not in z.files]
    if missing:
        sys.exit(f"{path}: missing parts {missing}")
    return sum((mpf(float(z[k][-1])) for k in PARTS), mpf(0))


truth = delta(sys.argv[1])
ref2 = truth - OFFSET
print(f"truth      Delta {mp.nstr(truth, 40)}  ({sys.argv[1]})")
print(f"truth - {mp.nstr(OFFSET, 5)}  {mp.nstr(ref2, 40)}")
for p in sys.argv[2:]:
    d = delta(p)
    print(f"{p}\n  Delta {mp.nstr(d, 40)}\n  minus truth {mp.nstr(d - truth, 6)}"
          f"\n  minus (truth - {mp.nstr(OFFSET, 5)}) {mp.nstr(d - ref2, 6)}")
