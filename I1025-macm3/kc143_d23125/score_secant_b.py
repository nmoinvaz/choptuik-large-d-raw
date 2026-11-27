#!/usr/bin/env python3
"""score_secant_b.py [--write] [--mutate=root|sec] : scores the secant, the root and the zero of kc143_d23125 against the items of BOTH registration entries of README.md (the first, 01:50 UTC,
and the second, 05:42 UTC, with the tol 5e-5 item of the 06:02 UTC entry), every number from the files: secant/secant.jsonl, secant/samples.csv, secant/secant.log, exits_kc143.txt,
point_summary.txt, zero_arithmetic_143.py (the zero by the line through the two roots, kc143_d230625/point_summary.txt and this lane's).
The first entry's secant time and memory items (800 to 1050 s per evaluation, 65 to 125 min, RSS (4.8, 6.3) and below 7 GiB) were set for the Python block 12 and are replaced by the second
entry's, as the second entry says; they are not scored.
Controls: --mutate=root (the read root moved down by 0.0062: the root, slope and zero items must flip to HIT), --mutate=sec (every evaluation 100 s longer: the (290, 400) s item must flip to HIT).
Tail sums are labeled arithmetic only, not a result. Read-only except for --write."""
import csv, json, math, re, subprocess, sys
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125/"
sys.path.insert(0, D)
import zero_arithmetic_143 as za
mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
recs = [json.loads(l) for l in open(D + "secant/secant.jsonl") if l.strip()]
ev = [r for r in recs if r.get("kind") == "eval"]; root = [r for r in recs if r.get("kind") == "root"][-1]
lo, hi = root["bracket"]; rt = root["lam_lin"]
a = [r for r in ev if r["lam"] == lo][0]; b = [r for r in ev if r["lam"] == hi][0]
assert a["sign"] * b["sign"] < 0
ratio = math.exp(a["ln"] - b["ln"]); rt_re = lo + (hi - lo) * (ratio / (ratio + 1) if a["sign"] > 0 else 1 / (ratio + 1))
assert abs(rt_re - rt) < 1e-15 and lo < rt < hi
nr = [r for r in ev if not r["robust"]]; assert len(nr) == 1
n1 = nr[0]; sgn_ok = n1["sign"] != b["sign"] and lo < n1["lam"] < hi and n1["lam"] < hi
# arithmetic only: the sign-change interval between the non-robust point and the last robust end, and the det-linear zero between them
ra = math.exp(n1["ln"] - b["ln"]); rt2 = n1["lam"] + (hi - n1["lam"]) * (ra / (ra + 1))
if mut == "root":
    shift = -0.0062; rt += shift
