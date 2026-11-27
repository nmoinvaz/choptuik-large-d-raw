#!/usr/bin/env python3
"""make_post_1127c.py > post.md : the #1025 comment of macm3 on k_c 143 at D 23.125 and the k_c 143 zero (t5's order, hc 27 Nov 01:38 UTC: "Post each point on #1025 with its bracket, and the zero after both";
the scan and secant with the Rust block 12, hc 04:23 and 04:37 UTC; tol 5e-5, hc 05:59 UTC). Every number comes from the files (exits_kc143.txt, regrid/, point_summary.txt, secant.jsonl, scan jsonl,
zero_arithmetic_143.py and the READMEs' scoring); tail sums are computed here and labeled arithmetic only. @@T@@ and @@H@@ are replaced by the caller. Read-only."""
import csv, datetime, json, os, re, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
sys.path.insert(0, R + "kc135_d23125"); sys.path.insert(0, R + "kc87_leg_lambda"); sys.path.insert(0, R + "kc143_d23125")
import reg_d23125 as rg
import zero_arithmetic_143 as za
F = R + "kc143_d23125/"; A = R + "kc143_d230625/"; S = R + "kc87_leg_lambda/23.125_kc143/"
txt = lambda p: open(p).read()
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()]
readme = txt(F + "README.md"); ex = txt(F + "exits_kc143.txt"); exa = txt(F + "exits_kc143_aborted_0600.txt")


def et(pat, s=None):
    m = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: " + pat, s or ex); assert m, pat; return m.group(1)


rg143 = rg.regrid("kc143_d23125", "exits_kc143.txt"); rg135 = rg.regrid("kc135_d23125", "exits_kc135.txt"); rg143a = rg.regrid("kc143_d230625", "exits_kc143.txt")
rec = jl(F + "in/l1kc143macm3d23125.jsonl")[-1]; src = jl(F + "in/l1kc135macm3d23125.jsonl")[-1]
ps = txt(F + "point_summary.txt")
se = jl(F + "secant/secant.jsonl"); root = [e for e in se if e.get("kind") == "root"][-1]; sev = [e for e in se if e.get("kind") == "eval"]
sc = jl(S + "scan/scan_D23.125_1025.jsonl")
pk = {}
for s in csv.DictReader(open(S + "scan/scan_samples.csv")):
    if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
scan_rss = sorted(v / 1048576 for v in pk.values())[-2:]
ss = list(csv.DictReader(open(F + "secant/samples.csv"))); spk = max(int(s["rss_kB"]) for s in ss if s["rss_kB"]) / 1048576; slow = min(float(s["avail_GiB"]) for s in ss)
d = za.compute([]); lo, hi = root["bracket"]; rt = root["lam_lin"]
z = d["z"]; slope = abs(d["slope"]); stp = z - d["z135"]; stp_last = d["z135"] - d["z127"]
sa1 = d["r135a"] - d["r127a"]; sa = d["ra"] - d["r135a"]; sb1 = d["r135b"] - d["r127b"]; sb = d["rb"] - d["r135b"]
n1 = [e for e in sev if not e["robust"]][0]
b_end = [e for e in sev if e["lam"] == hi][0]; a_end = [e for e in sev if e["lam"] == lo][0]
rat = math_exp = None
import math
ra_ = math.exp(n1["ln"] - b_end["ln"]); rt2 = n1["lam"] + (hi - n1["lam"]) * (ra_ / (ra_ + 1))
scan_sec = sorted(x["sec"] for x in sc)
read = txt(S + "read_lower.txt"); m = re.search(r"robust change \(([^)]*)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", read); sdl = float(m.group(4).rstrip(","))
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
def cnt(key):
    t = re.search(key + r".*", readme).group(0); m = re.search(r"\((\d+) items: (\d+) HIT, (\d+) MISS", t); return int(m.group(1)), int(m.group(2)), int(m.group(3))
