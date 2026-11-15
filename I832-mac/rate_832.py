#!/usr/bin/env python3
"""#832: the rate at which the linear range r falls with D, from delta_range.csv (the smallest resolved field's r per
state), over all states and over subsets, and between neighbours. Least-squares slopes of ln r against D; reported,
not judged. usage: python3 rate_832.py delta_range.csv"""
import csv
import sys

import numpy as np


def main(path):
    per = {}
    for row in csv.DictReader(open(path)):
        if row["resolved"] == "1":
            D, r = float(row["D"]), float(row["r"])
            per[D] = min(per.get(D, r), r)
    Ds = sorted(per)
    x, y = np.array(Ds), np.log([per[D] for D in Ds])
    for name, sel in (("all", x > 0), ("D <= 230.2", x <= 230.2), ("D >= 245", x >= 245), ("226 <= D", x >= 226)):
        if sel.sum() >= 2:
            print(f"  {name}: {int(sel.sum())} states, ln r falls by {-np.polyfit(x[sel], y[sel], 1)[0]:.3f} per unit of D")
    for a, b, ya, yb in zip(x, x[1:], y, y[1:]):
        print(f"  {a:.4f} -> {b:.4f}: {-(yb - ya) / (b - a):.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
