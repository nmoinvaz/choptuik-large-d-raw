#!/usr/bin/env python3
"""post_numbers.py D [PART]: prints every number of a #1025 post for the scanned point D of the k_c 87 leg2 (from files only): the scan rows, the repeat, the residuals against the registered rules
(the section of README.md for D is not parsed: the rules are recomputed from roots87.txt by chain_next.py's own logic), the local slope, time and memory of the scan, and the leg rows of the points of PART (a, b or c; default: the part that holds D)
that were accepted since the previous scanned point. Read-only."""
import csv, glob, json, os, re, sys, datetime as dt
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
L2 = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2")
D = float(sys.argv[1]); dn = repr(D)
roots = {}
for l in open(L + "/roots87.txt"):
    f = l.split()
    if len(f) >= 2 and not l.startswith("#"): roots[float(f[0])] = (float(f[1]), float(f[2]), float(f[3]))
root, lo, hi = roots[D]
below = sorted(x for x in roots if x < D); above = sorted(x for x in roots if x > D)
a, b = below[-1], below[-2]
sb = (roots[a][0] - roots[b][0]) / (a - b)
si = (roots[above[0]][0] - roots[a][0]) / (above[0] - a) if above else None
slope = sb if si is None else si
pred = roots[a][0] + slope * (D - a); pred2 = roots[a][0] - 0.33 * (D - a); pred3 = roots[a][0] + sb * (D - a)
print("== roots: D %r root %.6f range [%.6f, %.6f]; a=%r (%.6f), b=%r (%.6f)" % (D, root, lo, hi, a, roots[a][0], b, roots[b][0]))
print("rule: slope %.6f -> pred %.6f resid %+.6f%s; -0.33: pred %.6f resid %+.6f%s%s" % (slope, pred, root - pred, "" if abs(root - pred) <= 0.005 else " OUTSIDE 0.005", pred2, root - pred2,
      "" if abs(root - pred2) <= 0.005 else " OUTSIDE 0.005", ("; below-only slope %.6f pred %.6f resid %+.6f" % (sb, pred3, root - pred3)) if si is not None else ""))
new = (root - roots[a][0]) / (D - a); ph, pl = roots[a][2], roots[a][1]
print("new local slope %.4f (lower ends %.4f), range width %.6f = %.4f slope units; previous slope %.4f, change %+.4f" % (new, (lo - roots[a][1]) / (D - a), root - lo, (root - lo) / (D - a), sb, new - sb))
rows = [json.loads(x) for x in open("%s/%s/scan/scan_D%s_1025.jsonl" % (L, dn, dn))]
for r in rows: print("%.3f hyb %+d f64 %+d ln %.4f f64ln %.4f sec %d noise %s robust %s" % (r["lam"], r["sign"], r["f64_sign"], r["ln"], r["f64_ln"], r["sec"], r["noise"], r["noise_robust"]))
lowest = min(rows, key=lambda r: r["ln"])
print("hybrid ln|det| lowest at %.3f: %.4f; differs from float64 sign at %s" % (lowest["lam"], lowest["ln"], [r["lam"] for r in rows if r["sign"] != r["f64_sign"]]))
rep = [r for r in rows if r["lam"] == max(set(r2["lam"] for r2 in rows if [x["lam"] for x in rows].count(r2["lam"]) > 1), default=None)]
if len(rep) == 2: print("repeat lam %.3f identical but sec: %s (sec %s)" % (rep[0]["lam"], {k: v for k, v in rep[0].items() if k != "sec"} == {k: v for k, v in rep[1].items() if k != "sec"}, [x["sec"] for x in rep]))
sm = list(csv.DictReader(open("%s/%s/scan/scan_samples.csv" % (L, dn)))); pk = {}
for x in sm: pk[x["pid"]] = max(pk.get(x["pid"], 0), int(x["rss_kB"]))
print("scan RSS GB %s; avail min %.1f first %.1f; free%% min %d; disk %s; %s to %s" % ([round(v / 2**20, 2) for v in pk.values()], min(float(x["avail_GiB"]) for x in sm), float(sm[0]["avail_GiB"]), min(int(x["free_mem_pct"]) for x in sm), {x["free_disk"] for x in sm}, sm[0]["time_utc"], sm[-1]["time_utc"]))
st = open("%s/%s/steps.txt" % (L, dn)).read()
t0 = re.findall(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC proc 0 lambda", st); t1 = re.findall(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC scan done", st)
f = "%Y-%m-%d %H:%M:%S"
print("scan wall %s (%s to %s)" % (dt.datetime.strptime(t1[-1], f) - dt.datetime.strptime(t0[-1], f), t0[-1], t1[-1]))
print([l.strip()[:90] for l in re.findall(r"^.*(?:selftests|syscheck_1025.py exit).*$", st, re.M)][:0])
m = re.search(r"kc87_syscheck_1025.py exit (\d).*?controls --mutate=F exit (\d), --mutate=steps exit (\d).*?kc79_syscheck_1025.py on the k_c 87 state exit (\d).*?record \|F\| ([\d.e+-]+).*?steps (\d+)", st)
print("source check: exits %s (0 1 1 1 wanted), record |F| %s, steps %s" % (m.groups()[:4], m.group(5), m.group(6)) if m else "source check line not parsed")
print("hc root line sent: %s" % ("yes" if "ROOT D %s:" % dn in open(L + "/chain.log").read() else "NO"))
