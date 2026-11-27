#!/usr/bin/env python3
"""make_post_1127a.py > post.md : the #1025 comment of macm3 on k_c 135 at D 23.125 and the zero of k_c 135 (t5's seed rule, hc 26 Nov 20:09 UTC: a regrid from my accepted k_c 127
leg state at D 23.125, the new scanner, the secant; hc 27 Nov 01:32 UTC: "Post the point and the k_c 135 zero on #1025"). Every number comes from the files (regrid_summary.txt, the
exits and sample files of kc135_d23125 and kc135_d230625, point_summary.txt, secant.jsonl, the secant summaries of the other k_c, zero_arithmetic_135.txt's inputs, the READMEs'
scoring); tail sums are computed here and labeled arithmetic only. @@T@@ and @@H@@ are replaced by the caller. Read-only."""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kc135_d23125"))
import make_post_1126 as p
import reg_d23125 as rg
R = p.R; txt = p.txt; parse_sec = p.parse_sec; lz = p.lz; tail = p.tail
F = R + "kc135_d23125/"; F0 = R + "kc135_d230625/"; S = R + "kc87_leg_lambda/23.125_kc135/"; L = R + "kc127_leg/"


def exit_time(name, pat):
    m = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc135_d23125: " + pat, txt(F + "exits_kc135.txt"))
    assert m, pat
    return m.group(1)


def mins(a, b):
    f = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
    d = f(b) - f(a)
    return (d + 86400 if d < 0 else d) / 60.0


