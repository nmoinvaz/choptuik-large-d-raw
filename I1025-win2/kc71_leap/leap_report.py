#!/usr/bin/env python3
"""leap_report.py [DIR]: the report of the k_c 71 leap (#1025 kc71_leap) from states/l1kc71Lw1025.jsonl (the leap's converged points) and leap.log: per point D, h, |F|, |F| at the secant start, steps, the psi-constraint (cap 1e-2),
seconds, and the fold watch: the smallest regular singular value of J (sv_reg_small[0]), the tangent's size |J^+ dF/dn| (tan_norm, which diverges at a fold), the smallest singular value of the bordered matrix (sv_B_min), the fold candidate's
|cos| (cos_fold) and sv_fold, the number of near-null singular values (n_null); the events of leap.log (h halvings, the fold watch lines, failures, the stop or 'reached'); extremes; and the k_c 63 records (I1025-mac/d18) at D 18.4375 and 18.5 beside."""
import json
import os
import re
import sys

H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
RAWQ = "D:/choptuik-large-d-raw-push/I1025-mac/d18/"
rows = [json.loads(x) for x in open(H + "states/l1kc71Lw1025.jsonl") if x.strip()] if os.path.exists(H + "states/l1kc71Lw1025.jsonl") else []
log = open(H + "leap.log", errors="replace").read() if os.path.exists(H + "leap.log") else ""
print("| D | h | \\|F\\| | \\|F\\| at the secant start | steps | psi-constraint | s | sigma_reg (smallest regular sv of J) | \\|J+ dF/dn\\| | sv_B_min | cos_fold | sv_fold | n_null |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| %.6g | %.6g | %.3e | %.3e | %d | %.3e | %d | %.4e | %.4g | %.4e | %.3f | %.2e | %d |" % (
        r["D"], r["h"], r["F"], r["F_start"], r["steps"], r["constraint"], r["seconds"], r["sv_reg_small"][0], r["tan_norm"], r["sv_B_min"], r["cos_fold"], r["sv_fold"], r["n_null"]))
print()
if rows:
    c = max(rows, key=lambda r: r["constraint"])
    sv = min(rows, key=lambda r: r["sv_reg_small"][0])
    tn = max(rows, key=lambda r: r["tan_norm"])
    s = [r["seconds"] for r in rows]
    print("%d converged points, D %.6g to %.6g; seconds per point %d to %d (mean %.0f, sum %d)" % (len(rows), rows[0]["D"], rows[-1]["D"], min(s), max(s), sum(s) / len(s), sum(s)))
    print("psi-constraint: maximum %.3e at D %.6g (cap 1e-2); last %.3e at D %.6g" % (c["constraint"], c["D"], rows[-1]["constraint"], rows[-1]["D"]))
    print("fold watch: smallest sigma_reg %.4e at D %.6g (first %.4e, last %.4e); largest |J+ dF/dn| %.4g at D %.6g (first %.4g, last %.4g); smallest sv_B_min %.4e" % (
        sv["sv_reg_small"][0], sv["D"], rows[0]["sv_reg_small"][0], rows[-1]["sv_reg_small"][0], tn["tan_norm"], tn["D"], rows[0]["tan_norm"], rows[-1]["tan_norm"], min(r["sv_B_min"] for r in rows)))
ev = [x for x in log.splitlines() if x.startswith(("fold watch:", "failed at D", "stop at D", "reached D"))]
print("events in leap.log (fold watch halvings, failures, stop, reached): %s" % (ev if ev else "none"))
print("h values used: %s" % sorted({r["h"] for r in rows}))
print()
print("the k_c 63 leap's records beside (I1025-mac/d18/l1kc63Wm1025.jsonl):")
for l in open(RAWQ + "l1kc63Wm1025.jsonl"):
    r = json.loads(l)
    if r["D"] in (18.4375, 18.5):
        print("  D %.4f k_c 63: |F| %.4e, steps %d, psi-constraint %.3e, sigma_reg %.4e, |J+ dF/dn| %.4g, sv_B_min %.4e, n_null %d" % (
            r["D"], r["F"], r["steps"], r["constraint"], r["sv_reg_small"][0], r["tan_norm"], r["sv_B_min"], r["n_null"]))
