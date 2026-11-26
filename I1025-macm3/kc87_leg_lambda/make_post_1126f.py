#!/usr/bin/env python3
"""make_post_1126f.py > post.md : the #1025 comment of macm3 on the k_c 127 leg step to D 23.125 (t5's order, hc 26 Nov: one leg step from the D 23.0625 state, the guard,
the new scanner, the secant on the robust bracket; "Post on #1025 when the secant ends"): the leap row and the guard, the acceptance, the scan, the secant, lambda_1(23.125),
the zero of k_c 127, the threshold table at six k_c with steps and ratios, the noise row, the scoring. Every number comes from the files; tail sums are computed here and
labeled arithmetic only. @@T@@ replaced by the caller. Read-only."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post_1126 as p
R = p.R; txt = p.txt; parse_sec = p.parse_sec; lz = p.lz; tail = p.tail
L = R + "kc127_leg/"

def main():
    K = R + "kc_d23_secant/"
    A = {87: [(22.9375, parse_sec(K + "kc87b/secant_summary.txt")), (23.0, parse_sec(K + "kc87/secant_summary.txt"))],
         95: [(23.0, parse_sec(K + "kc95/secant_summary.txt")), (23.0625, parse_sec(K + "kc95L/secant_summary.txt"))],
         103: [(23.0, parse_sec(R + "kc103_d23/secant/secant_summary.txt")), (23.0625, parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"))],
         111: [(23.0, parse_sec(K + "kc111dh/secant_summary.txt")), (23.0625, parse_sec(R + "kc111_d230625/point_summary.txt"))],
         119: [(23.0, parse_sec(R + "kc119_d23/point_summary.txt")), (23.0625, parse_sec(R + "kc119_d230625/point_summary.txt"))],
         127: [(23.0625, parse_sec(R + "kc127_d230625/point_summary.txt")), (23.125, parse_sec(L + "point_D23.125_summary.txt"))]}
    for kc in A:
        for d, S in A[kc]:
            assert S is not None, (kc, d)
    row = [json.loads(l) for l in open(L + "leap.log") if l.startswith("{") and '"D": 23.125' in l][0]
    S125 = A[127][1][1]; S0625 = A[127][0][1]
    S119_22875 = parse_sec(R + "kc119_d22875/point_summary.txt")
    assert S119_22875 is not None
    P = []
    P.append("**#1025 macm3, k_c 127 leg step to D 23.125: the guard did not fire; lambda_1(23.125) = %+.8f, bracket 5e-6; the zero of k_c 127 at D 23.0675 (@@T@@).** t5's order (hc 26 Nov): one leap step of k_c 127 from two seeds (winb's accepted D 23.0 state, blob 7a1b150c, record eea03461, and my D 23.0625 state, blobs 7aae10c6 and 85a685f1) to D 23.125 at h 0.0625 with `ell_leap.py` and `leap_guard.py` (stop at max cos_t_reg >= 0.5); the kc127 check on the new state; the new scanner at lambda -0.06 to -0.02 plus a repeat of -0.04 (2 processes); the secant on the robust bracket, tol 1e-5; \"Post on #1025 when the secant ends.\" t5 registered lambda_1(23.125) = -0.040 +- 0.010 (zero near D 23.068); I registered -0.039 +- 0.006. **Both are met.** Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position. **Every tail sum below is arithmetic only, not a result.**" % S125["root"])
    P.append("### The leap (raw `I1025-macm3/kc127_leg/`, README with the registration first)\n")
    P.append("`ell_leap.py l1kc127Lmacm3 1 127 <seed A> 23.0 <seed B> 23.0625 23.125 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold`, 6 threads, `capped_run.py` 43200 s. Both seeds were first accepted on this machine (the k_c 127 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the k_c 119 and k_c 111 checks refuse them). Leap 15:30:44 to 16:17:15 UTC, exit 0, wall 2753 s, no halving, no memory alert, leap peak RSS 6.22 GiB, lowest available memory 12.1 GiB. **The guard did not fire** (no `leg_STOP.txt`).\n")
    P.append("| D | Delta | dDelta/dD | \\|F\\| | steps | psi-constraint | n_null | point seconds | max cos_t_reg |\n|---|---|---|---|---|---|---|---|---|\n| 23.125 | %.12f | %+.6f | %.3e | %d | %.3e | %d | %d | %.4f |" % (row["Delta"], (row["Delta"] - 1.176171291295) / 0.0625, row["F"], row["steps"], row["constraint"], row["n_null"], row["seconds"], max(row["cos_t_reg"])))
    P.append("\nThe table's dDelta/dD is the difference quotient from the D 23.0625 record (Delta 1.176171291295); the guard's own slope (`leg_points.txt`) is %s. Weak regular values %s with tangent cosines %s (delta_reg %s). The largest cosine, %.4f, is on the **fourth** regular mode and below the bar 0.5; the k_c 87, 95 and 103 legs fired at 0.5096, 0.5997 and 0.5776 on the third, as lambda_1 neared its zero. This leg crosses the k_c 127 zero (D 23.0675) and does not fire, with the third cosine at %.4f." % (
        open(L + "leg_points.txt").read().strip().splitlines()[-1].split("|")[3].strip(), ", ".join("%.4e" % x for x in row["sv_reg_small"]), ", ".join("%.4f" % x for x in row["cos_t_reg"]), ", ".join("%.4f" % x for x in row["delta_reg"]), max(row["cos_t_reg"]), row["cos_t_reg"][2]))
    P.append("\nAcceptance (16:17:42 UTC): `kc127_syscheck_1025.py` exit 0 (state |F| 2.9774808995e-10 equal to the record's, `freeze_from` 4182 steps equal to the record's), controls exit 1 1, the k_c 119 and k_c 111 checks refuse the state. Raw 9a6827edf: state blob e1dccb3c, record blob 58d3b080.")
    P.append("\n### The scan and the secant at D 23.125 (new scanner `d18_secant.py scan`, eb1396ad of wip/ell1-speed 92b9bf53)\n")
    P.append("Scan 16:17:47 to 16:56:11 UTC (38.4 min, 2 processes, 754 to 777 s per evaluation, peak RSS 4.97 GiB per process); secant 16:56:18 to 18:04:12 UTC, exit 0:\n")
    P.append("```\n" + txt(L + "point_D23.125_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 127 at D 23.125):** " + p.noise_row(L + "secant_D23.125/secant.jsonl", "k_c 127 D 23.125").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). This is the first of my k_c 127 secants that ended on tol (D 23.0625 stopped on a non-robust point): its seven evaluations are all robust and the bracket ends lie 1.1e-6 and 3.9e-6 from the root.")
    P.append("\n### The zero of k_c 127 and the threshold table at six k_c\n")
    T = ["| k_c | D pair used | lambda_1 at the two D (secant root [final bracket]) | slope per unit D | zero in D | zero over the bracket ends |", "|---|---|---|---|---|---|"]
    zer = {}; slp = {}
    for kc in (87, 95, 103, 111, 119, 127):
        (Da, Sa), (Db, Sb) = A[kc]
        z = lz(Da, Sa["root"], Db, Sb["root"]); sl = (Sb["root"] - Sa["root"]) / (Db - Da)
        zs = [lz(Da, ra, Db, rb) for ra in (Sa["lo"], Sa["hi"]) for rb in (Sb["lo"], Sb["hi"])]
        zer[kc] = z; slp[kc] = sl
        T.append("| %d | **%s and %s** | D %s: **%+.8f** [%.8f, %.8f]; D %s: **%+.8f** [%.8f, %.8f] | %+.5f | **%.5f** | %.5f to %.5f |" % (kc, Da, Db, Da, Sa["root"], Sa["lo"], Sa["hi"], Db, Sb["root"], Sb["lo"], Sb["hi"], sl, z, min(zs), max(zs)))
    P.append("\n".join(T))
    ks = (87, 95, 103, 111, 119, 127)
    z = [zer[k] for k in ks]; dz = [z[i + 1] - z[i] for i in range(5)]; rz = [dz[i + 1] / dz[i] for i in range(4)]
    P.append("\n**Steps of the zero in k_c:** %s (87 to 95, 95 to 103, 103 to 111, 111 to 119, 119 to 127); ratios %s. **Arithmetic only, not a result:** a geometric tail of the last ratio would put the limit of the zero at D %.4f (the previous ratio would put it at D %.4f). The zero of k_c 127 is the line through two roots 0.0625 apart in D, with the zero 0.005 from the nearer one; the k_c 119 zero is the line through D 23.0 and 23.0625 (the quadratic through its three D gives 23.05777, +0.00020), so the last ratio moves to %.4f if the quadratic is used for k_c 119 (arithmetic only). **The k_c 127 zero is not yet bracketed by a third D:** winb's D 23.0 scan and secant of k_c 127 were not in the raw repository at my fetch (@@F@@); with that root the three-point (quadratic) zero follows." % (
        ", ".join("%+.5f" % x for x in dz), ", ".join("%.4f" % x for x in rz), tail(z[5], dz[4], rz[3]), tail(z[5], dz[4], rz[2]), (z[5] - 23.05777) / (23.05777 - z[3])))
    P.append("\nD-slopes of lambda_1 (per unit D, over each k_c's pair): %s. The pairs are not at one D: k_c 119's own slope grows in size with D (%+.5f over D 22.875 to 23.0, %+.5f over 23.0 to 23.0625), so the k_c 127 value, over the higher pair D 23.0625 to 23.125, is not comparable with the earlier ones; winb's D 23.0 root of k_c 127 will give its slope over 23.0 to 23.0625. My register compared slopes at different D; that is the miss in the scoring below." % (", ".join("%d %+.4f" % (k, slp[k]) for k in ks), (A[119][0][1]["root"] - S119_22875["root"]) / (23.0 - 22.875), slp[119]))
    P.append("\n### Registrations and scoring\nThe registration was written in `kc127_leg/README.md` before the leap (15:29 UTC) and its status entries score it item by item; the zero arithmetic is `zero_arithmetic_127.txt` (script `zero127.py`; its `--mutate=sign` control exits 1). **Misses:** the guard fired (registered 65%%; it did not: max cos_t_reg 0.2860); n_null exactly 119 (50%%; 122, within 3 yes); max cos_t_reg in (0.3, 0.75) (80%%; 0.2860, just below); the leap's point wall 2500 to 6000 s (65%%; 2373 s, just below); the D-slope of lambda_1 (registered -0.65 to -0.72, read %+.4f). **Met:** the leap converged without halving; Delta in [1.17801, 1.17804]; constraint in (1.6e-3, 1.85e-3); steps within 10 of 4181; |F| below 5e-10; peak RSS below 10 GiB and no memory alert; exactly one robust change, in (-0.050, -0.040) (35%%); all 6 evaluations robust; the repeat bit-identical; the float64 sign equal to the hybrid sign at 6 of 6 (45%%); scan wall 35 to 60 min; the root within 0.006 of -0.039 (read %+.6f, difference %+.6f) and in t5's band; the secant exit 0 within 10 evaluations (55%%; 7 evaluations); its root inside the scan's estimator range; per evaluation 9 to 14 min (581 s); wall 55 to 110 min (4066 s); peak RSS below 7 GiB (4.22 GiB); the zero in 23.066 to 23.070 (read %.5f; t5's 23.068 differs by %+.5f)." % (slp[127], S125["root"], S125["root"] + 0.039, zer[127], zer[127] - 23.068))
    P.append("\nRaw: `I1025-macm3/kc127_leg/` and `I1025-macm3/kc87_leg_lambda/23.125_kc127/` at @@H@@. Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing of mine runs for this issue now. Next: t5's order.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
