"""D 61 M 32 with the cut, fresh against October's records (I160-macm3).

Boxes: this run's 8 box lines against each run of October's hp/data/modecount_D61.0264_M32.log (it holds two runs, 16 box lines, no CR). Determinants:
this run's cache against October's hp/data/modecount_D61.0264_M32_evals.jsonl at the shared lambdas, split by each October line's ending (CR = written on
Windows). Usage: python3 compare_D61_M32.py
"""
import json
import math
import os
import re
import statistics

H = os.path.expanduser("~/Source/choptuik-large-d/hp/data")


def boxes(p):
    out = []
    for l in open(p, newline=""):
        if l.startswith("  box "):
            l = l.rstrip("\r\n")
            m = re.search(r"winding of g ([+-][0-9.]+) -> (-?\d+); expected zeros inside (\d+), candidate poles inside (\d+) -> winding of det M (-?\d+), zeros of det M <= (\d+); max phase step ([0-9.]+) rad", l)
            out.append((l.split()[1], m.groups()))
    return out


fresh = boxes("count.log")
oct_all = boxes(os.path.join(H, "modecount_D61.0264_M32.log"))
print(f"fresh boxes {len(fresh)}, October's default log {len(oct_all)} box lines (runs of 8)")
for run in range(len(oct_all) // 8):
    oc = oct_all[8 * run:8 * run + 8]
    same_wind = all(a[1][1:6] == b[1][1:6] for a, b in zip(oc, fresh))
    same_line = all(a[1] == b[1] for a, b in zip(oc, fresh))
    steps = max(abs(float(a[1][6]) - float(b[1][6])) for a, b in zip(oc, fresh))
    print(f"  October run {run + 1}: winding of g, expected zeros, candidate poles, winding of det M, zeros <= identical in all 8: {same_wind}; "
          f"also the sign of the printed zero and the max phase step: {same_line} (largest phase step difference {steps:.1e} rad)")
print("  fresh :", [(n, g[3]) for n, g in fresh])
print("  October:", [(n, g[3]) for n, g in oct_all[:8]])
print()
cache = []
with open(os.path.join(H, "modecount_D61.0264_M32_evals.jsonl"), "rb") as fh:
    for raw in fh:
        cache.append((json.loads(raw.decode().strip()), raw.endswith(b"\r\n")))
new = {(r["re"], r["im"]): r for r in map(json.loads, open("data/modecount_D61.0264_M32_kf13_evals.jsonl"))}
print(f"October's cache {len(cache)} lines ({sum(1 for _, c in cache if c)} with CR, {sum(1 for _, c in cache if not c)} without); fresh {len(new)} points")
groups = {"CR lines": [], "non-CR lines": []}
for r, cr in cache:
    k = (r["re"], r["im"])
    if k in new:
        f = new[k]
        groups["CR lines" if cr else "non-CR lines"].append((abs(f["lnabs"] - r["lnabs"]), abs((f["arg"] - r["arg"] + math.pi) % (2 * math.pi) - math.pi), abs(f["pmin"] / r["pmin"] - 1)))
print("| group | shared points | largest d ln|det| | median | largest d arg | median | largest rel d pivot min |")
print("|---|---|---|---|---|---|---|")
for name, rows in groups.items():
    if rows:
        a, b, c = [x[0] for x in rows], [x[1] for x in rows], [x[2] for x in rows]
        print(f"| {name} | {len(rows)} | {max(a):.3e} | {statistics.median(a):.3e} | {max(b):.3e} | {statistics.median(b):.3e} | {max(c):.2e} |")
    else:
        print(f"| {name} | 0 | | | | | |")
