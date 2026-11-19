#!/usr/bin/env python3
"""radius_check1027.py (#1027, exploration): the M = 7 solve of each xi1 0.25 walk's best point (A, w, harmonics of the walk's last accepted point) repeated at xi1 0.2 and 0.3; prints r_1, the residuals and
|F7/F5|, |F5/F3| per radius, so that a radius-independent zero shows the same r_1 (small) and the same ratios. Logs in logs/radius_*."""
import json
import os
import sys
import numpy as np
os.environ.setdefault("W1027_PY", sys.executable)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import walk1027 as W

HERE = os.path.dirname(os.path.abspath(__file__))
name, xi = sys.argv[1], sys.argv[2]
d = json.load(open(os.path.join(HERE, "walks", f"walk_{name}_xi0.25.json")))
p = [q for q in d["points"] if q.get("ok") and q.get("x")][-1]
r = W.attempt(p["A"], p["w"], p["x"], xi, 2, f"radius_{name}_xi{xi}", os.path.join(HERE, "logs"))
n = lambda F: float(np.hypot(*F))
print(f"{name} point ({p['A']:.9f}, {p['w']:.9f}) from the xi1 0.25 walk: r_1 at 0.25 {p['r1'][0]:+.3e}{p['r1'][1]:+.3e}i, |F7/F5| {n(p['F7']) / n(p['F5']):.4f}, |F5/F3| {n(p['F5']) / n(p['F3']):.4f}")
print(f"{name} xi1 {xi}: " + (f"r_1 {r['r1'][0]:+.3e}{r['r1'][1]:+.3e}i |r_3| {r['r3']:.1e} |r_5| {r['r5']:.1e} |r_7| {r['r7']:.1e} |F7/F5| {n(r['F7']) / n(r['F5']):.4f}, |F5/F3| {n(r['F5']) / n(r['F3']):.4f}" if r.get("r1") else r["why"]))
