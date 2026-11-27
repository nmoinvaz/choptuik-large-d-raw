#!/usr/bin/env python3
"""score_scan_b.py [--write] [--mutate=bracket|sec] : scores the scan of kc143_d23125 against the scan items of BOTH registration entries of README.md (the first, 01:50 UTC, and the second, 05:42 UTC),
every number from the files: kc87_leg_lambda/23.125_kc143/{read_lower.txt, scan/scan_D23.125_1025.jsonl, scan/scan_samples.csv}, exits_kc143.txt.
Each item is scored as registered; the first entry's time and memory items were set for the Python block 12 and are replaced by the second entry's (not scored, as the second entry says).
Controls: --mutate=bracket (the read bracket replaced by (-0.035, -0.030): both bracket items must flip to HIT), --mutate=sec (every evaluation 200 s longer: the (340, 520) s item must flip to MISS).
Tail sums are labeled arithmetic only, not a result. Read-only except for --write."""
import csv, json, re, subprocess, sys
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125/"
S = D + "../kc87_leg_lambda/23.125_kc143/"
mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
rd = open(S + "read_lower.txt").read()
m = re.search(r"robust change \((\S+), (\S+)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", rd)
blo, bhi, s0, s1, dl, rlo, rhi = float(m.group(1).rstrip(",")), float(m.group(2).rstrip(",")), m.group(3), m.group(4), float(m.group(5).rstrip(",")), float(m.group(6).rstrip(",")), float(m.group(7).rstrip("]"))
nrob = int(re.search(r"robust changes: (\d+)", rd).group(1)); nonrob = re.search(r"not noise-robust: (.*)", rd).group(1).strip()
if mut == "bracket": blo, bhi = -0.035, -0.030
sc = [json.loads(l) for l in open(S + "scan/scan_D23.125_1025.jsonl") if l.strip()]
secs = [r["sec"] + (200 if mut == "sec" else 0) for r in sc]
ex = open(D + "exits_kc143.txt").read()
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: scan starts", ex).group(1)
t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: scan exit (\d+)", ex); ecode = int(t1.group(2)); t1 = t1.group(1)
wall = hms(t1) - hms(t0)
allrob = all(r["noise_robust"] and r["robust"] for r in sc)
rep = [r for r in sc if r["lam"] == -0.030]; assert len(rep) == 2
keys = [k for k in rep[0] if k not in ("sec", "sec_parts")]; ident = all(rep[0][k] == rep[1][k] for k in keys)
f64diff_pts = sorted({r["lam"] for r in sc if r["f64_sign"] != r["sign"]}); f64diff_n = sum(1 for r in sc if r["f64_sign"] != r["sign"])
pk = {}; low = 1e9
for r in csv.DictReader(open(S + "scan/scan_samples.csv")):
    if r["rss_kB"]: pk[r["pid"]] = max(pk.get(r["pid"], 0), int(r["rss_kB"]))
    if r["avail_GiB"]: low = min(low, float(r["avail_GiB"]))
