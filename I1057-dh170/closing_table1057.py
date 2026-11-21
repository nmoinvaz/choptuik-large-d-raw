#!/usr/bin/env python3
"""#1057 closing table: every ks_chain3b state read in this reopening (D 260.0073 to the last), from the near_null records of this folder: the two lowest vectors' sigma and Delta share, the pick (largest share), the angle alpha of the Delta direction in their plane (alpha1057.py's definition) and the pinned Delta component.
    closing_table1057.py"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import alpha1057 as al  # noqa: E402

rows = []
for p in glob.glob(os.path.join(HERE, "c3b_ks293_D*.json")):
    m = re.search(r"c3b_ks293_D(\d+\.\d+)\.json$", p)
    if not m:
        continue
    D = float(m.group(1))
    if D < 260.0:
        continue
    r = json.load(open(p)); v = r["vectors"]
    pick = max(range(len(v)), key=lambda i: v[i]["delta"])
    rows.append((r["D"], v[0]["sigma"], v[0]["delta"], v[1]["sigma"], v[1]["delta"], pick + 1, al.alpha_of(v[0]["delta"], v[1]["delta"]), r["step_pinned"]["delta"]))
rows.sort()
print("| D | σ(v1) | Δ share v1 | σ(v2) | Δ share v2 | Δ pick | α (°) | pinned Δ |")
print("|---|---|---|---|---|---|---|---|")
for D, s1, d1, s2, d2, pk, a, pin in rows:
    print(f"| {D:.4f} | {s1:.4e} | {d1:.3f} | {s2:.4e} | {d2:.3f} | v{pk} | {a:.2f} | {pin:+.1e} |")
print(f"{len(rows)} states")
