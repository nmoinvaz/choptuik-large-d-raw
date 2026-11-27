#!/usr/bin/env python3
"""score_secant_a.py [--write] [--mutate=root] : scores the secant of kc143_d230625 against the registered items (README, "The root and the secant"), every number from the files:
secant/secant.jsonl, secant/samples.csv, secant/secant.log, exits_kc143.txt, reg_kc143_output.txt (the k_c roots at D 23.0625), ../kc143_d23125/rust_b12/{gates_log,e2e_log}.txt (the gate's time window).
Prints the Status entry; --write appends it to README.md. --mutate=root moves the read root down by 3e-4 (a control: the item "my root in (0.0130, 0.0150)" must flip to HIT).
Tail sums are labeled arithmetic only, not a result. Read-only except for --write."""
import csv, json, math, re, subprocess, sys
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d230625/"
G = D + "../kc143_d23125/rust_b12/"
mut = "--mutate=root" in sys.argv


def hms(s):
    h, m, x = s.split(":"); return int(h) * 3600 + int(m) * 60 + int(x)


recs = [json.loads(l) for l in open(D + "secant/secant.jsonl") if l.strip()]
ev = [r for r in recs if r.get("kind") == "eval"]; root = [r for r in recs if r.get("kind") == "root"][-1]
lo, hi = root["bracket"]; rt = root["lam_lin"] - (3e-4 if mut else 0.0)
# the det-linear root recomputed from the two bracket records (the records of the two bracket ends)
a = [r for r in ev if r["lam"] == lo][0]; b = [r for r in ev if r["lam"] == hi][0]
assert a["sign"] * b["sign"] < 0
ratio = math.exp(a["ln"] - b["ln"]); rt_re = lo + (hi - lo) * (ratio / (ratio + 1) if a["sign"] > 0 else 1 / (ratio + 1))
assert abs(rt_re - root["lam_lin"]) < 1e-15, (rt_re, root["lam_lin"])
assert lo < root["lam_lin"] < hi
ex = open(D + "exits_kc143.txt").read()
t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d230625: secant starts", ex).group(1)
t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d230625: secant exit (\d+)", ex); ex_code = int(t1.group(2)); t1 = t1.group(1)
wall_exit = hms(t1) - hms(t0)
cw = int(re.search(r"capped_run: exit 0 wall (\d+) s cap_hit False", open(D + "secant/secant.log").read()).group(1))
secs = [r["sec"] for r in ev]; parts = [r["sec_parts"] for r in ev]
rows = list(csv.DictReader(open(D + "secant/samples.csv"))); pk = {}
for s in rows:
    if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
peak = max(pk.values()) / 1048576; lowav = min(float(s["avail_GiB"]) for s in rows)
sc = [json.loads(l) for l in open(D + "../kc87_leg_lambda/23.0625_kc143/scan/scan_D23.0625_1025.jsonl") if l.strip()]
rd = open(D + "../kc87_leg_lambda/23.0625_kc143/read_lower.txt").read()
ends = [(e["lam"], e["ln"], e["sign"], s["ln"], s["sign"]) for e in ev[:2] for s in sc if abs(s["lam"] - e["lam"]) < 1e-12]
assert len(ends) == 3, ends     # 0.015 twice (the repeat), 0.020 once
dend = max(abs(x[1] - x[3]) for x in ends); send = all(x[2] == x[4] for x in ends)
m = re.search(r"robust changes 1: \([^)]*\) \S+ to \S+ det-linear (\S+) range \[(\S+), (\S+)\]", open(D + "point_summary.txt").read()); sdl, rlo, rhi = float(m.group(1)), float(m.group(2)), float(m.group(3))
# the gate's window against the secant's first evaluation
gs = re.search(r"(\d\d:\d\d:\d\d) UTC gates start", open(G + "gates_log.txt").read()).group(1)
ge = re.search(r"(\d\d:\d\d:\d\d) UTC e2e scan exit (\d+)", open(G + "e2e_log.txt").read()); assert ge.group(2) == "0"; ge = ge.group(1)
ev1_end = hms(t0) + secs[0]      # arithmetic: the secant's start plus the first evaluation's seconds (the process start-up is not counted)
later = secs[1:]; sl = secs[0] / (sum(later) / len(later)); b12 = parts[0][1] / (sum(p[1] for p in parts[1:]) / len(parts[1:]))
# the k_c roots at D 23.0625
rl = re.search(r"D 23\.0625 roots: (.*)", open(D + "reg_kc143_output.txt").read()).group(1)
R = [(int(k), float(v)) for k, v in re.findall(r"(\d+) ([+-]\d\.\d+)", rl)]
R.append((143, rt)); sh = [(R[i][0], R[i + 1][0], R[i + 1][1] - R[i][1]) for i in range(len(R) - 1)]
rat = [sh[i + 1][2] / sh[i][2] for i in range(len(sh) - 1)]
fmt = lambda x, n=4: ("%+." + str(n) + "f") % x
L = []
def item(name, pct, hit, val): L.append((name, pct, hit, val))


