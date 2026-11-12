#!/usr/bin/env python3
"""Post hoc (not one of P1 to P8): the replica spread per odd harmonic cut. By #498 an even kf is the odd cut below it (plow_odd keeps the odd harmonics k <= kf), so the cuts (21, 22), (23, 24),
(25, 26), (27, 28), (29, 30) are five distinct operators. Per cut the spread s of analyze_cut.py; per pair the geometric mean of the available spreads (a pair of two spreads gives two independent
draws; kf 27 has no lambda_phys circle in #588, kf 28 stands for it); then the ratio between neighbouring odd cuts, the geometric mean of those ratios, and the two criteria of hypothesis_pair.json.
usage: python odd_harmonics.py   (reads cut_588.jsonl and ../replicas_588.jsonl)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_cut as A
recs = [json.loads(l) for l in open(os.path.join(HERE, "cut_588.jsonl"))]
old = [json.loads(l) for l in open(A.OLD)]
rows = A.analyze(recs, old)
s = {kf: rows[kf]["s"] for kf in rows}
pairs = [(21, (21, 22)), (23, (23, 24)), (25, (25, 26)), (27, (28,)), (29, (29,))]
pooled = {}
print("| odd cut | spreads used (kf: s) | pooled s (geometric mean) | ratio to the previous odd cut |")
print("|---|---|---|---|")
prev = None
rat = []
for odd, ks in pairs:
    g = math.exp(sum(math.log(s[k]) for k in ks) / len(ks))
    pooled[odd] = g
    r = g / prev if prev else None
    if r:
        rat.append(r)
    print(f"| {odd} | " + ", ".join(f"{k}: {s[k]:.3e}" for k in ks) + f" | {g:.3e} | " + (f"{r:.2f}" if r else "") + " |")
    prev = g
gm = math.exp(sum(math.log(r) for r in rat) / len(rat))
print(f"\ngeometric mean of the four ratios between neighbouring odd cuts: {gm:.2f} (range {min(rat):.2f} to {max(rat):.2f}); s(29) / s(21) = {pooled[29] / pooled[21]:.0f} over 4 odd steps = {(pooled[29] / pooled[21]) ** 0.25:.2f} a step")
h1 = s[28] / s[26]
h2 = s[29] / s[28]
print(f"hypothesis_pair.json: H1 s(28) / s(26) = {h1:.2f} (criterion 3 to 15): {'holds' if 3 <= h1 <= 15 else 'FAILS'}")
print(f"hypothesis_pair.json: H2 s(29) / s(28) = {h2:.2f} (H_pair 4 to 20; the smooth model 1.7 to 4.2): " + ("H_pair supported" if 4 <= h2 <= 20 else ("H_smooth supported" if 1.5 <= h2 <= 3.5 else "neither")))
nxt = pooled[29] * gm
print(f"extrapolated by the same ratio: s(31) about {nxt:.1e}" + (" (above 1e-4)" if nxt > 1e-4 else "") + "; s(29) = " + f"{pooled[29]:.2e} is " + ("below" if pooled[29] < 1e-4 else "above") + " 1e-4")
