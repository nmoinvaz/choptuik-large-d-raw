#!/usr/bin/env python3
"""score_scan.py: numbers of the k_c 103 D 23.0 scan from the files (scan jsonl, samples csv, steps.txt, read_lower.txt), for the README scoring.
usage: python3 score_scan.py [--mutate=repeat]   (the mutation perturbs the repeat of 0.00: the bit-identity check must report False)"""
import csv, json, re, sys
from datetime import datetime as T
S = "../kc87_leg_lambda/23.0_kc103/"
rows = [json.loads(l) for l in open(S + "scan/scan_D23.0_1025.jsonl")]
if "--mutate=repeat" in sys.argv:
    z = [r for r in rows if r["lam"] == 0.0]; z[1]["ln"] += 1e-12
print("evaluations %d, noise-robust %d" % (len(rows), sum(r["noise_robust"] for r in rows)))
print("float64 sign equals the hybrid sign at %d of %d" % (sum(r["f64_sign"] == r["sign"] for r in rows), len(rows)))
z = [r for r in rows if r["lam"] == 0.0]
print("repeat of 0.00 bit-identical (ln, f64_ln, sign): %s" % (len(z) == 2 and z[0]["ln"] == z[1]["ln"] and z[0]["f64_ln"] == z[1]["f64_ln"] and z[0]["sign"] == z[1]["sign"]))
print("signs by lambda: " + " ".join("%.2f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in sorted(rows, key=lambda r: r["lam"])))
print("ln|det| by lambda: " + " ".join("%.2f:%.3f" % (r["lam"], r["ln"]) for r in sorted(rows, key=lambda r: r["lam"]) if r["lam"] >= 0.0))
av, rss = [], {}
for r in csv.DictReader(open(S + "scan/scan_samples.csv")):
    av.append(float(r["avail_GiB"])); rss[r["pid"]] = max(rss.get(r["pid"], 0), int(r["rss_kB"]))
print("memory: %d samples, lowest available %.1f GiB (alert below 2 GiB, alert.log exists: %s), peak RSS per process GiB %s" % (len(av), min(av), __import__("os").path.exists(S + "scan/alert.log"), {k: round(v / 2**20, 2) for k, v in rss.items()}))
st = open(S + "steps.txt").read()
t0 = re.search(r"(\S+ \S+) UTC scan starts", st).group(1); t1 = re.search(r"(\S+ \S+) UTC scan done", st).group(1)
f = "%Y-%m-%d %H:%M:%S"; w = (T.strptime(t1, f) - T.strptime(t0, f)).total_seconds()
print("scan wall %d s = %.1f min (%s to %s UTC)" % (w, w / 60, t0, t1))
rd = open(S + "read_lower.txt").read()
m = re.search(r"robust change \((-?[\d.]+), (-?[\d.]+)\), ([-+]) to ([-+]), det-linear (-?[\d.]+), range \[(-?[\d.]+), (-?[\d.]+)\]", rd)
a, b, o, n, d, lo, hi = m.groups(); d, lo, hi = float(d), float(lo), float(hi)
print("root k_c 103: bracket (%s, %s), %s to %s, det-linear %.6f, estimator range [%.6f, %.6f] (a spread, not an enclosure)" % (a, b, o, n, d, lo, hi))
r87, r95 = -0.021546, 0.015921
print("k_c 87 %.6f, k_c 95 %.6f, k_c 103 %.6f: steps 87->95 %+.6f, 95->103 %+.6f, ratio %.4f" % (r87, r95, d, r95 - r87, d - r95, (d - r95) / (r95 - r87)))
print("arithmetic only, not a result: room below +0.03 is %.6f, i.e. %.3f of the last step; a geometric tail of the observed ratio would end at %.4f" % (0.03 - d, (0.03 - d) / (d - r95), d + (d - r95) * ((d - r95) / (r95 - r87)) / (1 - (d - r95) / (r95 - r87))))
print("predictions: root in (0.016,0.060): %s; in (-0.030,0.030): %s; |root-0.030|<0.015: %s; step positive: %s; step below +0.0374: %s" % (0.016 < d < 0.060, -0.03 < d < 0.03, abs(d - 0.03) < 0.015, d > r95, d - r95 < 0.0374))
