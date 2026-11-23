#!/usr/bin/env python3
"""#1025 kc87_d2025 (dh610) summarize_kc87.py: the regrid and the scan beside win2's k_c 87 and this machine's k_c 79, from regrid/, scan/, in/ref_*. No number is typed by hand.
usage (from this folder): python3 -I summarize_kc87.py > summary_kc87.txt"""
import json, glob, statistics
rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
r, w, s79 = rd("regrid/l1kc87dh610d2025.jsonl")[-1], rd("in/ref_win2_rec_k87_D20.2500.jsonl")[-1], rd("in/l1kc79dh610d2025.jsonl")[-1]
print("| record | this machine (Linux) | win2 (Windows) | difference |")
print("|---|---|---|---|")
for k in ("F_start", "F", "steps", "constraint", "Delta", "seconds"):
    a, b = r[k], w[k]
    d = "" if k == "seconds" else f"{a - b:+.3e}"
    print(f"| {k} | {a!r} | {b!r} | {d} |")
print(f"| Delta minus its k_c 79 source | {r['Delta'] - r['Delta_src']:+.6e} | {w['Delta'] - w['Delta_src']:+.6e} | |")
print(f"| Delta_src (the k_c 79 state's) | {r['Delta_src']!r} | {w['Delta_src']!r} | {r['Delta_src'] - w['Delta_src']:+.3e} |")
print(f"| steps: k_c 87 over k_c 79 | {r['steps']}/{s79['steps']} = {r['steps'] / s79['steps']:.4f} | {w['steps']}/{w['steps']} | |")
print()
rows = sorted((x for f in sorted(glob.glob("scan/scan_D20.25_p*.jsonl")) for x in rd(f)), key=lambda x: (x["lam"], x["sec"]))
wm = {round(x["lam"], 3): x for x in rd("in/ref_win2_scan_k87_D20.25.jsonl")}
km = {round(x["lam"], 3): x for x in rd("in/ref_dh610_kc79_scan_D20.25.jsonl")}
sg = lambda s: "+" if s > 0 else "-"
print("| lambda | hybrid sign (mine, win2, my k_c 79) | noise signs (robust) | float64 sign (mine, win2) | ln of abs det (mine, win2) | mine minus win2 | ln (my k_c 79) | seconds (mine) |")
print("|---|---|---|---|---|---|---|---|")
for x in rows:
    k = round(x["lam"], 3); v = wm.get(k); u = km.get(k)
    print(f"| {k:.2f} | {sg(x['sign'])}, {sg(v['sign']) if v else 'n/a'}, {sg(u['sign']) if u else 'n/a'} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])}, {sg(v['f64_sign']) if v else 'n/a'} | "
          f"{x['ln']:.6f}, {v['ln']:.6f} | {x['ln'] - v['ln']:+.6f} | {u['ln']:.6f} | {x['sec']} |" if v and u else f"| {k:.2f} | {sg(x['sign'])} | | | {x['ln']:.6f} | | | {x['sec']} |")
t = [x["sec"] for x in rows]
print()
print(f"scan points: {len(rows)} evaluations, seconds per point min {min(t)}, median {statistics.median(t):.0f}, max {max(t)}, sum {sum(t)}; outside 1000 to 1900 s: {sum(1 for q in t if not 1000 <= q <= 1900)}")
d = [x["ln"] - wm[round(x["lam"], 3)]["ln"] for x in rows if round(x["lam"], 3) in wm]
print(f"mine minus win2's ln|det| over the {len(d)} evaluations: min {min(d):+.6f}, max {max(d):+.6f}")
