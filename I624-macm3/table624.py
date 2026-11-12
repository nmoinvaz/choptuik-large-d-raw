#!/usr/bin/env python3
"""I624: share of non-linear entries (|d2 - 2 d1| > |d1|/2) among the entries changed by one ulp, D 61 at #584's q1 and s3, M 40, 48 (kf 23 and
#609's kf 27), 64 (#609/#612), with the blocks. Usage: python3 table624.py [I609 dir]"""
import os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
i609 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "I609-macm3")
def rec(path):
    if not os.path.exists(path): return None
    t = open(path).read()
    m = re.search(r"entries changed by one ulp (\d+) of", t)
    if not m: return None
    c = int(m.group(1)); b = int(re.search(r"> \|d1\|/2: (\d+)", t).group(1))
    j = re.search(r"counts, (\d+) in all", t)
    lst = [int(x) for x in re.search(r"rows by block of 4M: \[(.*?)\]", t).group(1).split()] if b else []
    if j: assert int(j.group(1)) == b == sum(lst), path
    cen, hor = (lst[0], lst[-1] if len(lst) > 1 else 0) if lst else (0, 0)
    lg = re.search(r"\|A\| (\S+), \|d1\| (\S+), \|d2\|", t)
    return b, c, 100 * b / c, cen, hor, (float(lg.group(2)) / float(lg.group(1)) if lg else None)
cases = [("M 40, kf 23 (resampled from M 64 kf 23)", f"{here}/M40_q1.log", f"{here}/M40_s3.log"),
         ("M 48, kf 23 (resampled from M 64 kf 23; added)", f"{here}/M48kf23_q1.log", f"{here}/M48kf23_s3.log"),
         ("M 48, kf 27 (I280-macm3's state; #609)", f"{i609}/D61_M48_q1.log", f"{i609}/D61_M48_s3.log"),
         ("M 64, kf 23 (I252-mac's state; #609)", f"{i609}/D61_M64_q1.log", f"{i609}/D61_M64_s3.log"),
         ("M 80, kf 23", f"{here}/M80_q1.log", f"{here}/M80_s3.log")]
print("| state | q1 non-linear (of changed): share, centre / horizon | s3 non-linear (of changed): share, centre / horizon | largest abs(d1)/abs(A) q1; s3 |")
print("|---|---|---|---|")
for lab, q, s in cases:
    a, b = rec(q), rec(s)
    f = lambda r: "setup refused (series gate)" if r is None else f"{r[0]} of {r[1]}: {r[2]:.3g}%, {r[3]} / {r[4]}"
    g = lambda r: "-" if r is None or r[5] is None else f"{r[5]:.1e}"
    print(f"| {lab} | {f(a)} | {f(b)} | {g(a)}; {g(b)} |")
