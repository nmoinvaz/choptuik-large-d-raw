#!/usr/bin/env python3
"""Table of the I609 logs (run_609.sh): per case the entries changed by one ulp, the entries with
|d2 - 2 d1| > |d1|/2, their share of the changed ones, the rows/cols by block of 4M, and the largest
relative jump |d1|/|A| among them. Usage: python3 table609.py [dir]"""
import glob, os, re, sys
d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
order = ["ctrl_M32_phys", "ctrl_M32_physfull", "D30_M32_pos", "D30_M40_phys", "D30_M40_pos", "D30_M48_phys", "D30_M48_phys_fresh", "D30_M48_pos",
         "D30_M64_phys", "D30_M64_pos", "D30_M80_phys", "D30_M80_pos", "D61_M48_q1", "D61_M48_s3", "D61_M64_q1", "D61_M64_s3"]
print("| case | at | changed by 1 ulp | non-linear | share | rows by block | cols by block | largest abs(d1)/abs(A) |")
print("|---|---|---|---|---|---|---|---|")
for name in order:
    f = os.path.join(d, name + ".log")
    if not os.path.exists(f):
        continue
    t = open(f).read()
    m = re.search(r"at (\S+)\+(\S+)i, n (\d+): entries changed by one ulp (\d+) of (\d+)", t)
    if not m:
        print(f"| {name} | no result | | | | | | |")
        continue
    ch = int(m.group(4))
    b = int(re.search(r"> \|d1\|/2: (\d+)", t).group(1))
    rows = re.search(r"rows by block of 4M: (\[.*?\]); cols by block: (\[.*?\])", t)
    lg = re.search(r"\|A\| (\S+), \|d1\| (\S+), \|d2\|", t)
    rel = f"{float(lg.group(2)) / float(lg.group(1)):.1e}" if lg else "-"
    print(f"| {name} | {m.group(1)}+{m.group(2)}i | {ch} | {b} | {100 * b / ch:.4f}% | {rows.group(1) if rows else '-'} | {rows.group(2) if rows else '-'} | {rel} |")
