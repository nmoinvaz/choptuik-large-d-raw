#!/usr/bin/env python3
"""check_logs1031.py LOG [--mutate=differ|control] [--expect 22]: reads a cols_ test log. Pass: exit 0 in the log, 'test result: ok. 2 passed', the line '333000 entries compared, none differ' once, and
every line with 'control:' (the control COLS_MUT_ULP, one ulp of p_1 in one lane) reads '0 of N entries differ ...; control: K differ' with K > 0, EXPECT such lines (22 in #1009 and here). --mutate=differ
turns the first line's '0 of' into '3 of' and --mutate=control sets the first K to 0: the check must then fail (exit 1). The first version of run1031.sh's summary counted only the lines with '(parallel: 0)'."""
import re
import sys

a = sys.argv[1:]
txt = open(a[0]).read().splitlines()
mut = next((x.split("=")[1] for x in a if x.startswith("--mutate=")), "")
exp = int(a[a.index("--expect") + 1]) if "--expect" in a else 22
pat = re.compile(r"^\s*(?:M|B) (\d+) (.+?): (\d+) of (\d+) entries differ(?: \(parallel: (\d+)\))?; control: (\d+) differ$")
lines = [l for l in txt if "control:" in l]
if mut == "differ" and lines:
    lines[0] = lines[0].replace(": 0 of", ": 3 of", 1)
if mut == "control" and lines:
    lines[0] = re.sub(r"control: \d+ differ", "control: 0 differ", lines[0])
bad, minK, n = [], None, 0
for l in lines:
    m = pat.match(l)
    if not m:
        bad.append(("unparsed", l.strip()[:100])); continue
    n += 1
    nd, par, k = int(m.group(3)), m.group(5), int(m.group(6))
    minK = k if minK is None else min(minK, k)
    if nd != 0 or (par is not None and int(par) != 0):
        bad.append(("differ", l.strip()[:100]))
    if k <= 0:
        bad.append(("control did not fire", l.strip()[:100]))
ex = [l for l in txt if l.startswith("exit ")]
ok = (not bad and n == exp and ex and ex[-1] == "exit 0" and any(l.startswith("test result: ok. 2 passed") for l in txt)
      and sum("333000 entries compared, none differ" in l for l in txt) == 1)
print(f"{a[0]}{' --mutate=' + mut if mut else ''}: {n} control lines (expect {exp}), smallest K {minK}, last '{ex[-1] if ex else None}', problems {bad[:3]}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