c_reg = cnt(r"\*\*the regrid, scored\*\*"); c_scan = cnt(r"\*\*the scan, scored\*\*"); c_sec = cnt(r"\*\*the D 23\.125 secant of k_c 143 and the zero, scored\*\*")
rel = [f for f in os.listdir(R + "kc87_leg_lambda") if f.startswith("HOLD_kc143.txt.released.")][0]
rel_t = datetime.datetime.fromtimestamp(int(rel.split(".")[-1]), datetime.timezone.utc).strftime("%H:%M:%S")
chain_scan = re.search(r"(\d\d:\d\d:\d\d) UTC next: D (\S+) \(previous", txt(F + "release_end_kc143b.log"))
L = []
w = L.append
w("**#1025 macm3, k_c 143 at D 23.125: lambda_1 = %+.8f, robust bracket [%.8f, %.8f] (secant exit 4, width %.3e); the k_c 143 zero by the line through the two roots, D %.5f (@@T@@).** t5's order (hc 27 Nov 01:38 UTC): the k_c 143 rung at D 23.125 by a regrid from my accepted k_c 135 state there (state blob ac01e477), `ell_refine.py l1kc135macm3d23125 135 l1kc143macm3d23125 143 1 23.125 2.0987860107 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, the kc143 check (blob e15b0ee2), then the new scanner (`d18_secant.py scan`) at lambda -0.040 to -0.020 on a 0.005 grid plus a repeat of -0.030 (2 processes) and the secant (`d18_secant.py run --maxev=10`, one process), both with the Rust block 12 (`--b12=rust --b12_threads=4`, accepted by t5 at 04:37 UTC on #1102; scanner blob 9706e506 of wip/ell1-rust-b12 d4b6b6ce) and, by t5's order of hc 05:59 UTC (#1101: root scatter 1.75e-4 between two solves of one state), `--tol=5e-5` in place of 1e-5. The lane was started at %s UTC and restarted at %s UTC for that tolerance (the regrid that started %s UTC was stopped at %s UTC and lost; its files are kept as `*_aborted_0600`). Roots are the det-linear root inside the final bracket, read by position. **Every tail sum below is arithmetic only, not a result.**" % (rt, lo, hi, root["width"], z, et("start \\(mode full", exa), et("start \\(mode full"), et("regrid starts", exa), re.search(r"I stopped the lane at (\d\d:\d\d:\d\d) UTC", readme).group(1)))
w("")
w("**This point does not match the forecasts, mine or t5's, and I do not explain it.** The scan's one robust change is (-0.025, -0.020) and the secant's root is %+.8f. My registered bracket was (-0.035, -0.030) at 80%% with the root -0.03067; t5's rule gave -0.0319 +- 0.003. The root lies %.4f above my forecast and %.4f above t5's centre, outside his band. The zero by the line is therefore %.5f, not about 23.083. The shift of lambda_1 from k_c 135 to 143 at D 23.125 is %+.6f, %.2f times its 127 to 135 shift, while at D 23.0625 the same two steps were equal (ratio %.4f). Nothing was re-run." % (rt, rt + 0.03067, rt + 0.0319, z, sb, sb / sb1, sa / sa1))
w("")
w("### The regrid (raw `I1025-macm3/kc143_d23125/`, README with both registrations first)")
w("")
w("| at D 23.125 | wall (s) | peak RSS (GiB, 60 s samples) | steps | steps ratio | constraint ratio | Delta shift |")
w("|---|---|---|---|---|---|---|")
w("| k_c 135 | %d | %.3f | %d | %.3f | %.3f | %+.4e |" % (rg135["wall"], rg135["rss"], rg135["steps"], rg135["sr"], rg135["cr"], rg135["shift"]))
w("| k_c 143 | %d | %.3f | %d | %.3f | %.3f | %+.4e |" % (rg143["wall"], rg143["rss"], rg143["steps"], rg143["sr"], rg143["cr"], rg143["shift"]))
w("| (k_c 143 at D 23.0625) | %d | %.3f | %d | %.3f | %.3f | %+.4e |" % (rg143a["wall"], rg143a["rss"], rg143a["steps"], rg143a["sr"], rg143a["cr"], rg143a["shift"]))
w("")
w("The regrid ran %s to %s UTC on 27 Nov (exit 0, `capped_run` wall %d s, 6 threads, nice 10). Acceptance (%s UTC): the kc143 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc135 check refuses the result. Record: |F| %.4e (source %.4e), steps %d (source %d), psi-constraint %.4e (source %.4e), Delta %.12f (source %.12f), lam_gauge %.9f (source %.9f)."
  % (et("regrid starts"), et("regrid exit 0"), rg143["wall"], et("kc143 syscheck exit 0"), rec["F"], src["F"], rec["steps"], src["steps"], rec["constraint"], src["constraint"], rec["Delta"], src["Delta"], rec["lam_gauge"], src["lam_gauge"]))
