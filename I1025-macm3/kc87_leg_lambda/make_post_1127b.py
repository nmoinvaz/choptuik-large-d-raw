#!/usr/bin/env python3
"""make_post_1127b.py > post.md : the #1025 comment of macm3 on k_c 143 at D 23.0625 (t5's order, hc 27 Nov 01:38 UTC: "Post each point on #1025 with its bracket, and the zero after both"; the scan's bracket
accepted and the secant ordered, hc 04:19 UTC). Every number comes from the files (exits_kc143.txt, regrid/, point_summary.txt, secant.jsonl, scan_samples.csv, reg_kc143_output.txt and the READMEs' scoring);
tail sums are computed here and labeled arithmetic only. @@T@@ and @@H@@ are replaced by the caller. Read-only."""
import csv, json, os, re, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
sys.path.insert(0, R + "kc135_d23125"); sys.path.insert(0, R + "kc87_leg_lambda")
import reg_d23125 as rg
F = R + "kc143_d230625/"; S = R + "kc87_leg_lambda/23.0625_kc143/"
txt = lambda p: open(p).read()
ex = txt(F + "exits_kc143.txt")


def et(pat):
    m = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d230625: " + pat, ex); assert m, pat; return m.group(1)


rg143 = rg.regrid("kc143_d230625", "exits_kc143.txt"); rg135 = rg.regrid("kc135_d230625", "exits_kc135.txt")
rec = [json.loads(l) for l in open(F + "in/l1kc143macm3d230625.jsonl") if l.strip()][-1]
src = [json.loads(l) for l in open(F + "in/l1kc135macm3d230625.jsonl") if l.strip()][-1]
ps = txt(F + "point_summary.txt")
se = [json.loads(l) for l in open(F + "secant/secant.jsonl") if l.strip()]; root = [e for e in se if e.get("kind") == "root"][-1]; sev = [e for e in se if e.get("kind") == "eval"]
sc = [json.loads(l) for l in open(S + "scan/scan_D23.0625_1025.jsonl") if l.strip()]
pk = {}
for s in csv.DictReader(open(S + "scan/scan_samples.csv")):
    if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
scan_rss = sorted(v / 1048576 for v in pk.values())[-2:]
rl = re.search(r"D 23\.0625 roots: (.*)", txt(F + "reg_kc143_output.txt")).group(1)
Rt = [(int(k), float(v)) for k, v in re.findall(r"(\d+) ([+-]\d\.\d+)", rl)]; Rt.append((143, root["lam_lin"]))
sh = [Rt[i + 1][1] - Rt[i][1] for i in range(len(Rt) - 1)]; rat = [sh[i + 1] / sh[i] for i in range(len(sh) - 1)]
ss = list(csv.DictReader(open(F + "secant/samples.csv"))); spk = max(int(s["rss_kB"]) for s in ss if s["rss_kB"]) / 1048576; slow = min(float(s["avail_GiB"]) for s in ss)
lo, hi = root["bracket"]; rt = root["lam_lin"]
scan_sec = sorted(x["sec"] for x in sc)
sread = re.search(r"robust changes 1: \(([^)]*)\) (\S+) to (\S+) det-linear (\S+) range \[(\S+), (\S+)\]", ps)
tabs = ["| k_c | lambda_1 at D 23.0625 | shift from the k_c before | ratio to the shift before |", "|---|---|---|---|"]
for i, (k, v) in enumerate(Rt):
    tabs.append("| %d | **%+.8f**%s | %s | %s |" % (k, v, " [%.8f, %.8f]" % (lo, hi) if k == 143 else "", "%+.8f" % sh[i - 1] if i else "", "%.4f" % rat[i - 2] if i >= 2 else ""))
sc_readme = txt(F + "README.md")
# the lane's scoring entries (counts of HIT and MISS) from the README, by command
def counts(key):
    m = re.search(key + r".*", sc_readme); return m.group(0) if m else ""
