#!/usr/bin/env python3
"""make_post_1125.py > post.md : the batched #1025 comment of 25 Nov (t5's order, hc ~12:0x UTC): the two-branch picture (F, S), every scan since the D 22.0 post, the k_c 95 D 22.3125 wide and high
scans, parts c and c2. Every number comes from the files (scan jsonl, read_lower.txt, wide_read.txt, make_branches.py, make_track.py, make_batch.py, the READMEs' scored paragraphs, the leg records).
@@T@@ in the first line is replaced by the caller. Read-only. usage: make_post_1125.py [--selftest]"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
L2 = R + "kc87_leg2/"; K95 = R + "kc95_d223125/"
PY = sys.executable

def run(script, *a):
    return subprocess.run([PY, HERE + "/" + script] + list(a), capture_output=True, text=True, check=True).stdout

def rows_of(folder):
    return [json.loads(l) for l in open("%s/%s/scan/scan_D%s_1025.jsonl" % (HERE, folder, re.match(r"[\d.]+", folder).group(0))) if l.strip()]

def reading(folder):
    t = open("%s/%s/%s" % (HERE, folder, "wide_read.txt" if os.path.exists("%s/%s/wide_read.txt" % (HERE, folder)) else "read_lower.txt")).read()
    ch = re.findall(r"change \((-?[\d.]+), (-?[\d.]+)\), ([-+] to [-+]), det-linear (-?[\d.]+), range \[(-?[\d.]+), (-?[\d.]+)\]", t)
    n = int(re.search(r"robust changes: (\d+)", t).group(1))
    assert n == len(ch), (folder, n, ch)
    return ch, t

def scans_table(folders):
    out = ["| scan folder (`kc87_leg_lambda/`) | D | lambda window | evaluations | noise-robust | robust changes: bracket, orientation as printed, det-linear (estimator range) |", "|---|---|---|---|---|---|"]
    for f in folders:
        rows = rows_of(f); lam = sorted(set(r["lam"] for r in rows)); ch, _ = reading(f)
        d = re.match(r"[\d.]+", f).group(0)
        kc = " (k_c 95)" if "kc95" in f else ""
        cs = "; ".join("(%s, %s), %s, **%s** ([%s, %s])" % c for c in ch) if ch else "none"
        out.append("| `%s` | %s%s | %g to %g | %d | %d | %s |" % (f, d, kc, lam[0], lam[-1], len(rows), sum(1 for r in rows if r["noise_robust"]), cs))
    return "\n".join(out)

def lam_table(folder):
    rows = rows_of(folder); by = {}
    for r in rows: by.setdefault(round(r["lam"], 4), []).append(r)
    out = ["| lambda | hybrid sign | ln\\|det\\| hybrid | float64 sign | ln\\|det\\| float64 |", "|---|---|---|---|---|"]
    for lam in sorted(by):
        r = by[lam][0]; two = " (two evaluations, bit-identical)" if len(by[lam]) > 1 and by[lam][0]["ln"] == by[lam][1]["ln"] and by[lam][0]["f64_ln"] == by[lam][1]["f64_ln"] else (" (two evaluations, DIFFER)" if len(by[lam]) > 1 else "")
        out.append("| %g%s | %+d | %.4f | %+d | %.4f |" % (lam, two, r["sign"], r["ln"], r["f64_sign"], r["f64_ln"]))
    return "\n".join(out)

def para(path, key):
    ls = [l.rstrip("\n") for l in open(path) if key in l]
    assert len(ls) == 1, (path, key, len(ls))
    return ls[0].lstrip("- ")

def main():
    LEG = "22.03125,22.0625,22.09375,22.125,22.15625,22.1875,22.21875,22.25,22.28125,22.3125,22.34375,22.375,22.40625,22.4375,22.46875,22.5,22.5625,22.625,22.6875,22.75,22.8125,22.875"
    prev = "22.15625=22.125,0.490845,0.490686,0.490845,22.25;22.1875=22.125,0.490845,0.490686,0.490845,22.25"
    pred = ("Registered in `kc87_leg_lambda/README.md` before each scan (grid, repeat, rule, readings and their weights), and the rule's prediction and residual are in this section's headline and the table above, "
            "and the README's log line of each scan scores the rest.")
    batch = run("make_batch.py", "22.125,22.15625,22.1875,22.25", "--part=auto", "--leg=" + LEG, "--prev=" + prev, "--rescan=22.125=22.125_rescan", "--delta-rows", "--wide", "--pred=" + ";".join("%s=%s" % (d, pred) for d in ("22.125", "22.15625", "22.1875", "22.25")))
    body = batch.split("\n", 1)[1]                      # without its first line (the old headline)
    branches = run("make_branches.py"); track = run("make_track.py")
    folders = ["22.125", "22.125_rescan", "22.125_low", "22.125_wide", "22.125_high", "22.15625", "22.15625_high", "22.1875", "22.1875_low", "22.1875_mid", "22.21875_full", "22.25", "22.25_low", "22.25_wide", "22.3125_kc95", "22.3125_kc95_high"]
    ch95, _ = reading("22.3125_kc95"); chh95, _ = reading("22.3125_kc95_high")
    ch21, t21 = reading("22.21875_full")
    k95 = K95 + "README.md"
    # part c / c2 status from the files
    cexits = open(L2 + "c/exits_leg2c.txt").read()
    stop = [l.strip() for l in open(L2 + "c/leap.log") if l.startswith("stop at D")][-1]
    last = [json.loads(l) for l in open(L2 + "c/leap.log") if l.startswith("{")][-1]
    cdone = open(L2 + "c/LEG_DONE.txt").read().strip()
    crec = [json.loads(l) for l in open(L2 + "c/l1kc87Lmacm3c.jsonl") if l.strip()]
    c2rec = [json.loads(l) for l in open(L2 + "c2/l1kc87Lmacm3c2.jsonl") if l.strip()]
    c2started = [l for l in open(L2 + "start_cont.log") if "STARTED" in l][-1][:19]
    c2root = re.findall(r"leap87c2 root pid (\d+) ([\d-]+ [\d:]+) UTC", open(L2 + "c2/exits_leg2c2.txt").read())[-1]
    c2pt = [l for l in open(L2 + "c2/exits_leg2c2.txt") if " point D " in l]
    P = []
    a = P.append
    a("**#1025 macm3, k_c 87 leg D 22.125 to 22.25: two l = 1 branches F and S; k_c 95 D 22.3125 wide and high scans; parts c and c2 (@@T@@ UTC 25 Nov).** One comment for every scan since the D 22.0 post (t5's order: the two-branch picture, the D 22.3125 k_c 95 wide and high scans, part c/c2 status; c2's rows go in the next post, at its crossing or every 3 hours).")
    a("")
    a("### What was scanned, and what each scan read\n")
    a("All on the pinned states of my k_c 87 part b2 leg (raw `I1025-macm3/kc87_leg2/b2/`) and the k_c 95 regrid of its D 22.3125 state; hybrid sign scans by `d18_hybsign.py` e089207a, read by `read_lower.py` 89309d3c (`wide_read.py` 29e14fab for the wide ones), repeats by `repeat_check.py` aaf598a9. "
      "Positions are the reader's printed brackets with the det-linear estimate; the estimator range is a spread over interpolation choices, not an enclosure. A root is read by position, and its printed orientation is its rank in position at that D "
      "(the signs read - below both roots, + between, - above), so a crossing of two roots swaps both printed orientations. The D 22.15625 low scan was stopped by t5's order (partial files in `22.15625_low/scan_aborted_0545/`); the D 22.25 refinement was dropped by order and never run.\n")
    a(scans_table(folders))
    a("")
    a("### The two-branch picture (F = lambda_1 of the leg, S = the steep second l = 1 mode)\n")
    a("Reading of the scans above (mine; t5 accepted it, 25 Nov ~09:45 UTC: \"two smooth branches, F (the leg's lambda_1) and S (steep, from above), crossing near D 22.171; printed orientation is rank. Keep F as lambda_1 in the tables; S is a second l = 1 mode\"). "
      "F is the flat branch the whole leg followed; S arrives from above (D 22.125) and falls steeply. Positions are the det-linear estimates (spread, not enclosures); the slopes are differences of those positions.\n")
    a(branches.strip())
    a("")
    a("Per D, every sign change over all scans merged (`make_track.py`):\n")
    a(track.strip())
    a("")
    a("Whether the meeting near D 22.171 is a simple crossing or an avoided one cannot be told from these scans (the two scanned D around it are 0.03125 apart). The two-branch reading supersedes my earlier single-branch readings (README log line 09:40 UTC).\n")
    a("Data from win2's posts, quoted and not mine: at D 22.28125 (k_c 87, my part b2 state) branch S is a simple zero at lambda_S = -0.1976, a `- to +` change, not a pole (comment 7160353778; negative-lambda scan 7158892703); "
      "k_c 95 at D 22.5 (a regrid of the same b2 state) has one `- to +` change in (0.300, 0.340), det-linear 0.339034, nothing else in -0.10 to 0.50 (comment 7160431678); win2's k_c 95 low scan of dh610's D 22.25 state read `-` at every lambda from 0.02 to 0.40, no robust change (comment 7155717522).\n")
    a("### D 22.21875, full scan (lambda 0.02 to 0.50 by 0.02 and a repeat of 0.10; folder `22.21875_full/`)\n")
    a("Source: my part b2 state at D 22.21875 (raw commit f4c8c7b528), `kc87_syscheck_1025.py` exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 and 1, the k_c 79 check refuses it (exit 1), %s. " % open(HERE + "/22.21875_full/VERDICT.txt").read().split(" (")[0].strip()
      + "Reading: %d robust changes, both orientations as printed: " % len(ch21) + "; ".join("(%s, %s) **%s**, det-linear %s (range [%s, %s])" % (c[0], c[1], c[2], c[3], c[4], c[5]) for c in ch21)
      + ". By rank: the lower one (`- to +`) is S, the upper one (`+ to -`) is F. " + re.search(r"repeat check .*", t21).group(0).split("/scan/")[-1].replace("scan_D22.21875_1025.jsonl: ", "repeat: ") + ".\n")
    a(lam_table("22.21875_full"))
    a("")
    a("### k_c 95 at D 22.3125 (regrid of my k_c 87 part b2 state; wide scan -0.10 to 0.50 by 0.04, high scan 0.50 to 0.70 by 0.02)\n")
    a("t5's orders (25 Nov): the k_c 95 D 22.3125 wide scan with the regrid recipe and lambda_0 rule of dh610's lanes; then, after the wide scan, the high scan (\"one '+ to -' by rank above F = S exists at k_c 95; none = not\"). Raw `I1025-macm3/kc95_d223125/` and `kc87_leg_lambda/22.3125_kc95/`, `22.3125_kc95_high/`; the predictions were registered before the regrid and before each scan (`kc95_d223125/README.md`); their scoring, from that README:\n")
    a("- " + para(k95, "**regrid ACCEPTED**").replace("`../kc87_leg_lambda/22.3125_kc95/`", "`kc87_leg_lambda/22.3125_kc95/`"))
    a("")
    w = para(k95, "**the wide scan is read**")
    for o, n in (("`wide_read.txt` here", "`wide_read.txt` in `kc95_d223125/`"), ("(08:10 UTC, above)", "(registered 08:10 UTC)"),
                 ("the signs at 0.46, 0.50 are all '+', and the sign at 0.50 is '+'", "the signs at 0.42, 0.46 and 0.50 are all '+'"),
                 ("(win2's D 22.25 low scan had none at 0.02 to 0.24)", "(win2's low scan of dh610's D 22.25 state: no robust change in 0.02 to 0.40, comment 7155717522)")):
        assert w.count(o) == 1, o
        w = w.replace(o, n)
    a("- " + w)
    a("")
    h = para(k95, "**the high scan is read**")
    o = "`wide_read_high.txt` and `read_lower_high.txt` here"; assert h.count(o) == 1
    a("- " + h.replace(o, "`wide_read_high.txt` and `read_lower_high.txt` in `kc95_d223125/`"))
    a("")
    a("**Wide scan, D 22.3125, k_c 95:**\n")
    a(lam_table("22.3125_kc95"))
    a("")
    a("**High scan, D 22.3125, k_c 95:**\n")
    a(lam_table("22.3125_kc95_high"))
    a("")
    a("Result: one root at k_c 95, D 22.3125, F in (%s, %s), `%s`, det-linear %s (estimator range [%s, %s]); no `+ to -` change up to 0.70, so by t5's rule no S at k_c 95 in (0.50, 0.70] at this D. The chord between win2's k_c 95 roots (0.434264 at D 22.25, quoted from dh610's data in win2's comment 7160431678, and 0.339034 at D 22.5) gives %.4f at D 22.3125 (arithmetic on those two quoted values, not a result), inside my bracket.\n"
      % (ch95[0][0], ch95[0][1], ch95[0][2], ch95[0][3], ch95[0][4], ch95[0][5], 0.434264 + (0.339034 - 0.434264) * (22.3125 - 22.25) / (22.5 - 22.25)))
    a("### Parts c and c2\n")
    a("Part c (`kc87_leg2/c/`, h 0.0625, `--cmax 1e-2`, the new pin 5816d7b3) accepted %d points, D %s to D %s (the table below: psi-constraint %.3e at D %s). It %s at %s, at the constraint bar: `%s`; the rejected D %s row's unrounded psi-constraint is %r (above the bar 1e-2), |F| %.3e (below 1e-8). "
      % (len(crec), crec[0]["D"], crec[-1]["D"], crec[-1]["constraint"], crec[-1]["D"], "ended", re.findall(r"([\d-]+ [\d:]+) UTC", cdone)[0].split(" ")[1] + " UTC with exit 1 (the leap's own stop)", stop, last["D"], last["constraint"], last["F"])
      + "**Discrepancy, mine and fixed:** my starter for part c2 (`start_cont.sh`) compared the printed constraint 1.00e-02 with the bar 1e-02 by `>`, said 'part c2 not needed' at 10:55:25 UTC, and t5 ordered the start by hand and the test fixed to `>=`; the fix was checked by running the extracted test, old and new, on the real stop line (old exit 1, new exit 0) and on three planted lines (all exit 1). "
      "My companion loop `delta_rows_loop.sh` read the same stale line, ended at 10:57:22 UTC and was relaunched at 10:59:28 UTC (it keeps the weak-mode rows of c2).\n")
    a("Part c2 (`kc87_leg2/c2/`: tag l1kc87Lmacm3c2, seeds = part c's last two accepted states D %s and D %s, `--cmax 2e-2`, h 0.0625, to D 24.0, pins and guard, watchdog 3 h per point, crossing stop, cap 12 h) was started by hand at 10:56:26 UTC and its leap started %s UTC (root pid %s); start hc to t5 %s UTC. "
      % (crec[-2]["D"], crec[-1]["D"], c2root[1], c2root[0], c2started)
      + "Rows with psi-constraint above 1e-2 are **REDUCED QUALITY** in every table; the goal past D 22.9 is to locate lambda_1 = 0 approximately, not digits. "
      + "First c2 row (D %s, constraint %.3e, n_null %d): %s; c2's rows go in the next post.\n" % (c2rec[-1]["D"], c2rec[-1]["constraint"], c2rec[-1]["n_null"], "REDUCED QUALITY" if c2rec[-1]["constraint"] > 1e-2 else "within the bar"))
    a("The chain (`scan_chain.sh`) stays held (`HOLD_low2.txt`, `HOLD_refine.txt`) until t5 releases it; the leg's unscanned points (D 22.375 and 22.5 of part b2, part c's and c2's points, and phase 2's in-between points) wait for that.\n")
    a("### The batch of the lambda_1 points (the format of the earlier posts)\n")
    a(body.replace("Each point below carries its own tables.", "Each point below carries its own tables (the first, narrow scan of that point around the chord; the other windows of the same D are in the table of scans above)."))
    return "\n".join(P)

if __name__ == "__main__":
    out = main()
    if "--selftest" in sys.argv:
        assert "@@T@@" in out.split("\n")[0] and out.count("### ") >= 7 and len(out) < 65000, (len(out), out.count("### "))
        print("selftest ok, %d chars" % len(out))
    else:
        sys.stdout.write(out + "\n")
