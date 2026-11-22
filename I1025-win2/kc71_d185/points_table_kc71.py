#!/usr/bin/env python3
"""points_table_kc71.py [DIR]: the evaluations of the four k_c 71 scan processes (scan_P1..P4.jsonl) as markdown tables: lambda, hybrid sign, hybrid ln|det|, the noise signs, the float64 sign and ln|det|, the seconds; and the per-process seconds per point."""
import json
import os
import sys

H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
for P in (1, 2, 3, 4):
    path = H + "scan_P%d.jsonl" % P
    rows = [json.loads(x) for x in open(path) if x.strip()] if os.path.exists(path) else []
    print("### process P%d" % P)
    print()
    print(r"| lambda | hybrid sign | hybrid ln\|det\| | noise 1e-15 signs (2 seeds) | float64 sign | float64 ln\|det\| | s |")
    print("|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: r["lam"]):
        print("| %.2f | %+d | %.10f | %s | %+d | %.10f | %d |" % (r["lam"], r["sign"], r["ln"], [int(x) for x in r["noise"]], r["f64_sign"], r["f64_ln"], r["sec"]))
    if rows:
        s = [r["sec"] for r in rows]
        print()
        print("process P%d: %d points, %d to %d s per point, mean %.0f s, sum %d s" % (P, len(s), min(s), max(s), sum(s) / len(s), sum(s)))
    print()
