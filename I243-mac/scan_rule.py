#!/usr/bin/env python3
"""I243-mac: the intervals of a count record that the alias rule of #242 (hp/modecount_wind.py) would bisect at once,
from the record's samples alone (no determinants).

    python3 scan_rule.py RESULTS.jsonl [ALIAS]          (ALIAS default pi/2; the last record of the file is read)

For each interval, the local scale is |Delta ln g| / h (ln|g| change and wrapped phase step) on the interval and up to 3
intervals each side, and at the first and last 3 intervals of an edge also the largest scale of the other edges' 3
intervals at that corner. An interval is flagged when h * scale > ALIAS (or its step exceeds the record's tol). A flag
says where the re-evaluation with the new rule (modecount_wind.py on a copy of the cache) adds determinants first; the
cascade after it is not predicted here. Control: #212's kf 23 record must have T's last two intervals flagged.
"""
import json
import math
import sys

rec = [json.loads(line) for line in open(sys.argv[1])][-1]
alias = float(sys.argv[2]) if len(sys.argv) > 2 else math.pi / 2
NB = 3


def wrap(a):
    return math.remainder(a, 2 * math.pi)


edges = {}
for name, e in rec["edges"].items():
    z0, z1 = complex(*e["z0"]), complex(*e["z1"])
    L = abs(z1 - z0)
    S = e["samples"]
    h = [(b[0] - a[0]) * L for a, b in zip(S[:-1], S[1:])]
    st = [wrap(b[2] - a[2]) for a, b in zip(S[:-1], S[1:])]
    sc = [abs(complex(b[1] - a[1], s)) / hh for a, b, s, hh in zip(S[:-1], S[1:], st, h)]
    edges[name] = (z0, z1, S, h, st, sc)
corner = {}
for name, (z0, z1, S, h, st, sc) in edges.items():
    corner[(z0, name)] = max(sc[:NB])
    corner[(z1, name)] = max(sc[-NB:])
nflag = 0
for name, (z0, z1, S, h, st, sc) in edges.items():
    ends = [max([s for (p, nm), s in corner.items() if p == z and nm != name] + [0.0]) for z in (z0, z1)]
    for i in range(len(h)):
        s = max(sc[max(i - NB, 0):i + NB + 1] + ([ends[0]] if i < NB else []) + ([ends[1]] if i >= len(h) - NB else []))
        if h[i] * s > alias or abs(st[i]) > rec["tol"]:
            nflag += 1
            a, b = z0 + S[i][0] * (z1 - z0), z0 + S[i + 1][0] * (z1 - z0)
            print(f"{rec['tag']} {name}: interval {a.real:.4f}{a.imag:+.4f}i .. {b.real:.4f}{b.imag:+.4f}i, h {h[i]:.4f}, "
                  f"step {st[i]:+.3f}, dln|g| {S[i + 1][1] - S[i][1]:+.3f}, scale {s:.2f}/unit, h*scale {h[i] * s:.2f}")
print(f"{rec['tag']}: {nflag} of {sum(len(v[3]) for v in edges.values())} intervals flagged (alias {alias:.4f})")
