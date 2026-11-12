#!/usr/bin/env python3
"""#534, post hoc (not in the protocol, run after the real series was read; the planted verdict and the real results do not depend on it).
usage: python posthoc_534.py --raw=<raw worktree>
(1) The window residual rms of the real series with and without the second harmonic (an F test for the two added columns), per series and window.
(2) The planted agreement test again at the noise the windows actually show (0.0015 instead of 0.006): the critical value of Q on S1A and the power on S2, 300 fresh seeds each,
    through the same pipeline (second_harmonic_534.py with its NOISE set)."""
import math
import sys

import numpy as np
from scipy.stats import f as fdist

import second_harmonic_534 as sh

raw = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--raw=")][0]
pp = sh.load_pp(raw)
D, Y = pp.collect51()
F = pp.Fitter(D, 3)
ms = sh.masks(D)
print("(1) window residual rms with and without the second harmonic (quadratic trend in the window, phase of the p2 chirp)")
print("| series | window | states | rms, first harmonic only | rms, with the second | F (2, dof) | p |\n|---|---|---|---|---|---|---|")
for i in (1, 2):
    y = Y[:, i - 1]
    best, f0 = F.fit_free(y)
    for w, m in enumerate(ms):
        full = sh.window_fit(pp, D, y, best["theta"], m)
        Dw, yw = D[m], y[m]
        ph = pp.phase(Dw, *best["theta"])
        xc = (Dw - Dw.mean()) / (0.5 * (Dw.max() - Dw.min()))
        X1 = np.column_stack([xc ** k for k in range(sh.DEG + 1)] + [np.cos(ph), np.sin(ph)])
        e1 = yw - X1 @ np.linalg.lstsq(X1, yw, rcond=None)[0]
        rss1, rss2 = float(e1 @ e1), full["rms"] ** 2 * len(yw)
        dof2 = full["dof"]
        Fv = ((rss1 - rss2) / 2) / (rss2 / dof2)
        print(f"| sigma_{i} | {sh.NAMES[w]} | {len(yw)} | {math.sqrt(rss1 / len(yw)):.4f} | {full['rms']:.4f} | {Fv:.1f} (2, {dof2}) | {fdist.sf(Fv, 2, dof2):.1e} |")
print("\n(2) the planted agreement test at noise 0.0015 (windows' actual residual rms 0.0006 to 0.0018), 300 fresh seeds per scenario")
sh.NOISE = 0.0015
res = {}
for scen, off in (("S1A", 100000), ("S2", 200000)):
    qs = []
    for s in range(300):
        rng = np.random.default_rng(sh.SEED0[scen] + off + s)
        y = sh.planted_y(pp, D, sh.SCEN[scen], rng)
        th, rows = sh.pipeline(pp, F, D, y)
        qs.append(sh.qstat(rows)[0])
    res[scen] = np.array(qs)
crit = float(np.percentile(res["S1A"], 95))
power = float(np.mean(res["S2"] > crit))
print(f"Q critical value at noise 0.0015 (95th percentile of S1A) {crit:.2f}; power on S2 (rho 0.03, 0.066, 0.12) {100 * power:.0f}% (at noise 0.006: critical value 7.91, power 52%)")
print("the observed Q values (sigma_1 1.59, sigma_2 0.02, p2 chirp phase) against this critical value: " + ("both below" if max(1.59, 0.02) <= crit else "sigma_1's above"))
