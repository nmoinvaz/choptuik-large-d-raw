#!/usr/bin/env python3
"""#817: each arm's Delta after its accepted step 0, read from the log, against the two references.

    python3 -I delta_end817.py TRUTH.npz LOG [LOG ...]

The arms were stopped at step 1 (the coordinator's order, 2026-11-15 06:56 UTC) before octo_corrector.py planted wrote its
state (--out .npz and .json are written at the end of a run), so no eight-part Delta of an arm's state exists. What the
log has is the step's line "on 0: |F| a -> b, |dz| c -> d, lam L, dDelta X": X is the full Newton step's Delta part and
the accepted move in Delta is L * X (the step is dominated by Delta, |dz| equals |dDelta| to the printed digits). The
start is the truth with the 576 unknowns before Delta moved, so its Delta is the truth's. The result carries the three
printed digits of X, or four where the trial lines print |dz| as 2.018e-11, and is not an eight-part sum. No verdict."""
import re
import sys

import numpy as np
from mpmath import mp, mpf

mp.dps = 60
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
OFFSET = mpf("2.0184e-11")
z = np.load(sys.argv[1], allow_pickle=False)
truth = sum((mpf(float(z[k][-1])) for k in PARTS), mpf(0))
ref2 = truth - OFFSET
print(f"truth Delta {mp.nstr(truth, 30)}, truth - 2.0184e-11 {mp.nstr(ref2, 30)}")
STEP = re.compile(r"^  on 0: \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+),")
TRIAL = re.compile(r"^    on 0 trial lam 1: .*vs \|dz\| (\S+) ")
for p in sys.argv[2:]:
    dz4 = None
    for ln in open(p):
        m = TRIAL.match(ln)
        if m:
            dz4 = mpf(m.group(1))
        m = STEP.match(ln)
        if m:
            lam, dd = mpf(m.group(5)), mpf(m.group(6))
            for label, x in (("dDelta as printed", dd), ("-|dz| of the trial lines", -dz4)):
                move = lam * x
                print(f"{p}: step 0 lam {m.group(5)}, {label} {mp.nstr(x, 4)}: move L*X = {mp.nstr(move, 4)}"
                      f", Delta - truth = {mp.nstr(move, 4)}, Delta - (truth - 2.0184e-11) = {mp.nstr(move + OFFSET, 6)}")
            break
    else:
        print(f"{p}: no step 0 line")
