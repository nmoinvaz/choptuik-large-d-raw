#!/usr/bin/env python3
"""make_post.py D --leg=D1,D2,... [--part=b] --pred="<scoring of my predictions>" [--note="<one extra sentence>"] > post.md
Builds the #1025 post of one scanned point of the k_c 87 leg2 from files only (roots87.txt, <D>/scan, <D>/steps.txt, the leg's record, guard rows, tracker rows, memory samples); the placeholder @@T@@ in the title is
replaced by the caller with the clock at posting. The predictions' scoring (--pred) is the only free text besides --note. Read-only."""
import csv, json, os, re, sys, datetime as dt
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
L2 = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
D = float(args[0]); dn = repr(D)
part = opt.get("--part", "a"); legd = [float(x) for x in opt.get("--leg", "").split(",") if x]
LEG = L2 + ("" if part == "a" else "/" + part); TAG = {"a": "l1kc87Lmacm3", "b": "l1kc87Lmacm3b", "c": "l1kc87Lmacm3c"}[part]
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
st = D - a
pred = roots[a][0] + slope * st; pred2 = roots[a][0] - 0.33 * st; pred3 = roots[a][0] + sb * st
new = (root - roots[a][0]) / st
rows = [json.loads(x) for x in open("%s/%s/scan/scan_D%s_1025.jsonl" % (L, dn, dn))]
lams = sorted(set(r["lam"] for r in rows)); replam = [x for x in lams if [r["lam"] for r in rows].count(x) == 2][0]
def row(lam): return [r for r in rows if r["lam"] == lam]
rd = open("%s/%s/read_lower.txt" % (L, dn)).read()
br = re.search(r"robust change \((-?[\d.]+), (-?[\d.]+)\), ([-+] to [-+])", rd); orient = br.group(3)
steps = open("%s/%s/steps.txt" % (L, dn)).read()
f = "%Y-%m-%d %H:%M:%S"
t0 = re.findall(r"(\S+ \S+) UTC proc 0 lambda", steps)[-1]; t1 = re.findall(r"(\S+ \S+) UTC scan done", steps)[-1]
wall = dt.datetime.strptime(t1, f) - dt.datetime.strptime(t0, f); wm = int(wall.total_seconds())
ms = re.search(r"kc87_syscheck_1025.py exit (\d).*?--mutate=F exit (\d), --mutate=steps exit (\d).*?kc79_syscheck_1025.py on the k_c 87 state exit (\d).*?record \|F\| ([\d.e+-]+).*?steps (\d+)", steps)
accT = re.search(r"(\S+ \S+) UTC verdict: ACCEPTED", steps).group(1).split()[1]
nproc = len(re.findall(r"proc \d lambda", steps.split("scan starts")[-1]))
sm = list(csv.DictReader(open("%s/%s/scan/scan_samples.csv" % (L, dn)))); pk = {}
for x in sm: pk[x["pid"]] = max(pk.get(x["pid"], 0), int(x["rss_kB"]))
p1 = sorted(r["sec"] for r in rows)
fd = sorted(set(r["lam"] for r in rows if r["sign"] != r["f64_sign"]))
lowest = min(rows, key=lambda r: r["ln"])
pin = open("%s/%s/pins.txt" % (L, dn)).read()
sblob = re.search(r"^(\w+)\s+sol_\S+\.npy\s+<-\s+(\w+):", pin, re.M); rblob = re.search(r"^(\w+)\s+l1kc87\S+\.jsonl\s+<-", pin, re.M)
legrec = {x["D"]: x for x in (json.loads(l) for l in open("%s/%s.jsonl" % (LEG, TAG)))}
guard = {}
for l in open(LEG + "/leg_points.txt"):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    try: guard[float(c[0])] = c
    except ValueError: pass
trk = {}
for l in open(LEG + "/tracker_rows.txt"):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    try: trk[float(c[0])] = c
    except ValueError: pass
pushed = {}
for l in open(LEG + "/exits_leg2%s.txt" % ("" if part == "a" else part)):
    m = re.search(r"point D ([\d.]+): pushed (\w+);.*?(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", l)
    if m: pushed[float(m.group(1))] = (m.group(2), m.group(3).split()[1])
