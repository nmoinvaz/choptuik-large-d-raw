#!/usr/bin/env python3
"""make_post_1126g.py > post.md : the #1025 comment of macm3 on k_c 135 at D 23.0625 (t5's order, hc 26 Nov 18:08 UTC: regrid from my accepted k_c 127 state there, the new scanner, the secant on the robust
bracket, tol 1e-5; ruling 21:06 UTC: the robust bracket of the non-robust secant stands; "Post the point on #1025 with the bracket"). Every number comes from the files (regrid_summary.txt of the four lanes,
the exits and sample files, point_summary.txt, secant.jsonl, the READMEs' scoring); tail sums are computed here and labeled arithmetic only. @@T@@ and @@H@@ are replaced by the caller. Read-only."""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kc135_d23125"))
import make_post_1126 as p
import reg_d23125 as rg
R = p.R; txt = p.txt; parse_sec = p.parse_sec; lz = p.lz
F = R + "kc135_d230625/"; S = R + "kc87_leg_lambda/23.0625_kc135/"

def main():
    K = R + "kc_d23_secant/"
    roots = {95: parse_sec(K + "kc95L/secant_summary.txt"), 103: parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"), 111: parse_sec(R + "kc111_d230625/point_summary.txt"),
             119: parse_sec(R + "kc119_d230625/point_summary.txt"), 127: parse_sec(R + "kc127_d230625/point_summary.txt"), 135: parse_sec(F + "point_summary.txt")}
    for k, v in roots.items(): assert v is not None, k
    r = {k: v["root"] for k, v in roots.items()}; ks = (95, 103, 111, 119, 127, 135)
    st = [r[ks[i + 1]] - r[ks[i]] for i in range(5)]; ra = [st[i + 1] / st[i] for i in range(4)]
    S135 = roots[135]
    W135 = re.search(r"root bracket \[\S+, \S+\], width (\S+), signs", txt(F + "point_summary.txt")).group(1)
    SL127 = re.search(r"slope per unit D: (\S+)", txt(R + "kc127_leg/zero_arithmetic_127.txt")).group(1)
    regs = {k: rg.regrid(f, e) for k, f, e in ((111, "kc111_d230625", "exits_kc111.txt"), (119, "kc119_d230625", "exits_kc119b.txt"), (127, "kc127_d230625", "exits_kc127.txt"), (135, "kc135_d230625", "exits_kc135.txt"))}
    rec = [json.loads(l) for l in open(F + "in/l1kc135macm3d230625.jsonl") if l.strip()][-1]
    src = [json.loads(l) for l in open(F + "in/l1kc127macm3d230625.jsonl") if l.strip() and json.loads(l)["D"] == 23.0625][-1]
    sm = list(csv.DictReader(open(S + "scan/scan_samples.csv"))); pk = {}
    for s in sm:
        if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
    sc = [json.loads(l) for l in open(S + "scan/scan_D23.0625_1025.jsonl")]
    P = []
    P.append(f"**#1025 macm3, k_c 135 at D 23.0625: lambda_1 = {S135['root']:+.8f}, robust bracket [{S135['lo']:.8f}, {S135['hi']:.8f}], width {W135}; both registered predictions met; the secant stopped on a non-robust interior point, so the bracket stands (@@T@@).** t5's order (hc 26 Nov 18:08 UTC): k_c 135 at D 23.0625 from my accepted k_c 127 state there (state blob 7aae10c6, record 85a685f1), `ell_refine.py l1kc127macm3d230625 127 l1kc135macm3d230625 135 1 23.0625 2.0990016035 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`; the kc135 check (`kc135_syscheck_1025.py` b353d466; exit 0, controls 1 1, the kc127 check refuses); the new scanner at lambda 0.000, 0.005, 0.010, 0.015 plus a repeat of 0.010 (2 processes); the secant, tol 1e-5. t5's ruling (hc 21:06 UTC): the robust bracket stands (exit 4). Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position. **Every tail sum below is arithmetic only, not a result.**")
    P.append("### The regrid (raw `I1025-macm3/kc135_d230625/`, README with the registration first)\n")
    t = ["| lane | wall (s) | peak RSS (GiB, 60 s samples) | steps | steps ratio | constraint ratio | Delta shift |", "|---|---|---|---|---|---|---|"]
    for k in (111, 119, 127, 135):
        v = regs[k]; t.append(f"| k_c {k} | {v['wall']} | {v['rss']:.3f} | {v['steps']} | {v['sr']:.3f} | {v['cr']:.3f} | {v['shift']:+.4e} |")
    P.append("\n".join(t))
    P.append(f"\nThe k_c 135 regrid ran 18:13:22 to 19:22:06 UTC (exit 0, `capped_run` wall 4124 s, 6 threads, nice 10). Acceptance (19:22:12 UTC): the kc135 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc127 check refuses the result. Record: |F| {rec['F']:.4e} (source {src['F']:.4e}), steps {rec['steps']} (source {src['steps']}), psi-constraint {rec['constraint']:.4e} (source {src['constraint']:.4e}), Delta {rec['Delta']:.12f}. No traceback; lowest available memory 11.3 GiB. The lane's hc line printed `regrid wall 4135 s`; that is the time to the hc line (it includes the checks and the push), the wall is 4124 s.")
    P.append("### The scan (new scanner `d18_secant.py scan`, eb1396ad of wip/ell1-speed 92b9bf53) and the secant\n")
    P.append(f"Scan 19:22:22 to 20:06:36 UTC (44.2 min, 2 processes, {min(x['sec'] for x in sc)} to {max(x['sec'] for x in sc)} s per evaluation, peak RSS {max(pk.values())/1048576:.2f} GiB per process); secant 20:06:50 to 21:06:33 UTC, **exit 4** (non-robust interior point):\n")
    P.append("```\n" + txt(F + "point_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 135 at D 23.0625):** " + p.noise_row(F + "secant/secant.jsonl", "k_c 135 D 23.0625").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The non-robust point is the det-linear root itself (dln 0.111 against the bar 0.1), so its distance from the root is 0 and the row's constant reads the bracket ends; the k_c 127 row at D 23.0625 was 1.1e-08 to 1.2e-08. The two ends of the robust bracket are robust (dln 3.2e-03 and 1.5e-04).")
    P.append("### lambda_1 at D 23.0625 by k_c, and the step of the root\n")
    T = ["| k_c | lambda_1 at D 23.0625 (secant root [final bracket]) | step from the previous k_c | ratio of the steps |", "|---|---|---|---|"]
    for i, k in enumerate(ks):
        T.append(f"| {k} | **{r[k]:+.8f}** [{roots[k]['lo']:.8f}, {roots[k]['hi']:.8f}] | " + (f"{st[i-1]:+.6f}" if i else "") + " | " + (f"{ra[i-2]:.4f}" if i >= 2 else "") + " |")
    P.append("\n".join(T))
    P.append(f"\nThe k_c 135 root exceeds the k_c 127 root by **{st[4]:+.6f}**; the ratios of the steps are {', '.join('%.4f' % x for x in ra)} (the last two, {ra[2]:.4f} and {ra[3]:.4f}, are nearly equal; my register took ratios 0.5 to 0.9, which give +0.0072 to +0.0101, and the read ratio is inside). The k_c 135 zero in D by the k_c 127 slope ({SL127} per unit D, the pair 23.0625 to 23.125) is {23.0625 + r[135] / -float(SL127):.5f} (**arithmetic only, not a result**); the zero by two k_c 135 roots waits for the D 23.125 point, whose lane started 21:07:46 UTC.")
    P.append("### Registrations and scoring\nThe registration was written in `kc135_d230625/README.md` before the regrid (18:12 UTC) and its status entries score it item by item (regrid, scan and secant). **Predictions on the final bracket's det-linear root " + f"{S135['root']:+.8f}" + ":** t5's +0.008 +- 0.004 **met** (difference " + f"{S135['root'] - 0.008:+.6f}" + "); mine +0.0087 +- 0.003 **met** (difference " + f"{S135['root'] - 0.0087:+.6f}" + "). **Met:** the regrid accepted; no exception or array limit; steps within 15 of 4443 (4442); constraint in (0.8e-3, 1.4e-3) and below 1e-2; |F| below 5e-10; peak RSS below 12 GiB; no memory alert; exactly one robust change (90%), its bracket (0.005, 0.010) (60%); all 5 evaluations noise-robust; the repeat of 0.010 bit-identical; scan wall 35 to 55 min (44.2); scan peak RSS below 7 GiB; the secant's root inside the scan's estimator range; per evaluation 650 to 800 s (714 to 717 s); peak RSS below 7 GiB (5.62 GiB). **Misses:** the regrid's Delta shift in (-3.0e-6, -1.0e-6) (60%; -3.7646e-6); regrid wall 2900 to 3800 s (70%; 4124 s); regrid peak RSS in (8.5, 11) GiB and above k_c 127's 7.51 GiB (70% and 90%; 7.423 GiB); the float64 sign equal to the hybrid sign at all 5 (50%; 3 of 5, it is -1 everywhere and the hybrid sign is needed at 0.000 and 0.005); scan seconds per evaluation 700 to 950 (65%; 711 to 970); scan peak RSS per process in (5.3, 6.8) GiB (65%; 5.13 GiB); the secant exit 0 within 10 evaluations (55%; exit 4 after 5, the registered 40% outcome); the secant wall 75 to 120 min (60%; 59.5 min).")
    P.append("### Next\nt5's seed rule (hc 20:09 UTC): D 23.125 at k_c 135 by a regrid from my accepted k_c 127 leg state there (blob e1dccb3c, record 58d3b080), with the scan and the secant, in `kc135_d23125/` (README with the registration first, raw ea00c37f2, second entry e820fafbb). Registered there before the regrid: the scan at lambda -0.045 to -0.025 by 0.005 plus a repeat of -0.035, and the root at D 23.125 as 0.00939087 minus 0.0625 times a slope magnitude of 0.70 +- 0.03, i.e. -0.034359 +- 0.001875 (t5's rule alone: -0.036159); the zero of k_c 135 by the line through its two roots then, and with win2's D 23.0 later by the quadratic. The regrid started 21:07:46 UTC. HOLD_low2 stays held; I release it when that scan ends and only its secant runs (t5's order of 20:35 UTC).")
    P.append("\nRaw: `I1025-macm3/kc135_d230625/` and `I1025-macm3/kc87_leg_lambda/23.0625_kc135/` at @@H@@.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
