#!/usr/bin/env python3
"""make_post_1126e.py > post.md : the #1025 comment of macm3 on k_c 127 at D 23.0625 (t5's order, hc 26 Nov: "Post it on #1025."; t5's ruling: exit 4 with a non-robust interior point stands as the robust bracket): the roots at D 23.0625 for
k_c 95 to 127, the k_c 127 regrid, scan with the new scanner and secant, the noise row. Every number comes from the files; tail sums are computed here, labeled arithmetic only. @@T@@ replaced by the caller."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post_1126 as p
R = p.R; txt = p.txt; parse_sec = p.parse_sec; tail = p.tail

def main():
    K = R + "kc_d23_secant/"
    S = {95: parse_sec(K + "kc95L/secant_summary.txt"), 103: parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"), 111: parse_sec(R + "kc111_d230625/point_summary.txt"),
         119: parse_sec(R + "kc119_d230625/point_summary.txt"), 127: parse_sec(R + "kc127_d230625/point_summary.txt")}
    P = []
    P.append("**#1025 macm3, k_c 127 at D 23.0625 (the sixth resolution): lambda_1 = +0.00364182, robust bracket [0.00323094, 0.00364870]; regrid, scan with the new scanner, secant (@@T@@).** t5's order (hc 26 Nov): \"Post it on #1025.\" t5's ruling: exit 4 with a non-robust interior point stands as the robust bracket; both registrations are met (t5 +0.003 +- 0.004, mine +0.002 +- 0.003). Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position. **Every tail sum below is arithmetic only, not a result.**")
    P.append("### lambda_1 at D 23.0625 by k_c (secant roots)\n")
    T = ["| k_c | state | root at D 23.0625 [final bracket] | tool exit | step from the previous k_c | ratio of successive steps |", "|---|---|---|---|---|---|"]
    st = {95: "win2's leg state (reduced-quality lineage)", 103: "my leg point (the guard stopped the leg there)", 111: "my regrid of my k_c 103 state", 119: "my regrid of my k_c 111 state", 127: "my regrid of my k_c 119 state (psi-constraint 1.56e-3)"}
    prev = None; steps = []
    for kc in (95, 103, 111, 119, 127):
        s = S[kc]; sp = "" if prev is None else "%+.6f" % (s["root"] - prev)
        if prev is not None: steps.append(s["root"] - prev)
        rt = "" if len(steps) < 2 or prev is None else "%.4f" % (steps[-1] / steps[-2])
        T.append("| %d | %s | **%+.8f** [%.8f, %.8f] | %s | %s | %s |" % (kc, st[kc], s["root"], s["lo"], s["hi"], "0 (tol 1e-5)" if s["status"] == "tol" else "4 (nonrobust; width %.1e)" % s["width"], sp, rt))
        prev = s["root"]
    P.append("\n".join(T))
    r = steps[-1] / steps[-2]
    P.append("\nSteps %s; ratios %s. The ratio of the last step, %.4f, is the largest of the three (t5 registered about 0.72, I registered 0.6). **Arithmetic only, not a result:** a geometric tail of that ratio would end at %+.4f. The root is positive at D 23.0625, so the zero of k_c 127 lies above D 23.0625: with D 23.0 it needs a second D for k_c 127 (winb's regrid at D 23.0 is pending); t5 expects the extrapolated zero near D 23.068." % (", ".join("%+.6f" % x for x in steps), ", ".join("%.4f" % (steps[i + 1] / steps[i]) for i in range(len(steps) - 1)), r, tail(S[127]["root"], steps[-1], r)))
    P.append("### k_c 127 at D 23.0625: regrid, scan, secant (raw `I1025-macm3/kc127_d230625/`, README with the registration first, raw 22839e56d)\n")
    P.append("Source: my accepted k_c 119 state at D 23.0625 (blob 57f67269, record 659c62e5). The k_c 119 check accepted it (controls 1 1; the k_c 111 and k_c 127 checks refused it); `kc127_syscheck_1025.py` (raw `I1025-mac/checks` at d1baa986c, blob 898ebefa: the k_c 111 check with 111 changed to 127 and a header comment line) accepted the result (controls 1 1; the k_c 119 check refused it). `ell_refine.py` 631e5801, lambda_0(23.0625) = 2.0990016035, 6 threads, `capped_run.py` 28800 s. " + txt(R + "kc127_d230625/regrid/regrid_summary.txt").strip() + ". Wall 2853 s; **peak RSS 7.51 GiB (the k_c 119 regrids reached 5.5 to 5.6)**, no memory alert, no array limit at k_c 127. The scan used the new scanner (`d18_secant.py scan`, 92b9bf53, eb1396ad): lambda -0.02, -0.01, 0.00, 0.01 plus a repeat of 0.00 on 2 processes (peak RSS per scan process 5.04 GiB); then `d18_secant.py run`:")
    P.append("```\n" + txt(R + "kc127_d230625/point_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 127 at D 23.0625):** " + p.noise_row(R + "kc127_d230625/secant/secant.jsonl", "k_c 127 D 23.0625").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The evaluation that stopped the tool lay 3.4e-7 from the det-linear root of its bracket with dln 1.39; the two robust evaluations nearest the root give dln x distance 1.1e-8 and 1.2e-8.")
    P.append("\n### Registrations and scoring\nThe registration was written in `kc127_d230625/README.md` before the regrid and its log entries score it. Misses: the regrid's Delta shift (registered -1.4e-6 to -0.4e-6, read -1.878e-6: the shifts did not keep falling); the float64 sign equal to the hybrid sign at all 5 scan points (it differed at 0.01); the secant exit (registered exit 0 at 55%, exit 4 at 40%: it stopped on the non-robust point, which stands as the robust bracket by t5's ruling); the regrid's peak RSS was above my 6.5 GiB (7.51 GiB, inside the registered 8 GiB). The root: +0.002 registered (t5 +0.003), +0.003642 read.\n\nChain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672). Next (t5's order): one leg step of k_c 127 from this state to D 23.125 with the guard (`leap_guard.py`, stop at max cos_t_reg >= 0.5), to bracket the zero; t5 registers lambda_1(23.125) = -0.040 +- 0.010.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
