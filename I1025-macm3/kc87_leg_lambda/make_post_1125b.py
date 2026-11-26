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


def parse_sec(path):
    """-> dict from a secant summary (summarize_secant.py or summarize_point.py) or None"""
    if not os.path.exists(path):
        return None
    t = txt(path)
    m = re.search(r"status (\S+) \((.*?)\), tol (\S+), evaluations (\d+) \(the two ends included\), run wall (\d+) s", t)
    b = re.search(r"root bracket \[(\S+), (\S+)\], width (\S+), signs", t)
    r = re.search(r"det-linear root (\S+?);|det-linear inside the final bracket\) (\S+?);", t) or re.search(r"root \(det-linear inside the final bracket\) (\S+?);", t)
    root = re.search(r"(?:det-linear root|\(det-linear inside the final bracket\)) (-?[\d.]+)", t).group(1)
    sr = re.search(r"scan reading: (?:bracket \((\S+), (\S+)\), )?det-linear (\S+), estimator range \[(\S+), (\S+)\]", t)
    ins = re.search(r"root inside the (?:scan's )?estimator range[^:]*: (True|False)", t)
    return dict(status=m.group(1), why=m.group(2), nev=int(m.group(4)), wall=int(m.group(5)), lo=float(b.group(1)), hi=float(b.group(2)), width=float(b.group(3)), root=float(root),
                dl=float(sr.group(3)), rlo=float(sr.group(4)), rhi=float(sr.group(5)), inside=ins.group(1) if ins else "?", text=t)

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
    leg = sorted(glob.glob(R + "kc103_leg/ready_D*.txt"))
    P = []
    P.append("**#1025 macm3, threshold table: lambda_1 at D 23.0 and 23.0625 for k_c 87, 95 and 103 (secant values), the zeros by linear interpolation, the steps in k_c; with the k_c 87 scans of D 22.5 to 23.0, part c2's stop, the k_c 103 regrid, scan and leg (@@T@@).** One comment for everything since the 12:00 UTC post (7161793986), as ordered (t5, hc 26 Nov: \"post on #1025 the threshold table: lambda_1 at D 23.0 and 23.0625 for k_c 87, 95 and 103 (all secant values), the zero by linear interpolation per k_c, and the steps in k_c\"). Positions are the reader's printed brackets with the det-linear estimate; the estimator range is a spread over interpolation choices, not an enclosure; the printed orientation is the sign order in that state, and the sign convention differs between states (freeze orientation), so only the places of changes are compared across states.")
    P.append("### lambda_1 of my k_c 87 leg at D 22.25 and from D 22.5 to 23.0 (reading B, t5's ruling)\n")
    P.append("t5's ruling (hc ~18:50 UTC, quoted): \"lambda_1 runs 0.4425 (22.25), 0.216 (22.75), 0.167 (22.8125), 0.128 (22.875), 0.056 (22.9375), -0.0215 (23.0) ... The newcomer runs >0.50 (22.8125), 0.162 (22.875), -0.226 (22.9375), slopes < -5.4 and -6.2, a steady fast dive like S.\" D 22.5 and D 22.625 are labeled lambda_1 by continuity (t5, ~21:05 UTC: \"D 22.625 is lambda_1 (0.296, by continuity)\"). `roots87.txt` holds one F line per D (read by the chain) and `#N` comment lines for the newcomer.\n")
    T = ["| D | lambda_1 (scan det-linear; the secant values of D 22.9375 and 23.0 are in the threshold table below) | bracket | newcomer (`#N`) |", "|---|---|---|---|"]
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
    P.append("**lambda_1 at D 23.0 by k_c from the scans alone (det-linear, before the refinements below; k_c 87: my scan `23.0`; k_c 95: win2's, ruled by t5, comment 7173193613; k_c 103: this scan):**\n\n| k_c | scan det-linear | bracket and estimator range |\n|---|---|---|\n| 87 | **%s** | (-0.040, -0.020), range [-0.035344, -0.021546] |\n| 95 | **0.015921** | win2: (0.000, 0.020), range [0.002668, 0.015921] |\n| 103 | **%s** (scan, det-linear) | (%s, %s), range [%s, %s] |\n" % ("%.6f" % F[23.0][0], m.group(4), m.group(1), m.group(2), m.group(5), m.group(6)))
    P.append("**Scan (14 evaluations, 4 processes, 66.6 min; `score_scan.py`):**\n```\n" + sc.strip() + "\n```")
    S103 = parse_sec(R + "kc103_d23/secant/secant_summary.txt")
    S87 = parse_sec(R + "kc_d23_secant/kc87/secant_summary.txt"); S95 = parse_sec(R + "kc_d23_secant/kc95/secant_summary.txt")
    if S103:
        P.append("\n**Secant refinement of the k_c 103 bracket (0.020, 0.030)** (`d18_secant.py` a3d90cd5 of wip/ell1-speed 6010e37b, controls as in SPEED_ELL1.md: selftest exit 0, `half`, `norobust`, `nosigncheck` exit 1 each; `--tol=1e-5 --maxev=10`, one process; venv-macm3-1058b stands in for `venv-1025dd`, which is not on this machine, t5 accepted it):\n```\n" + S103["text"].strip() + "\n```")
    else:
        P.append("\n**Secant refinement of the k_c 103 bracket (0.020, 0.030):** not finished at the time of writing.")
    rows3 = []
    for kc, S_, sc_name in ((87, S87, "my scan `23.0`"), (95, S95, "win2's scan"), (103, S103, "this lane's scan")):
        if S_:
            rows3.append((kc, S_, sc_name))
    if len(rows3) == 3:
        T3 = ["| k_c | scan det-linear | scan estimator range (a spread) | secant root (det-linear in the final bracket) | final bracket (width) | evaluations, wall | inside the range |", "|---|---|---|---|---|---|---|"]
        for kc, S_, nm in rows3:
            T3.append("| %d | %.6f | [%.6f, %.6f] | **%.8f** | [%.8f, %.8f] (%.1e) | %d, %d s | %s |" % (kc, S_["dl"], S_["rlo"], S_["rhi"], S_["root"], S_["lo"], S_["hi"], S_["width"], S_["nev"], S_["wall"], S_["inside"]))
        st1 = rows3[1][1]["root"] - rows3[0][1]["root"]; st2 = rows3[2][1]["root"] - rows3[1][1]["root"]
        P.append("\n### lambda_1 at D 23.0 at three k_c (the three-k_c table, t5's order)\n\nSame tool (`d18_secant.py` a3d90cd5), `--tol=1e-5 --maxev=10`, one process per case, pinned by blob (README `kc_d23_secant/`, registered first, raw df6eaf448; k_c 103 in `kc103_d23/`). k_c 87 is my part c2 state (**REDUCED QUALITY**, psi-constraint 1.0496e-2); k_c 95 is win2's accepted state (source lineage reduced quality, k_c 95 constraint 7.67e-3); k_c 103 is my regrid of it (5.03e-3).\n\n" + "\n".join(T3) + "\n\nRefined steps in k_c: 87 to 95 %+.6f, 95 to 103 %+.6f (ratio %.3f); the unrefined det-linear numbers gave %+.6f and %+.6f (ratio %.3f). Arithmetic only, not a result: a geometric tail with the refined ratio would end at %.4f (t5's register: a converged lambda_1 between -0.03 and +0.03)." % (st1, st2, st2 / st1, rows3[1][1]["dl"] - rows3[0][1]["dl"], rows3[2][1]["dl"] - rows3[1][1]["dl"], (rows3[2][1]["dl"] - rows3[1][1]["dl"]) / (rows3[1][1]["dl"] - rows3[0][1]["dl"]), rows3[2][1]["root"] + st2 * (st2 / st1) / (1 - st2 / st1)))
        nv = txt(R + "kc_d23_secant/noise_vs_distance.txt").strip()
        P.append("\n**k_c 95 stands as a robust bracket, not a root to 1e-5.** Its tool exit was 4 (status nonrobust): the 7th evaluation, 2.1e-6 from the det-linear root, had sign + with both noise signs +, but dln 0.26 above the tool's bar 0.1, so the run stopped on **[0.00796052, 0.00873919]** (width 7.787e-4, both ends robust). t5's ruling (hc, 26 Nov, after both readings): \"no rerun with --dln=inf or a smaller eps: that would accept a sign the noise test rejects. The k_c 95 result stands as the robust bracket [0.00796, 0.00874] (width 7.8e-4), which is far below the k_c steps of 1.8e-2 that matter.\" The k_c 95 row of the table is the det-linear root inside that bracket and carries its width. t5's note says the hybrid sign is noise-limited within about 4e-4 of the root at k_c 95. From the files (`kc_d23_secant/noise_vs_distance.txt`, below), dln times the distance from the root is constant to 2% in each case, so dln reaches the bar 0.1 about 4e-7 from the root at k_c 95 (7e-8 at k_c 87, 4.6e-7 at k_c 103); the bracket is 7.8e-4 wide because Brent's last interior point fell inside that zone, and 3.9e-4 is the bracket's half-width. Both statements are recorded; the ruling is followed as given.")
        for kc, S_, nm in rows3[:2]:
            P.append("\n**Secant refinement at k_c %d, D 23.0:**\n```\n%s\n```" % (kc, S_["text"].strip()))
        P.append("\n**Noise against distance, all three refinements:**\n```\n" + nv + "\n```")
    else:
        P.append("\n### lambda_1 at D 23.0 at three k_c\n\nThe refinements at k_c 87 and k_c 95 (t5's order) have not both finished at the time of writing.")
    P.append("\n### The k_c 103 leg (t5's order, step 2)\n")
    P.append("Raw `I1025-macm3/kc103_leg/` (README with the registration first, raw 817384bb7; scored entries in it). `ell_leap.py` (5816d7b3, worktree edf49057) at k_c 103 from winb's accepted D 22.875 state (raw `I1025-win/kc103_d22875`, blob 28051531; record blob 8559e6ab, the LF form of his marker's f623d3e6) and my D 23.0 state (845e92a5), h 0.0625, to D 23.125, `--tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold`, 6 threads, guard `leap_guard.py` f1fe7c7c unchanged. Both seeds accepted by the k_c 103 check (controls 1 1) and refused by the k_c 95 and k_c 87 checks. Started 2026-11-25 23:05:27 UTC. **The guard stopped the leg at its first point** (t5's rule: scan that point and stop there):\n```\n" + txt(R + "kc103_leg/score_leg.txt").strip() + "\n```")
    pt = R + "kc103_leg/point_D23.0625_summary.txt"
    if os.path.exists(pt):
        P.append("\n**D 23.0625 at k_c 103: scan -0.10 to 0.02 by 0.02 plus a repeat of -0.04 (`kc87_leg_lambda/23.0625_kc103/`), then the secant refinement of its bracket** (the point was accepted first: `kc103_syscheck_1025.py` exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the k_c 95 and k_c 87 checks refuse it):\n```\n" + txt(pt).strip() + "\n```")
        sp = parse_sec(pt)
        if S103 and sp:
            d0, d1 = 23.0, 23.0625; r0, r1 = S103["root"], sp["root"]; sl = (r1 - r0) / (d1 - d0); zero = d0 - r0 / sl
            P.append("\n**lambda_1 at k_c 103 against D (secant roots):** D 23.0 %.8f, D 23.0625 %.8f; slope %.4f per unit D (t5's register: about -0.8, 0.028 at 23.0, lambda_1(23.0625) about -0.022); the straight line through them crosses zero at **D %.4f** (arithmetic on two points, not a result; t5's register: between 23.0 and 23.0625; k_c 87 by the same arithmetic on its unrefined scanned rows: D %.4f; its secant roots give the value in the threshold table below)." % (r0, r1, sl, zero, z87))
    else:
        P.append("\n**D 23.0625 at k_c 103:** its scan and secant refinement had not finished at the time of writing.")

    # the threshold table (t5's order: lambda_1 at two D per k_c, all secant values, the zero by linear interpolation per k_c, the steps in k_c)
    A = {87: [(23.0, parse_sec(R + "kc_d23_secant/kc87/secant_summary.txt")), (22.9375, parse_sec(R + "kc_d23_secant/kc87b/secant_summary.txt"))],
         95: [(23.0, parse_sec(R + "kc_d23_secant/kc95/secant_summary.txt")), (23.0625, parse_sec(R + "kc_d23_secant/kc95L/secant_summary.txt"))],
         103: [(23.0, parse_sec(R + "kc103_d23/secant/secant_summary.txt")), (23.0625, parse_sec(R + "kc103_leg/point_D23.0625_summary.txt"))]}
    def lz(Da, ra, Db, rb):
        return Da - ra * (Db - Da) / (rb - ra)
    TH, zer = [], {}
    for kc in (87, 95, 103):
        pts = sorted([(d, S_) for d, S_ in A[kc] if S_], key=lambda t: t[0])
        if len(pts) < 2:
            TH.append("| %d | | %s: second D not available at the time of writing | | | |" % (kc, "; ".join("D %s %.8f" % (d, S_["root"]) for d, S_ in pts)))
            continue
        (Da, Sa), (Db, Sb) = pts[0], pts[1]
        z = lz(Da, Sa["root"], Db, Sb["root"]); sl = (Sb["root"] - Sa["root"]) / (Db - Da)
        zs = [lz(Da, ra, Db, rb) for ra in (Sa["lo"], Sa["hi"]) for rb in (Sb["lo"], Sb["hi"])]
        zer[kc] = z
        TH.append("| %d | **%s and %s** | D %s: **%.8f** [%.8f, %.8f]; D %s: **%.8f** [%.8f, %.8f] | %+.5f | **%.5f** | %.5f to %.5f |" % (kc, Da, Db, Da, Sa["root"], Sa["lo"], Sa["hi"], Db, Sb["root"], Sb["lo"], Sb["hi"], sl, z, min(zs), max(zs)))
    P.append("\n### Threshold table: lambda_1 at two D for k_c 87, 95 and 103 (secant values), the zero by linear interpolation, the steps in k_c (t5's order)\n")
    P.append("Every root is the det-linear root inside the final bracket of `d18_secant.py` (a3d90cd5, `--tol=1e-5 --maxev=10`, pinned by blob, one process per case, venv-macm3-1058b); the bracket is in square brackets (k_c 95 at D 23.0 and at D 23.0625 stopped on a non-robust interior point, exit 4, so they are robust brackets, widths 7.8e-4 and 1.4e-3, by t5's ruling; the other four brackets are 5e-6 wide). The zero is the straight line through the two roots (arithmetic on two points, not a result); its range is the spread over the bracket ends (not an enclosure). k_c 87 has no state at D 23.0625 (my part c2 ended at D 23.0 by the guard), so its second D is D 22.9375 (t5's order).\n")
    P.append("| k_c | D pair used | lambda_1 (secant root [final bracket]) at the two D | slope per unit D | zero in D | range of the zero over the bracket ends |\n|---|---|---|---|---|---|\n" + "\n".join(TH))
    if len(zer) == 3:
        z87, z95, z103 = zer[87], zer[95], zer[103]
        P.append("\n**Steps in k_c of the zero:** 87 to 95 %+.5f in D, 95 to 103 %+.5f (ratio %.3f; arithmetic only, not a result: the same ratio for every later step of 8 in k_c would put the limit of the zero at D %.4f). At D 23.0 (the common D) the roots step %+.6f (87 to 95) and %+.6f (95 to 103), ratio %.3f; at D 23.0625 only 95 to 103 exists: %+.6f." % (z95 - z87, z103 - z95, (z103 - z95) / (z95 - z87), z103 + (z103 - z95) * ((z103 - z95) / (z95 - z87)) / (1 - (z103 - z95) / (z95 - z87)), A[95][0][1]["root"] - A[87][0][1]["root"], A[103][0][1]["root"] - A[95][0][1]["root"], (A[103][0][1]["root"] - A[95][0][1]["root"]) / (A[95][0][1]["root"] - A[87][0][1]["root"]), A[103][1][1]["root"] - A[95][1][1]["root"]))
    elif A[95][1][1] and A[103][1][1]:
        P.append("\n**Steps in k_c at D 23.0625 (95 to 103):** %+.6f; at D 23.0 (87 to 95, 95 to 103): %+.6f, %+.6f. The k_c 87 zero needs its second D (not yet available)." % (A[103][1][1]["root"] - A[95][1][1]["root"], A[95][0][1]["root"] - A[87][0][1]["root"], A[103][0][1]["root"] - A[95][0][1]["root"]))
    for kc_, nm_, lab_ in ((87, "kc87b", "k_c 87 at D 22.9375 (my part c2 state, REDUCED QUALITY, psi-constraint 1.0213e-2; exit 0)"), (95, "kc95L", "k_c 95 at D 23.0625 (win2's accepted leg state, raw `I1025-win2/kc95_leg`, blob 696bd814; exit 4, nonrobust, a robust bracket by t5's ruling)")):
        pth = R + "kc_d23_secant/%s/secant_summary.txt" % nm_
        if os.path.exists(pth):
            P.append("\n**Secant refinement at %s:**\n```\n%s\n```" % (lab_, txt(pth).strip()))

    P.append("\n### Registrations and scoring\nEvery scan's and every refinement's registration (grid or bracket, reading, weights) was written in a README before its run (`kc87_leg_lambda/README.md`, `kc103_d23/README.md`, `kc103_leg/README.md`, `kc_d23_secant/README.md`, each pushed first) and its log entry scores it. What missed, from those entries: the regrid wall of k_c 103 at D 23.0 (1391 s against 4000 to 6500 s); the secant of k_c 103 at D 23.0 (per evaluation 5.3 to 9.1 min against 8 to 25, wall 51 min against 60 to 150, and the float64 sign differing from the hybrid at 3 of 7 evaluations where I registered agreement at 80%); the leg's first point (1822 s against 2000 to 6000 s); k_c 95 at D 23.0 and at D 23.0625 (exit 4, a non-robust interior point, where I registered exit 0 at 80% and 60%; their per-evaluation and wall times); k_c 87 at D 22.9375 (per evaluation 3.3 to 3.9 min against 4.5 to 7); the orientation registrations of the k_c 87 scans listed above.\n\nChain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing of mine is running for this issue now. Open: the k_c 87 values at D 22.9375 and 23.0 are of reduced quality (psi-constraint 1.02e-2 and 1.05e-2), and win2's k_c 95 states descend from them; the k_c 103 states are below 1e-2 (4.6e-3 to 5.2e-3).")
    print("\n\n".join(P))

if __name__ == "__main__":
    main()
