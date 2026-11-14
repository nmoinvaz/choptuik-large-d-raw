#!/usr/bin/env python3
"""#795: #782's estimators on #776's series (the kept plan) and on #795's (the plan made at the state), per base.
    PYTHONPATH=<dir of singularity_type.py>:<checkout>/hp python3 compare795.py RAW [--mutate=shift]
Per base D0 in 259.2582 and 259.4928: Delta's ratio and Dlog (s, mu) and the 24 rows' ratio median D* on each plan.
(A) Delta's Dlog D* and the rows' ratio median D* on the new plan within 0.01 of the kept plan's; (B) Delta's mu by both
estimators in [0.25, 0.75] on both plans at D0 259.4928; the largest relative change of Delta's coefficients (orders
5..24) between the plans is reported. --mutate=shift moves the new plan's D* by 0.5, which must fail (A) at both bases.
Exit 0 when (A) and (B) hold (with --mutate=shift: when (A) fails at both bases)."""
import os
import statistics
import sys

import numpy as np
from jet_singularity import load_jet, row_series
from singularity_type import DPS, dlog_fit, kind, ratio_fit
import mpmath as mp

mp.mp.dps = DPS
raw = sys.argv[1]
shift = 0.5 if "--mutate=shift" in sys.argv else 0.0


def est(path):
    Z, m = load_jet(path)
    c, _ = row_series(Z, "delta")
    r, d = ratio_fit(c), dlog_fit(c)
    rows = [int(i) for i in np.argsort(np.abs(np.asarray(Z[8][0])))[::-1][:24]]
    rr = [ratio_fit(row_series(Z, str(i))[0]) for i in rows]
    rd = statistics.median([m["D"] + x[0] for x in rr if x])
    return m["D"], c, r, d, rd


okA = okB = True
failA = 0
print("| D0 | plan | Delta ratio: D*, mu | Delta dlog: D*, mu | rows' ratio median D* |\n|---|---|---|---|---|")
for D in ("259.2582", "259.4928"):
    k = est(os.path.join(raw, "I776-dh370", "repro", f"jet_pin3_D{D}.npz"))
    n = est(os.path.join(raw, "I795-dh370", "newplan", f"jet_pin3_D{D}.npz"))
    for name, e, sh in (("kept", k, 0.0), ("new", n, shift)):
        D0, c, r, d, rd = e
        print(f"| {D0:.4f} | {name} | {D0 + r[0] + sh:.4f}, {r[1]:+.3f} {kind(r[1])} | {D0 + d[0] + sh:.4f}, {d[1]:+.3f} {kind(d[1])} | {rd + sh:.4f} |")
    a = abs((n[0] + n[3][0] + shift) - (k[0] + k[3][0])) <= 0.01 and abs((n[4] + shift) - k[4]) <= 0.01
    failA += not a
    okA &= a
    if D == "259.4928":
        okB = all(0.25 <= x <= 0.75 for x in (k[2][1], k[3][1], n[2][1], n[3][1]))
    ch = max(abs(float(x - y) / float(y)) for x, y in zip(n[1][4:], k[1][4:]) if y != 0)
    print(f"  D0 {D}: (A) {'met' if a else 'FAILED'}; largest relative change of Delta's coefficients 5..24 between plans {ch:.2e}")
print(f"(A) {'met' if okA else 'FAILED'} at both bases; (B) {'met' if okB else 'FAILED'} at D0 259.4928")
if shift:
    sys.exit(0 if failA == 2 else 1)
sys.exit(0 if okA and okB else 1)