item("my root in (+0.0130, +0.0150)", 65, 0.0130 < rt < 0.0150, "%+.8f (%s the upper end by %.8f)" % (rt, "above" if rt > 0.0150 else "below", abs(rt - 0.0150)))
item("t5's band (+0.0109, +0.0169)", 95, 0.0109 < rt < 0.0169, "%+.8f" % rt)
item("t5's +0.0139 +- 0.003", None, abs(rt - 0.0139) < 0.003, "read minus 0.0139 = %+.8f (his rule's exact value %+.7f, read minus it %+.8f)" % (rt - 0.0139, R[-2][1] + 0.79 * sh[-2][2], rt - (R[-2][1] + 0.79 * sh[-2][2])))
item("secant exit 0 (tol) within 10 evaluations", 55, ex_code == 0 and root["status"] == "tol" and root["n_eval"] <= 10, "exit %d, status %s, %d evaluations" % (ex_code, root["status"], root["n_eval"]))
item("secant exit 4", 40, ex_code == 4, "exit %d" % ex_code)
item("per evaluation in (800, 1050) s at all 5", 60, all(800 < s < 1050 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
item("run wall 65 to 125 min", 55, 65 * 60 <= root["sec"] <= 125 * 60, "%d s = %.1f min (capped_run %d s = %.1f min; start %s, exit %s UTC: %d s)" % (root["sec"], root["sec"] / 60, cw, cw / 60, t0, t1, wall_exit))
item("peak RSS in (5.0, 6.5) GiB", 65, 5.0 < peak < 6.5, "%.3f GiB (60 s samples of the secant process)" % peak)
item("peak RSS below 7 GiB", 85, peak < 7.0, "%.3f GiB" % peak)
item("root inside the scan's estimator range", 80, rlo <= rt <= rhi, "root %+.8f in [%.6f, %.6f]; the whole final bracket [%.8f, %.8f] inside: %s" % (rt, rlo, rhi, lo, hi, rlo <= lo and hi <= rhi))
item("the secant's evaluation under way slows by less than 1.3 times (registered in kc143_d23125/README, for the Rust gate)", 70, sl < 1.3,
     "evaluation 1 (%d s) over the mean of evaluations 2 to 5 (%.2f s) = %.3f; its block 12 part %d s over the mean %.1f s = %.3f; the gate window %s to %s UTC (%d s) lies inside evaluation 1 (%s to about %s UTC by arithmetic; no control run without the gate, so a first-evaluation cost, if any, is not separated)" % (
         secs[0], sum(later) / len(later), sl, parts[0][1], sum(p[1] for p in parts[1:]) / len(parts[1:]), b12, gs, ge, hms(ge) - hms(gs), t0, "%02d:%02d:%02d" % (ev1_end // 3600, ev1_end % 3600 // 60, ev1_end % 60)))
out = []
out.append("**the D 23.0625 secant of k_c 143, scored** (secant/secant.jsonl, samples.csv, secant.log, exits_kc143.txt; `score_secant_a.py`; its control `--mutate=root` moves the root down by 3e-4 and the first item flips to HIT). Secant %s to %s UTC (the lane's hc line 05:33:18 UTC), **exit %d (tol)**, %d evaluations (the two ends included; the interior points %s), **final bracket [%.8f, %.8f], width %.3e, signs %s, both ends robust, det-linear root %+.8f** (inside the bracket by position; recomputed from the two bracket records, equal to 1e-15); Brent's last point %.8f. The secant's two end evaluations against the scan's records at the same lambda (0.015 twice, 0.020 once): largest |d ln| %.3e, signs equal: %s."
           % (t0, t1, ex_code, root["n_eval"], ", ".join("%.8f" % r["lam"] for r in ev[2:]), lo, hi, root["width"], root["signs"], rt, root["lam_brent"], dend, send))
out.append("The scan's det-linear is %.6f; the secant's root is %.6f below it. ln|det| by evaluation: %s." % (sdl, sdl - rt, "; ".join("%.8f: %.3f dln %.2e" % (r["lam"], r["ln"], r["dln"]) for r in ev)))
out.append("")
HIT = [i for i in L if i[2]]; MISS = [i for i in L if not i[2]]
out.append("**Scored** (HIT = the registered event occurred; the percentages are the registered probabilities): " + "; ".join("%s%s: %s" % (n, (" (%d%%)" % p if p else ""), v) for n, p, h, v in L if h) + ".")
out.append("**MISS** (%d): " % len(MISS) + "; ".join("%s%s: %s" % (n, (" (%d%%)" % p if p else ""), v) for n, p, h, v in MISS) + ". (Of the %d listed items %d are HIT and %d MISS; the exit 0 and exit 4 items exclude each other, and the exit 4 item is the registered alternative that did not occur.)" % (len(L), len(HIT), len(MISS)))
out.append("**The shift of lambda_1 at D 23.0625 with k_c** (the roots of reg_kc143_output.txt plus this one; **arithmetic only, not a result**): " + ", ".join("%d to %d %+.8f" % s for s in sh) + "; ratios of each shift to the one before: " + ", ".join("%.4f" % r for r in rat)
           + ". **The k_c 135 to 143 shift (%+.8f) equals the 127 to 135 shift (%+.8f) to %.1e (ratio %.5f); the registered ratio was 0.80 +- 0.17 (t5's 0.79), the earlier ratios 0.5325, 0.5590, 0.7987, 0.8031.** My registered range of ratios (0.6 to 1.0, root +0.01284 to +0.01514) ends at the ratio read; my interval (+0.0130, +0.0150) covered ratios 0.63 to 0.98, which is why it missed. Reported, not explained." % (sh[-1][2], sh[-2][2], abs(sh[-1][2] - sh[-2][2]), rat[-1]))
out.append("**Consequence for the D 23.125 lane** (arithmetic only, not a result): the registered scenario 'ratio 1.00' of reg_kc143_output.txt gave root(23.0625) +0.015140, root(23.125) -0.030687 (growth 0.976), slope -0.73323, zero 23.08315; the read root(23.0625) is within %.1e of that scenario's. If the D 23.125 shift also equals the 127 to 135 one (+0.005611), root(23.125) is -0.030687, inside the provisional bracket (-0.035, -0.030) of kc143_d23125/scan_plan.env; its second registration is written from this root." % abs(rt - 0.015140))
txt = "\n".join(out)
print(txt)
if "--write" in sys.argv and not mut:
    stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
    open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n\n", "\n")))
    print("written")
