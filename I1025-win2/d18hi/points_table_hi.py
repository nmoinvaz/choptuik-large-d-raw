#!/usr/bin/env python3
"""points_table.py [DIR]: the 41 points of the D 18.1875 hybrid scan above the d18mid window, lambda 1.95 to 2.35 (scan_hi_D18.1875_A.jsonl and _B.jsonl) as a markdown table: lambda, process, hybrid sign, hybrid ln|det|, the noise signs (1e-15, 2 seeds),
the float64 sign and ln|det|, the seconds; the repeated point 1.95 from both processes; and the per-process seconds per point."""
import json
import os
import sys

H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
rows = []
for P in "AB":
    for line in open(H + "scan_hi_D18.1875_%s.jsonl" % P):
        if line.strip():
            r = json.loads(line)
            r["P"] = P
            rows.append(r)
rows.sort(key=lambda r: (round(r["lam"], 2), r["P"]))
print(r"| lambda | process | hybrid sign | hybrid ln\|det\| | noise 1e-15 signs (2 seeds) | float64 sign | float64 ln\|det\| | s |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| %.2f | %s | %+d | %.10f | %s | %+d | %.10f | %d |" % (r["lam"], r["P"], r["sign"], r["ln"], [int(x) for x in r["noise"]], r["f64_sign"], r["f64_ln"], r["sec"]))
print()
for P in "AB":
    s = [r["sec"] for r in rows if r["P"] == P]
    print("process %s: %d points, %d to %d s per point, mean %.0f s, sum %d s" % (P, len(s), min(s), max(s), sum(s) / len(s), sum(s)))
a = [r for r in rows if round(r["lam"], 2) == 1.95]
if len(a) == 2:
    print("repeated point 1.95: A sign %+d ln %.10f f64 %+d %.10f; B sign %+d ln %.10f f64 %+d %.10f; ln difference %.3e" % (
        a[0]["sign"], a[0]["ln"], a[0]["f64_sign"], a[0]["f64_ln"], a[1]["sign"], a[1]["ln"], a[1]["f64_sign"], a[1]["f64_ln"], a[0]["ln"] - a[1]["ln"]))
