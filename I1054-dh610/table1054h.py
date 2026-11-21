#!/usr/bin/env python3
"""table1054h.py TAG [TAG ...]: job 5's report, one row per D: the flag-on polish of job 4's flag-off state (resolve<TAG>_r1.log) and the flag-off re-polish of it
(resolve<TAG>_r0.log), each read by classify.py (notes/EXACT_RECIP.md 3.5), and where the flag-on one converged the change of delta_job5_<TAG>.json (job 4's
flag-off state -> the flag-on base) and of delta<TAG>.json (the flag-off re-polish -> the flag-on base) with its share of the nearest row's quoted error and its ratio to
+3.290002e-13, the change at D 241.96."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify  # noqa: E402

H = os.path.dirname(os.path.abspath(__file__)) + "/"
REF = 3.290002e-13
print("| D | flag off, re-polish of job 4's state | flag on | change vs job 4's state | change vs the re-polish | nearest row, quoted error | share (vs job 4's state) | change / 3.290002e-13 |")
print("|---|---|---|---|---|---|---|---|")


def cell(r):
    if r["reading"] == "converged":
        return f"converged, {r['steps']} steps, max\\|F\\| {r['last_maxF']:.1e}"
    if r["reading"] == "stopped at start":
        return f"stopped at its start, pinned max\\|F\\| {r['start_maxF']}"
    if r["reading"] == "not converged":
        f = r.get("first_step")
        return (f"not converged, {r['steps']} steps, last max\\|F\\| {r['last_maxF']:.1e}" + (" (--qd_it cap)" if r.get("qd_it_cap") else "")
                + (f", first step \\|dz\\| {f[1]}" if f else "") + f", {r['projection_failed_lines']} projection failed lines")
    return r["reading"]


def load(p):
    return json.load(open(p)) if os.path.exists(p) else None


for T in sys.argv[1:]:
    r0 = classify(H + f"resolve{T}_r0.log") if os.path.exists(H + f"resolve{T}_r0.log") else dict(reading="no log")
    r1 = classify(H + f"resolve{T}_r1.log") if os.path.exists(H + f"resolve{T}_r1.log") else dict(reading="no log")
    ch = ch0 = row = share = ratio = "none"
    if r1["reading"] == "converged":
        j, j0 = load(H + f"delta_job5_{T}.json"), load(H + f"delta{T}.json")
        if j:
            ch = f"{j['change']:+.6e}"
            ratio = f"{j['change'] / REF:.3g}"
            e = (j.get("csv_rows") or [None])[0]
            if e:
                row = f"D {float(e['D']):.4f}, {float(e['err']):.1e} ({e['err_kind']})"
                share = f"{abs(j['change']) / float(e['err']):.2e}"
        if j0 and r0["reading"] == "converged":
            ch0 = f"{j0['change']:+.6e}"
    print(f"| {T} | {cell(r0)} | {cell(r1)} | {ch} | {ch0} | {row} | {share} | {ratio} |")
