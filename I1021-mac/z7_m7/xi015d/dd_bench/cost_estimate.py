#!/usr/bin/env python3
"""#1021 cost estimate of a double-double hier_nb walk: per-residual times and residuals per solve of the xi1 0.15 control
solves (../z7/logs/fix_control5_xi0.15_*.log at M = 5, fix_control_xi0.15_*.log at M = 7), times a dd factor from 5
(bench_dd.log: conv at L = 7 measured 5.2x) to 20 (assumed for dd division, exp and the stepper), for walks of 8 (the
controls') to 25 solves (walk1026b's --maxit). Prints the ranges."""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
for M, pat in ((5, "fix_control5_xi0.15_*.log"), (7, "fix_control_xi0.15_*.log")):
    s = r = n = 0
    for f in glob.glob(os.path.join(HERE, "..", "z7", "logs", pat)):
        m = re.findall(r"FIXED-A M \d+:.*\[(\d+) s, (\d+) residuals\]", open(f).read())
        if m:
            n += 1; s += int(m[-1][0]); r += int(m[-1][1])
    per, rps = s / r, r / n
    lo, hi = per * 5, per * 20
    print(f"M = {M}: {n} solves, {1e3 * per:.0f} ms per residual, {rps:.0f} residuals per solve; dd {lo:.2f}-{hi:.2f} s per residual, "
          f"{lo * rps / 60:.1f}-{hi * rps / 60:.1f} min per solve, walk of 8-25 solves {8 * lo * rps / 3600:.2f}-{25 * hi * rps / 3600:.1f} h")
