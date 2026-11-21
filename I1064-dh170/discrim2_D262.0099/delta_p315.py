#!/usr/bin/env python3
"""#1064 part 4: Delta of saved bases at 140 digits and the difference. usage (from hp/): python3 delta_p315.py BASE_A BASE_B   prints Delta(A), Delta(B), Delta(B) - Delta(A), the largest |difference| of the other
state components and the D of each; Delta is the last component of the eight-part state (the sum of its parts)."""
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, os.environ.get("HP_DIR", os.path.dirname(os.path.abspath(__file__))))
from octo_corrector import load_o  # noqa: E402

mp.mp.dps = 140
a, b = sys.argv[1], sys.argv[2]
za, ma = load_o(a)
zb, mb = load_o(b)
L = len(za[0])


def comp(z, c):
    return mp.fsum(mp.mpf(float(p[c])) for p in z)


da, db = comp(za, L - 1), comp(zb, L - 1)
print(f"A {a}: ks {ma.get('ks')}, D {ma.get('D_str', ma['D'])}, Delta {mp.nstr(da, 45)}")
print(f"B {b}: ks {mb.get('ks')}, D {mb.get('D_str', mb['D'])}, Delta {mp.nstr(db, 45)}")
print(f"Delta(B) - Delta(A) = {mp.nstr(db - da, 12)}")
dm = max(abs(comp(zb, c) - comp(za, c)) for c in range(L - 1))
print(f"largest |component difference| over the other {L - 1} components: {mp.nstr(dm, 6)}")
