#!/usr/bin/env python3
"""#535 follow-up: how the local period fit (quadratic trend + one sinusoid, scan from 1.1, the method of (A) in period_535.py) reads planted periods in the 12 new states' layout (D 204.13 to 209.63, spacing 0.5, noise 0.006,
amplitude 0.11, quadratic trend like the data): the mean and spread of the fitted period over 200 seeds for the three models of #533's comment (2.404 the p2 chirp, 2.334 the linear drift, 2.560 the constant period),
and where the measured sigma_1 value of results_period_535.txt lies. usage: python bias_535.py [measured]   (default 2.380)"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I521-win2", "I516-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import analysis_521 as a21  # noqa: E402
meas = float(sys.argv[1]) if len(sys.argv) > 1 else 2.380
D = np.arange(204.1312, 209.7, 0.5)
u = (D - 228.0) / 10.0
print("| planted period | mean fitted | sd of the fitted | measured 2.380 is (in sd) from the mean |\n|---|---|---|---|")
for ptrue in (2.404, 2.334, 2.560):
    fits = []
    for s in range(200):
        y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.11 * np.sin(2 * np.pi * (D - 207.0) / ptrue + 0.7) + np.random.default_rng(700 + s).normal(0, 0.006, len(D))
        fits.append(a21.fit(D, y, 1.1, True)["P"])
    m, sd = float(np.mean(fits)), float(np.std(fits))
    print(f"| {ptrue} | {m:.3f} | {sd:.3f} | {(meas - m) / sd:+.1f} |")
