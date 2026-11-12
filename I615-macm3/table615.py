#!/usr/bin/env python3
"""I615: lambda(32) and lambda(48) of the D 58 brackets on the exact determinant (this folder) beside #458's double-double LU values
(I458-macm3), the spreads over b1 to b5, the differences, the controls. Usage: python3 table615.py [I458 dir]"""
import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
i458 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "I458-macm3")
S = "up12_D58.0060"
def load(d, b):
    f = os.path.join(d, f"gamma_{S}_{b}.jsonl")
    if not os.path.exists(f) or os.path.getsize(f) == 0: return None
    r = json.loads(open(f).readline())
    log = open(os.path.join(d, f"gamma_{S}_{b}.log")).read()
    m48 = log.split("M = 48: series truncation at the solution")[-1]
    n48 = len(re.findall(r"^\s+lam \d", m48, re.M))
    return dict(l32=r["lam"], l48=r["M48"]["lam"], n32=r["n_det"], n48=n48, secs=r["seconds"] + r["M48"]["seconds"], floor=r["M48"]["floor"])
bs = ["b1", "b2", "b3", "b4", "b5", "b1r"]
new = {b: load(here, b) for b in bs}
old = {b: load(i458, b) for b in bs}
print("| bracket | λ(32) ball | λ(32) LU (#458) | λ(48) ball | λ(48) LU (#458) | ball − LU at M 48 | dets M 32 / M 48 (ball) | run time M 32 + M 48 (s) | floor check |")
print("|---|---|---|---|---|---|---|---|---|")
for b in bs:
    n, o = new[b], old[b]
    if n is None: print(f"| {b} | not finished | | | | | | | |"); continue
    print(f"| {b} | {n['l32']!r} | {o['l32']!r} | {n['l48']!r} | {o['l48']!r} | {n['l48'] - o['l48']:+.2e} | {n['n32']} / {n['n48']} | {n['secs']:.0f} | {n['floor']} |")
def spread(d, k):
    v = [d[b][k] for b in bs[:5] if d[b] is not None]
    return (max(v) - min(v), min(v), max(v), len(v)) if v else None
for k, lab in (("l32", "λ(32)"), ("l48", "λ(48)")):
    for nm, d in (("ball", new), ("LU (#458)", old)):
        s = spread(d, k)
        if s: print(f"\nSpread over b1 to b5 of {lab}, {nm}: {s[0]:.3e} (min {s[1]!r}, max {s[2]!r}, {s[3]} brackets)")
if new["b1r"] and new["b1"]:
    print(f"\nControl b1r vs b1: λ(32) {'bit for bit equal' if new['b1r']['l32'] == new['b1']['l32'] else 'DIFFERENT'}, λ(48) {'bit for bit equal' if new['b1r']['l48'] == new['b1']['l48'] else 'DIFFERENT'}")
