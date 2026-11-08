"""I184-macm3: the new B (box centred at p^) against #103's B (centred at the stored double x^). The centre is not printed by the run, so its effect is read off B.
    python3 compare_B_old_new.py        (from this folder; reads ../I103-macm3/B_M5_sub1e-18.json)
"""
import json
import numpy as np

def load(p):
    sb = json.load(open(p))
    mid = np.array([[complex(float(e[0][0]), float(e[1][0])) for e in row] for row in sb["B"]])
    rad = np.array([[max(float(e[0][1]), float(e[1][1])) for e in row] for row in sb["B"]])
    return sb, mid, rad

new, mn, rn = load("B_M5_sub1e-18_phat.json")
old, mo, ro = load("../I103-macm3/B_M5_sub1e-18.json")
d = np.abs(mn - mo)
print(f"entries {mn.size}, steps new {new['steps']} old {old['steps']}, max radius of B new {rn.max():.3e} old {ro.max():.3e}")
print(f"max |mid_new - mid_old| = {d.max():.3e} at {np.unravel_index(d.argmax(), d.shape)}; over rad_new {(d / rn).max():.3f}, over rad_old {(d / ro).max():.3f}")
print(f"entries with |mid_new - mid_old| > rad_new: {(d > rn).sum()} of {d.size}; entries with new ball disjoint from old ball: {(d > rn + ro).sum()}")
print(f"phat from box file p vs centre_passed.txt: {'equal' if ','.join(json.load(open('../I103-macm3/A_M2_6a_M5_sub1e-18.json'))['p']) == open('centre_passed.txt').read().strip() else 'DIFFER'}")
