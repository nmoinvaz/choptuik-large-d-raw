#!/usr/bin/env python3
"""Do the stage-1 circles of #573 and #574 cover their rectangles? A circle's winding counts only the zeros inside it, so a zero in a gap would go unseen.
usage: python coverage_57x.py            (prints, per task, the number of grid points farther than R from every centre and the largest distance)
       python coverage_57x.py --selftest (the controls: a dropped circle and R 0.35 must leave points uncovered, the full set at R 0.36 none)
#573: centres Re 1.85, 2.35 x Im 0.25, 0.75 (and the mirrors, not needed for the upper rectangle), R 0.36, rectangle 1.6 <= Re <= 2.6, 0 <= Im <= 1.0.
#574: centres Re 1.85 ... 4.35 (step 0.5) x Im 1.25, 1.75, R 0.36, rectangle 1.6 <= Re <= 4.6, 1.0 <= Im <= 2.0. Grid step 0.001."""
import math, sys


def check(centres, R, re_lo, re_hi, im_lo, im_hi, step=0.001):
    nx, ny = round((re_hi - re_lo) / step), round((im_hi - im_lo) / step)
    unc, worst, n = 0, 0.0, 0
    for a in range(nx + 1):
        x = re_lo + (re_hi - re_lo) * a / nx
        near = [c for c in centres if abs(x - c[0]) < R + 0.4]
        for b in range(ny + 1):
            y = im_lo + (im_hi - im_lo) * b / ny
            d = min(math.hypot(x - cx, y - cy) for cx, cy in (near or centres))
            worst = max(worst, d)
            n += 1
            if d > R:
                unc += 1
    return unc, worst, n


C573 = [(r, i) for r in (1.85, 2.35) for i in (0.25, 0.75)]
C574 = [(r, i) for r in (1.85, 2.35, 2.85, 3.35, 3.85, 4.35) for i in (1.25, 1.75)]
RECT573, RECT574 = (1.6, 2.6, 0.0, 1.0), (1.6, 4.6, 1.0, 2.0)

if "--selftest" in sys.argv:
    ok = True
    for name, C, rect in (("573", C573, RECT573), ("574", C574, RECT574)):
        u_full = check(C, 0.36, *rect, step=0.005)[0]
        u_drop = check(C[:3] + C[4:], 0.36, *rect, step=0.005)[0]
        u_small = check(C, 0.35, *rect, step=0.005)[0]
        good = u_full == 0 and u_drop > 0 and u_small > 0
        ok &= good
        print(f"#{name}: full set R 0.36 uncovered {u_full} (must be 0), one circle dropped {u_drop} (must be > 0), R 0.35 {u_small} (must be > 0): {'ok' if good else 'FAIL'}")
    sys.exit(0 if ok else 1)

for name, C, rect in (("573", C573, RECT573), ("574", C574, RECT574)):
    unc, worst, n = check(C, 0.36, *rect)
    print(f"#{name}: {n} grid points, {unc} farther than 0.36 from every centre, largest distance to a centre {worst:.4f} (0.5/sqrt(2) = {0.5 / math.sqrt(2):.4f})")
sys.exit(0)
