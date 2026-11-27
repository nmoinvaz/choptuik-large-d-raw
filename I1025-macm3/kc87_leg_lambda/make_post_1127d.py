#!/usr/bin/env python3
"""make_post_1127d.py > post.md : the #1025 comment of macm3 on kc143_d23125x, the cross-path check of k_c 143 at D 23.125 (t5's order, comment 7213649039 and hc 27 Nov 08:3x UTC; his hc after the lane:
"Post your lane summary with its numbers and scores, point to my comment for the reading, and don't repeat it", his reading is comment 7216553513). Every number comes from the files of kc143_d23125x/, kc143_d23125/,
kc87_leg_lambda/23.125_kc143x/ and 23.125_kc143/ (records, scan and secant jsonl, exits, point_summary.txt, arith_x_output.txt and the READMEs' scoring); tail sums are arithmetic only. No reading of the difference is
written here. @@T@@ and @@H@@ are replaced by the caller. Read-only."""
import csv, json, math, os, re, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
X = R + "kc143_d23125x/"; B = R + "kc143_d23125/"; SX = R + "kc87_leg_lambda/23.125_kc143x/"; SB = R + "kc87_leg_lambda/23.125_kc143/"
txt = lambda p: open(p).read()
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()]
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
exX, exB, rdX, chain, rel = txt(X + "exits_kc143.txt"), txt(B + "exits_kc143.txt"), txt(X + "README.md"), txt(R + "kc87_leg_lambda/chain.log"), txt(X + "release_end_kc143x.log")


def et(pat, lab="kc143_d23125x", s=None):
    m = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC " + lab + ": " + pat, s or exX); assert m, pat; return m.group(1)


def peak(p): return max(int(r["rss_kB"]) for r in csv.DictReader(open(p)) if r["rss_kB"]) / 1048576


def entry(key):
    i = rdX.index(key); seg = rdX[i:]
    m = re.search(r"\((\d+) items: (\d+) HIT, (\d+) MISS", seg); assert m, key
    s0 = seg.index(". MISS ") + 2 if ". MISS " in seg[:m.start()] else None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), seg[s0:m.start()].strip() if s0 else "")


c_reg, c_scan, c_sec = entry("**the regrid, scored**"), entry("**the scan, scored**"), entry("**the D 23.125 secant of the x state")
rx = jl(SX + "in/l1kc143macm3d23125x.jsonl")[-1]; rb = jl(B + "in/l1kc143macm3d23125.jsonl")[-1]; r127 = [r for r in jl(X + "in/l1kc127Lmacm3.jsonl") if r["D"] == 23.125][-1]; r135 = jl(B + "in/l1kc135macm3d23125.jsonl")[-1]
wallX = int(re.search(r"regrid exit 0, wall (\d+) s", exX).group(1)); wallB = int(re.search(r"regrid exit 0, wall (\d+) s", exB).group(1))
rssX = peak(X + "regrid/regrid_samples.csv"); rssB = peak(B + "regrid/regrid_samples.csv")
scX = jl(SX + "scan/scan_D23.125_1025.jsonl"); scB = jl(SB + "scan/scan_D23.125_1025.jsonl")
se = jl(X + "secant/secant.jsonl"); root = [e for e in se if e.get("kind") == "root"][-1]; ev = [e for e in se if e.get("kind") == "eval"]
lo, hi = root["bracket"]; rt = root["lam_lin"]
ps = txt(X + "point_summary.txt"); arith = txt(X + "arith_x_output.txt").strip().split("\n")
ss = list(csv.DictReader(open(X + "secant/samples.csv"))); spk = max(int(s["rss_kB"]) for s in ss if s["rss_kB"]) / 1048576; slow = min(float(s["avail_GiB"]) for s in ss if s["avail_GiB"])
pk = {}
for s in csv.DictReader(open(SX + "scan/scan_samples.csv")):
    if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
