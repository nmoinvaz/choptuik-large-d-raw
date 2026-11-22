#!/usr/bin/env python3
"""points_table_leap.py DIR D: the evaluations of the four scan processes of one D (scan_D<D>_P1..P4.jsonl) as markdown tables, with the per-process seconds per point."""
import json
import os
import sys

H = sys.argv[1].replace("\\", "/").rstrip("/") + "/"
tag = "%g" % float(sys.argv[2])
for P in (1, 2, 3, 4):
    path = H + "scan_D%s_P%d.jsonl" % (tag, P)
    rows = [json.loads(x) for x in open(path) if x.strip()] if os.path.exists(path) else []
    print("### D %s, process P%d" % (tag, P))
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
