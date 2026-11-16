#!/usr/bin/env python3
"""#903 on dh610: the rungs of the order-160 run from D 200, read only.

    python3 -I rungs903.py DIR CONTROL RUNG [RUNG ...]

DIR is I903-dh610/, CONTROL the control's name (p130_200) and each RUNG a rung's name (p160_200, ...); the rung's log is
DIR/<name>.log and its saved base DIR/<name>/base_pin3_*.npz. Per rung it prints the final octo-double max|F|, the lowest
pivot of the first Jacobian (the first 'piv a..b' of its log, the start point's), ln(p_K / p_130) with the control's p, and
Delta of the base (its eight parts summed exactly at 60 digits) and Delta_K - Delta_130."""
import glob
import os
import re
import sys

import numpy as np
from mpmath import mp, mpf

mp.dps = 60
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
PIV = re.compile(r"^\s+on \d+: .*?piv ([0-9.e+-]+)\.\.([0-9.e+-]+)")
NEWTON = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (converged|not converged)")


def read(d, name):
    lines = open(os.path.join(d, name + ".log"), errors="replace").read().splitlines()
    piv = [float(m.group(1)) for m in map(PIV.match, lines) if m]
    newton = [m for m in map(NEWTON.search, lines) if m]
    base = sorted(glob.glob(os.path.join(d, name, "base_pin3_*.npz")))
    delta = None
    if base:
        z = np.load(base[0], allow_pickle=False)
        delta = sum((mpf(float(z[k][-1])) for k in PARTS), mpf(0))
    last = newton[-1] if newton else None
    return dict(name=name, p_first=piv[0] if piv else None, p_min=min(piv) if piv else None, delta=delta,
                steps=int(last.group(1)) if last else None, fmax=last.group(2) if last else None,
                verdict=last.group(3) if last else "no octo-double Newton line", base=bool(base))


d, control, rungs = sys.argv[1], sys.argv[2], sys.argv[3:]
c = read(d, control)
print("| rung | octo-double steps | final max\\|F\\| | p first Jacobian | p min over steps | ln(p_K/p_130) | Delta (8 parts) | Delta_K - Delta_130 |")
print("|---|---|---|---|---|---|---|---|")
for r in [c] + [read(d, n) for n in rungs]:
    ln = mp.log(mpf(r["p_first"]) / mpf(c["p_first"])) if r["p_first"] and c["p_first"] else None
    dd = r["delta"] - c["delta"] if r["delta"] is not None and c["delta"] is not None else None
    print(f"| {r['name']} | {r['steps']} {r['verdict']} | {r['fmax']} | {r['p_first']} | {r['p_min']} | "
          f"{mp.nstr(ln, 6) if ln is not None else '-'} | {mp.nstr(r['delta'], 25) if r['delta'] is not None else '-'} | "
          f"{mp.nstr(dd, 6) if dd is not None else '-'} |")
