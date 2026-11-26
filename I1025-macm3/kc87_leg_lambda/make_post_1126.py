#!/usr/bin/env python3
"""make_post_1126.py > post.md : the #1025 comment of macm3 on the four-k_c threshold (t5's order, hc 26 Nov, "post the four-k_c threshold table on #1025 now. Put the D 23.0 roots and their steps in it, and the zeros
22.97893, 23.00808, 23.03011, 23.04627 with their steps and ratios. Label each tail sum arithmetic only."): the secant roots at D 23.0 and D 23.0625 for k_c 87, 95, 103 and 111, the zeros by linear interpolation, the steps and ratios,
the k_c 111 regrid, scan and secant at D 23.0625, Part B (dh170's k_c 111 state at D 23.0), the noise against distance. Every number comes from the files (secant summaries and jsonl, the scan summaries, regrid_summary.txt, the READMEs'
scored entries); the tail sums are computed here. @@T@@ in the first line is replaced by the caller. Read-only. usage: make_post_1126.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post_1125b as m
R = m.R; txt = m.txt; parse_sec = m.parse_sec

def tail(c, s2, r):
    return c + s2 * r / (1 - r)

def lz(Da, ra, Db, rb):
    return Da - ra * (Db - Da) / (rb - ra)

def noise_row(path, label):
    ev = [json.loads(l) for l in open(path) if l.strip()]
    e = [r for r in ev if r.get("kind") == "eval"]; root = [r for r in ev if r.get("kind") == "root"][0]; lin = root["lam_lin"]
    cs = [(abs(r["lam"] - lin) * r["dln"]) for r in e if r["robust"] and 0 < abs(r["lam"] - lin) < 2e-4]
    worst = max((r for r in e), key=lambda r: r["dln"])
    return "| %s | %s | %.3e | %.1e (at %.2e from the root) | %s | %s |" % (label, root["status"], root["width"], worst["dln"], abs(worst["lam"] - lin), "%.1e to %.1e" % (min(cs), max(cs)) if cs else "-", "%.1e" % (min(cs) / 0.1) if cs else "-")

def main():
    K = R + "kc_d23_secant/"
    A = {87: [(22.9375, parse_sec(K + "kc87b/secant_summary.txt")), (23.0, parse_sec(K + "kc87/secant_summary.txt"))],
         95: [(23.0, parse_sec(K + "kc95/secant_summary.txt")), (23.0625, parse_sec(K + "kc95L/secant_summary.txt"))],
         103: [(23.0, parse_sec(R + "kc103_d23/secant/secant_summary.txt")), (23.0625, parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"))],
         111: [(23.0, parse_sec(K + "kc111dh/secant_summary.txt")), (23.0625, parse_sec(R + "kc111_d230625/point_summary.txt"))]}
    for kc in A:
        for d, S in A[kc]:
            assert S is not None, (kc, d)
    root23 = {kc: dict(A[kc])[23.0] for kc in A}; root236 = {kc: dict(A[kc])[23.0625] for kc in (95, 103, 111)}
    P = []
    P.append("**#1025 macm3, the threshold at four resolutions: lambda_1 at D 23.0 for k_c 87, 95, 103 and 111, the zeros in D, their steps and ratios; k_c 111 at D 23.0625 and dh170's k_c 111 state at D 23.0 (@@T@@).** t5's order (hc 26 Nov): \"post the four-k_c threshold table on #1025 now. Put the D 23.0 roots and their steps in it, and the zeros 22.97893, 23.00808, 23.03011, 23.04627 with their steps and ratios. Label each tail sum arithmetic only.\" Every root below is the det-linear root inside the final bracket of `d18_secant.py` (a3d90cd5 of wip/ell1-speed 6010e37b, `--tol=1e-5 --maxev=10`, pinned by blob, one process per case, `venv-macm3-1058b`), read by position; the bracket is in square brackets. Exit 4 (status nonrobust: an interior point whose 1e-15 noise test moves ln|det| by more than the tool's bar 0.1) leaves the robust bracket, which stands (t5's ruling at k_c 95: no rerun with `--dln=inf` or a smaller eps). **A tail sum is arithmetic on the numbers shown, not a result.**")
    P.append("### lambda_1 at D 23.0 by k_c\n")
    T = ["| k_c | state | root at D 23.0 [final bracket] | tool exit | step from the previous k_c |", "|---|---|---|---|---|"]
    src = {87: "my part c2 state (REDUCED QUALITY, psi-constraint 1.0496e-2)", 95: "win2's accepted state (reduced-quality lineage, 7.67e-3)", 103: "my regrid of it (5.03e-3)", 111: "dh170's regrid of my k_c 103 state (3.48e-3)"}
    prev = None; steps = []
    for kc in (87, 95, 103, 111):
        S = root23[kc]; st = "" if prev is None else "%+.6f" % (S["root"] - prev);
        if prev is not None: steps.append(S["root"] - prev)
        T.append("| %d | %s | **%.8f** [%.8f, %.8f] | %s | %s |" % (kc, src[kc], S["root"], S["lo"], S["hi"], "0 (tol 1e-5)" if S["status"] == "tol" else "4 (nonrobust; bracket width %.1e)" % S["width"], st))
        prev = S["root"]
    P.append("\n".join(T))
    r1, r2 = steps[1] / steps[0], steps[2] / steps[1]
    P.append("\nSteps %+.6f, %+.6f, %+.6f; ratios of successive steps %.4f and %.4f (the unrefined det-linear numbers of the scans gave +0.037467 and +0.012354, ratio 0.330). **Arithmetic only, not a result:** a geometric tail of the last ratio would end at %.4f; t5's register for a converged lambda_1 is between -0.03 and +0.03, and t5's prediction for k_c 119 at D 23.0 is +0.040 +- 0.003 (the last step times a ratio near 0.51)." % (steps[0], steps[1], steps[2], r1, r2, tail(root23[111]["root"], steps[2], r2)))
    P.append("\n### lambda_1 at D 23.0625 by k_c, and the zeros in D\n")
    T = ["| k_c | root at D 23.0625 [final bracket] | tool exit |", "|---|---|---|"]
    for kc in (95, 103, 111):
        S = root236[kc]; T.append("| %d | **%.8f** [%.8f, %.8f] | %s |" % (kc, S["root"], S["lo"], S["hi"], "0 (tol 1e-5)" if S["status"] == "tol" else "4 (nonrobust; bracket width %.1e)" % S["width"]))
    P.append("\n".join(T))
    s236 = [root236[103]["root"] - root236[95]["root"], root236[111]["root"] - root236[103]["root"]]
    P.append("\nSteps at D 23.0625: %+.6f (95 to 103), %+.6f (103 to 111), ratio %.4f; arithmetic only: a geometric tail of that ratio would end at %.4f. k_c 87 has no state at D 23.0625 (my part c2 ended at D 23.0 by the guard), so its second D is D 22.9375.\n" % (s236[0], s236[1], s236[1] / s236[0], tail(root236[111]["root"], s236[1], s236[1] / s236[0])))
    T = ["| k_c | D pair used | lambda_1 at the two D (secant root) | slope per unit D | zero in D | zero over the four bracket-end combinations |", "|---|---|---|---|---|---|"]
    zer = {}
    for kc in (87, 95, 103, 111):
        (Da, Sa), (Db, Sb) = A[kc]
        z = lz(Da, Sa["root"], Db, Sb["root"]); sl = (Sb["root"] - Sa["root"]) / (Db - Da)
        zs = [lz(Da, ra, Db, rb) for ra in (Sa["lo"], Sa["hi"]) for rb in (Sb["lo"], Sb["hi"])]
        zer[kc] = z
        T.append("| %d | **%s and %s** | %.8f; %.8f | %+.5f | **%.5f** | %.5f to %.5f |" % (kc, Da, Db, Sa["root"], Sb["root"], sl, z, min(zs), max(zs)))
    P.append("\n".join(T))
    zl = [zer[95] - zer[87], zer[103] - zer[95], zer[111] - zer[103]]
    P.append("\n**Steps of the zero in k_c:** %+.5f (87 to 95), %+.5f (95 to 103), %+.5f (103 to 111); ratios %.4f and %.4f. **Arithmetic only, not a result:** a geometric tail of the last ratio would put the limit of the zero at D %.4f." % (zl[0], zl[1], zl[2], zl[1] / zl[0], zl[2] / zl[1], tail(zer[111], zl[2], zl[2] / zl[1])))
    # k_c 111 at D 23.0625
    P.append("\n### k_c 111 at D 23.0625: regrid, scan, secant (raw `I1025-macm3/kc111_d230625/`, README first raw e789e056a)\n")
    P.append("From my accepted k_c 103 state at D 23.0625 (the leg's point, blob aa7b61a6; record 3cd84ab0), dh170's k_c 111 recipe (`ell_refine.py` 631e5801, 6 threads, lambda_0(23.0625) = 2.0990016035). The k_c 103 check accepted the source (controls 1 1; the k_c 95 and k_c 111 checks refused it); `kc111_syscheck_1025.py` (85aeb312) accepted the result (controls 1 1; the k_c 103 check refused it). " + txt(R + "kc111_d230625/regrid/regrid_summary.txt").strip() + ". Wall 2102 s (registered 1500 to 3500 s). The scan, as t5 widened it after my question (my register had the root above the ordered window's upper end -0.02): -0.08 to 0.02 by 0.01 plus a repeat of -0.01, then the secant on its bracket:")
    P.append("```\n" + txt(R + "kc111_d230625/point_summary.txt").strip() + "\n```")
    P.append("\n### Part B: dh170's k_c 111 state at D 23.0 (raw `I1025-dh170/kc111_d23/`, state c0edd3c1, record 74d49790), secant here (raw `I1025-macm3/kc_d23_secant/kc111dh/`, README first raw ed4dc4a9c)\n")
    P.append("His scan's round 1 (5 of 8 evaluations: -0.04, -0.02, 0.00, 0.02, 0.04) read with the pinned `read_lower.py` on a copy gives the same bracket and range as his partial reading; his round 2 was not waited for. The k_c 111 check accepted the state (controls 1 1; the k_c 103 and k_c 95 checks refused it). The secant stopped at a non-robust interior point (exit 4), so the result is the robust bracket:")
    P.append("```\n" + txt(K + "kc111dh/secant_summary.txt").strip() + "\n```")
    P.append("\n### Noise of the sign near the root\n")
    P.append("For each refinement: the largest dln of its evaluations and where it fell, and dln times the distance from the det-linear root for the robust evaluations within 2e-4 of it (the product is constant in a case, so dln reaches the bar 0.1 at that constant over 0.1; in the three cases that stopped on a non-robust point the product rests on one or two robust evaluations and the root is only bracketed; at k_c 111 D 23.0 the non-robust evaluation is the det-linear root of its bracket, so its distance prints as 0). From `secant.jsonl` of each case.\n")
    N = ["| case | tool status | final bracket width | largest dln (distance from the root) | dln x distance | distance where dln = 0.1 |", "|---|---|---|---|---|---|"]
    for label, path in (("k_c 87 D 23.0", K + "kc87/secant/secant.jsonl"), ("k_c 87 D 22.9375", K + "kc87b/secant/secant.jsonl"), ("k_c 95 D 23.0", K + "kc95/secant/secant.jsonl"), ("k_c 95 D 23.0625", K + "kc95L/secant/secant.jsonl"),
                        ("k_c 103 D 23.0", R + "kc103_d23/secant/secant.jsonl"), ("k_c 103 D 23.0625", R + "kc103_leg/secant_D23.0625/secant.jsonl"), ("k_c 111 D 23.0", K + "kc111dh/secant/secant.jsonl"), ("k_c 111 D 23.0625", R + "kc111_d230625/secant/secant.jsonl")):
        N.append(noise_row(path, label))
    P.append("\n".join(N))
    P.append("\nThe two k_c 95 cases and k_c 111 at D 23.0 stopped on a non-robust interior point: the tool's last point fell inside the zone where dln exceeds the bar, 4e-7 to 6e-7 wide (t5's note had 4e-4; the bracket's half-width is 3.9e-4 at k_c 95 D 23.0, which is what is wide).")
    P.append("\n### Registrations and scoring\nEach run's registration was written in a README before it ran and its log entry scores it (`kc111_d230625/README.md`, `kc_d23_secant/README.md`). Misses in this batch: the exit 4 of k_c 95 at D 23.0625 (registered 35%) and of k_c 111 at D 23.0 (registered 25%); per-evaluation times of k_c 95 at D 23.0625 (4.5 to 5.0 min against 5 to 9) and k_c 87 at D 22.9375 (3.3 to 3.9 against 4.5 to 7). I also typed a tail sum by hand into a README (-0.0030 where the file gives +0.0058) and corrected it the same hour; every number here comes from the files.\n\nChain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672). Next (t5's order): k_c 119 at D 23.0 from dh170's k_c 111 state (raw `I1025-macm3/kc119_d23/`), a fifth resolution to test the step ratio; t5 registers the root at +0.040 +- 0.003.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