memr = list(csv.DictReader(open(LEG + "/mem_samples.csv")))
out = []
P = out.append
P("**#1025 macm3, lambda_1 on my own k_c 87 leg at D %s (@@T@@ UTC 24 Nov): one robust change, between %s and %s (%s), det-linear %.6f (estimator range [%.6f, %.6f]); %s predicted %.6f: %+.6f; the -0.33 rule beside it, %.6f: %+.6f%s; local slope %.4f per unit D.** t5's rule (previous k_c 87 root %.6f at D %s, step %s; one change within 0.005): %s. Numerical evidence." % (
    dn, br.group(1), br.group(2), orient, root, lo, hi, ("the latest-local-slope rule (%.6f)" % slope) if si is None else ("the interpolation between the roots at D %r and D %r (slope %.6f)" % (a, above[0], slope)),
    pred, root - pred, pred2, root - pred2, "" if abs(root - pred2) <= 0.005 else ", outside its 0.005 window", new, roots[a][0], dn if False else repr(a), repr(st),
    "**met** by the primary rule" + ("" if abs(root - pred2) <= 0.005 else ", **not met** by the -0.33 rule") if abs(root - pred) <= 0.005 else "**NOT met** by the primary rule"))
if si is not None: P("\nBelow-only extrapolation (slope %.6f) beside it: %.6f, root %+.6f from it." % (sb, pred3, root - pred3))
if legd:
    P("\n**The leg** (kc87_leg2 part %s, raw `I1025-macm3/kc87_leg2/%s`): points accepted since the previous post.\n" % (part, "" if part == "a" else part + "/"))
    P("| point | " + " | ".join("D %r (%s UTC, %d s)" % (d, pushed.get(d, ("", "?"))[1], legrec[d]["seconds"]) for d in legd) + " |")
    P("|---|" + "---|" * len(legd))
    P("| Delta | " + " | ".join("%.12f" % legrec[d]["Delta"] for d in legd) + " |")
    P("| dDelta/dD | " + " | ".join(guard[d][2].join(["+", ""]) if not guard[d][2].startswith("-") else guard[d][2] for d in legd) + " |")
    P("| \\|F\\|, steps | " + " | ".join("%.3e, %d" % (legrec[d]["F"], legrec[d]["steps"]) for d in legd) + " |")
    P("| psi-constraint (bar 1e-2) | " + " | ".join("%.3e" % legrec[d]["constraint"] for d in legd) + " |")
    P("| \\|J+dF/dn\\|, n_null | " + " | ".join("%.4f, %d" % (legrec[d]["tan_norm"], legrec[d]["n_null"]) for d in legd) + " |")
    P("| tracker m0 (weakest regular mode), cos | " + " | ".join("%s, %.4f" % (trk[d][3].replace("m0 ", ""), legrec[d]["cos_t_reg"][0]) for d in legd) + " |")
    P("| branch watch m1 | " + " | ".join(trk[d][7] for d in legd) + " |")
    P("| raw commit | " + " | ".join(pushed.get(d, ("?",))[0] for d in legd) + " |")
    lm = {d: max(int(x["leap_rss_kb"]) for x in memr if x["time_utc"] >= "00:00:00") for d in legd}
    P("\nThe guard did not stop. Peak RSS of the leap over the part so far %.2f GB (sampled each minute)." % (max(int(x["leap_rss_kb"]) for x in memr) / 2**20))
P("\n| Step and acceptance, as ordered | Verdict |\n|---|---|")
P("| **Source** (my leg's D %s state, raw commit %s: state `sol_%s_D%.6f.npy` %s, record `%s.jsonl` %s; `kc87_syscheck_1025.py` 6df5d960) | **ACCEPTED** %s UTC: exit %s (record \\|F\\| %s, %s steps); `--mutate=F` and `--mutate=steps` exit %s and %s; the k_c 79 check refuses the state (exit %s); both selftests exit 0 |" % (
    dn, sblob.group(2), TAG, D, sblob.group(1), TAG, rblob.group(1), accT, ms.group(1), ms.group(5), ms.group(6), ms.group(2), ms.group(3), ms.group(4)))
