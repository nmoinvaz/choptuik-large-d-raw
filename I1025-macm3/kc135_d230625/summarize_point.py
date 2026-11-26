#!/usr/bin/env python3
"""summarize_point.py SCANDIR SECDIR: the numbers of one point (lambda printed to 3 decimals: the k_c 135 scan steps by 0.005; each repeated lambda is listed once) from the files: the scan (SCANDIR/scan/scan_D*_1025.jsonl, SCANDIR/read_lower.txt) and its secant refinement (SECDIR/secant.jsonl,
SECDIR/secant.log, SECDIR/samples.csv). The root is read by position: the final bracket and the det-linear root inside it; the scan's estimator range is a spread over interpolation choices, not an enclosure.
usage: summarize_point.py SCANDIR SECDIR [--mutate=range]   (the mutation moves the range by +0.01: the 'inside' line must then read False)"""
import csv, glob, json, os, re, sys
args = [a for a in sys.argv[1:] if not a.startswith("--")]
S, E = args[0], args[1]
scan = [json.loads(l) for f in glob.glob(S + "/scan/scan_D*_1025.jsonl") for l in open(f) if l.strip()]
rd = open(S + "/read_lower.txt").read()
ch = re.findall(r"robust change \((-?[\d.]+), (-?[\d.]+)\), ([-+]) to ([-+]), det-linear (-?[\d.]+), range \[(-?[\d.]+), (-?[\d.]+)\]", rd)
n = int(re.search(r"robust changes: (\d+)", rd).group(1))
print("scan: %d evaluations, %d noise-robust; robust changes %d: %s" % (len(scan), sum(r["noise_robust"] for r in scan), n,
      "; ".join("(%s, %s) %s to %s det-linear %s range [%s, %s]" % c for c in ch) or "none"))
print("signs by lambda: " + " ".join("%.3f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in sorted(scan, key=lambda r: r["lam"])))
print("float64 sign equals the hybrid sign at %d of %d" % (sum(r["f64_sign"] == r["sign"] for r in scan), len(scan)))
rep = {}
for r in scan: rep.setdefault(round(r["lam"], 6), []).append(r)
for lam, rs in sorted(rep.items()):
    if len(rs) > 1: print("repeat of %.3f bit-identical (ln, f64_ln, sign): %s" % (lam, all(x["ln"] == rs[0]["ln"] and x["f64_ln"] == rs[0]["f64_ln"] and x["sign"] == rs[0]["sign"] for x in rs)))
print("ln|det| by lambda: " + " ".join("%.3f:%.3f" % (r["lam"], r["ln"]) for r in sorted(scan, key=lambda r: r["lam"]) if r is rep[round(r["lam"], 6)][0]))
if len(ch) != 1:
    print("secant: not summarized (the scan reads %d robust changes, one wanted)" % len(ch)); sys.exit(0)
a, b, o, nn, dl, rlo, rhi = ch[0]; dl, rlo, rhi = float(dl), float(rlo), float(rhi)
if "--mutate=range" in sys.argv: rlo += 0.01; rhi += 0.01
recs = [json.loads(l) for l in open(E + "/secant.jsonl") if l.strip()]
ev = [r for r in recs if r.get("kind") == "eval"]; root = [r for r in recs if r.get("kind") == "root"]
assert len(root) == 1, "root records: %d" % len(root)
root = root[0]; lin = root["lam_lin"]; br = root["bracket"]
print("secant: status %s (%s), tol %g, evaluations %d (the two ends included), run wall %d s" % (root["status"], root["why"] or "-", root["tol"], root["n_eval"], root["sec"]))
print("secant root bracket [%.8f, %.8f], width %.3e, signs %s, robust %s; det-linear root %.8f; Brent's last point %s" % (br[0], br[1], root["width"], root["signs"], root["robust"], lin, "%.8f" % root["lam_brent"] if root["lam_brent"] is not None else None))
print("scan reading: bracket (%s, %s), det-linear %.6f, estimator range [%.6f, %.6f]" % (a, b, dl, rlo, rhi))
print("secant root inside the scan's estimator range: %s; whole final bracket inside: %s; root below the scan's det-linear: %s" % (rlo <= lin <= rhi, rlo <= br[0] and br[1] <= rhi, lin < dl))
bylam = {round(r["lam"], 6): r for r in scan}
for r in ev:
    s = bylam.get(round(r["lam"], 6))
    if s: print("end lambda %.3f: secant ln %.6f sign %+d, scan ln %.6f sign %+d, |d ln| %.3e" % (r["lam"], r["ln"], r["sign"], s["ln"], s["sign"], abs(r["ln"] - s["ln"])))
print("evals: " + "; ".join("%.8f %+d ln %.6f dln %.2e robust %s %d s" % (r["lam"], r["sign"], r["ln"], r["dln"], r["robust"], r["sec"]) for r in ev))
print("dln largest %.3e, mean seconds per evaluation %.0f" % (max(r["dln"] for r in ev), sum(r["sec"] for r in ev) / len(ev)))
if os.path.exists(E + "/samples.csv"):
    av, rss = [], 0
    for r in csv.DictReader(open(E + "/samples.csv")):
        if r["rss_kB"]: av.append(float(r["avail_GiB"])); rss = max(rss, int(r["rss_kB"]))
    print("secant memory: %d samples, lowest available %.1f GiB, peak RSS %.2f GiB" % (len(av), min(av) if av else -1, rss / 2**20))
