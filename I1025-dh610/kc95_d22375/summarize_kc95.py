#!/usr/bin/env python3
"""#1025 kc95_d22375 (dh610) summarize_kc95.py [PRED]: the scan rows of D<D>/ as a table (lambda, hybrid sign, noise signs, float64 sign, ln|det|, seconds) and the second-order facts, from scan/ and the source record.
No number is typed by hand. usage (from this folder): python3 -I summarize_kc95.py > summary_kc95.txt"""
import json, sys, glob, statistics
D = '22.375'
rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
rows = sorted((x for f in sorted(glob.glob(f"scan/scan_D{D}_p*.jsonl")) for x in rd(f)), key=lambda x: (x["lam"], x["sec"]))
sg = lambda v: "+" if v > 0 else "-"
print("| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |")
print("|---|---|---|---|---|---|")
for x in rows:
    print(f"| {x['lam']:.3f} | {sg(x['sign'])} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])} | {x['ln']!r} | {x['sec']} |")
t = [x["sec"] for x in rows]
print()
print(f"scan points: {len(rows)} evaluations, seconds per point min {min(t)}, median {statistics.median(t):.0f}, max {max(t)}, sum {sum(t)}; outside 1800 to 4000 s: {[(round(x['lam'], 3), x['sec']) for x in rows if not 1800 <= x['sec'] <= 4000]}")
import os
tag = open(f"tag.txt").read().strip() if os.path.exists(f"tag.txt") else "l1kc95dh610d22375"
rec = [r for r in rd(f"in/{tag}.jsonl") if r["D"] == float(D)][-1]
print(f"the regridded record at D {D}: |F| {rec['F']!r}, steps {rec['steps']}, constraint {rec['constraint']!r}, Delta {rec['Delta']!r}, h {rec.get('h')}, seconds {rec.get('seconds')}")
fl = [x for x in rows if (x["f64_sign"] > 0) != (x["sign"] > 0)]
print(f"float64 sign differs from the hybrid at: {[round(x['lam'], 3) for x in fl]}")
