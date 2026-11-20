#!/usr/bin/env python3
"""#1021 start rule (the coordinator, comment 7039516484, 20 Nov 12:26 UTC): the xi1 0.15 M = 5 walk of a box may start from
the box's own best xi1 0.2 M = 5 iterate. REPEAT_OUT is m5/m5_repeat.py's output for the box's 0.2 solve; its "counted:" log
(same folder) is that iterate. START is the box's "A W B3 C3" at its M = 3 zero (the walk's start point). Prints
"A W B3 C3 B5 C5": START's A, W and the counted log's end state (F_3/F_1, F_5/F_1 times A, as walk1026.py and m5_repeat.py
read them; the log prints 6 decimals). The counted log's |r_3|, |r_5| go to stderr. Exit 1 when the log is not at xi1 0.2 or
not at START's (A, W) to the log's 9 decimals (control: a START of another box must exit 1).
    python start02.py REPEAT_OUT START"""
import os
import re
import sys

rep, start = sys.argv[1:3]
A, W, _, _ = open(start).read().split()
cnt = re.findall(r"^counted: (\S+)$", open(rep).read(), re.M)
if len(cnt) != 1:
    sys.exit(f"{rep}: {len(cnt)} 'counted:' lines, not 1")
log = os.path.join(os.path.dirname(os.path.abspath(rep)), cnt[0])
t = open(log).read()
m = re.findall(r"FIXED-A M 5: A ([0-9.]+)\s+w/w_inf ([0-9.]+)", t)
f3 = re.findall(r"F_3/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_3 ([0-9.]+e[+-]\d+)", t)
f5 = re.findall(r"F_5/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_5 ([0-9.]+e[+-]\d+)", t)
xi = re.search(r"--xi1=([0-9.]+)", t).group(1)
if not (m and f3 and f5):
    sys.exit(f"{log}: no FIXED-A block")
la, lw = m[-1]
if xi != "0.2" or abs(float(la) - float(A)) > 6e-10 or abs(float(lw) - float(W)) > 6e-10:
    sys.exit(f"{log}: xi1 {xi}, (A, w) ({la}, {lw}), not xi1 0.2 at START's ({A}, {W})")
Af = float(la)
x = [float(f3[-1][0]) * Af, float(f3[-1][1]) * Af, float(f5[-1][0]) * Af, float(f5[-1][1]) * Af]
print(A, W, *(f"{v:.10f}" for v in x))
print(f"{cnt[0]}: |r_3| {f3[-1][2]}, |r_5| {f5[-1][2]}, xi1 {xi}, A {la}, w/w_inf {lw}", file=sys.stderr)
