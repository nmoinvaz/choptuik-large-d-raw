#!/usr/bin/env python3
"""Per-cut summary of the ulp-replica spreads of #588 (reads replicas_588.jsonl through analyze_588.analyze): for each kf the number of zeros, the range and the geometric mean of the replica
spread s, the range of s / own estimate, the number flagged (s > 3 x estimate), the median ratio of the replicas' own estimates to s, and the growth of the geometric mean between cuts.
usage: python percut_588.py"""
import json, math, os, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_588 as A, replicas_588 as RP
rows = A.analyze(RP.circles(), [json.loads(l) for l in open(os.path.join(HERE, "replicas_588.jsonl"))])
g = lambda v: math.exp(sum(map(math.log, v)) / len(v))
print("| kf | zeros | replica spread s, range | s, geometric mean | s / own estimate, range | flagged | median (replicas' own estimate / s) | spread of s in the ensemble (std of ln s) |\n|---|---|---|---|---|---|---|---|")
gm = {}
for kf in (22, 25, 27):
    R = [r for r in rows if r["kf"] == kf]
    s = [r["s"] for r in R]
    gm[kf] = g(s)
    print(f"| {kf} | {len(R)} | {min(s):.1e} to {max(s):.1e} | {g(s):.2e} | {min(r['ratio'] for r in R):.1f} to {max(r['ratio'] for r in R):.1f} | {sum(r['flag'] for r in R)} | {st.median(r['rep_est'] / r['s'] for r in R):.2f} | {st.pstdev([math.log(x) for x in s]):.2f} |")
print(f"\ngrowth of the geometric mean: kf 22 to 25 x{gm[25] / gm[22]:.1f} (x{(gm[25] / gm[22]) ** (1 / 3):.1f} a step), kf 25 to 27 x{gm[27] / gm[25]:.1f} (x{(gm[27] / gm[25]) ** 0.5:.1f} a step)")
print(f"replicas: {sum(r['n'] for r in rows)} shifted used of {sum(r['n_all'] for r in rows)}; controls bit equal {sum(r['ctl_ok'] for r in rows)} of {len(rows)}")
ev = [json.loads(l)["sec"] for l in open(os.path.join(HERE, "replicas_588_evals.jsonl"))]
print(f"determinants {len(ev)}, median {st.median(ev):.1f} s (min {min(ev):.1f}, max {max(ev):.1f}), {sum(ev) / 3600:.1f} h of single-thread time")