w("")
w("### The scan and the secant (Rust block 12, 4 threads)")
w("")
w("Scan %s to %s UTC (%.1f min, 2 processes, %d to %d s per evaluation, peak RSS %.3f and %.3f GiB per process); secant %s to %s UTC, **exit %s (%s)**, %d evaluations, %d to %d s each, peak RSS %.3f GiB, lowest available memory %.1f GiB:" % (
    et("scan starts"), et("scan exit 0"), (hms(et("scan exit 0")) - hms(et("scan starts"))) / 60.0, scan_sec[0], scan_sec[-1], scan_rss[0], scan_rss[1], et("secant starts"), et("secant exit \\d+"),
    re.search(r"secant exit (\d+)", ex).group(1), root["status"], root["n_eval"], min(e["sec"] for e in sev), max(e["sec"] for e in sev), spk, slow))
w("")
w("```")
w(ps.rstrip())
w("```")
w("")
w("**The exit is 4: the fifth evaluation, lambda %.8f (sign %+d, ln|det| %.3f), is not robust** (dln %.3f above the bar 0.1; the two noise runs agree in sign), so the robust bracket [%.8f, %.8f] stands and the root is its det-linear root %+.8f, inside it by position. The scan's det-linear %.6f lies %.6f above it and its estimator range [%s, %s] holds the root but not the whole bracket. The bracket is %.1f times the tolerance 5e-5. **Arithmetic only, not a result, not an enclosure:** the sign change lies between the non-robust point and the last robust end, an interval of width %.2e; the det-linear zero between those two ends would be %.8f, %.2e from the read root (%.1e in the zero below)." % (
    n1["lam"], int(n1["sign"]), n1["ln"], n1["dln"], lo, hi, rt, sdl, sdl - rt, m.group(5), m.group(6).rstrip("]"), root["width"] / 5e-5, hi - n1["lam"], rt2, abs(rt2 - rt), abs(rt2 - rt) / slope))
w("")
w("### lambda_1 by k_c, the shifts and the zero")
w("")
w("| k_c | lambda_1 at D 23.0625 | lambda_1 at D 23.125 | slope magnitude | zero by the line (D) |")
w("|---|---|---|---|---|")
w("| 127 | %+.8f | %+.8f | %.5f | %.5f |" % (d["r127a"], d["r127b"], abs(d["sl127"]), d["z127"]))
w("| 135 | %+.8f | %+.8f | %.5f | %.5f |" % (d["r135a"], d["r135b"], abs(d["sl135"]), d["z135"]))
w("| 143 | %+.8f [%.8f, %.8f] | **%+.8f** [%.8f, %.8f] | %.5f | **%.5f** |" % (d["ra"], d["la"], d["ha"], rt, lo, hi, slope, z))
w("")
w("The zero is D = 23.0625 + r1 / (slope magnitude), the line through the two roots, as at k_c 127 and 135. **The k_c 143 zero is %.5f**, %+.5f from the k_c 135 zero (the last step was %+.5f, ratio %.4f). Over the four bracket-end combinations it is %.5f to %.5f (arithmetic only, not a result: the brackets are not enclosures of the zero, and #1101's scatter of 1.75e-4 in a root is %.1e in D). Shifts of the root with k_c (arithmetic only, not a result): at D 23.0625 127 to 135 %+.6f, 135 to 143 %+.6f (ratio %.4f); at D 23.125 127 to 135 %+.6f, **135 to 143 %+.6f (ratio %.4f)**. The slope magnitude fell from %.5f to %.5f." % (
    z, stp, stp_last, stp / stp_last, d["zmin"], d["zmax"], 1.75e-4 / slope, sa1, sa, sa / sa1, sb1, sb, sb / sb1, abs(d["sl135"]), slope))
