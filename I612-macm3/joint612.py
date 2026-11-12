#!/usr/bin/env python3
"""Parse a modecount_smooth.py --joint log (I612): count, the non-zero (row block, column block) entries with their share of
the block (4M x 4M), the rows' and columns' fields (p, m, a, c) and the tau lanes' min / median / max (and lanes with none).
Usage: python3 joint612.py LOG M"""
import re, sys
import numpy as np
t = open(sys.argv[1]).read()
M = int(sys.argv[2])
cnt = int(re.search(r"> \|d1\|/2: (\d+)", t).group(1))
m = re.search(r"counts, (\d+) in all:\n((?:\s+\d+)+\n)+", t)
head = re.search(r"counts, (\d+) in all:\n", t)
rows = []
for line in t[head.end():].split("\n"):
    if re.fullmatch(r"\s+\d+(\s+\d+)*", line): rows.append([int(x) for x in line.split()])
    else: break
J = np.array(rows)
assert J.sum() == cnt == int(head.group(1)), (J.sum(), cnt)
print(f"count {cnt}, joint sums to {J.sum()} ({J.shape[0]} x {J.shape[1]} blocks of 4M = {4*M})")
for a, b in zip(*np.nonzero(J)):
    print(f"  block ({a}, {b}): {J[a, b]} = {100 * J[a, b] / (4 * M) ** 2:.1f}% of the block")
for lab in ("rows", "cols"):
    f = re.search(lab + r" by field \(p, m, a, c\): \[(.*?)\]; by tau lane: \[(.*?)\]", t, re.S)
    fld = [int(x) for x in f.group(1).split()]; lane = np.array([int(x) for x in f.group(2).split()])
    assert sum(fld) == cnt and lane.sum() == cnt and len(lane) == M
    print(f"  {lab}: fields p {fld[0]}, m {fld[1]}, a {fld[2]}, c {fld[3]}; tau lanes min {lane.min()}, median {int(np.median(lane))}, max {lane.max()}, lanes with none {(lane == 0).sum()} of {M}")
