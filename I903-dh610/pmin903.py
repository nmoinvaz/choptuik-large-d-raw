#!/usr/bin/env python3
"""#903 on dh610: the fixed-order chain's bases against a reference chain at the same D, read only.

    python3 -I pmin903.py CHAIN.log REF.log [REF2.log ...]

From CHAIN.log: each 'step N: D x, pivots a..b' line (the series of the base at D x; a is the base's p_min) and each
accepted attempt 'a X -> D Y: ...' with the last 'octo-double Newton: n steps, max|F| M, converged' line before it. From each
REF.log (T138's chain_o.log at order 130 for D up to 225, #603's chain_nsr.log from D 253.9): its 'step N: D x, pivots'
lines. Prints, per base D, p_min, the reference's p_min at the same D (to 1e-6 in D), their ratio and the max|F| of the
step that reached that D."""
import re
import sys

STEP = re.compile(r"^step (\d+): D (\S+), pivots (\S+?)\.\.")
END = re.compile(r"^\s+a (\S+) -> D (\S+): ")
NEWTON = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (converged|not converged)")


def steps(path):
    out = {}
    for ln in open(path, errors="replace"):
        m = STEP.match(ln)
        if m:
            out[round(float(m.group(2)), 6)] = float(m.group(3))
    return out


chain, refs = sys.argv[1], [steps(p) for p in sys.argv[2:]]
mine, fmax, last = {}, {}, None
for ln in open(chain, errors="replace"):
    m = STEP.match(ln)
    if m:
        mine[round(float(m.group(2)), 6)] = float(m.group(3))
    m = NEWTON.search(ln)
    if m:
        last = (m.group(2), m.group(3))
    m = END.match(ln)
    if m and last and last[1] == "converged":
        fmax[round(float(m.group(2)), 6)] = last[0]
print("| base D | p_min (this chain) | reference p_min, same D | ratio | max\\|F\\| of the step that reached D |")
print("|---|---|---|---|---|")
for D in sorted(mine):
    ref = next((r[D] for r in refs if D in r), None)
    print(f"| {D:g} | {mine[D]:.2e} | {f'{ref:.2e}' if ref else '-'} | {f'{mine[D] / ref:.3g}' if ref else '-'} | {fmax.get(D, '-')} |")
