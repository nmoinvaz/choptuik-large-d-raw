"""I861-rpi5: the Pi's B (box centred at p^, lemma6_jump_M.py --save-B) against macm3's B of #184.
    python3 compare_B_pi_mac.py PI_B.json MAC_B.json
"""
import json, sys
import numpy as np

def load(p):
    sb = json.load(open(p))
    mid = np.array([[complex(float(e[0][0]), float(e[1][0])) for e in row] for row in sb["B"]])
    rad = np.array([[max(float(e[0][1]), float(e[1][1])) for e in row] for row in sb["B"]])
    return sb, mid, rad

a, ma, ra = load(sys.argv[1]); b, mb, rb = load(sys.argv[2])
assert ma.shape == mb.shape
d = np.abs(ma - mb)
print(f"entries {ma.size}, steps Pi {a['steps']} Mac {b['steps']}, max radius of B Pi {ra.max():.3e} Mac {rb.max():.3e} "
      f"(ratio {ra.max() / rb.max():.3f}), median radius ratio Pi / Mac {np.median(ra / rb):.3f}")
print(f"max |mid_Pi - mid_Mac| = {d.max():.3e} at {np.unravel_index(d.argmax(), d.shape)}; over rad_Pi {(d / ra).max():.3f}, over rad_Mac {(d / rb).max():.3f}")
print(f"entries with |mid_Pi - mid_Mac| > rad_Pi: {(d > ra).sum()} of {d.size}; entries with the Pi ball disjoint from the Mac ball: {(d > ra + rb).sum()}")
print(f"radius ratios Pi / Mac: min {(ra / rb).min():.3f}, max {(ra / rb).max():.3f}")

# the midpoints as printed strings (80 digits), to see below double precision
from decimal import Decimal, getcontext
getcontext().prec = 80
A, Bm = json.load(open(sys.argv[1]))["B"], json.load(open(sys.argv[2]))["B"]
n = same = 0
worst = Decimal(0)
for rowa, rowb in zip(A, Bm):
    for x, y in zip(rowa, rowb):
        for p, q in zip(x, y):
            n += 1
            if p[0] == q[0]:
                same += 1
            else:
                da, db = Decimal(p[0]), Decimal(q[0])
                worst = max(worst, abs(da - db) / max(abs(da), abs(db)))
print(f"midpoint strings (re and im parts): {n}, identical {same}, worst relative difference of the others {float(worst):.2e}")
