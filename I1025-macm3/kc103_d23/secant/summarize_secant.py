#!/usr/bin/env python3
"""summarize_secant.py: the numbers of the k_c 103 D 23.0 secant refinement from the files (secant.jsonl, secant.log, samples.csv, the scan's jsonl and read_lower.txt).
t5's register (hc 25 Nov ~22:55 UTC): the root lies inside the scan's estimator range [0.023982, 0.028275] (a spread over interpolation choices, not an enclosure).
usage: summarize_secant.py [DIR] [--mutate=range]   (the mutation moves the range by +0.01: the 'inside' lines must then read False)"""
import csv, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = next((a for a in sys.argv[1:] if not a.startswith("--")), HERE)
SCAN = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/23.0_kc103/")
rd = open(SCAN + "read_lower.txt").read()
m = re.search(r"robust change \((-?[\d.]+), (-?[\d.]+)\), ([-+]) to ([-+]), det-linear (-?[\d.]+), range \[(-?[\d.]+), (-?[\d.]+)\]", rd)
RLO, RHI = float(m.group(6)), float(m.group(7)); DL = float(m.group(5))
if "--mutate=range" in sys.argv:
    RLO += 0.01; RHI += 0.01
recs = [json.loads(l) for l in open(D + "/secant.jsonl") if l.strip()]
ev = [r for r in recs if r.get("kind") == "eval"]; root = [r for r in recs if r.get("kind") == "root"]
assert len(root) == 1, "root records: %d" % len(root)
root = root[0]
scan = {round(r["lam"], 4): r for r in (json.loads(l) for l in open(SCAN + "scan/scan_D23.0_1025.jsonl"))}
print("status %s (%s), tol %g, evaluations %d (the two ends included), run wall %d s" % (root["status"], root["why"] or "-", root["tol"], root["n_eval"], root["sec"]))
print("root bracket [%.8f, %.8f], width %.3e, signs %s, robust %s" % (root["bracket"][0], root["bracket"][1], root["width"], root["signs"], root["robust"]))
lin = root["lam_lin"]; br = root["bracket"]
print("root (det-linear inside the final bracket) %.8f; Brent's last point %s" % (lin, "%.8f" % root["lam_brent"] if root["lam_brent"] is not None else None))
print("scan reading: det-linear %.6f, estimator range [%.6f, %.6f]" % (DL, RLO, RHI))
print("root inside the estimator range [%.6f, %.6f] (bracket and det-linear root): %s; whole final bracket inside: %s; below the scan's det-linear %.6f: %s" % (
    RLO, RHI, RLO <= lin <= RHI and RLO <= br[0] and br[1] <= RHI, br[0] >= RLO and br[1] <= RHI, DL, lin < DL))
print("evals: " + "; ".join("%.8f %+d ln %.6f dln %.2e robust %s %d s %s" % (r["lam"], r["sign"], r["ln"], r["dln"], r["robust"], r["sec"], r["sec_parts"]) for r in ev))
for lam in (0.02, 0.03):
    r = [x for x in ev if abs(x["lam"] - lam) < 1e-12]
    if r:
        s = scan[round(lam, 4)]
        print("ends: lambda %.2f: secant ln %.6f sign %+d, scan ln %.6f sign %+d, |d ln| %.3e (the float64 M by ell_fastm against the complex step; SPEED_ELL1.md saw 2.7e-5 and 1.5e-3 at k_c 103)" % (lam, r[0]["ln"], r[0]["sign"], s["ln"], s["sign"], abs(r[0]["ln"] - s["ln"])))
        print("ends: lambda %.2f float64 sign %+d (scan %+d)" % (lam, r[0]["f64_sign"], s["f64_sign"]))
print("dln largest %.3e, per evaluation seconds %s, mean %.0f s" % (max(r["dln"] for r in ev), [r["sec"] for r in ev], sum(r["sec"] for r in ev) / len(ev)))
av, rss = [], 0
if os.path.exists(D + "/samples.csv"):
    for r in csv.DictReader(open(D + "/samples.csv")):
        if r["rss_kB"]: av.append(float(r["avail_GiB"])); rss = max(rss, int(r["rss_kB"]))
    print("memory: %d samples, lowest available %.1f GiB, peak RSS %.2f GiB, alert.log absent" % (len(av), min(av) if av else -1, rss / 2**20))
