#!/usr/bin/env python3
"""Do the twelve lower circles of #574 and #582 (R 0.36, kf 27) cover the lower strip 1.6 <= Re <= 4.6, -2.0 <= Im <= -1.0?
A circle's winding counts only the zeros inside it, so a zero in a gap would go unseen.
usage: python coverage_582.py            (the twelve centres: Re 1.85 ... 4.35 step 0.5 x Im -1.25, -1.75; grid step 0.001)
       python coverage_582.py --selftest (controls: the full set leaves nothing uncovered, a dropped circle and R 0.35 leave points uncovered)
Exit 1 when a point is uncovered (or a control does not behave)."""
import math, sys


def check(centres, R, re_lo, re_hi, im_lo, im_hi, step=0.001):
    nx, ny = round((re_hi - re_lo) / step), round((im_hi - im_lo) / step)
    unc, worst = 0, 0.0
    for a in range(nx + 1):
        x = re_lo + (re_hi - re_lo) * a / nx
        near = [c for c in centres if abs(x - c[0]) < R + 0.4] or centres
        for b in range(ny + 1):
            y = im_lo + (im_hi - im_lo) * b / ny
            d = min(math.hypot(x - cx, y - cy) for cx, cy in near)
            worst = max(worst, d)
            unc += d > R
    return unc, worst


C = [(r, i) for r in (1.85, 2.35, 2.85, 3.35, 3.85, 4.35) for i in (-1.25, -1.75)]
RECT = (1.6, 4.6, -2.0, -1.0)
if "--selftest" in sys.argv:
    full = check(C, 0.36, *RECT, step=0.005)[0]
    drop = check(C[:3] + C[4:], 0.36, *RECT, step=0.005)[0]
    small = check(C, 0.35, *RECT, step=0.005)[0]
    ok = full == 0 and drop > 0 and small > 0
    print(f"full set R 0.36 uncovered {full} (must be 0), one circle dropped {drop} (must be > 0), R 0.35 {small} (must be > 0): {'ok' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
unc, worst = check(C, 0.36, *RECT)
print(f"lower strip: {unc} grid points farther than 0.36 from every centre, largest distance to a centre {worst:.4f} (0.5/sqrt(2) = {0.5 / math.sqrt(2):.4f})")
sys.exit(1 if unc else 0)
