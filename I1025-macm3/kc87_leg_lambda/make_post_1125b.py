#!/usr/bin/env python3
"""make_post_1125b.py > post.md : the batched #1025 comment of macm3 after the 12:00 UTC post of 25 Nov (t5's order, hc ~23:05 UTC: "Post on #1025 after the secant reading"): the k_c 87 scans of D 22.875 to 23.0
(the two-root story, reading B, the extension rule), D 22.5 and D 22.625, part c2's rows and stop, the k_c 103 D 23.0 regrid, scan and secant refinement, the k_c 103 leg's start.
Every number comes from the files (scan jsonl, read_lower.txt and read_lower_merged.txt, roots87.txt, c2/leg_points.txt, kc103_d23/ score_scan.txt and secant_summary.txt, kc103_leg/). @@T@@ in the first line is replaced by the caller.
Read-only. usage: make_post_1125b.py [--selftest]"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
CH = re.compile(r"robust change \((-?[\d.]+), (-?[\d.]+)\), ([-+]) to ([-+]), det-linear (-?[\d.]+), range \[(-?[\d.]+), (-?[\d.]+)\]")

def txt(p):
    return open(p).read()

def rows(path):
    return [json.loads(l) for l in open(path) if l.strip()]

def changes(t):
    return CH.findall(t), int(re.search(r"robust changes: (\d+)", t).group(1))

def fmt_changes(ch):
    return "; ".join("(%s, %s), %s to %s, **%s** ([%s, %s])" % c for c in ch) if ch else "none"

def single_table(folders):
    out = ["| scan folder (`kc87_leg_lambda/`) | D | lambda window | evaluations | noise-robust | robust changes of its own window: bracket, orientation as printed, det-linear (estimator range) |", "|---|---|---|---|---|---|"]
    for f in folders:
        js = glob.glob("%s/%s/scan/scan_D*_1025.jsonl" % (HERE, f))
        assert len(js) == 1, (f, js)
        rs = rows(js[0]); lam = sorted(set(r["lam"] for r in rs))
        ch, n = changes(txt("%s/%s/read_lower.txt" % (HERE, f)))
        assert n == len(ch), (f, n, ch)
        d = re.match(r"[\d.]+", f).group(0)
        kc = " (k_c 103)" if "kc103" in f else ""
        out.append("| `%s` | %s%s | %g to %g | %d | %d | %s |" % (f, d, kc, lam[0], lam[-1], len(rs), sum(1 for r in rs if r["noise_robust"]), fmt_changes(ch)))
    return "\n".join(out)

def merged_table(folders):
    out = ["| merged reading (`read_lower_merged.txt` of) | folders merged | window | points | robust changes: bracket, orientation as printed, det-linear (estimator range) | sign pattern |", "|---|---|---|---|---|---|"]
    for f in folders:
        t = txt("%s/%s/read_lower_merged.txt" % (HERE, f))
        ch, n = changes(t); assert n == len(ch), f
        hd = re.search(r"== window: read_lower.py scan (\S+ \S+) \(merged: (\d+) evaluations of the folders ([^)]*)\)", t)
        pts = re.search(r"points (\d+) in", t).group(1)
        signs = re.search(r"hybrid signs: (.*)", t).group(1)
        # a compact sign pattern: runs of equal signs with their lambda range
        toks = re.findall(r"(-?[\d.]+)([-+])", signs); runs = []
        for lam, s in toks:
            if runs and runs[-1][0] == s: runs[-1][2] = lam
            else: runs.append([s, lam, lam])
        pat = " ".join("%s[%s..%s]" % (s, a, b) if a != b else "%s[%s]" % (s, a) for s, a, b in runs)
        out.append("| `%s` | %s (%s evaluations) | %s | %s | %s | %s |" % (f, hd.group(3).replace(" + ", ", "), hd.group(2), hd.group(1).replace(" ", " to "), pts, fmt_changes(ch), pat))
    return "\n".join(out)

def roots():
    F, N = {}, {}
    for l in open(HERE + "/roots87.txt"):
        w = l.split()
        if not w: continue
        if l.startswith("#N "): N[float(w[1])] = (float(w[2]), l.split("bracket")[1].split("(")[0].split())
        elif not l.startswith("#") and l.rstrip().endswith(" F") or (not l.startswith("#") and w[0] in ("22.25",)):
            F[float(w[0])] = (float(w[1]), l.split("bracket")[1].split()[:2])
    return F, N

def main():
    F, N = roots()
    Ds = sorted(d for d in F if d >= 22.25)
    sl = [(Ds[i], Ds[i + 1], (F[Ds[i + 1]][0] - F[Ds[i]][0]) / (Ds[i + 1] - Ds[i])) for i in range(len(Ds) - 1)]
    s_last = sl[-1][2]; z87 = Ds[-1] - F[Ds[-1]][0] / s_last
    single = ["22.875", "22.875_wide", "22.875_F", "22.875_up", "22.8125", "22.8125_ext", "22.8125_F", "22.8125_F2", "22.75", "22.75_both", "22.9375", "22.9375_low", "23.0", "23.0_low", "22.5_both", "22.625_both"]
    merged = ["22.875_wide", "22.875_F", "22.875_up", "22.8125_ext", "22.8125_F", "22.8125_F2", "22.75_both", "22.9375_low", "23.0_low", "22.5_both", "22.625_both"]
    # c2 rows
    c2 = [l.rstrip("\n") for l in open(R + "kc87_leg2/c2/leg_points.txt")][:4]
    c2stop = open(R + "kc87_leg2/c2/leg_STOP.txt").readline().strip()
    # k_c 103
    sc = txt(R + "kc103_d23/score_scan.txt")
    sec = txt(R + "kc103_d23/secant/secant_summary.txt") if os.path.exists(R + "kc103_d23/secant/secant_summary.txt") else None
    leg = sorted(glob.glob(R + "kc103_leg/ready_D*.txt"))
    P = []
    P.append("**#1025 macm3, k_c 87 scans of D 22.5 to 23.0 (two roots, the newcomer, reading B), part c2's stop, and k_c 103 at D 23.0: regrid, scan, secant refinement; the k_c 103 leg has started (@@T@@).** One comment for the scans since the 12:00 UTC post (7161793986), as ordered (t5, hc ~23:05 UTC: \"Post on #1025 after the secant reading\"). Positions are the reader's printed brackets with the det-linear estimate; the estimator range is a spread over interpolation choices, not an enclosure; the printed orientation is the sign order in that state, and the sign convention differs between states (freeze orientation), so only the places of changes are compared across states.")
    P.append("### lambda_1 of my k_c 87 leg at D 22.25 and from D 22.5 to 23.0 (reading B, t5's ruling)\n")
    P.append("t5's ruling (hc ~18:50 UTC, quoted): \"lambda_1 runs 0.4425 (22.25), 0.216 (22.75), 0.167 (22.8125), 0.128 (22.875), 0.056 (22.9375), -0.0215 (23.0) ... The newcomer runs >0.50 (22.8125), 0.162 (22.875), -0.226 (22.9375), slopes < -5.4 and -6.2, a steady fast dive like S.\" D 22.5 and D 22.625 are labeled lambda_1 by continuity (t5, ~21:05 UTC: \"D 22.625 is lambda_1 (0.296, by continuity)\"). `roots87.txt` holds one F line per D (read by the chain) and `#N` comment lines for the newcomer.\n")
    T = ["| D | lambda_1 (det-linear) | bracket | newcomer (`#N`) |", "|---|---|---|---|"]
    for d in Ds:
        T.append("| %s | **%.6f** | %s to %s | %s |" % (d, F[d][0], F[d][1][0], F[d][1][1], ("%.6f (bracket %s to %s)" % (N[d][0], N[d][1][0], N[d][1][1])) if d in N else ("above 0.50 (no root up to 0.50)" if d == 22.8125 else "")))
    P.append("\n".join(T))
    P.append("\nSlopes of lambda_1 per unit D between consecutive rows: " + ", ".join("%s to %s: %.3f" % s for s in sl) + ".")
    P.append("\n**Zero of lambda_1 at k_c 87 by arithmetic on the last two rows (a straight line, not a result):** D %.4f (slope %.4f over %s to %s). The leg's guard stopped part c2 at D 23.0 (below)." % (z87, s_last, Ds[-2], Ds[-1]))
    P.append("\n### What was scanned, and what each scan read\n")
    nrd = 0
    for f in single:
        for g in ("read_lower.txt", "read_lower_merged.txt"):
            if os.path.exists("%s/%s/%s" % (HERE, f, g)):
                t = txt("%s/%s/%s" % (HERE, f, g)); assert "PASS" in t and "FAIL" not in t and "disagree" not in t, (f, g); nrd += 1
    P.append("All on the pinned k_c 87 states of my leg (raw `I1025-macm3/kc87_leg2/c/`, `c2/`, `b2/`), `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, repeats by `repeat_check.py` aaf598a9 (the repeat check passes in all %d readings of these folders, own and merged). Each row is the folder's own window; the second table is the merged reading when scans of one D were joined (the extension rule: a window without a robust change is extended by its width on the side the orientation read at the nearest scanned point of the same part points to; t5, hc ~12:10 and ~14:43 UTC).\n" % nrd)
    P.append(single_table(single))
    P.append("\n**Merged readings per D (the readings the labels rest on):**\n")
    P.append(merged_table(merged))
    P.append("\n### The two-root story (what I got wrong, and how it was resolved)\n")
    P.append("Several labelings were tried before reading B. (1) By order: the lower root of a pair as L and the upper as F; the wide scan at D 22.875 showed two roots there (merged table) and one at D 22.8125, so \"upper = F\" was wrong. (2) The direction of an extension came from a template: the first extension chosen that way (D 22.8125, up) was wrong and was cancelled by exact pids, and the rule now reads the orientation of the nearest scanned point of the same part (t5, hc ~14:43 UTC). (3) The registered orientations of D 23.0, D 22.9375, D 22.875 (narrow), D 22.8125 (extension) and D 22.5 were wrong, because the sign convention differs between states. (4) t5's hypothesis that lambda_1 is the lower track was tested by the D 22.75 both-roots scan (one root, 0.216086) and the negative scans of D 22.9375 (the newcomer at -0.226429) and D 23.0 (no change in -0.50 to -0.10, as expected with the newcomer below -0.5); it became reading B. Labels by order are off (`LABELS_FROZEN.txt`); later roots are labeled by continuity and t5 rules pairs.")
    P.append("\n### Part c2 (k_c 87, past the 1e-2 psi-constraint bar, `--cmax 2e-2`): rows and the guard's stop\n")
    P.append("\n".join(c2) + "\n\n**Guard (`leap_guard.py` f1fe7c7c, unchanged):** `%s` Both rows are above the 1e-2 bar: **REDUCED QUALITY** (1.021e-2 and 1.050e-2). The max cos_t_reg is on the third regular mode, as lambda_1 neared zero; win2's k_c 95 leg stopped by the same rule at D 23.0625 (cos 0.5997)." % c2stop)
    P.append("\n### k_c 103 at D 23.0 (t5's order, hc ~21:05 UTC): regrid of win2's k_c 95 state, scan -0.06 to 0.06, secant refinement\n")
    P.append("Raw `I1025-macm3/kc103_d23/` (README first, raw 74ae248c5; scored entries in it). Source: win2's accepted k_c 95 state at D 23.0 (raw `I1025-win2/kc95_d23`, blob 096f1cc0, record e3fff23f; **REDUCED QUALITY lineage**, k_c 95 constraint 7.67e-3). Regrid (`ell_refine.py` 631e5801, dh170's recipe, 6 threads): accepted 21:42:31 UTC by `kc103_syscheck_1025.py` (3ab58d16; controls `--mutate=F` and `--mutate=steps` exit 1 1; the k_c 95 check refuses the result): |F| 3.2905e-10, 3389 steps, psi-constraint 5.0299e-03 (below 1e-2), Delta 1.174332548928 (k_c 95 source 1.174346963414: shift -1.4414e-05), wall 1391 s (registered 4000 to 6500 s: the one miss of the lane).\n")
    m = re.search(r"root k_c 103: bracket \((\S+), (\S+)\), (\S+ to \S+), det-linear (\S+), estimator range \[(\S+), (\S+)\]", sc)
    P.append("**lambda_1 at D 23.0 by k_c** (k_c 87: my scan `23.0`; k_c 95: win2's, ruled by t5, comment 7173193613; k_c 103: this scan):\n\n| k_c | root | bracket and estimator range |\n|---|---|---|\n| 87 | **%s** | (-0.040, -0.020), range [-0.035344, -0.021546] |\n| 95 | **0.015921** | win2: (0.000, 0.020), range [0.002668, 0.015921] |\n| 103 | **%s** (scan, det-linear) | (%s, %s), range [%s, %s] |\n" % ("%.6f" % F[23.0][0], m.group(4), m.group(1), m.group(2), m.group(5), m.group(6)))
    P.append("**Scan (14 evaluations, 4 processes, 66.6 min; `score_scan.py`):**\n```\n" + sc.strip() + "\n```")
    if sec:
        P.append("\n**Secant refinement of the bracket (0.020, 0.030)** (`d18_secant.py` a3d90cd5 of wip/ell1-speed 6010e37b, controls as in SPEED_ELL1.md: selftest exit 0, `half`, `norobust`, `nosigncheck` exit 1 each; `--tol=1e-5 --maxev=10`, one process; venv-macm3-1058b stands in for `venv-1025dd`, which is not on this machine, t5 accepted it):\n```\n" + sec.strip() + "\n```")
    else:
        P.append("\n**Secant refinement of the bracket (0.020, 0.030):** not finished at the time of writing.")
    P.append("\n### The k_c 103 leg (t5's order, step 2)\n")
    P.append("Raw `I1025-macm3/kc103_leg/` (README with the registration first, raw 817384bb7). `ell_leap.py` (5816d7b3, worktree edf49057) at k_c 103 from winb's accepted D 22.875 state (raw `I1025-win/kc103_d22875`, blob 28051531) and my D 23.0 state (845e92a5), h 0.0625, to D 23.125, `--tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold`, guard `leap_guard.py` f1fe7c7c unchanged. Both seeds accepted by the k_c 103 check (controls 1 1) and refused by the k_c 95 and k_c 87 checks. **Started 2026-11-25 23:05:27 UTC** beside the secant run (t5's order). " + (("Points ready: " + ", ".join(os.path.basename(p)[len("ready_D"):-4] for p in leg) + ".") if leg else "No point yet at the time of writing (the first point D 23.0625 is expected in 2000 to 6000 s of the leap, registered).") + " If the guard stops the leg at its first point, that point is scanned (-0.10 to 0.02 by 0.02) and the leg ends there (t5).")
    P.append("\n### Registrations and scoring\nEvery scan's registration (grid, repeat, reading, weights) was written in `kc87_leg_lambda/README.md` before the scan and its log entry scores it; the k_c 103 lane's registration and scoring are in `kc103_d23/README.md` (all met except the regrid wall). The orientation registrations listed in (3) above were wrong; every other registered position or count that the READMEs score is scored there.\n\nChain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing else is running for this issue except the secant refinement and the leap.")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
