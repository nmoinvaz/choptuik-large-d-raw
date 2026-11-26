#!/usr/bin/env python3
"""make_post_1126b.py > post.md : the #1025 comment of macm3 on k_c 119 at D 23.0 (t5's order, hc 26 Nov: "Post it on #1025, with any tail sum labeled arithmetic only."): the five-k_c table at D 23.0, the k_c 119 regrid, scan and secant, the
noise row, the scanner change. Every number comes from the files (secant summaries and jsonl, point_summary.txt, regrid_summary.txt, the READMEs' scored entries); the tail sum is computed here. @@T@@ is replaced by the caller. Read-only."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post_1126 as p
R = p.R; txt = p.txt; parse_sec = p.parse_sec

def main():
    K = R + "kc_d23_secant/"
    S = {87: parse_sec(K + "kc87/secant_summary.txt"), 95: parse_sec(K + "kc95/secant_summary.txt"), 103: parse_sec(R + "kc103_d23/secant/secant_summary.txt"),
         111: parse_sec(K + "kc111dh/secant_summary.txt"), 119: parse_sec(R + "kc119_d23/point_summary.txt")}
    src = {87: "my part c2 state (REDUCED QUALITY, psi-constraint 1.0496e-2)", 95: "win2's accepted state (reduced-quality lineage, 7.67e-3)", 103: "my regrid of it (5.03e-3)", 111: "dh170's regrid of my k_c 103 state (3.48e-3)", 119: "my regrid of dh170's k_c 111 state (2.14e-3)"}
    P = []
    P.append("**#1025 macm3, k_c 119 at D 23.0 (the fifth resolution): lambda_1 = +0.04106103, bracket 5e-6, regrid, scan and secant (@@T@@).** t5's order (hc 26 Nov): \"Post it on #1025, with any tail sum labeled arithmetic only.\" t5's register: the root at D 23.0 is +0.040 +- 0.003 (the last step 0.009058 times a ratio near 0.51); it is met. Roots are the det-linear root inside the final bracket of `d18_secant.py` (a3d90cd5, `--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position.")
    P.append("### lambda_1 at D 23.0 by k_c (secant roots)\n")
    T = ["| k_c | state | root at D 23.0 [final bracket] | tool exit | step from the previous k_c | ratio of successive steps |", "|---|---|---|---|---|---|"]
    prev = None; steps = []
    for kc in (87, 95, 103, 111, 119):
        s = S[kc]; st = "" if prev is None else "%+.6f" % (s["root"] - prev)
        if prev is not None: steps.append(s["root"] - prev)
        rt = "" if len(steps) < 2 or prev is None else "%.4f" % (steps[-1] / steps[-2])
        T.append("| %d | %s | **%.8f** [%.8f, %.8f] | %s | %s | %s |" % (kc, src[kc], s["root"], s["lo"], s["hi"], "0 (tol 1e-5)" if s["status"] == "tol" else "4 (nonrobust; width %.1e)" % s["width"], st, rt))
        prev = s["root"]
    P.append("\n".join(T))
    r = steps[-1] / steps[-2]; tail = S[119]["root"] + steps[-1] * r / (1 - r)
    P.append("\nSteps %s; ratios %s. **Arithmetic only, not a result:** a geometric tail of the last ratio (%.4f) would end at %.4f; the ratio is not constant (0.5218, 0.5090, 0.6069), so the tail is a guide to the size of the remaining steps and no more. t5's register for a converged lambda_1 is between -0.03 and +0.03; the D 23.0 roots now sit at +0.041 and are still rising." % (", ".join("%+.6f" % x for x in steps), ", ".join("%.4f" % (steps[i + 1] / steps[i]) for i in range(len(steps) - 1)), r, tail))
    P.append("### k_c 119 at D 23.0: regrid, scan, secant (raw `I1025-macm3/kc119_d23/`, README with the registration first, raw aa7da4fbf)\n")
    P.append("Source: dh170's accepted k_c 111 state at D 23.0 (raw `I1025-dh170/kc111_d23`, blob c0edd3c1, record 74d49790). The k_c 111 check accepted it (controls 1 1; the k_c 103 and k_c 119 checks refused it). `kc119_syscheck_1025.py` (raw `I1025-mac/checks` at 0d6db56f4, blob fc6e0dd6: the k_c 111 check with 111 changed to 119 and one added header comment line) accepted the result (controls 1 1; the k_c 111 check refused it). `ell_refine.py` 631e5801, 6 threads, `capped_run.py` 28800 s in place of `timeout` (macOS has none). " + txt(R + "kc119_d23/regrid/regrid_summary.txt").strip() + ". Wall 2282 s; peak RSS 5.64 GiB. The scan: -0.02 to 0.06 by 0.02 plus a repeat of 0.04 (the scan driver requires a repeat), run on 2 processes in 3 rounds (t5's change: about 7 GiB per k_c 119 process), `d18_hybsign.py` e089207a (the scan started before the scanner change); then the secant:")
    P.append("```\n" + txt(R + "kc119_d23/point_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 119):** " + p.noise_row(R + "kc119_d23/secant/secant.jsonl", "k_c 119 D 23.0").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The product is constant to a few percent over the evaluations within 2e-4 of the root, as in the earlier cases (k_c 87 7.4e-9, k_c 95 3.6e-8 to 5.3e-8, k_c 103 4.5e-8 to 5.7e-8, k_c 111 5.8e-8 to 7.1e-8).")
    P.append("\n### Registrations and scoring\nThe registration was written in `kc119_d23/README.md` before the regrid and its log entries score it. Misses: the regrid's psi-constraint (registered 2.5e-3 from a ratio 0.72 that the earlier ratios 0.656, 0.693 did not support; the file has 2.139e-3, ratio 0.614); the float64 sign differing from the hybrid sign at 2 of the 6 scan evaluations and at 4 of the 7 secant evaluations (the double-double block 12 decides the sign near the root); the scan wall (50.6 min against 70 to 150: two processes ran 17 min per round). Everything else registered held, including the root: +0.0401 registered (t5 +0.040 +- 0.003), +0.04106 read.\n\n**Scanner change (t5, hc 26 Nov):** scans that have not started use `d18_secant.py scan` (wip/ell1-speed 92b9bf53, blob eb1396ad); this scan was already running and keeps `d18_hybsign.py`. The new scanner's selftest exits 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1 (logged in the READMEs; the next folder `kc119_d230625/` uses it). **Running now:** k_c 119 at D 23.0625 from my k_c 111 state there (raw `I1025-macm3/kc119_d230625/`), to give k_c 119's threshold zero (t5 registers the root at -0.004 +- 0.005 and the zero near D 23.057; dh370 runs the same point on Linux as the cross-check). Chain held.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
