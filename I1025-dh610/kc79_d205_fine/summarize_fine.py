#!/usr/bin/env python3
"""#1025 kc79_d205_fine (dh610) summarize_fine.py [--mutate]: the scan's rows beside dh170's and this machine's k_c 87 ones, from scan/, in/. No number is typed by hand.
The two-point det-linear root (lam1 + h / (1 + exp(ln2 - ln1))) of this scan's rows at 1.06 and 1.09 is the coarse estimate; its control: the same formula on dh170's rows must give his reader's 1.087574 within 1e-5,
else exit 1; --mutate flips the sign of the exponent, which must make the control fail (exit 1). usage (from this folder): python3 -I summarize_fine.py > summary_fine.txt"""
import json, math, re, statistics, sys
rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
mut = "--mutate" in sys.argv
rows = sorted(rd("scan/scan_D20.5_all.jsonl"), key=lambda x: x["lam"])
dm = {round(x["lam"], 3): x for x in rd("in/ref_dh170_k79_scan_D20.5.jsonl")}
km = {round(x["lam"], 3): x for x in rd("in/ref_dh610_kc87_scan_D20.5.jsonl")}
sg = lambda v: "+" if v > 0 else "-"
print("| lambda | hybrid sign (this build k_c 79, dh170 k_c 79, this build k_c 87) | noise signs (robust) | float64 sign | ln of abs det (this build k_c 79, dh170 k_c 79) | seconds |")
print("|---|---|---|---|---|---|")
for x in rows:
    k = round(x["lam"], 3); d = dm.get(k); u = km.get(k)
    print(f"| {k:.3f} | {sg(x['sign'])}, {sg(d['sign']) if d else 'n/a'}, {sg(u['sign']) if u else 'n/a'} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])} | {x['ln']!r}, {d['ln']!r} | {x['sec']} |" if d else
          f"| {k:.3f} | {sg(x['sign'])}, n/a, {sg(u['sign']) if u else 'n/a'} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])} | {x['ln']!r}, n/a | {x['sec']} |")
t = [x["sec"] for x in rows]
print()
print(f"scan points: {len(rows)} evaluations, seconds per point min {min(t)}, median {statistics.median(t):.0f}, max {max(t)}, sum {sum(t)}; outside 800 to 1700 s: {[(round(x['lam'], 3), x['sec']) for x in rows if not 800 <= x['sec'] <= 1700]}")


def root(a, b):
    sgn = -1 if mut else 1
    return a["lam"] + (b["lam"] - a["lam"]) / (1 + math.exp(sgn * (b["ln"] - a["ln"])))


at = lambda R, x: [q for q in R if abs(q["lam"] - x) < 1e-9][0]
ref = float(re.search(r"det-linear (\d\.\d+)", open("in/dh170_k79_read_lower.txt").read()).group(1))
ctl = root(at(list(dm.values()), 1.06), at(list(dm.values()), 1.09))
mine = root(at(rows, 1.06), at(rows, 1.09))
fine = float(re.search(r"det-linear (\d\.\d+)", open("read_lower.txt").read()).group(1))
k87 = float(re.search(r"det-linear (\d\.\d+)", open("in/ref_dh610_kc87_read_lower_D20.5.txt").read()).group(1))
k87coarse = root(at(list(km.values()), 1.06), at(list(km.values()), 1.09))
print()
print(f"control: the two-point root of dh170's rows at 1.06 and 1.09 is {ctl:.6f}; his reader's det-linear is {ref:.6f}; difference {ctl - ref:+.2e} (bar 1e-5): {'ok' if abs(ctl - ref) <= 1e-5 else 'CONTROL FAILED'}")
print(f"two-point root of this build's k_c 79 rows at 1.06 and 1.09: {mine:.6f} (minus dh170's reader {mine - ref:+.2e})")
print(f"this scan's reader (0.005 grid, k_c 79): det-linear {fine:.6f}; this machine's k_c 87 (0.005 grid, ../kc87_d205): {k87:.6f}; k_c 79 minus k_c 87 {fine - k87:+.6f}")
print(f"coarse (0.03 grid) minus fine, k_c 79: {mine - fine:+.6f}; k_c 87: {k87coarse - k87:+.6f} (the k_c 87 rows' two-point value {k87coarse:.6f})")
sys.exit(0 if abs(ctl - ref) <= 1e-5 else 1)
