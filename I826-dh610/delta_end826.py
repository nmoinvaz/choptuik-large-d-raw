#!/usr/bin/env python3
"""#826: Delta - Delta(truth) of an arm's last accepted state, from the log, for an arm stopped before it wrote its state.

    python3 -I delta_end826.py TRUTH.npz LOG

`octo_corrector.py planted` writes its .npz and .json at the end of a run, so an arm that is stopped has no state. The
log's accepted-step lines "on k: |F| a -> b, |dz| c -> d, lam L, dDelta X" give the Delta part X of the full Newton
step and the accepted move L * X. The start is the truth itself (--rel 0), so Delta - Delta(truth) after the accepted
steps is the sum of L * X over them, to the three printed digits of X, and is not an eight-part sum. No verdict."""
import re
import sys

import numpy as np
from mpmath import mp, mpf

mp.dps = 60
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
z = np.load(sys.argv[1], allow_pickle=False)
truth = sum((mpf(float(z[k][-1])) for k in PARTS), mpf(0))
print(f"truth Delta {mp.nstr(truth, 30)}")
STEP = re.compile(r"^  on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+),")
tot = mpf(0)
for ln in open(sys.argv[2]):
    m = STEP.match(ln)
    if m:
        move = mpf(m.group(6)) * mpf(m.group(7))
        tot += move
        print(f"step {m.group(1)}: |F| {m.group(2)} -> {m.group(3)}, lam {m.group(6)}, dDelta {m.group(7)}, "
              f"move {mp.nstr(move, 4)}, Delta - truth so far {mp.nstr(tot, 5)}")
