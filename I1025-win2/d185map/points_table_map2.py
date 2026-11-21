#!/usr/bin/env python3
"""points_table_map2.py [DIR]: the evaluations of the two windows of the D 18.5 map (scan_A.jsonl: lambda 2.40 repeat, then 2.41 to 2.60; scan_B.jsonl: lambda 1.55 repeat, then 1.00 to 1.54) as markdown tables: lambda, hybrid sign,
hybrid ln|det|, the noise signs (1e-15, 2 seeds), the float64 sign and ln|det|, the seconds; and the per-process seconds per point."""
import json
import os
import sys

H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
for P, path, title in (("A", H + "scan_A.jsonl", "window A (2.40 repeat, then 2.41 to 2.60)"), ("B1", H + "b_split/scan_B1.jsonl", "window B1 (1.55 repeat, then 1.28 to 1.54)"),
                       ("B2", H + "b_split/scan_B2.jsonl", "window B2 (1.55 repeat, then 1.00 to 1.27)"), ("Bstopped", H + "scan_B_stopped.jsonl", "the first run's stopped B (1.55 repeat, then 1.00 on; information)")):
    rows = [json.loads(x) for x in open(path) if x.strip()] if os.path.exists(path) else []
    print("### " + title)
    print()
    print(r"| lambda | hybrid sign | hybrid ln\|det\| | noise 1e-15 signs (2 seeds) | float64 sign | float64 ln\|det\| | s |")
    print("|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: r["lam"]):
        print("| %.2f | %+d | %.10f | %s | %+d | %.10f | %d |" % (r["lam"], r["sign"], r["ln"], [int(x) for x in r["noise"]], r["f64_sign"], r["f64_ln"], r["sec"]))
    if rows:
        s = [r["sec"] for r in rows]
        print()
        print("process %s: %d points, %d to %d s per point, mean %.0f s, sum %d s" % (P, len(s), min(s), max(s), sum(s) / len(s), sum(s)))
    print()