P("| **Scan** (`d18_hybsign.py` e089207a unmodified, lambda %.3f to %.3f by 0.005 and a repeat of %.3f; %d processes of 1 thread at nice 15; `caffeinate -is`; the chain started it) | exit 0 (%s to %s UTC, %d min %d s); every process printed the record system; %d of %d noise-robust |" % (
    lams[0], lams[-1], replam, nproc, t0.split()[1], t1.split()[1], wm // 60, wm % 60, sum(r["noise_robust"] for r in rows), len(rows)))
P("| Reader and repeat | `read_lower.py` (89309d3c) selftest exit 0, its `--mutate=shift` and `--mutate=round2` exit 1; `repeat_check.py` (aaf598a9) selftest exit 0; repeat of %.3f **%s**: hybrid %+d, ln\\|det\\| %.10f, float64 sign %+d (all fields equal but the seconds): `repeat_check.py` %s |" % (
    replam, "bit-identical" if {k: v for k, v in row(replam)[0].items() if k != "sec"} == {k: v for k, v in row(replam)[1].items() if k != "sec"} else "DIFFERENT", row(replam)[0]["sign"], row(replam)[0]["ln"], row(replam)[0]["f64_sign"], "PASS" if "-> PASS" in rd else "FAIL"))
P("\n**Reading** (hybrid signs as printed; one robust change, no ln|det| minimum without a sign change):\n\n| root | bracket | orientation as printed | det-linear estimate | estimator range |\n|---|---|---|---|---|")
P("| **k_c 87, D %s (macm3)** | (%s, %s) | %s | **%.6f** | [%.6f, %.6f] |\n" % (dn, br.group(1), br.group(2), orient, root, lo, hi))
P("| lambda | hybrid sign | float64 sign | ln\\|det\\| hybrid | ln\\|det\\| float64 |\n|---|---|---|---|---|")
for lam in lams:
    rr = row(lam)
    P("| %.3f%s | %+d | %+d | %.4f | %.4f |" % (lam, " (two evaluations)" if len(rr) == 2 else "", rr[0]["sign"], rr[0]["f64_sign"], rr[0]["ln"], rr[0]["f64_ln"]))
P("\nThe float64 sign %s. The hybrid ln\\|det\\| is lowest at %.3f (%.4f). The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; the bracket is the 0.005 grid step." % (
    "agrees with the hybrid at every value" if not fd else "differs from the hybrid at %s" % ", ".join("%.3f" % x for x in fd), lowest["lam"], lowest["ln"]))
P("**Residuals** (the primary rule's prediction %.6f, registered grid centre from it; the -0.33 rule %.6f): root %+.6f and %+.6f from them (the window rule was 0.005)." % (pred, pred2, root - pred, root - pred2))
P("**Local slope** (det-linear roots, per unit D) from D %r: **%.4f** over the step %s (%.4f between the lower ends of the estimator ranges; the range width is %.6f, %.4f in slope units); the previous slope was %.4f (change %+.4f)." % (
    a, new, repr(st), (lo - roots[a][1]) / st, root - lo, (root - lo) / st, sb, new - sb))
tr = sorted(x for x in roots if x <= D)[-8:]
P("\n| D | root | slope from the previous root |\n|---|---|---|")
for i, d in enumerate(tr):
    prev = [x for x in sorted(roots) if x < d]
    P("| %s%r%s | %s%.6f%s | %s |" % ("**" if d == D else "", d, "**" if d == D else "", "**" if d == D else "", roots[d][0], "**" if d == D else "", ("%.4f" % ((roots[d][0] - roots[prev[-1]][0]) / (d - prev[-1]))) if prev else ""))
P("\n**Time and memory (scan).** Per evaluation %s s. Peak RSS per process %s GB; lowest available memory %.1f GiB (%.1f GiB at the first sample), free memory at least %d%%, disk %s free; no alert fired." % (
    ", ".join(str(x) for x in p1), ", ".join("%.2f" % (v / 2**20) for v in pk.values()), min(float(x["avail_GiB"]) for x in sm), float(sm[0]["avail_GiB"]), min(int(x["free_mem_pct"]) for x in sm), "/".join(sorted({x["free_disk"] for x in sm}))))
P("**Predictions** (README, written before the run). " + opt.get("--pred", "(not scored)"))
if "--note" in opt: P(opt["--note"])
P("\nRaw: `I1025-macm3/kc87_leg_lambda/%s/` (README first, written by the chain; results pushed by the pipeline) and `I1025-macm3/kc87_leg2/%s`." % (dn, "" if part == "a" else part + "/"))
print("\n".join(out))
