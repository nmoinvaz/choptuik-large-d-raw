#!/usr/bin/env python3
"""scan_vs_b_x.py [--mutate=lam] > scan_vs_b_x_output.txt : the scan of kc143_d23125x against the scan of kc143_d23125 (the k_c 135-based state) at the lambda they share (-0.030 twice, -0.025, -0.020):
hybrid sign, float64 sign, ln|det| and the det-linear estimates of the one robust change, read from kc87_leg_lambda/23.125_kc143{x,}/ (scan jsonl, read_lower.txt).
Arithmetic only, not a result. --mutate=lam moves the lambda of the x records by 0.001 so that no lambda is shared (must exit 1)."""
import json, re, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/"
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()]
B = rd(R + "23.125_kc143/scan/scan_D23.125_1025.jsonl"); X = rd(R + "23.125_kc143x/scan/scan_D23.125_1025.jsonl")
if "--mutate=lam" in sys.argv:
    for r in X: r["lam"] = round(r["lam"] + 0.001, 6)
bl = {}
for r in B: bl.setdefault(r["lam"], r)
pairs = [(x, bl[x["lam"]]) for x in X if x["lam"] in bl]
if not pairs: print("no shared lambda"); sys.exit(1)
est = lambda p: float(re.search(r"det-linear (\S+),", open(p).read()).group(1))
eB, eX = est(R + "23.125_kc143/read_lower.txt"), est(R + "23.125_kc143x/read_lower.txt")
print("shared lambda (the repeat of -0.030 included): hybrid sign x / B, float64 sign x / B, ln|det| x, B, x minus B")
for x, b in pairs:
    print("  %+.3f  hybrid %+d / %+d  float64 %+d / %+d  ln %.4f, %.4f, %+.4f" % (x["lam"], x["sign"], b["sign"], x["f64_sign"], b["f64_sign"], x["ln"], b["ln"], x["ln"] - b["ln"]))
d = [x["ln"] - b["ln"] for x, b in pairs]
print("ln|det| x minus B over the shared lambda: min %+.4f, max %+.4f, spread %.4f" % (min(d), max(d), max(d) - min(d)))
print("det-linear estimate of the one robust change: x %+.6f (- to +), B %+.6f (+ to -), x minus B %+.6f; B's secant root -0.02449537, x estimate minus it %+.6f" % (eX, eB, eX - eB, eX + 0.02449537))
print("hybrid sign at the shared lambda: same at %d of %d, opposite at %d; float64 sign: same at %d, opposite at %d" % (
    sum(x["sign"] == b["sign"] for x, b in pairs), len(pairs), sum(x["sign"] != b["sign"] for x, b in pairs), sum(x["f64_sign"] == b["f64_sign"] for x, b in pairs), sum(x["f64_sign"] != b["f64_sign"] for x, b in pairs)))
