#!/usr/bin/env python3
"""#404: fit/summary_<D>.md from fit_analysis_<D>.txt, fit/roots_32xN_<D>.log and the records. usage: python summary_404.py D54.9961"""
import json
import re
import sys

D = sys.argv[1]
print("| N | root a - hp | root b - hp | spread a - b | E(N) | max abs(z_b - z_a) | max abs(B(e,e)) / max abs(e) | Newton steps a, b | seconds a, b | peak GB a, b |")
print("|---|---|---|---|---|---|---|---|---|---|")
an = open(f"fit_analysis_{D}.txt").read()
dval = {"D60.0020": 60.001952, "D54.9961": 54.996085, "D50.0075": 50.007491, "D40.0201": 40.020065}[D]
for N in (99, 103, 107, 111, 115, 119, 123):
    m = re.search(rf"\| {N} \| ([+\-0-9.e]+) \| ([+\-0-9.e]+) \| ([+\-0-9.e]+) \| ([0-9.e\-]+) \|", an)
    ea, eb, dab, E = m.groups()
    t = open(f"fit/roots_32x{N}_{D}.log").read()
    mz = re.search(r"max\|z2 - z1\| ([0-9.e\-+]+)", t).group(1)
    mb = re.search(r"max\|B\(e, e\)\| / max\|e\| ([0-9.e\-+]+)", t).group(1)
    rec = {}
    for tag in ("a101", "b121"):
        for ln in open(f"roots/{tag}_32x{N}.jsonl"):
            r = json.loads(ln)
            if abs(r["D"] - dval) < 1e-5:
                rec[tag] = r
    print(f"| {N} | {ea} | {eb} | {dab} | {E} | {mz} | {mb} | {len(rec['a101']['products'])}, {len(rec['b121']['products'])} | {rec['a101']['secs']:.0f}, {rec['b121']['secs']:.0f} | {rec['a101']['rss_peak_gb']}, {rec['b121']['rss_peak_gb']} |")
