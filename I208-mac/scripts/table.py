#!/usr/bin/env python3
"""table.py [R]: the per-row table of #208 from this folder's cmp_*.json, rayid_*.log and exits.txt (markdown)."""
import glob
import json
import os
import re
import sys

R = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def walls():
    w = {}
    p = os.path.join(R, "exits.txt")
    if os.path.exists(p):
        for ln in open(p):
            m = re.match(r"(\S+): rc (\d+), wall (\d+) s", ln)
            if m:
                w[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return w


def rayid(name):
    p = os.path.join(R, f"rayid_{name}.log")
    if not os.path.exists(p):
        return "-"
    txt = open(p).read()
    m = re.search(r"ray BOX lines: (\w+) \((\d+) of (\d+)", txt)
    v = "PASS" if "VERDICT: PASS" in txt else "FAIL"
    return f"{m.group(1)} {m.group(3)} lines, {v}" if m else v


def main():
    w = walls()
    print("| run | stops | overlap | inside | radius review / stored, last stop | worst \\|mid diff\\|/(r+r) | "
          "verdict | ray identity | wall |")
    print("|---|---|---|---|---|---|---|---|---|")
    for f in sorted(glob.glob(os.path.join(R, "cmp_*.json"))):
        name = os.path.basename(f)[4:-5]
        d = json.load(open(f))
        rows = d["rows"]
        last = rows[-1] if rows else {}
        rad = f"{last.get('r_review', 0):.2e} / {last.get('r_stored', 0):.2e}" if rows else "-"
        rc, wall = w.get(name, (None, None))
        print(f"| {name} | {len(rows)} | {d['n'] - d['missed']}/{d['n']} | {d.get('inside', '-')}/{d['n']} | {rad} | "
              f"{d['worst_sep']:.1e} | {'PASS' if d['passed'] else 'FAIL'} ({d['expect']}) | {rayid(name)} | "
              f"{wall if wall is not None else '-'} s |")


if __name__ == "__main__":
    main()