nh_reg = len(re.findall(r"HIT ", re.search(r"\*\*the regrid, scored\*\*.*", sc_readme).group(0))); nm_reg = len(re.findall(r"MISS ", re.search(r"\*\*the regrid, scored\*\*.*", sc_readme).group(0)))
sc_line = re.search(r"\*\*the scan, scored\*\*.*", sc_readme).group(0); nh_sc = len(re.findall(r"HIT ", sc_line)); nm_sc = len(re.findall(r"MISS ", sc_line))
se_line = re.search(r"\*\*the D 23\.0625 secant of k_c 143, scored\*\*.*", sc_readme).group(0)
L = []
w = L.append
w("**#1025 macm3, k_c 143 at D 23.0625: lambda_1 = %+.8f, bracket [%.8f, %.8f], width %.3e, both ends robust (@@T@@).** t5's order (hc 27 Nov 01:38 UTC): the k_c 143 rung at D 23.0625 by a regrid from my accepted k_c 135 state there (state blob a6253940, record 49ba2db8), `ell_refine.py l1kc135macm3d230625 135 l1kc143macm3d230625 143 1 23.0625 2.0990016035 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, the kc143 check (blob e15b0ee2), the new scanner at lambda 0.005 to 0.025 plus a repeat of 0.015 (2 processes) and the secant (tol 1e-5, `d18_secant.py run --maxev=10`, one process; scanner eb1396ad of wip/ell1-speed 92b9bf53, block 12 in Python, because the lane was started before the Rust block 12 of #1102). t5's ruling (hc 04:19 UTC): the scan's one robust change (0.015, 0.020) accepted as the bracket. Roots are the det-linear root inside the final bracket, read by position. **Every tail sum below is arithmetic only, not a result.**" % (rt, lo, hi, root["width"]))
w("")
w("### The regrid (raw `I1025-macm3/kc143_d230625/`, README with the registration first)")
w("")
w("| at D 23.0625 | wall (s) | peak RSS (GiB, 60 s samples) | steps | steps ratio | constraint ratio | Delta shift |")
w("|---|---|---|---|---|---|---|")
w("| k_c 135 | %d | %.3f | %d | %.3f | %.3f | %+.4e |" % (rg135["wall"], rg135["rss"], rg135["steps"], rg135["sr"], rg135["cr"], rg135["shift"]))
w("| k_c 143 | %d | %.3f | %d | %.3f | %.3f | %+.4e |" % (rg143["wall"], rg143["rss"], rg143["steps"], rg143["sr"], rg143["cr"], rg143["shift"]))
w("")
w("The regrid ran %s to %s UTC on 27 Nov (exit 0, `capped_run` wall %d s, 6 threads, nice 10). Acceptance (%s UTC): the kc143 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc135 check refuses the result. Record: |F| %.4e (source %.4e), steps %d (source %d), psi-constraint %.4e (source %.4e), Delta %.12f (source %.12f). The k_c 87 chain was held beside it (t5's ruling, hc 01:51 UTC)."
  % (et("regrid starts"), et("regrid exit 0"), rg143["wall"], et("kc143 syscheck exit 0"), rec["F"], src["F"], rec["steps"], src["steps"], rec["constraint"], src["constraint"], rec["Delta"], src["Delta"]))
w("")
w("### The scan (new scanner `d18_secant.py scan`) and the secant")
w("")
w("Scan %s to %s UTC (%.1f min, 2 processes, %d to %d s per evaluation, peak RSS %.3f and %.3f GiB per process); secant %s to %s UTC, **exit %s** (tol), %d evaluations, %d to %d s each:" % (
    et("scan starts"), et("scan exit 0"), (lambda a, b: (b - a) / 60.0)(*[sum(int(x) * k for x, k in zip(t.split(":"), (3600, 60, 1))) for t in (et("scan starts"), et("scan exit 0"))]), scan_sec[0], scan_sec[-1], scan_rss[0], scan_rss[1],
    et("secant starts"), et("secant exit \\d+"), re.search(r"secant exit (\d+)", ex).group(1), root["n_eval"], min(e["sec"] for e in sev), max(e["sec"] for e in sev)))