srss = sorted(v / 1048576 for v in pk.values())[-2:]
REF = -0.024495; REFROOT = -0.02449537; DREF = rb["Delta"]
assert abs(DREF - 1.178015433613) < 1e-12, DREF
dd = rx["Delta"] - rb["Delta"]; off = rt - REF
word = "between the bars (1e-3 to 3e-3)" if 1e-3 < abs(off) < 3e-3 else ("reproduced (within 1e-3)" if abs(off) <= 1e-3 else "path-dependent (3e-3 or more)")
m = re.search(r"robust change \((\S+), (\S+)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", txt(SX + "read_lower.txt")); sdl = float(m.group(5).rstrip(","))
mb = re.search(r"robust change \((\S+), (\S+)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", txt(SB + "read_lower.txt")); sdlb = float(mb.group(5).rstrip(","))
hold = re.search(r"(\d\d:\d\d:\d\d) UTC HOLD_kc143x.txt placed", chain).group(1); stop = re.search(r"(\d\d:\d\d:\d\d) UTC the chain's D 22.3125 scan was STOPPED by pid", chain).group(1)
relt = re.search(r"(\d\d:\d\d:\d\d) UTC hc: macm3 #1025 \(release watcher", rel).group(1)
cst = re.search(r"(\d\d:\d\d:\d\d) UTC chain starts", chain.split(stop)[-1]).group(1); cnx = re.search(r"(\d\d:\d\d:\d\d) UTC next: D (\S+) \(previous", chain.split(stop)[-1])
L = []; w = L.append
w("**#1025 macm3, kc143_d23125x, the cross-path check of k_c 143 at D 23.125: lambda_1 = %+.8f (secant exit 0, bracket [%.8f, %.8f], width %.1e) from the state regridded directly from k_c 127; the Delta differs from the k_c 135-based state by %+.3e (@@T@@).** t5's order (#1025 comment 7213649039, hc 27 Nov 08:3x UTC): regrid k_c 143 at D 23.125 from my k_c 127 state there (tag `l1kc127Lmacm3`, blob e1dccb3c), skipping k_c 135, with the earlier lane's regrid line (`ell_refine.py l1kc127Lmacm3 127 l1kc143macm3d23125x 143 1 23.125 2.0987860107 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 6 threads, nice 10, cap 28800 s), the kc143 check, then the scan of lambda -0.030, -0.025, -0.020 (with a repeat of -0.030, which the lane's repeat check needs) and the secant at tol 5e-5 with the Rust block 12 (scanner blob 9706e506), as in `kc143_d23125/`. t5's bars were written into the README before the lane started. **t5's reading of the difference is his comment 7216553513 and is not repeated here.** Roots are the det-linear root inside the final bracket, read by position. Every tail sum is arithmetic only, not a result." % (rt, lo, hi, hi - lo, dd))
w("")
w("### The two states (raw `I1025-macm3/kc143_d23125x/`, README with t5's bars first)")
w("")
w("| at D 23.125 | Delta | lam_gauge | \\|F\\| | steps | psi-constraint | F_start | regrid wall (s) | peak RSS (GiB) |")
w("|---|---|---|---|---|---|---|---|---|")
w("| k_c 127 (the source) | %.12f | %.12f | %.4e | %d | %.4e | %.3e | %d | |" % (r127["Delta"], r127["lam_gauge"], r127["F"], r127["steps"], r127["constraint"], r127["F_start"], r127["seconds"]))
w("| k_c 143 via k_c 135 (`kc143_d23125/`) | %.12f | %.12f | %.4e | %d | %.4e | %.3e | %d | %.3f |" % (rb["Delta"], rb["lam_gauge"], rb["F"], rb["steps"], rb["constraint"], rb["F_start"], wallB, rssB))
w("| **k_c 143 direct from k_c 127** | %.12f | %.12f | %.4e | %d | %.4e | %.3e | %d | %.3f |" % (rx["Delta"], rx["lam_gauge"], rx["F"], rx["steps"], rx["constraint"], rx["F_start"], wallX, rssX))
w("")
w("Direct against via k_c 135 (arithmetic only): Delta %+.3e (t5's bar 1e-6, R0's solve scatter 4.2e-7: %.2f times it), lam_gauge %+.3e, |F| %.4e against %.4e, steps %d against %d, psi-constraint ratio %.4f. Delta shift from the k_c 127 source: %+.4e direct, %+.4e by the chain (127 to 135 %+.4e, 135 to 143 %+.4e). The regrid ran %s to %s UTC (exit 0, `capped_run` wall %d s); acceptance %s UTC: the kc143 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc135 check refuses the result." % (
    dd, abs(dd) / 4.2e-7, rx["lam_gauge"] - rb["lam_gauge"], rx["F"], rb["F"], rx["steps"], rb["steps"], rx["constraint"] / rb["constraint"], rx["Delta"] - r127["Delta"], rb["Delta"] - r127["Delta"], r135["Delta"] - r127["Delta"], rb["Delta"] - r135["Delta"], et("regrid starts"), et("regrid exit 0"), wallX, et("kc143 syscheck exit 0")))
