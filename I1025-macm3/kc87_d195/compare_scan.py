#!/usr/bin/env python3
"""#1025 macm3b kc87_d195 (my analysis script, information only): this machine's scan points against dh610's at the lambda values both evaluated (1.36 to 1.42).
Usage: compare_scan.py MINE_JSONL REF_JSONL"""
import json, sys
mine = {r["lam"]: r for r in map(json.loads, open(sys.argv[1]) if True else [])}
ref = {r["lam"]: r for r in map(json.loads, open(sys.argv[2]))}
sg = lambda x: "+" if x > 0 else "-"
print("lambda | hybrid sign mine / dh610's | ln|det| mine | ln|det| dh610's | difference | noise-robust mine / dh610's")
same = 0; tot = 0
for lam in sorted(set(mine) & set(ref)):
    a, b = mine[lam], ref[lam]; tot += 1; same += (a["sign"] == b["sign"])
    print("%.2f | %s / %s | %.6f | %.6f | %+.6f | %s / %s" % (lam, sg(a["sign"]), sg(b["sign"]), a["ln"], b["ln"], a["ln"] - b["ln"], a["noise_robust"], b["noise_robust"]))
print("common lambdas %d, same hybrid sign at %d" % (tot, same))