w("")
w("```")
w(ps.rstrip())
w("```")
w("")
w("The scan's det-linear (%s) is %.6f above the secant's root; the secant's root lies inside the scan's estimator range [%s, %s] and the whole final bracket does too." % (sread.group(4), float(sread.group(4)) - rt, sread.group(5), sread.group(6)))
w("")
w("### lambda_1 at D 23.0625 by k_c, and the shifts")
w("")
w("\n".join(tabs))
w("")
w("**The k_c 135 to 143 shift is %+.8f; the 127 to 135 shift was %+.8f** (ratio %.5f, difference %.1e): it did not shrink. The earlier ratios were %s. **Arithmetic only, not a result:** the same shift once more would put the root at k_c 151 at %+.5f." % (sh[-1], sh[-2], rat[-1], abs(sh[-1] - sh[-2]), ", ".join("%.4f" % r for r in rat[:-1]), rt + sh[-1]))
w("")
w("### Registrations and scoring")
w("The registration was written in `kc143_d230625/README.md` before the regrid (01:45 UTC) and its status entries score it item by item (regrid, scan, secant; `score_secant_a.py`, whose control `--mutate=root` flips the first item). **t5's root** (+0.0139 +- 0.003; the rule alone, +0.0139326): read minus 0.0139 = %+.8f, **inside**. **My root** (+0.0140 +- 0.0010, in (+0.0130, +0.0150), 65%%): **MISS**, above the upper end by %.8f (my range of shift ratios, 0.6 to 1.0, ended at the ratio read, %.4f; my interval covered 0.63 to 0.98). Regrid: %d HIT, %d MISS (the Delta shift %+.4e lies beyond the registered (-8.0e-6, -0.8e-6)). Scan: %d HIT, %d MISS (my 55%% bracket (0.010, 0.015), while the bracket read, (0.015, 0.020), was my 30%% one and counts as HIT; the float64 sign equals the hybrid sign at 2 of 6, registered at 12%%). Secant: exit 0 within 10 evaluations (55%%) HIT, per evaluation in (800, 1050) s at all five HIT (mean %.0f s), run wall 65 to 125 min (%.1f min) HIT, peak RSS below 7 GiB (%.3f GiB) HIT, root inside the scan's estimator range HIT; **MISS:** my root, and the peak RSS in (5.0, 6.5) GiB (%.3f GiB, below it). The Rust block 12 gates of #1102 ran beside evaluation 1 (04:27:02 to 04:34:25 UTC); that evaluation took %d s against a mean of %.1f s for the four after it (1.221, registered under 1.3, HIT; no control without the gate). Lowest available memory in the secant %.1f GiB."
  % (rt - 0.0139, rt - 0.0150, rat[-1], nh_reg, nm_reg, rg143["shift"], nh_sc, nm_sc, sum(e["sec"] for e in sev) / len(sev), root["sec"] / 60.0, spk, spk, sev[0]["sec"], sum(e["sec"] for e in sev[1:]) / 4.0, slow))
w("")
w("### Next")
w("D 23.125 at k_c 143 follows as ordered (`kc143_d23125/`): the regrid from my accepted k_c 135 state there, then the scan and the secant with the Rust block 12 (`--b12=rust --b12_threads=4`, accepted by t5 at 04:37 UTC on #1102; the scan runs 2 processes of 4 threads). Its second registration, written from this root, goes in first. The k_c 143 zero by the line through the two roots follows with that point. The k_c 87 chain stays held through both k_c 143 lanes (t5, hc 01:51 and 04:21 UTC).")
w("")
w("Raw: `I1025-macm3/kc143_d230625/` and `I1025-macm3/kc87_leg_lambda/23.0625_kc143/` at @@H@@.")
print("\n".join(L))
