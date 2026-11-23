#!/usr/bin/env python3
"""probe_floors.py [LOGS]: for each of x1's floor_max probe logs (logs/start_x1_xi{0.2,0.17}_fm.log, --verbose=2), the Jacobian-sensitivity table K it prints
(max |d r_l / d x_nu| per level l, from the first inner solve) and the residuals at which each level's top solve stopped, with the ratio stop / K_l (K_l is the
row's largest entry). A float64 rounding floor puts that ratio at a few ulp, about 1e-15 to 1e-14 (ulp 1.1e-16), for every radius and level;
this is a consistency check, not a test of the cause. Also the level-3 residual sequence."""
import os
import re
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
for xi in ("0.2", "0.17"):
    txt = open(os.path.join(d, f"start_x1_xi{xi}_fm.log")).read()
    K = {int(m[0]): max(float(m[1]), float(m[2])) for m in re.findall(r"^\s+l (\d): [0-9.e+]+\s+([0-9.e+]+)\s+([0-9.e+]+)", txt, re.M)}
    print(f"xi1 {xi}: K_1 {K[1]:.2e}  K_3 {K[3]:.2e}  K_5 {K[5]:.2e}  (max |d r_l / d x_nu| over nu = 3, 5)")
    for lev in (5, 3):
        st = re.findall(rf"level {lev} \(top\): stop at \|r_{lev}\| ([0-9.e+-]+): (.*)", txt)
        vals = [float(s[0]) for s in st]
        reasons = sorted(set(s[1] for s in st))
        lo, hi = min(vals), max(vals)
        print(f"  level {lev}: {len(vals)} top solves stopped at |r_{lev}| {lo:.2e} to {hi:.2e}; stop / K_{lev} = {lo / K[lev]:.1e} to {hi / K[lev]:.1e}; reasons: {'; '.join(reasons)}")
    seq = re.findall(r"^level 3 it (\d+): \|r_3\| ([0-9.e+-]+)", txt, re.M)
    print("  level 3 iterations: " + ", ".join(f"{float(v):.2e}" for _, v in seq) + " then the stop")
