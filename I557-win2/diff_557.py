#!/usr/bin/env python3
"""#557 side look (not an acceptance): the sums and differences of each pair, ln sigma_1 + ln sigma_2, ln sigma_2 - ln sigma_1, ln sigma_3 + ln sigma_4 and ln sigma_4 - ln sigma_3, over the 51 states D >= 210.13, fitted by
polynomials in u = (D - 228) / 10 of degree 1 to 4: the rms residual and the range. The merge test of joint_557.py finds one shared phase for each pair; if the two oscillations are in antiphase with equal amplitudes the sum
carries none of it (a smooth trend) and the difference carries twice.
usage: python diff_557.py   (run from I557-win2; needs joint_557.py)"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import joint_557 as j  # noqa: E402
D, Y = j.all_states()
sel = D >= 210.0
u = (D[sel] - 228.0) / 10.0
for name, y in (("ln sigma_1 + ln sigma_2", Y[sel, 1] + Y[sel, 0]), ("ln sigma_2 - ln sigma_1", Y[sel, 1] - Y[sel, 0]), ("ln sigma_3 + ln sigma_4", Y[sel, 3] + Y[sel, 2]), ("ln sigma_4 - ln sigma_3", Y[sel, 3] - Y[sel, 2]), ("ln sigma_1 (for scale)", Y[sel, 0]), ("ln sigma_3 (for scale)", Y[sel, 2])):
    row = []
    for d in (1, 2, 3, 4):
        c = np.polyfit(u, y, d)
        row.append(float(np.sqrt(np.mean((y - np.polyval(c, u)) ** 2))))
    print(f"{name}: range {y.min():+.3f} to {y.max():+.3f}; rms residual of a polynomial of degree 1, 2, 3, 4: " + ", ".join(f"{r:.4f}" for r in row))

# the hold-outs of the sums (no oscillation in them): fit a polynomial of degree 2, 3, 4 on the training states, predict the test states
print("\nhold-outs of the sums (polynomial of degree d in u fitted on the training states, rms prediction error of the sum; half of it is each series' share if the trend is shared):")
cfg = (("H1", (D >= 210.0) & (D <= 232.7), D > 232.7), ("H2", D >= 214.0, (D < 214.0) & (D >= 210.0)), ("H3", D >= 210.0, D < 210.0))
for name, (a, b) in (("ln sigma_1 + ln sigma_2", (0, 1)), ("ln sigma_3 + ln sigma_4", (2, 3))):
    y = Y[:, a] + Y[:, b]
    for h, tr, te in cfg:
        ut, ue = (D[tr] - 228.0) / 10.0, (D[te] - 228.0) / 10.0
        row = []
        for d in (2, 3, 4):
            c = np.polyfit(ut, y[tr], d)
            row.append(float(np.sqrt(np.mean((y[te] - np.polyval(c, ue)) ** 2))))
        print(f"  {name} {h}: degree 2, 3, 4: " + ", ".join(f"{r:.4f}" for r in row))