pks = sorted(v / 1048576 for v in pk.values())[-2:]
A = D + "../kc143_d230625/"
r1 = [json.loads(l) for l in open(A + "secant/secant.jsonl") if l.strip() and json.loads(l).get("kind") == "root"][-1]["lam_lin"]
sdlA = float(re.search(r"det-linear (\S+) range", open(A + "point_summary.txt").read()).group(1))
rg = open(A + "reg_kc143_output.txt").read()
mm = re.search(r"D 23\.125 roots: 127 (\S+), 135 (\S+);", rg); r127b, r135b = float(mm.group(1).rstrip(",")), float(mm.group(2).rstrip(","))
r135a = float(re.search(r"135 (\+0\.00939\d+)", rg).group(1))
br = lambda a, b: abs(blo - a) < 1e-9 and abs(bhi - b) < 1e-9
L = []
def item(entry, name, pct, hit, val): L.append((entry, name, pct, hit, val))
item("1+2", "exactly one robust change in the window", 90, nrob == 1, "%d robust change; not noise-robust points: %s" % (nrob, nonrob))
item("1", "bracket (-0.035, -0.030)", 55, br(-0.035, -0.030), "read (%+.3f, %+.3f), %s to %s, det-linear %+.6f, range [%+.6f, %+.6f]" % (blo, bhi, s0, s1, dl, rlo, rhi))
item("2", "bracket (-0.035, -0.030)", 80, br(-0.035, -0.030), "read (%+.3f, %+.3f)" % (blo, bhi))
item("1", "bracket (-0.025, -0.020) (the registered 5% alternative)", 5, br(-0.025, -0.020), "read (%+.3f, %+.3f)" % (blo, bhi))
item("2", "bracket (-0.025, -0.020) (the registered 1% alternative)", 1, br(-0.025, -0.020), "read (%+.3f, %+.3f)" % (blo, bhi))
item("1", "all 6 evaluations noise-robust", 85, allrob, "%d of %d robust, dln largest %.2e" % (sum(1 for r in sc if r["noise_robust"] and r["robust"]), len(sc), max(r["dln"] for r in sc)))
item("2", "all 6 evaluations noise-robust", 88, allrob, "same")
item("1", "the repeat of -0.030 bit-identical", 90, ident, "ln %.10f and %.10f, every field but sec and sec_parts equal: %s" % (rep[0]["ln"], rep[1]["ln"], ident))
item("2", "the repeat of -0.030 bit-identical", 90, ident, "same")
item("1", "float64 sign equal to the hybrid sign at all 6", 12, f64diff_n == 0, "differs at lambda %s (%d of 6 evaluations, 2 of 5 distinct lambda)" % (", ".join("%+.3f" % x for x in f64diff_pts), f64diff_n))
item("2", "float64 sign equal to the hybrid sign at all 6", 12, f64diff_n == 0, "same")
item("2", "seconds per evaluation in (340, 520) at all 6", 70, all(340 < s < 520 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
item("2", "scan wall 17 to 32 min", 60, 17 * 60 <= wall <= 32 * 60, "%d s = %.1f min (%s to %s UTC, exit %d)" % (wall, wall / 60, t0, t1, ecode))
item("2", "peak RSS per scan process in (5.5, 7.0) GiB", 70, all(5.5 < p < 7.0 for p in pks), "%s GiB (60 s samples, the two scan processes)" % ", ".join("%.3f" % p for p in pks))
item("2", "peak RSS per scan process below 8 GiB", 90, all(p < 8.0 for p in pks), "%.3f GiB" % pks[-1])
item("2", "lowest available memory in the scan above 4 GiB", 80, low > 4.0, "%.1f GiB" % low)
H = [i for i in L if i[3]]; M = [i for i in L if not i[3]]
fmt = lambda i: "%s%s [entry %s]: %s" % (i[1], " (%d%%)" % i[2], i[0], i[4])
out = []
out.append("**the scan, scored** (read_lower.txt, scan/scan_D23.125_1025.jsonl, scan_samples.csv, exits_kc143.txt; `score_scan_b.py`, controls `--mutate=bracket` (read bracket set to (-0.035, -0.030): both bracket items must flip to HIT) and `--mutate=sec` (200 s added to every evaluation: the (340, 520) s item must flip to MISS)): scan %s to %s UTC (%.1f min), exit %d, 2 processes of 4 Rust threads. Hybrid signs %s; **robust change (%+.3f, %+.3f), %s to %s, det-linear %+.6f, estimator range [%+.6f, %+.6f] (an estimator range, not an enclosure; the root is read from the secant)**. The first entry's time and memory items (scan seconds 1000 to 1500, wall 55 to 85 min, peak RSS (5.8, 7.2) GiB) were set for the Python block 12 and are replaced by the second entry's, as the second entry says; they are not scored."
           % (t0, t1, wall / 60.0, ecode, " ".join("%+.3f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in sc[:1] + sc[1:3] + sc[4:]), blo, bhi, s0, s1, dl, rlo, rhi))
out.append("Scoring, HIT = the registered event occurred (entry 1 = the first registration, entry 2 = the second; 1+2 = in both with the same text): " + "; ".join("HIT " + fmt(i) for i in H) + ". " + "; ".join("MISS " + fmt(i) for i in M) + ". (%d items: %d HIT, %d MISS; the bracket items listed as registered alternatives are the events that did not occur when they are MISS.)" % (len(L), len(H), len(M)))
out.append("**The bracket miss.** The one robust change is in the registered alternative (-0.025, -0.020) (5%% in the first entry, 1%% in the second), not in (-0.035, -0.030) (55%% and 80%%). The scan's det-linear estimate %+.6f is %.4f above my second entry's root -0.03067, %.4f above t5's -0.0319, and %.4f above the first entry's provisional -0.0318 (arithmetic only, not a result; the estimator is not the root, in lane A it was %.6f above the secant's root). The shift from my k_c 135 root at D 23.125 (%+.8f) would be %+.6f against %+.6f at 127 to 135 and %+.8f at D 23.0625 for 135 to 143 (arithmetic only, not a result). Reported to t5 by hc at 08:04:49 UTC by date -u; not explained."
           % (dl, dl + 0.03067, dl + 0.0319, dl + 0.0318, sdlA - r1, r135b, dl - r135b, r135b - r127b, r1 - r135a))
txt = "\n".join(out)
print(txt)
if "--write" in sys.argv and not mut:
    stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
    open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " ")))
    print("written")