def main():
    K = R + "kc_d23_secant/"
    A = {87: [(22.9375, parse_sec(K + "kc87b/secant_summary.txt")), (23.0, parse_sec(K + "kc87/secant_summary.txt"))],
         95: [(23.0, parse_sec(K + "kc95/secant_summary.txt")), (23.0625, parse_sec(K + "kc95L/secant_summary.txt"))],
         103: [(23.0, parse_sec(R + "kc103_d23/secant/secant_summary.txt")), (23.0625, parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"))],
         111: [(23.0, parse_sec(K + "kc111dh/secant_summary.txt")), (23.0625, parse_sec(R + "kc111_d230625/point_summary.txt"))],
         119: [(23.0, parse_sec(R + "kc119_d23/point_summary.txt")), (23.0625, parse_sec(R + "kc119_d230625/point_summary.txt"))],
         127: [(23.0625, parse_sec(R + "kc127_d230625/point_summary.txt")), (23.125, parse_sec(L + "point_D23.125_summary.txt"))],
         135: [(23.0625, parse_sec(F0 + "point_summary.txt")), (23.125, parse_sec(F + "point_summary.txt"))]}
    for kc in A:
        for d, X in A[kc]:
            assert X is not None, (kc, d)
    S135a = A[135][0][1]; S135b = A[135][1][1]; S127a = A[127][0][1]; S127b = A[127][1][1]
    W = re.search(r"root bracket \[\S+, \S+\], width (\S+), signs", txt(F + "point_summary.txt")).group(1)
    regs = {"23.0625": rg.regrid("kc135_d230625", "exits_kc135.txt"), "23.125": rg.regrid("kc135_d23125", "exits_kc135.txt")}
    rec = [json.loads(l) for l in open(F + "in/l1kc135macm3d23125.jsonl") if l.strip()][-1]
    src = [json.loads(l) for l in open(F + "in/l1kc127Lmacm3.jsonl") if l.strip() and json.loads(l)["D"] == 23.125][-1]
    sm = list(csv.DictReader(open(S + "scan/scan_samples.csv"))); pk = {}
    for s in sm:
        if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
    sc = [json.loads(l) for l in open(S + "scan/scan_D23.125_1025.jsonl")]
    se = [json.loads(l) for l in open(F + "secant/secant.jsonl") if l.strip()]; sev = [e for e in se if e.get("kind") == "eval"]
    ss = list(csv.DictReader(open(F + "secant/samples.csv")))
    t_reg0, t_reg1 = exit_time("regrid", "regrid starts"), exit_time("regrid", "regrid exit 0")
    t_sc0, t_sc1 = exit_time("scan", r"scan starts"), exit_time("scan", "scan exit 0")
    t_se0, t_se1 = exit_time("secant", "secant starts"), exit_time("secant", "secant exit 0")
    zr = open(F + "zero_arithmetic_135.txt").read()
    # the zeros by the line through two roots, per k_c
    zer = {}; slp = {}; T = ["| k_c | D pair used | lambda_1 at the two D (secant root [final bracket]) | slope per unit D | zero in D | zero over the bracket ends |", "|---|---|---|---|---|---|"]
    for kc in (87, 95, 103, 111, 119, 127, 135):
        (Da, Sa), (Db, Sb) = A[kc]
        z = lz(Da, Sa["root"], Db, Sb["root"]); sl = (Sb["root"] - Sa["root"]) / (Db - Da)
        zs = [lz(Da, ra, Db, rb) for ra in (Sa["lo"], Sa["hi"]) for rb in (Sb["lo"], Sb["hi"])]
        zer[kc] = z; slp[kc] = sl
        T.append("| %d | **%s and %s** | D %s: **%+.8f** [%.8f, %.8f]; D %s: **%+.8f** [%.8f, %.8f] | %+.5f | **%.5f** | %.5f to %.5f |" % (kc, Da, Db, Da, Sa["root"], Sa["lo"], Sa["hi"], Db, Sb["root"], Sb["lo"], Sb["hi"], sl, z, min(zs), max(zs)))
    ks = (87, 95, 103, 111, 119, 127, 135)
    z = [zer[k] for k in ks]; dz = [z[i + 1] - z[i] for i in range(6)]; rz = [dz[i + 1] / dz[i] for i in range(5)]
    sh0 = S135a["root"] - S127a["root"]; sh1 = S135b["root"] - S127b["root"]
    c = S135a["root"] - 0.70 * 0.0625; h = 0.03 * 0.0625; lo_r, hi_r = c - h, c + h
    rule = S127b["root"] + sh0
    assert S135b["root"] < lo_r and abs((S135b["root"] - lo_r) + 6.35e-05) < 1e-6
    P = []
    P.append("**#1025 macm3, k_c 135 at D 23.125: lambda_1 = %+.8f, bracket [%.8f, %.8f], width %s, both ends robust; the zero of k_c 135 at D %.5f, %+.5f beyond the k_c 127 zero (@@T@@).** t5's order (hc 26 Nov 20:09 UTC, the seed rule): D 23.125 at k_c 135 as at D 23.0625, a regrid from my accepted k_c 127 leg state there (state blob e1dccb3c, record 58d3b080), `ell_refine.py l1kc127Lmacm3 127 l1kc135macm3d23125 135 1 23.125 2.0987860107 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, the kc135 check, the new scanner at lambda -0.045 to -0.025 plus a repeat of -0.035 (2 processes) and the secant (tol 1e-5, `d18_secant.py run --maxev=10`, one process, `venv-macm3-1058b`). t5's rulings: the scan's one robust change accepted as the bracket (hc 26 Nov 22:56 UTC), the point accepted (hc 27 Nov 01:32 UTC). Roots are the det-linear root inside the final bracket, read by position. **Every tail sum below is arithmetic only, not a result.**" % (S135b["root"], S135b["lo"], S135b["hi"], W, z[6], dz[5]))
    P.append("### The regrid (raw `I1025-macm3/kc135_d23125/`, README with the two registration entries first)\n")
    t = ["| k_c 135 at | wall (s) | peak RSS (GiB, 60 s samples) | steps | steps ratio | constraint ratio | Delta shift |", "|---|---|---|---|---|---|---|"]
    for d in ("23.0625", "23.125"):
        v = regs[d]; t.append(f"| D {d} | {v['wall']} | {v['rss']:.3f} | {v['steps']} | {v['sr']:.3f} | {v['cr']:.3f} | {v['shift']:+.4e} |")
    P.append("\n".join(t))
    P.append(f"\nThe D 23.125 regrid ran {t_reg0} to {t_reg1} UTC on 26 Nov (exit 0, `capped_run` wall {regs['23.125']['wall']} s, 6 threads, nice 10). Acceptance (22:07:25 UTC): the kc135 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc127 check refuses the result. Record (blob f22d1e21; state ac01e477): |F| {rec['F']:.4e} (source {src['F']:.4e}), steps {rec['steps']} (source {src['steps']}), psi-constraint {rec['constraint']:.4e} (source {src['constraint']:.4e}), Delta {rec['Delta']:.12f} (source {src['Delta']:.12f}). No traceback; lowest available memory {min(float(r['avail_GiB']) for r in csv.DictReader(open(F + 'regrid/regrid_samples.csv')) if r['avail_GiB']):.1f} GiB. The lane's hc line printed `regrid wall 3585 s`; that is the time to the hc line (it includes the checks and the push), the wall is {regs['23.125']['wall']} s.")
    P.append("### The scan (new scanner `d18_secant.py scan`, eb1396ad of wip/ell1-speed 92b9bf53) and the secant\n")
    P.append(f"Scan {t_sc0} to {t_sc1} UTC ({mins(t_sc0, t_sc1):.1f} min, 2 processes, {min(x['sec'] for x in sc)} to {max(x['sec'] for x in sc)} s per evaluation, peak RSS {max(pk.values())/1048576:.2f} GiB per process); secant {t_se0} to {t_se1} UTC (26 to 27 Nov), **exit 0** (tol):")
    P.append("```\n" + txt(F + "point_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 135 at D 23.125):** " + p.noise_row(F + "secant/secant.jsonl", "k_c 135 D 23.125").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The secant ended on tol with all six evaluations robust, as the k_c 127 secant at D 23.125 did; the D 23.0625 secant of k_c 135 stopped on a non-robust point (exit 4).")
    P.append("### lambda_1 at k_c 127 and 135, D 23.0625 and 23.125, and the zero of k_c 135\n")
    P.append("| k_c | D 23.0625 (secant root [final bracket]) | D 23.125 (secant root [final bracket]) | slope per unit D | zero in D |\n|---|---|---|---|---|\n" + "\n".join(
        "| %d | **%+.8f** [%.8f, %.8f] | **%+.8f** [%.8f, %.8f] | %+.5f | **%.5f** |" % (kc, a['root'], a['lo'], a['hi'], b['root'], b['lo'], b['hi'], slp[kc], zer[kc]) for kc, a, b in ((127, S127a, S127b), (135, S135a, S135b))))
    P.append(f"\nThe shift of the root from k_c 127 to k_c 135 is **{sh0:+.6f}** at D 23.0625 and **{sh1:+.6f}** at D 23.125 (a growth factor {sh1/sh0:.3f}; the shifts between k_c 95 and 119 grew by 1.63 to 1.77 from D 23.0 to 23.0625, and this one fell). The slope of the root in D over D 23.0625 to 23.125 is {slp[135]:+.5f} at k_c 135 and {slp[127]:+.5f} at k_c 127: its size rose by {abs(slp[135])-abs(slp[127]):.5f}. The zero by the line through the two roots, over the four bracket-end combinations ({min(lz(23.0625, x, 23.125, y) for x in (S135a['lo'], S135a['hi']) for y in (S135b['lo'], S135b['hi'])):.5f} to {max(lz(23.0625, x, 23.125, y) for x in (S135a['lo'], S135a['hi']) for y in (S135b['lo'], S135b['hi'])):.5f}), is **D {z[6]:.5f}**; the k_c 127 zero by the same pair of D is {z[5]:.5f}. The arithmetic is `kc135_d23125/zero_arithmetic_135.txt` (script `zero135.py`; its `--mutate=sign` control exits 1).")
    P.append("### The threshold table at seven k_c\n")
    P.append("\n".join(T))
    P.append("\n**Steps of the zero in k_c:** %s (87 to 95, 95 to 103, 103 to 111, 111 to 119, 119 to 127, 127 to 135); ratios %s. **Arithmetic only, not a result:** a geometric tail of the last ratio (%.4f) would put the limit of the zero at D %.4f (the previous ratio, %.4f, at D %.4f). The zeros of k_c 127 and 135 are lines through roots 0.0625 apart in D at the **same pair** (D 23.0625 and 23.125), so their step %+.5f is like for like; the zeros of k_c 87 to 119 are lines through the pairs D 22.9375 and 23.0 (k_c 87) or D 23.0 and 23.0625, and the k_c 119 quadratic through its three D gives 23.05777, so the step 119 to 127 mixes pairs (with the quadratic the last two steps are %+.5f and %+.5f, arithmetic only). **The zeros of k_c 127 and k_c 135 are not yet bracketed by a third D:** winb's D 23.0 secant of k_c 127 (`I1025-win/kc127_d23`, scan det-linear 0.048098, secant started 19:50:17 UTC) and win2's D 23.0 secant of k_c 135 (`I1025-win2/kc135_d23`, scan det-linear 0.049763, the latest commit: the first interior point 0.049763 is -, bracket (0.045, 0.049763)) were not finished in the raw repository at my fetch (@@F@@); with their roots the three-point (quadratic) zeros follow." % (
        ", ".join("%+.5f" % x for x in dz), ", ".join("%.4f" % x for x in rz), rz[4], tail(z[6], dz[5], rz[4]), rz[3], tail(z[6], dz[5], rz[3]), dz[5], z[5] - 23.05777, z[6] - z[5]))
    P.append(f"\nD-slopes of lambda_1 (per unit D, over each k_c's pair): {', '.join('%d %+.4f' % (k, slp[k]) for k in ks)}.")
    P.append("### Registrations and scoring\nThe registration was written in `kc135_d23125/README.md` before the regrid (first entry 20:13 UTC, second entry 21:07 UTC, from the D 23.0625 secant's final root) and its status entries score it item by item (regrid, scan and secant; `zero_arithmetic_135.txt`). **Met:** the regrid accepted; no exception or array limit; Delta shift in (-7.0e-6, -1.0e-6) (%+.4e); steps ratio in (1.055, 1.072) (%.4f), steps within 25 of 4445 (%d); constraint in (1.0e-3, 1.25e-3) (%.4e) and below 1e-2; |F| below 5e-10; peak RSS below 9 GiB (%.3f GiB); no memory alert; exactly one robust change in (-0.045, -0.025) (90%%), its bracket (-0.040, -0.035) (33%%); all 6 evaluations noise-robust; the repeat of -0.035 bit-identical; per evaluation %d to %d s in (700, 1050); scan wall 38 to 52 min (%.1f); scan peak RSS per process below 6 GiB (%.3f GiB); **the zero of k_c 135 in (23.0745, 23.0770) (65%%; read %.5f)**. **Misses:** regrid wall 3800 to 4700 s (65%%; %d s); regrid peak RSS in (7.0, 8.0) GiB (70%%; %.3f GiB); the float64 sign equal to the hybrid sign at all 6 (15%%; at 2 of 6); scan peak RSS per process in (5.0, 5.3) GiB (65%%; %.3f GiB); the bracket (-0.035, -0.030) (50%%; the read bracket is the 33%% one); **the root in (%.5f, %.5f) (60%%; read %+.8f, below the lower end by %.2e, t5 confirmed)**; the slope magnitude below k_c 127's %.4f (75%%; %.5f). **t5's root** (the rule alone, %+.6f; he quotes -0.0362): read minus it %+.6f (minus -0.0362: %+.6f). **Recorded, not registered:** the secant's evaluations took %d to %d s (mean %.0f s) against 714 to 717 s at D 23.0625, and its wall %s s against 3573 s, while the k_c 87 chain (HOLD_low2 released %s UTC on t5's order, 4-process scans at nice 20) ran beside it: its scans of D 21.4375, 21.84375, 21.90625, 21.96875, 22.03125 and 22.0625 finished at 23:20, 23:43, 00:05, 00:28, 00:50 and 01:13 UTC; the chain is the one difference I know of and the slowdown is not isolated (no control run). The secant's peak RSS was %.2f GiB and the lowest available memory %.1f GiB; no memory alert." % (
        regs["23.125"]["shift"], regs["23.125"]["sr"], regs["23.125"]["steps"], rec["constraint"], regs["23.125"]["rss"], min(x["sec"] for x in sc), max(x["sec"] for x in sc), mins(t_sc0, t_sc1), max(pk.values()) / 1048576, z[6], regs["23.125"]["wall"], regs["23.125"]["rss"], max(pk.values()) / 1048576,
        lo_r, hi_r, S135b["root"], lo_r - S135b["root"], abs(slp[127]), abs(slp[135]), rule, S135b["root"] - rule, S135b["root"] + 0.0362,
        min(e["sec"] for e in sev), max(e["sec"] for e in sev), sum(e["sec"] for e in sev) / len(sev), S135b["wall"], "22:57:09", max(int(r["rss_kB"]) for r in ss if r["rss_kB"]) / 1048576, min(float(r["avail_GiB"]) for r in ss if r["avail_GiB"])))
    P.append("### Next\nNo further step is registered in `kc135_d23125/README.md`. The quadratic zeros wait for winb's D 23.0 root of k_c 127 and win2's D 23.0 root of k_c 135. The k_c 87 chain (pid 99672) runs on its own (HOLD_low2 released); nothing else of mine runs for this issue. Next: t5's order.")
    P.append("\nRaw: `I1025-macm3/kc135_d23125/` and `I1025-macm3/kc87_leg_lambda/23.125_kc135/` at @@H@@.")
    print("\n\n".join(P))


if __name__ == "__main__":
    main()
