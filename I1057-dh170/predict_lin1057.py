#!/usr/bin/env python3
"""#1057: out-of-sample predictions of the D-linear-slopes two-mode fit (twomode_lin1057.py, window A or B) at D values not yet read.

    predict_lin1057.py A|B D1 D2 ...   sigma_lowest, sigma_upper, their ratio and the model's Delta share of the lowest vector at each D"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twomode_lin1057 as t  # noqa: E402

w = sys.argv[1]
D, lo, up, s1, s2 = t.load([f"c3b_ks293_D{d:.4f}" for d in t.WINDOWS[w]])
th, rms = t.fit(D, lo, up)
x = np.asarray([float(v) for v in sys.argv[2:]]) - D[-1]
a, b = t.pair(th, x)
sh = t.share(th, x)
print(f"window {w}: fit on D {D[0]:.4f} to {D[-1]:.4f}, gamma {th[6]:.4f}, D_c {t.crossing(th, -2, 1) + D[-1]:.3f}, rms {rms:.2e}")
print(f"{'D':>9} {'sigma_lowest':>13} {'sigma_upper':>12} {'upper/lowest':>13} {'model share of the lowest':>26}")
for d, p, q, s in zip(sys.argv[2:], a, b, sh):
    print(f"{float(d):9.4f} {float(p):13.4e} {float(q):12.4e} {float(q / p):13.3f} {float(s):26.3f}")
