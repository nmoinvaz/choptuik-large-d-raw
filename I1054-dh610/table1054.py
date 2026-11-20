#!/usr/bin/env python3
"""table1054.py SUFFIX TAG [TAG ...]: a markdown table of the flag-off (resolve<TAG>_r0.log) and flag-on (resolve<TAG>_r<SUFFIX>.log, SUFFIX 1 or 1b) polishes
read by classify.py, with the change of delta<TAG>[b].json and its share of the nearest row's quoted error. SUFFIX 1b reads delta<TAG>b.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify  # noqa: E402

H = os.path.dirname(os.path.abspath(__file__)) + "/"
suf, tags = sys.argv[1], sys.argv[2:]
print("| D | flag off | flag on | change (on - off) | nearest row, quoted error | share |")
print("|---|---|---|---|---|---|")


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


for T in tags:
    r0 = classify(H + f"resolve{T}_r0.log")
    r1 = classify(H + f"resolve{T}_r{suf}.log")
    jp = H + f"delta{T}{'b' if suf == '1b' else ''}.json"
    ch = row = share = "none"
    if r0["reading"] == "converged" and r1["reading"] == "converged" and os.path.exists(jp):
        j = json.load(open(jp))
        ch = f"{j['change']:+.6e}"
        rows = j.get("csv_rows") or []
        if rows:
            e = rows[0]
            row = f"D {float(e['D']):.4f}, {float(e['err']):.1e} ({e['err_kind']})"
            share = f"{abs(j['change']) / float(e['err']):.2e}"
    print(f"| {T} | {cell(r0)} | {cell(r1)} | {ch} | {row} | {share} |")
