#!/usr/bin/env python3
"""#1025 kc79_d2025 (dh610) summarize_kc79.py: the regrid and the scan beside win2's, from regrid/, scan/, in/ref_win2_*. No number is typed by hand. usage (from this folder): python3 -I summarize_kc79.py > summary_kc79.txt"""
import json, glob, statistics
rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
r, w = rd("regrid/l1kc79dh610d2025.jsonl")[-1], rd("in/ref_win2_rec_k79_D20.2500.jsonl")[-1]
print("| record | this machine (Linux) | win2 (Windows) | difference |")
print("|---|---|---|---|")
for k in ("F_start", "F", "steps", "constraint", "Delta", "seconds"):
    a, b = r[k], w[k]
    d = "" if k == "seconds" else f"{a - b:+.3e}"
    print(f"| {k} | {a!r} | {b!r} | {d} |")
print(f"| Delta minus its k_c 71 source | {r['Delta'] - r['Delta_src']:+.6e} | {w['Delta'] - w['Delta_src']:+.6e} | |")
print()
rows = sorted((x for f in sorted(glob.glob("scan/scan_D20.25_p*.jsonl")) for x in rd(f)), key=lambda x: (x["lam"], x["sec"]))
wm = {round(x["lam"], 2): x for x in rd("in/ref_win2_scan_k79_D20.25.jsonl")}
sg = lambda s: "+" if s > 0 else "-"
print("| lambda | hybrid sign (mine, win2) | noise signs (robust) | float64 sign (mine, win2) | ln of abs det (mine, win2) | mine minus win2 | seconds (mine) |")
print("|---|---|---|---|---|---|---|")
for x in rows:
    k = round(x["lam"], 2); v = wm.get(k)
    print(f"| {k:.2f} | {sg(x['sign'])}, {sg(v['sign']) if v else 'n/a'} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])}, {sg(v['f64_sign']) if v else 'n/a'} | {x['ln']:.6f}, {v['ln']:.6f} | {x['ln'] - v['ln']:+.6f} | {x['sec']} |" if v else f"| {k:.2f} | {sg(x['sign'])}, n/a | | | {x['ln']:.6f} | | {x['sec']} |")
s = [x["sec"] for x in rows]
print()
print(f"scan points: {len(rows)} evaluations, seconds per point min {min(s)}, median {statistics.median(s):.0f}, max {max(s)}, sum {sum(s)}; outside 800 to 1800 s: {sum(1 for t in s if not 800 <= t <= 1800)}")
