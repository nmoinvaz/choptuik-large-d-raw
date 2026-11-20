#!/usr/bin/env python3
"""check251b.py LOG: the coordinator's pass rule for the D 251.88 flag-on polish with --od_start_F 0, fixed before the run:
the log has no "attempt stopped"; its "octo-double Newton: K steps, max|F| X" line has X <= 1e-50; and "base polish saved as" follows it.
Prints each condition and PASS or FAIL, exit 0 or 1. Controls: the flag-off log (resolve251_r0.log) must PASS, the stopped run (resolve251_r1.log) must FAIL."""
import re
import sys

lines = open(sys.argv[1]).read().splitlines()
stopped = [i for i, ln in enumerate(lines) if "attempt stopped" in ln]
newton = [(i, ln) for i, ln in enumerate(lines) if "octo-double Newton:" in ln]
saved = [i for i, ln in enumerate(lines) if ln.startswith("base polish saved as")]
conds = []
conds.append(("no 'attempt stopped' line", not stopped, f"{len(stopped)} such lines"))
X = None
if newton:
    m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.]+e[-+]?\d+)", newton[-1][1])
    if m:
        X = float(m.group(2))
        conds.append(("'octo-double Newton: K steps, max|F| X' has X <= 1e-50", X <= 1e-50, f"K {m.group(1)}, X {X:.1e}"))
if X is None:
    conds.append(("'octo-double Newton: K steps, max|F| X' has X <= 1e-50", False, "no such line"))
conds.append(("'base polish saved as' follows it", bool(newton and saved and saved[-1] > newton[-1][0]), f"{len(saved)} such lines"))
ok = all(c[1] for c in conds)
for name, good, note in conds:
    print(f"  {'ok  ' if good else 'FAIL'} {name} ({note})")
print(f"{sys.argv[1]}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
