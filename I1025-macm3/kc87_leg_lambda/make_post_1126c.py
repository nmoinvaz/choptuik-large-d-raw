#!/usr/bin/env python3
"""make_post_1126c.py > post.md : the #1025 comment of macm3 on k_c 119 at D 23.0625 and the threshold table at five k_c (t5's order, hc 26 Nov: "to give k_c 119's threshold zero today ... Post on #1025 when the secant ends."): the roots at D 23.0
and D 23.0625, the zeros by linear interpolation, the steps and ratios, the k_c 119 regrid, the scan with the NEW scanner and the secant. Every number comes from the files; tail sums are computed here and labeled arithmetic only. @@T@@ replaced by the caller."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post_1126 as p
R = p.R; txt = p.txt; parse_sec = p.parse_sec; lz = p.lz; tail = p.tail

def main():
    K = R + "kc_d23_secant/"
    A = {87: [(22.9375, parse_sec(K + "kc87b/secant_summary.txt")), (23.0, parse_sec(K + "kc87/secant_summary.txt"))],
         95: [(23.0, parse_sec(K + "kc95/secant_summary.txt")), (23.0625, parse_sec(K + "kc95L/secant_summary.txt"))],
         103: [(23.0, parse_sec(R + "kc103_d23/secant/secant_summary.txt")), (23.0625, parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"))],
         111: [(23.0, parse_sec(K + "kc111dh/secant_summary.txt")), (23.0625, parse_sec(R + "kc111_d230625/point_summary.txt"))],
         119: [(23.0, parse_sec(R + "kc119_d23/point_summary.txt")), (23.0625, parse_sec(R + "kc119_d230625/point_summary.txt"))]}
    for kc in A:
        for d, S in A[kc]: assert S is not None, (kc, d)
    P = []
    P.append("**#1025 macm3, k_c 119 at D 23.0625 and the threshold zero at five resolutions: zeros 22.97893, 23.00808, 23.03011, 23.04627, 23.0576 (@@T@@).** t5's order (hc 26 Nov): k_c 119 at D 23.0625 from my k_c 111 state there \"to give k_c 119's threshold zero today\"; t5 registered the root at -0.004 +- 0.005 and the zero near D 23.057. Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position, brackets in square brackets; the zero of each k_c is the straight line through its two roots (arithmetic on two points, not a result). **Every tail sum below is arithmetic only, not a result.**")
    P.append("### The threshold table: lambda_1 at two D per k_c, the zero in D, and the D pair each k_c uses\n")
    T = ["| k_c | D pair used | lambda_1 at the two D (secant root [final bracket]) | slope per unit D | zero in D | zero over the bracket ends |", "|---|---|---|---|---|---|"]
    zer = {}
    for kc in (87, 95, 103, 111, 119):
        (Da, Sa), (Db, Sb) = A[kc]
        z = lz(Da, Sa["root"], Db, Sb["root"]); sl = (Sb["root"] - Sa["root"]) / (Db - Da)
        zs = [lz(Da, ra, Db, rb) for ra in (Sa["lo"], Sa["hi"]) for rb in (Sb["lo"], Sb["hi"])]
        zer[kc] = z
        T.append("| %d | **%s and %s** | D %s: **%.8f** [%.8f, %.8f]; D %s: **%.8f** [%.8f, %.8f] | %+.5f | **%.5f** | %.5f to %.5f |" % (kc, Da, Db, Da, Sa["root"], Sa["lo"], Sa["hi"], Db, Sb["root"], Sb["lo"], Sb["hi"], sl, z, min(zs), max(zs)))
    P.append("\n".join(T))
    z = [zer[k] for k in (87, 95, 103, 111, 119)]; dz = [z[i + 1] - z[i] for i in range(4)]; rz = [dz[i + 1] / dz[i] for i in range(3)]
    P.append("\n**Steps of the zero in k_c:** %s (87 to 95, 95 to 103, 103 to 111, 111 to 119); ratios %s. **Arithmetic only, not a result:** a geometric tail of the last ratio would put the limit of the zero at D %.4f. t5's register for k_c 119 (zero near D 23.057): read %.5f." % (", ".join("%+.5f" % x for x in dz), ", ".join("%.4f" % x for x in rz), tail(z[4], dz[3], rz[2]), z[4]))
    r0 = [A[kc][-1][1]["root"] for kc in (95, 103, 111, 119)]; s0 = [r0[i + 1] - r0[i] for i in range(3)]
    d0 = [dict(A[kc])[23.0]["root"] for kc in (87, 95, 103, 111, 119)]; s1 = [d0[i + 1] - d0[i] for i in range(4)]
    P.append("\n**Roots at D 23.0:** %s; steps %s; ratios %s (a geometric tail of the last ratio would end at %.4f, arithmetic only). **Roots at D 23.0625:** %s for k_c 95, 103, 111, 119; steps %s; ratios %s (tail %.4f, arithmetic only). k_c 87 has no state at D 23.0625 (my part c2 ended at D 23.0 by the guard); its pair is D 22.9375 and 23.0." % (
        ", ".join("%+.8f" % x for x in d0), ", ".join("%+.6f" % x for x in s1), ", ".join("%.4f" % (s1[i + 1] / s1[i]) for i in range(3)), tail(d0[-1], s1[-1], s1[-1] / s1[-2]),
        ", ".join("%+.8f" % x for x in r0), ", ".join("%+.6f" % x for x in s0), ", ".join("%.4f" % (s0[i + 1] / s0[i]) for i in range(2)), tail(r0[-1], s0[-1], s0[-1] / s0[-2])))
    P.append("\n### k_c 119 at D 23.0625: regrid, scan with the new scanner, secant (raw `I1025-macm3/kc119_d230625/`, README with the registration first, raw efdd1c937)\n")
    P.append("Source: my accepted k_c 111 state at D 23.0625 (blob 871f58c2, record 29448608). The k_c 111 check accepted it (controls 1 1; the k_c 103 and k_c 119 checks refused it); `kc119_syscheck_1025.py` (fc6e0dd6) accepted the result (controls 1 1; the k_c 111 check refused it). `ell_refine.py` 631e5801, 6 threads, `capped_run.py` 28800 s. " + txt(R + "kc119_d230625/regrid/regrid_summary.txt").strip() + ". Wall 2663 s; peak RSS 5.62 GiB. **The scan used the new scanner** (t5's change, hc 26 Nov): `d18_secant.py scan` of wip/ell1-speed 92b9bf53, blob eb1396ad, whose selftest exits 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1 (logged in the README before the scan); my driver `kc87_leg_lambda/pointnew.sh` was tested first on the k_c 119 D 23.0 state against the old record at 0.04 (|d ln| 2.57e-5, sign equal, the repeat bit-identical, `_test_pointnew/`). Plan: lambda -0.04, -0.02, 0.00, 0.02 plus a repeat of -0.02, at most 2 processes; then `d18_secant.py run`:")
    P.append("```\n" + txt(R + "kc119_d230625/point_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 119 at D 23.0625):** " + p.noise_row(R + "kc119_d230625/secant/secant.jsonl", "k_c 119 D 23.0625").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1).")
    P.append("\n### Registrations and scoring\nThe registration was written in `kc119_d230625/README.md` before the regrid and its log entries score it (regrid, scan and secant). Nothing registered for this lane missed (the regrid, the scan and the secant are all scored there); the root was registered at -0.0027 (t5 -0.004 +- 0.005) and read at %+.5f, the zero registered near D 23.0586 (t5 23.057) and read at %.5f.\n\nChain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing of mine is running for this issue now. dh370's Linux run of the same point is the cross-check. Next (t5's order): the third D for k_c 119, D 22.875, regridded from dh610's accepted k_c 111 state there (raw `I1025-dh610/kc111_d22875`, blobs a8fe443e and 5233ffe8), the new scanner at lambda 0.10 to 0.13, then the secant; t5 registers 0.122 +- 0.006." % (A[119][1][1]["root"], zer[119]))
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
