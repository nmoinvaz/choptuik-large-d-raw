#!/usr/bin/env python3
"""#752 check 2: the rebuilt predictions (R/) against #742's stored ones, bit for bit, every part.
usage: python3 cmp_pred.py RAW [--mutate ulp]
--mutate ulp moves one entry of the rebuilt prediction by one ulp before comparing (the control, which must fail).
Exit 1 when a pair differs."""
import sys

import numpy as np

raw = sys.argv[1]
mutate = "--mutate" in sys.argv
pairs = [("I752-mac/R/pred_pin13_D118.0000.npz", "I742-win/L/pred_pin13_D118.0000.npz"),
         ("I752-mac/R/pred_pin13_D118.0000.npz", "I742-win/N/pred_pin13_D118.0000.npz"),
         ("I752-mac/R/pred_pin13_D117.5000.npz", "I742-win/M/pred_pin13_D117.5000.npz")]
bad = 0
for ours, ref in pairs:
    a, b = np.load(f"{raw}/{ours}"), np.load(f"{raw}/{ref}")
    same, worst = True, 0.0
    for k in ("zh", "zl", "z2", "z3"):
        x = np.array(a[k])
        if mutate and k == "zh":
            x[100] = np.nextafter(x[100], np.inf)
        same &= bool(np.array_equal(x, b[k]))
        worst = max(worst, float(np.abs(x - b[k]).max()))
    print(f"  {ours} vs {ref}: {'bit for bit equal' if same else 'DIFFERS, largest part difference ' + format(worst, '.2e')}")
    bad += not same
print(f"{'PASS' if not bad else 'FAIL'}{' (--mutate ulp)' if mutate else ''}")
sys.exit(1 if bad else 0)
