#!/usr/bin/env python3
"""#949: sigma_Delta, sigma_2 (the second-lowest singular value of near_null.py, vector 2) and sigma_pair of the newest ks_chain3b states, with the interval slopes
(-d ln sigma / dD) against the previous states (coordinator's request, hc 2026-11-19: report sigma_Delta, sigma_2 and sigma_pair at D 247.28 with the slope against the last three states).
    python sig2_949.py [N=5]       the last N states of ks_chain3b (c3b_*.json) in D order, one row each, then the slopes of the last three intervals"""
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
rows = []
for p in glob.glob(os.path.join(HERE, "c3b_ks*_D*.json")):
    r = json.load(open(p))
    v = r["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    pair = [i for i in range(len(v)) if i != d and {("p1", 3), ("m_h", 3)} <= {(b, k) for b, k, _ in v[i]["top"]}]
    others = sorted((i for i in range(len(v)) if i != d and i not in pair), key=lambda i: v[i]["sigma"])
    rows.append(dict(D=float(r["D"]), sd=v[d]["sigma"], share=v[d]["delta"], s2=v[others[0]]["sigma"], s2v=others[0] + 1, s2share=v[others[0]]["delta"],
                     sp=math.sqrt(v[pair[0]]["sigma"] * v[pair[1]]["sigma"]) if len(pair) == 2 else float("nan"),
                     conv=[v[d]["conv"], v[others[0]]["conv"]] + [v[i]["conv"] for i in pair], dvec=d + 1))
rows.sort(key=lambda r: r["D"])
rows = rows[-N:]
print(f"{'D':>9} {'sigma_Delta':>12} {'Dshare':>7} {'sigma_2':>12} {'(vec, Dshare)':>14} {'s2/sD':>6} {'sigma_pair':>12}   convergence (Delta, sigma_2, pair)")
for r in rows:
    print(f"{r['D']:9.4f} {r['sd']:12.4e} {r['share']:7.3f} {r['s2']:12.4e} {'(' + str(r['s2v']) + ', ' + format(r['s2share'], '.3f') + ')':>14} {r['s2'] / r['sd']:6.2f} {r['sp']:12.4e}   "
          + " ".join(f"{c:.0e}" for c in r["conv"]))
print("\nslopes -d ln sigma / dD over the interval ending at each state (positive = falling):")
for a, b in zip(rows, rows[1:]):
    dD = b["D"] - a["D"]
    sl = lambda k: -math.log(b[k] / a[k]) / dD
    print(f"  {a['D']:9.4f} -> {b['D']:9.4f} (dD {dD:.4f}): sigma_Delta {sl('sd'):+.4f}, sigma_2 {sl('s2'):+.4f}, sigma_pair {sl('sp'):+.4f}")
