#!/usr/bin/env python3
"""#1025 kc87_d205 (dh610) summarize_kc87d205.py [--mutate]: the regrid and the scan beside dh170's k_c 79 D 20.5 record and scan, from regrid/, scan/, in/. No number is typed by hand.
Also the two-point det-linear root of this scan's rows at 1.06 and 1.09 (dh170's 0.03 grid; a post-hoc like-for-like estimate, written after the reading), with its control: the same formula on dh170's rows
at 1.06 and 1.09 must give his reader's 1.087574 within 1e-5, else exit 1; --mutate flips the sign of the exponent, which must make the control fail (exit 1).
usage (from this folder): python3 -I summarize_kc87d205.py > summary_kc87d205.txt"""
import json, glob, math, re, statistics, sys
rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
mut = "--mutate" in sys.argv
r, s = rd("regrid/l1kc87dh610d205.jsonl")[-1], rd("in/l1kc79dh170d205.jsonl")[-1]
print("| record | k_c 87, this machine (regrid) | k_c 79 source, dh170's machine | k_c 87 minus k_c 79 |")
print("|---|---|---|---|")
for k in ("F_start", "F", "steps", "constraint", "Delta", "seconds"):
    a, b = r[k], s[k]
    print(f"| {k} | {a!r} | {b!r} | {'' if k == 'seconds' else format(a - b, '+.3e')} |")
print(f"| steps ratio | {r['steps'] / s['steps']:.4f} | | |")
print()
rows = sorted((x for f in sorted(glob.glob("scan/scan_D20.5_p*.jsonl")) for x in rd(f)), key=lambda x: (x["lam"], x["sec"]))
hm = {round(x["lam"], 3): x for x in rd("in/ref_dh170_k79_scan_D20.5.jsonl")}
sg = lambda v: "+" if v > 0 else "-"
print("| lambda | hybrid sign (k_c 87 mine, k_c 79 dh170) | noise signs (robust) | float64 sign | ln of abs det (k_c 87 mine, k_c 79 dh170) | seconds |")
print("|---|---|---|---|---|---|")
for x in rows:
    k = round(x["lam"], 3); v = hm.get(k)
    print(f"| {k:.3f} | {sg(x['sign'])}, {sg(v['sign']) if v else 'n/a'} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])} | {x['ln']:.6f}, {v['ln']:.6f} | {x['sec']} |" if v else
          f"| {k:.3f} | {sg(x['sign'])}, n/a | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])} | {x['ln']:.6f}, n/a | {x['sec']} |")
t = [x["sec"] for x in rows]
print()
print(f"scan points: {len(rows)} evaluations, seconds per point min {min(t)}, median {statistics.median(t):.0f}, max {max(t)}, sum {sum(t)}; outside 1300 to 2100 s: {[(round(x['lam'], 3), x['sec']) for x in rows if not 1300 <= x['sec'] <= 2100]}")


def root(a, b):
    sgn = -1 if mut else 1
    return a["lam"] + (b["lam"] - a["lam"]) / (1 + math.exp(sgn * (b["ln"] - a["ln"])))


at = lambda R, x: [q for q in R if abs(q["lam"] - x) < 1e-9][0]
ref = float(re.search(r"det-linear (\d\.\d+)", open("in/dh170_k79_read_lower.txt").read()).group(1))
ctl = root(at(list(hm.values()), 1.06), at(list(hm.values()), 1.09))
mine = root(at(rows, 1.06), at(rows, 1.09))
print()
print(f"control: the two-point root of dh170's rows at 1.06 and 1.09 is {ctl:.6f}; his reader's det-linear is {ref:.6f}; difference {ctl - ref:+.2e} (bar 1e-5): {'ok' if abs(ctl - ref) <= 1e-5 else 'CONTROL FAILED'}")
print(f"this scan's rows at 1.06 and 1.09, same formula (dh170's 0.03 grid): {mine:.6f}; minus dh170's reader {mine - ref:+.6f}")
ch = re.search(r"det-linear (\d\.\d+)", open("read_lower.txt").read()).group(1)
print(f"this scan's reader (0.005 grid): det-linear {ch}; minus the two-point value on the 0.03 grid {float(ch) - mine:+.6f}; minus dh170's reader {float(ch) - ref:+.6f}")
sys.exit(0 if abs(ctl - ref) <= 1e-5 else 1)