sec = [r["sec"] + (100 if mut == "sec" else 0) for r in ev]
ex = open(D + "exits_kc143.txt").read()
t_launch = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: start \(mode full", ex).group(1)
t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: secant starts", ex).group(1)
t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: secant exit (\d+)", ex); ecode = int(t1.group(2)); t1 = t1.group(1)
lane = hms(t1) - hms(t_launch)
rows = list(csv.DictReader(open(D + "secant/samples.csv"))); pk = {}
for s in rows:
    if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
peak = max(pk.values()) / 1048576; lowav = min(float(s["avail_GiB"]) for s in rows)
sc = [json.loads(l) for l in open(D + "../kc87_leg_lambda/23.125_kc143/scan/scan_D23.125_1025.jsonl") if l.strip()]
m = re.search(r"robust change \([^)]*\), \S to \S, det-linear (\S+), range \[(\S+), (\S+)\]", open(D + "../kc87_leg_lambda/23.125_kc143/read_lower.txt").read()); sdl, rlo, rhi = float(m.group(1).rstrip(",")), float(m.group(2).rstrip(",")), float(m.group(3).rstrip("]"))
# the zero by the line, from zero_arithmetic_143 (the mutated root is passed through the same function)
d = za.compute(["--mutate=r2"] if False else [])
if mut == "root":
    d["rb"] = rt; d["z"] = za.lz(d["ra"], rt); d["slope"] = (rt - d["ra"]) / (za.Db - za.Da)
z = d["z"]; slope = abs(d["slope"]); stp = z - d["z135"]; stp_last = d["z135"] - d["z127"]
sb1 = d["r135b"] - d["r127b"]; sa = d["ra"] - d["r135a"]
# ends of the scan against the secant's (the same lambda, the same state)
ends = [(e["lam"], e["ln"], e["sign"], s["ln"], s["sign"]) for e in ev[:2] for s in sc if abs(s["lam"] - e["lam"]) < 1e-12]; assert len(ends) == 2, ends
dend = max(abs(x[1] - x[3]) for x in ends)
L = []
def item(entry, name, pct, hit, val): L.append((entry, name, pct, hit, val))
item("1", "root in (-0.0330, -0.0306) (mine, provisional, -0.0318 +- 0.0012)", 65, -0.0330 < rt < -0.0306, "%+.8f" % rt)
item("2", "root in (-0.03086, -0.03055)", 60, -0.03086 < rt < -0.03055, "%+.8f" % rt)
item("2", "root in (-0.03124, -0.02992)", 85, -0.03124 < rt < -0.02992, "%+.8f (above the upper end by %.5f)" % (rt, rt + 0.02992))
item("2", "root above t5's central -0.0319", 95, rt > -0.0319, "%+.8f, %+.6f above it" % (rt, rt + 0.0319))
item("2", "root inside t5's band (-0.0349, -0.0289)", 98, -0.0349 < rt < -0.0289, "%+.8f, above the upper end by %.6f" % (rt, rt + 0.0289))
item("1", "slope magnitude above k_c 135's 0.73102", 75, slope > 0.73102, "%.5f" % slope)
item("1+2", "slope magnitude in (0.7310, 0.7360)", 60, 0.7310 < slope < 0.7360, "%.5f" % slope)
item("1+2", "secant exit 0 (tol) within 10 evaluations", 55, ecode == 0 and root["status"] == "tol", "exit %d, status %s, %d evaluations" % (ecode, root["status"], root["n_eval"]))
item("1+2", "secant exit 4", 40, ecode == 4, "exit %d (%s)" % (ecode, root["why"]))
item("2", "per evaluation in (290, 400) s at all of them", 65, all(290 < s < 400 for s in sec), "%s s, mean %.0f s" % (", ".join(map(str, sec)), sum(sec) / len(sec)))
item("2", "run wall 20 to 45 min", 65, 20 * 60 <= root["sec"] <= 45 * 60, "%d s = %.1f min (%s to %s UTC)" % (root["sec"], root["sec"] / 60, t0, t1))
item("2", "peak RSS in (5.5, 7.0) GiB", 65, 5.5 < peak < 7.0, "%.3f GiB (60 s samples of the secant process, %d samples)" % (peak, len(rows)))
item("2", "peak RSS below 8 GiB", 90, peak < 8.0, "%.3f GiB" % peak)
item("1+2", "root inside the scan's estimator range", 80, rlo <= rt <= rhi, "root %+.8f in [%+.6f, %+.6f]; the whole final bracket [%.8f, %.8f] inside: %s" % (rt, rlo, rhi, lo, hi, rlo <= lo and hi <= rhi))
item("06:02", "final bracket width at most 5e-5", 90, root["width"] <= 5e-5, "width %.3e" % root["width"])
item("2", "the lane (launch to the secant exit line) 115 to 175 min", 60, 115 * 60 <= lane <= 175 * 60, "%d s = %.1f min (%s to %s UTC)" % (lane, lane / 60, t_launch, t1))
item("1", "zero in (23.0795, 23.0830)", 65, 23.0795 < z < 23.0830, "%.5f" % z)
item("1", "zero step from the k_c 135 zero +0.0063 +- 0.0010", None, abs(stp - 0.0063) < 0.0010, "%+.5f" % stp)
item("2", "zero in (23.0829, 23.0835)", 80, 23.0829 < z < 23.0835, "%.5f" % z)
item("2", "zero in (23.0830, 23.0833)", 60, 23.0830 < z < 23.0833, "%.5f" % z)
item("2", "zero step in (+0.0075, +0.0082)", 80, 0.0075 < stp < 0.0082, "%+.5f" % stp)
item("2", "zero step at least 0.9 of the last step %+.5f" % stp_last, 95, stp >= 0.9 * stp_last, "%+.5f (ratio %.4f)" % (stp, stp / stp_last))
item("2", "my zero inside t5's band 23.0816 +- 0.003", 95, 23.0786 < z < 23.0846, "%.5f (above its upper end by %.5f)" % (z, z - 23.0846))
item("2", "my zero above t5's central 23.0816", 90, z > 23.0816, "%.5f, %+.5f" % (z, z - 23.0816))
H = [i for i in L if i[3]]; M = [i for i in L if not i[3]]
fmt = lambda i: "%s%s [entry %s]: %s" % (i[1], " (%d%%)" % i[2] if i[2] else "", i[0], i[4])
out = []
out.append("**the D 23.125 secant of k_c 143 and the zero, scored** (secant/secant.jsonl, samples.csv, secant.log, exits_kc143.txt, point_summary.txt, `zero_arithmetic_143.py` -> `zero_arithmetic_143.txt`; `score_secant_b.py`, controls `--mutate=root` (root moved down by 0.0062: the root, slope and zero items flip to HIT) and `--mutate=sec` (100 s added to every evaluation: the (290, 400) s item flips to HIT)). Secant %s to %s UTC (the lane's hc line 08:25:47 UTC), tol 5e-5, Rust block 12 with 4 threads, one process, **exit %d (%s)**, %d evaluations (the two ends included; the interior points %s), **final robust bracket [%.8f, %.8f], width %.3e, signs %s, both ends robust, det-linear root %+.8f** (inside the bracket by position; recomputed from the two bracket records, equal to 1e-15); Brent's last point %.8f. The fifth evaluation, lambda %.8f (sign %+d, ln|det| %.3f), is **not robust** (dln %.3f above the bar 0.1; the two noise runs agree in sign), so the exit is 4 and the robust bracket stands. The secant's two end evaluations against the scan's records at the same lambda (-0.025 once, -0.020 once): largest |d ln| %.3e."
           % (t0, t1, ecode, root["status"], root["n_eval"], ", ".join("%.8f" % r["lam"] for r in ev[2:]), lo, hi, root["width"], root["signs"], rt, root["lam_brent"], n1["lam"], int(n1["sign"]), n1["ln"], n1["dln"], dend))
out.append("The scan's det-linear is %.6f; the secant's root is %.6f below it. ln|det| by evaluation: %s. **Arithmetic only, not a result, not an enclosure:** the sign change lies between the non-robust point (%.8f, sign %+d) and the last robust end (%.8f, sign %+d), an interval of width %.2e; the det-linear zero between those two ends would be %.8f, %.2e from the non-robust point and %.2e from the read root; as a root in D the read root and this one differ by %.1e (the zero by the line moves by about %.1e)." % (
    sdl, sdl - rt, "; ".join("%.8f: %.3f dln %.2e" % (r["lam"], r["ln"], r["dln"]) for r in ev), n1["lam"], int(n1["sign"]), hi, int(b["sign"]), hi - n1["lam"], rt2, rt2 - n1["lam"], abs(rt2 - rt), abs(rt2 - rt), abs(rt2 - rt) / slope))
out.append("")
out.append("Scoring, HIT = the registered event occurred (entry 1 = the first registration, entry 2 = the second, 06:02 = the tol 5e-5 entry; 1+2 = in both with the same text; no percentage = no probability registered, the item is t5's or a rule's): " + "; ".join("HIT " + fmt(i) for i in H) + ". " + "; ".join("MISS " + fmt(i) for i in M) + ". (%d items: %d HIT, %d MISS; exit 0 and exit 4 exclude each other.)" % (len(L), len(H), len(M)))
out.append("**t5's items** (arithmetic only, not a result): his root -0.0319 +- 0.003: read minus -0.0319 = %+.6f, **outside** his band; his zero 23.0816 +- 0.003: read %.5f, %+.5f, **outside** his band. The read root is %.6f above my second entry's central -0.03067, and the upper end of its 85%% interval, -0.02992, is %.5f below the read root." % (rt + 0.0319, z, z - 23.0816, rt + 0.03067, rt + 0.02992))
out.append("**The shift of lambda_1 with k_c** (the roots of reg_kc143_output.txt, the point summaries and this one; **arithmetic only, not a result**): at D 23.0625 127 to 135 %+.6f, 135 to 143 %+.6f (ratio %.4f); at D 23.125 127 to 135 %+.6f, **135 to 143 %+.6f (ratio %.4f, 2.1 times the earlier shift)**. The slope magnitude over D 23.0625 to 23.125 by k_c: 127 %.5f, 135 %.5f, 143 %.5f. The zero by the line: k_c 127 %.5f, 135 %.5f, 143 %.5f; steps %+.5f then %+.5f (ratio %.4f). Reported, **not explained**. Facts of the regrid of this rung, D 23.125 against D 23.0625: wall %d against %d s, peak RSS %.3f against %.3f GiB, Delta shift %+.4e against %+.4e; the record's lam_gauge changed from k_c 135 to 143 by %+.3e (D 23.0625: %+.3e)."
           % (d["r135a"] - d["r127a"], sa, sa / (d["r135a"] - d["r127a"]), sb1, d["rb"] - d["r135b"], (d["rb"] - d["r135b"]) / sb1, abs(d["sl127"]), abs(d["sl135"]), slope, d["z127"], d["z135"], z, stp_last, stp, stp / stp_last,
              int(re.search(r"regrid exit 0, wall (\d+) s", ex).group(1)), int(re.search(r"regrid exit 0, wall (\d+) s", open(D + "../kc143_d230625/exits_kc143.txt").read()).group(1)),
              max(int(r["rss_kB"]) for r in csv.DictReader(open(D + "regrid/regrid_samples.csv")) if r["rss_kB"]) / 1048576, max(int(r["rss_kB"]) for r in csv.DictReader(open(D + "../kc143_d230625/regrid/regrid_samples.csv")) if r["rss_kB"]) / 1048576,
              (lambda f: f["Delta"] - f["Delta_src"])([json.loads(l) for l in open(D + "in/l1kc143macm3d23125.jsonl") if l.strip()][-1]), (lambda f: f["Delta"] - f["Delta_src"])([json.loads(l) for l in open(D + "../kc143_d230625/in/l1kc143macm3d230625.jsonl") if l.strip()][-1]),
              (lambda f, g: f["lam_gauge"] - g["lam_gauge"])([json.loads(l) for l in open(D + "in/l1kc143macm3d23125.jsonl") if l.strip()][-1], [json.loads(l) for l in open(D + "in/l1kc135macm3d23125.jsonl") if l.strip()][-1]),
              (lambda f, g: f["lam_gauge"] - g["lam_gauge"])([json.loads(l) for l in open(D + "../kc143_d230625/in/l1kc143macm3d230625.jsonl") if l.strip()][-1], [json.loads(l) for l in open(D + "../kc143_d230625/in/l1kc135macm3d230625.jsonl") if l.strip()][-1])))
txt = "\n".join(out)
print(txt)
if "--write" in sys.argv and not mut:
    stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
    open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n\n", "\n").replace("\n", " ")))
    print("written")
