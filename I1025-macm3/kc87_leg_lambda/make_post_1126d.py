#!/usr/bin/env python3
"""make_post_1126d.py > post.md : the #1025 comment of macm3 on k_c 119 at D 22.875 (t5's order, hc 26 Nov: "Post it on #1025."): the three D of k_c 119, the line and quadratic zeros, the regrid, scan (new scanner) and secant at D 22.875,
the noise row. Every number comes from the files; the zero arithmetic is the output of kc119_d22875/zero_arithmetic.txt (venv python); tail sums none. @@T@@ replaced by the caller."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post_1126 as p
R = p.R; txt = p.txt; parse_sec = p.parse_sec

def main():
    S = {22.875: parse_sec(R + "kc119_d22875/point_summary.txt"), 23.0: parse_sec(R + "kc119_d23/point_summary.txt"), 23.0625: parse_sec(R + "kc119_d230625/point_summary.txt")}
    P = []
    P.append("**#1025 macm3, k_c 119 at D 22.875: lambda_1 = +0.11797426, bracket 5e-6; k_c 119 at three D, the zero by a line and by a quadratic (@@T@@).** t5's order (hc 26 Nov): \"Post it on #1025.\" t5's register for the root: 0.122 +- 0.006; mine 0.120 +- 0.006; both are met. Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position.")
    P.append("### k_c 119 at three D (secant roots)\n")
    T = ["| D | state | root [final bracket] | tool exit | scanner of the scan |", "|---|---|---|---|---|"]
    st = {22.875: "my regrid of dh610's k_c 111 state (psi-constraint 1.91e-3)", 23.0: "my regrid of dh170's k_c 111 state (2.14e-3)", 23.0625: "my regrid of my k_c 111 state (2.27e-3)"}
    sc = {22.875: "`d18_secant.py scan` eb1396ad", 23.0: "`d18_hybsign.py` e089207a", 23.0625: "`d18_secant.py scan` eb1396ad"}
    for d in (22.875, 23.0, 23.0625):
        s = S[d]; T.append("| %s | %s | **%+.8f** [%.8f, %.8f] | %s | %s |" % (d, st[d], s["root"], s["lo"], s["hi"], "0 (tol 1e-5)" if s["status"] == "tol" else "4 (nonrobust)", sc[d]))
    P.append("\n".join(T))
    P.append("\n**The zero of k_c 119 (arithmetic on three points, not a result; `kc119_d22875/zero_arithmetic.txt`):**\n```\n" + txt(R + "kc119_d22875/zero_arithmetic.txt").strip() + "\n```\nThe quadratic puts the zero 0.00020 above the line; the earlier zeros (k_c 87 to 111) are lines through two D (the post of comment 7189722079), so the line value 23.05757 is the one that compares with them.")
    P.append("### k_c 119 at D 22.875: regrid, scan, secant (raw `I1025-macm3/kc119_d22875/`, README with the registration first, raw 5dfbfe396)\n")
    P.append("Source: dh610's accepted k_c 111 state at D 22.875 (raw `I1025-dh610/kc111_d22875` at 33c6c6fb, blob a8fe443e, record 5233ffe8, tag l1kc111dh610d22875; dh610's regrid of winb's k_c 103 state). The k_c 111 check accepted it (controls 1 1; the k_c 103 and k_c 119 checks refused it); `kc119_syscheck_1025.py` (fc6e0dd6) accepted the result (controls 1 1; the k_c 111 check refused it). `ell_refine.py` 631e5801, lambda_0(22.875) = 2.0996545550, 6 threads, `capped_run.py` 28800 s. " + txt(R + "kc119_d22875/regrid/regrid_summary.txt").strip() + ". Wall 2272 s; peak RSS 5.51 GiB. The scan used the new scanner (`d18_secant.py scan`, wip/ell1-speed 92b9bf53, eb1396ad; selftest and the three mutations logged in the README before the scan): lambda 0.10, 0.11, 0.12, 0.13 plus a repeat of 0.12 on 2 processes; then `d18_secant.py run`:")
    P.append("```\n" + txt(R + "kc119_d22875/point_summary.txt").strip() + "\n```")
    P.append("\n**Noise of the sign near the root (k_c 119 at D 22.875):** " + p.noise_row(R + "kc119_d22875/secant/secant.jsonl", "k_c 119 D 22.875").replace("|", " ").strip() + " (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1).")
    P.append("\n### Registrations and scoring\nThe registration was written in `kc119_d22875/README.md` before the regrid and its log entries score it. One item missed: the float64 sign equal to the hybrid sign at all 5 scan evaluations (registered 55%; it differed at both evaluations of 0.12, where the hybrid sign is -). Everything else held, including the steps of the regrid (3912 registered, 3912 read). The root: 0.120 registered (t5 0.122), +0.11797 read.\n\nChain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672). Next (t5's order): k_c 127 at D 23.0625 from my k_c 119 state there (raw `I1025-macm3/kc127_d230625/`), with winb's k_c 127 at D 23.0 to give k_c 127's threshold; t5 registers the root at +0.003 +- 0.004.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
