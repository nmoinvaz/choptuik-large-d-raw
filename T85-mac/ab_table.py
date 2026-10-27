"""T85: the waypoint table. Per D both runs reached: Delta_full1 of A (last node 0.8) and B (0.85), A - B (the
uncertainty of Delta_full1 there, a spread between two discretisations), and the rational formula's value for
scale. Run from solver/data of the code repository (formula_all's loaders read the scan files from there).

    cd solver/data && python3 ../../../raw-T85/ab_table.py [DIR]      (DIR: the run folder, default raw-T85)
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), ".."))
import formula_all  # noqa: E402

R = sys.argv[1] if len(sys.argv) > 1 else "/Users/nathan/Source/raw-T85/"


def full1(path):
    out = {}
    for line in open(path):
        if line.strip():
            r = json.loads(line)
            if "Delta_full1" in r:
                out[round(r["D"], 4)] = (r["Delta_full1"] + r.get("Delta_full1_lo", 0.0), r["F"], r["dDelta_pin"], r["its"])
    return out


A, B = full1(os.path.join(R, "x80.jsonl")), full1(os.path.join(R, "x85.jsonl"))
print(f"A (0.8): {len(A)} points to D {max(A, default=0)}; B (0.85): {len(B)} points to D {max(B, default=0)}")
print(f"{'D':>7} {'A Delta_full1':>18} {'B Delta_full1':>18} {'A - B':>9} {'A - formula':>12} {'dDelta_pin A':>13} {'B':>9}")
for D in sorted(set(A) & set(B)):
    a, b, f = A[D][0], B[D][0], formula_all.delta(D)
    print(f"{D:7.2f} {a:18.13f} {b:18.13f} {a - b:+9.1e} {a - f:+12.1e} {A[D][2]:+13.1e} {B[D][2]:+9.1e}")
