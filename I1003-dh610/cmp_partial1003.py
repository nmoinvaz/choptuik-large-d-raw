#!/usr/bin/env python3
"""cmp_partial1003.py PARTIAL.json REF.json [--mutate]: the partial file's sigma_str entries against the reference's, string by string
(the partial file has no doubles). Pass: every entry equal (relative difference 0.0). --mutate changes one digit of the reference's entry 7 (the run must fail).
Exit 1 on failure."""
import json
import sys
import mpmath as mp

mp.mp.dps = 40
a = sys.argv[1:]
pil, ref = json.load(open(a[0])), json.load(open(a[1]))
mut = "--mutate" in a
rs = [list(p) for p in ref["sigma_str"]]
if mut:
    rs[7][0] = rs[7][0][:-3] + ("0" if rs[7][0][-3] != "0" else "1") + rs[7][0][-2:]
n = len(pil["sigma_str"])
print(f"partial k_done {pil['k_done']} entries {n} vs reference entries {len(rs)} ; string compare only (no doubles in the partial file)")
worst, bad = mp.mpf(0), []
for k in range(n):
    p = [mp.mpf(x) for x in pil["sigma_str"][k]]
    r = [mp.mpf(x) for x in rs[k]]
    mod = max(mp.sqrt(r[0] ** 2 + r[1] ** 2), mp.sqrt(p[0] ** 2 + p[1] ** 2))
    d = max(abs(p[0] - r[0]), abs(p[1] - r[1])) / mod if mod else mp.mpf(0)
    same = pil["sigma_str"][k] == rs[k]
    worst = max(worst, d)
    if not same:
        bad.append((k, mp.nstr(d, 3)))
    print(f"sigma_{k}: max rel diff {mp.nstr(d, 3) if d else '0.0'}, strings equal {same}")
print(f"{'PASS' if not bad else 'FAIL'}: worst {mp.nstr(worst, 3) if worst else 0}, unequal {bad}" + (" (control --mutate)" if mut else ""))
sys.exit(0 if not bad else 1)