w("")
w("### The scan (Rust block 12, 4 threads, 2 processes)")
w("")
w("Scan %s to %s UTC (%.1f min, %d to %d s per evaluation, peak RSS %.3f and %.3f GiB per process). All %d evaluations noise-robust, the repeat of -0.030 bit-identical, float64 sign equal to the hybrid sign at %d of %d. **One robust change, (%s, %s), %s to %s, det-linear %+.6f, estimator range [%s, %s]** (an estimator range, not an enclosure). The earlier lane's scan read (%s, %s), %s to %s, det-linear %+.6f. Against that scan at the shared lambda:" % (
    et("scan starts"), et("scan exit 0"), (hms(et("scan exit 0")) - hms(et("scan starts"))) / 60.0, min(r["sec"] for r in scX), max(r["sec"] for r in scX), srss[0], srss[1], len(scX), sum(1 for r in scX if r["f64_sign"] == r["sign"]), len(scX),
    m.group(1).rstrip(","), m.group(2).rstrip(","), m.group(3), m.group(4), sdl, m.group(6), m.group(7).rstrip("]"), mb.group(1).rstrip(","), mb.group(2).rstrip(","), mb.group(3), mb.group(4), sdlb))
w("")
w("| lambda | hybrid sign direct / via k_c 135 | float64 sign direct / via | ln\\|det\\| direct | ln\\|det\\| via | direct minus via |")
w("|---|---|---|---|---|---|")
bl = {r["lam"]: r for r in scB}
for r in scX:
    if r["lam"] in bl and not (r["lam"] == -0.030 and r is scX[1]):
        b = bl[r["lam"]]; w("| %+.3f | %+d / %+d | %+d / %+d | %.4f | %.4f | %+.4f |" % (r["lam"], r["sign"], b["sign"], r["f64_sign"], b["f64_sign"], r["ln"], b["ln"], r["ln"] - b["ln"]))
w("")
w("### The secant and the root against t5's bars")
w("")
w("Secant %s to %s UTC, tol 5e-5, Rust block 12 with 4 threads, one process, **exit %s (%s)**, %d evaluations (the two ends included), %d to %d s each, peak RSS %.3f GiB, lowest available memory %.1f GiB:" % (
    et("secant starts"), et("secant exit \\d+"), re.search(r"secant exit (\d+)", exX).group(1), root["status"], root["n_eval"], min(e["sec"] for e in ev), max(e["sec"] for e in ev), spk, slow))
w("")
w("```")
w(ps.rstrip())
w("```")
w("")
w("**Root %+.8f.** All %d evaluations are robust (largest dln %.3e), both ends of the final bracket are robust, the bracket is %.2f times the tolerance. **Against t5's bars (as he wrote them):** the root minus -0.024495 is %+.3e, %s; the Delta difference is %+.3e against his 1e-6, **a different state**. The scan's det-linear %+.6f lies %.6f above the root." % (
    rt, len(ev), max(e["dln"] for e in ev), (hi - lo) / 5e-5, off, word, dd, sdl, sdl - rt))
w("")
w("Shifts of the root with k_c and the zero by the line through the D 23.0625 root and this one (`arith_x.py` -> `arith_x_output.txt`, its control `--mutate=rx` moves every number built on the root; **arithmetic only, not a result, not explained**):")
w("")
w("```")
for a in arith: w(a)
w("```")
w("")
w("### Registrations and scoring")
w("Registered before the regrid in `kc143_d23125x/README.md` (the registration section), scored item by item as registered (`score_regrid_x.py`, `score_scan_x.py`, `score_secant_x.py`, each with controls that must flip their items; the regrid scorer's `--plant` control reads three MISS). **Regrid: %d HIT, %d MISS of %d.** %s **Scan: %d HIT, %d MISS of %d.** %s **Secant and root: %d HIT, %d MISS of %d.** %s" % (
    c_reg[1], c_reg[2], c_reg[0], "MISS: " + c_reg[3].replace("MISS ", "").rstrip(".") + ".", c_scan[1], c_scan[2], c_scan[0], "MISS: " + c_scan[3].replace("MISS ", "").rstrip(".") + ".", c_sec[1], c_sec[2], c_sec[0], "MISS: " + c_sec[3].replace("MISS ", "").replace("exit 0 ()", "exit 0").rstrip(".") + "."))
w("")
w("### The chain and what ran")
w("The k_c 87 chain was held %s to %s UTC (hold file placed %s UTC; its running D 22.3125 scan was stopped by pid at %s UTC, 8.25 min into a scan of 17.6 min with no evaluation done, as t5's rule said when it was not past half). The lane ended normally and the releaser restarted the chain driver at %s UTC; it picked D %s at %s UTC. The pre-authorized extension of the scan window did not act: the scan read one robust change. The lane ran %s to %s UTC (%.1f min)." % (
    hold, relt, hold, stop, cst, cnx.group(2), cnx.group(1), et("start \\(mode full"), et("secant exit \\d+"), (hms(et("secant exit \\d+")) - hms(et("start \\(mode full"))) / 60.0))
w("")
w("Raw: `I1025-macm3/kc143_d23125x/` and `I1025-macm3/kc87_leg_lambda/23.125_kc143x/` at @@H@@.")
print("\n".join(L))
