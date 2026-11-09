#!/usr/bin/env python3
"""I230-mac: scan every edge of a count's record for intervals that may hide a whole 2 pi turn (no determinants).

    python3 alias_scan.py RESULTS.jsonl [MAX_TURN_FRACTION]

For each interval of each edge, the phase change predicted from the neighbouring intervals' rates (the median of up to
three on each side, times the interval's length) is compared with the interval's own wrapped step. An interval is
flagged when the prediction differs from the step by more than pi (a hidden turn would differ by about 2 pi), or when
its length times the largest neighbouring rate exceeds 2 pi * MAX_TURN_FRACTION (default 0.5: the interval could hold
half a turn or more that the samples cannot see). A flag is a reason to re-sample, not a proof of a missed turn; no
flag is no proof either (a rate can change faster than the neighbours show). Control: on #212's kf 23 record the two
intervals of T that t_check.py found to hide 3 turns must be flagged.
"""
import json
import math
import sys

import numpy as np

rec = [json.loads(l) for l in open(sys.argv[1])][-1]
frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
nflag = 0
for name, e in rec["edges"].items():
    z0, z1 = complex(*e["z0"]), complex(*e["z1"])
    L = abs(z1 - z0)
    S = e["samples"]
    t = np.array([s[0] for s in S])
    ph = np.array([s[2] for s in S])
    h = np.diff(t) * L
    st = np.array([math.remainder(b - a, 2 * math.pi) for a, b in zip(ph[:-1], ph[1:])])
    rate = st / h
    for i in range(len(h)):
        nb = np.concatenate([rate[max(i - 3, 0):i], rate[i + 1:i + 4]])
        if len(nb) == 0:
            continue
        pred = float(np.median(nb)) * h[i]
        big = h[i] * float(np.max(np.abs(nb))) > 2 * math.pi * frac
        if abs(pred - st[i]) > math.pi or big:
            nflag += 1
            a, b = z0 + t[i] * (z1 - z0), z0 + t[i + 1] * (z1 - z0)
            print(f"{rec['tag']} {name}: interval {a.real:.4f}{a.imag:+.4f}i .. {b.real:.4f}{b.imag:+.4f}i, h {h[i]:.4f}, "
                  f"step {st[i]:+.3f}, predicted {pred:+.2f}, largest neighbouring rate {np.max(np.abs(nb)):.1f}/unit")
print(f"{rec['tag']}: {nflag} intervals flagged (fraction {frac})")
