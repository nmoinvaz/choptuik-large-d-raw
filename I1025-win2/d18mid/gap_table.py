#!/usr/bin/env python3
"""gap_table.py [DIR]: #1025 d18mid on win2: the robust sign changes (orientation, bracket, estimator range) of the D 18.1875 hybrid scan of this folder (scan_D18.1875_A.jsonl and _B.jsonl; D 18.0625 is win2b's)
beside the earlier scans of the pair (I1025-mac/d18: D 18, D 18.25, D 18.5), all read by xfkappa's reader (d18d_read.py, blob 6b608903: the same merge, robust-change and estimator-range code), and the gap
between the pair's two roots against D. The gap interval is [lower bound of the upper root's range - upper bound of the lower root's range, upper bound of the upper root - lower bound of the lower root]; it is
information (the estimator range is not a bound, AGENTS.md: say what an error bar is). win2b's D 18.0625 and winb's D 18.125 are not here; the coordinator reads the gap against D with them.
Repeated points (lambda 1.75, in both processes): the reader's rule, same sign and ln|det| within 1e-6; a disagreement prints STOP-level and exits 2.
Control: the reader on the D 18 scan must give roots near 1.775 (- to +) and 1.807 (+ to -) and on the D 18.25 scan one root near 1.7425 (- to +), each within 0.005, the numbers in the coordinator's hc; else exit 1."""
import json
import os
import sys

RAWQ = "D:/choptuik-large-d-raw-push/I1025-mac/d18/"
sys.path.insert(0, RAWQ)
H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
import d18d_read as rr  # noqa: E402  (its module level reads sys.argv only for the --mutate and --above flags)

SETS = [
    (18.0, [RAWQ + "d18_scan_1025.jsonl", RAWQ + "d18_scanlow_1025.jsonl"], "I1025-mac/d18 (1.55 to 1.90)"),
    (18.1875, [H + "scan_D18.1875_A.jsonl", H + "scan_D18.1875_B.jsonl"], "this folder (1.70 to 1.95, two processes)"),
    (18.25, [RAWQ + "d1825_scan_1025.jsonl"], "I1025-mac/d18 (1.55 to 1.95)"),
    (18.5, [RAWQ + "d185_scan_1025.jsonl"], "I1025-mac/d18 (1.55 to 1.90)"),
]


def load(files, D):
    rows = []
    for f in files:
        if not os.path.exists(f):
            continue
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                assert r["D"] == D, "%s: D %s is not %s" % (f, r["D"], D)
                rows.append(r)
    return rows


out = []
res = {}
repl = []
print("| D | source | points | robust changes: orientation, bracket, det-linear, estimator range | minima of ln\\|det\\| without a sign change | gap interval (upper - lower root) |")
print("|---|---|---|---|---|---|")
for D, files, src in SETS:
    rows = load(files, D)
    if not rows:
        print("| %g | %s | 0 | no scan file | | |" % (D, src))
        continue
    S, rep = rr.merge(rows)
    r = rr.read(S, rep, None, lambda *a: None)
    rob, non = rr.rd.changes(S)
    mins = rr.rc.minima(S, rob + non)
    free = [(round(m["lam"], 2), round(m["depth"], 4)) for m in mins if not m["beside"]]
    roots = r["roots"]
    res[D] = roots
    if rep:
        repl.append((D, rep))
    bad = [x["lam"] for x in S if not x["noise_robust"]]
    ch = "; ".join("%s (%.2f, %.2f), %.6f, [%.6f, %.6f]" % (x["orient"], x["br"][0], x["br"][1], x["lin"], x["lo"], x["hi"]) for x in roots) or "none"
    if non:
        ch += "; not counted (touch a non-robust point): " + ", ".join("(%.2f, %.2f)" % c["br"] for c in non)
    gap = ""
    if len(roots) >= 2:
        lo, up = roots[0], roots[-1]
        gap = "[%.6f, %.6f]" % (up["lo"] - lo["hi"], up["hi"] - lo["lo"])
    pts = "%d (%.2f to %.2f)%s" % (len(S), S[0]["lam"], S[-1]["lam"], "; not noise-robust: %s" % bad if bad else "")
    print("| %g | %s | %s | %s | %s | %s |" % (D, src, pts, ch, free or "none", gap or "-"))
print()
bad_rep = False
for D, rp in repl:
    print("repeated points at D %g (the same lambda in both processes; same sign and ln|det| within 1e-6): %s" % (D, [(k, "agree" if a else "DISAGREE", "%+.1e" % d) for k, a, d in rp]))
    bad_rep = bad_rep or any(not a for _, a, _ in rp)
ok = True
def near(roots, i, orient, x):
    return len(roots) > i and roots[i]["orient"] == orient and abs(roots[i]["lin"] - x) < 0.005

c1 = 18.0 in res and len(res[18.0]) == 2 and near(res[18.0], 0, "- to +", 1.775) and near(res[18.0], 1, "+ to -", 1.807)
c2 = 18.25 in res and len(res[18.25]) == 1 and near(res[18.25], 0, "- to +", 1.7425)
print("control: the reader on the D 18 scan gives roots near 1.775 (- to +) and 1.807 (+ to -): %s" % ("ok" if c1 else "FAILED"))
print("control: the reader on the D 18.25 scan gives one root near 1.7425 (- to +): %s" % ("ok" if c2 else "FAILED"))
if not (c1 and c2):
    sys.exit(1)
if bad_rep:
    print("STOP-level: a repeated point disagrees with its earlier evaluation")
    sys.exit(2)
