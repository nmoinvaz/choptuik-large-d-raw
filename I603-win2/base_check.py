#!/usr/bin/env python3
"""#603: the exact Delta (the last entry of every part zh, zl, z2..z7 summed in mpmath) of the start state against the state it replaces (crawlG's D 225.13125 on the double-double projector's rows)
and the table's row. usage: python base_check.py BASE.npz CRAWLG.npz DELTA_ALL.csv"""
import csv, json, sys
import numpy as np
from mpmath import mp, mpf
mp.dps = 60


def delta(path):
    z = np.load(path)
    parts = [k for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in z.files]
    return sum((mpf(float(z[k][-1])) for k in parts), mpf(0)), parts, json.loads(str(z["meta"]))["D"]


b, pb, Db = delta(sys.argv[1])
g, pg, Dg = delta(sys.argv[2])
row = [r for r in csv.DictReader(open(sys.argv[3])) if abs(float(r["D"]) - 225.13125) < 1e-9][0]
t = sum((mpf(float(row[k])) for k in ("Delta_q0", "Delta_q1", "Delta_q2", "Delta_q3") if row[k] != ""), mpf(0))
print(f"base   D {Db}: parts {pb}: Delta {mp.nstr(b, 30)}")
print(f"crawlG D {Dg}: parts {pg}: Delta {mp.nstr(g, 30)}")
print(f"table  D 225.13125 ({row['kind']}, err {row['err']}): Delta {mp.nstr(t, 30)}")
print(f"base - crawlG = {mp.nstr(b - g, 6)}   base - table = {mp.nstr(b - t, 6)}   (#595: the shift to the exact rows is -7.8e-16 at D 225.13)")