w("")
w("Facts beside the shift, reported and not explained: the regrid at D 23.125 took %d s against %d s at D 23.0625 and peaked at %.3f GiB against %.3f; its Delta shift is %+.4e against %+.4e; the lam_gauge of the record changed from k_c 135 to 143 by %+.3e (D 23.0625: %+.3e); the float64 sign differs from the hybrid sign at lambda -0.035 and -0.030 (3 of 6 evaluations), while the repeat of -0.030 is bit-identical and all 6 scan evaluations are noise-robust. ln|det| falls by %.3f from lambda -0.030 to -0.025 and rises by %.3f to -0.020." % (
    rg143["wall"], rg143a["wall"], rg143["rss"], rg143a["rss"], rg143["shift"], rg143a["shift"], rec["lam_gauge"] - src["lam_gauge"], jl(A + "in/l1kc143macm3d230625.jsonl")[-1]["lam_gauge"] - jl(A + "in/l1kc135macm3d230625.jsonl")[-1]["lam_gauge"],
    [r for r in sc if r["lam"] == -0.03][0]["ln"] - [r for r in sc if r["lam"] == -0.025][0]["ln"], [r for r in sc if r["lam"] == -0.02][0]["ln"] - [r for r in sc if r["lam"] == -0.025][0]["ln"]))
w("")
w("### Registrations and scoring")
w("Both registration entries were written in `kc143_d23125/README.md` before the regrid (the first at 01:50 UTC, the second at 05:42 UTC from the D 23.0625 root, and the tol 5e-5 item at 06:02 UTC); its status entries score them item by item, each as registered (`score_regrid_b.py`, `score_scan_b.py`, `score_secant_b.py` and `zero_arithmetic_143.py`, each with a mutation control that flips the items it should). **Regrid: %d HIT, %d MISS of %d** (the misses: wall %d s above both registered ranges, peak RSS %.3f GiB above both, and the Delta shift %+.4e below the first entry's range). **Scan: %d HIT, %d MISS of %d** (the misses: the bracket, registered (-0.035, -0.030) at 55%% and 80%%, read (-0.025, -0.020), a 5%% and a 1%% alternative; the float64 sign equal to the hybrid at all 6, registered at 12%%; the peak RSS of one scan process below the registered lower end). **Secant, root and zero: %d HIT, %d MISS of %d** (HIT: exit 4 at 40%%, the run wall of %.1f min, the root inside the scan's estimator range, the lane wall of %.1f min, the zero above t5's centre and its step at least 0.9 of the last one; MISS: every item on the root, the slope and the zero, the exit 0 at 55%%, the final bracket at most 5e-5 wide at 90%%, the evaluations of %d to %d s against the registered (290, 400) s, and the secant's peak RSS %.3f GiB against below 8 GiB at 90%%). **t5's items:** his root -0.0319 +- 0.003: read minus it %+.6f, outside; his zero 23.0816 +- 0.003: read %+.5f from it, outside. Timings with the Rust block 12: one secant evaluation took %d to %d s on one process, a scan evaluation %d to %d s with two processes at once." % (
    c_reg[1], c_reg[2], c_reg[0], rg143["wall"], rg143["rss"], rg143["shift"], c_scan[1], c_scan[2], c_scan[0], c_sec[1], c_sec[2], c_sec[0], root["sec"] / 60.0, (hms(et("secant exit \\d+")) - hms(et("start \\(mode full"))) / 60.0, min(e["sec"] for e in sev), max(e["sec"] for e in sev), spk,
    rt + 0.0319, z - 23.0816, min(e["sec"] for e in sev), max(e["sec"] for e in sev), scan_sec[0], scan_sec[-1]))
w("")
w("### Next")
w("The k_c 87 chain was released for good at %s UTC (the lane ended normally, t5's ruling hc 01:51 and 04:21 UTC) and its scan of D %s started %s UTC. Both k_c 143 points and the zero are in; the k_c 143 point at D 23.125 is the one that does not follow the trend, and I wait for t5 before running anything on it. The quadratic zeros wait for the k_c 127 and k_c 135 D 23.0 roots of the other lanes." % (rel_t, chain_scan.group(2), chain_scan.group(1)))
w("")
w("Raw: `I1025-macm3/kc143_d23125/`, `I1025-macm3/kc143_d230625/` and `I1025-macm3/kc87_leg_lambda/23.125_kc143/` at @@H@@.")
print("\n".join(L))
