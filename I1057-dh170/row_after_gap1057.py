#!/usr/bin/env python3
"""#1057: the facts of D 260.9271, the first accepted state of dh370's leg 13, which row949.py cannot print (its interval slope is empty: the previous state D 260.8483 is
unclassified). Reads the near_null JSONs of this folder and the registered prediction values (prediction_D260.9271.txt); prints, changes nothing.
    row_after_gap1057.py"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from row949 import picks  # noqa: E402


def rec(D):
    return json.load(open(os.path.join(HERE, f"c3b_ks293_D{D}.json")))


a, b = rec("260.8483"), rec("260.9271")
da, db = a["D"], b["D"]
va, vb = a["vectors"], b["vectors"]
d, k2 = picks(b)
print(f"D {db:.4f}: the Delta vector (largest share) is v{d + 1}, sigma_2 is v{k2 + 1}")
for i in range(2):
    print(f"  v{i + 1}: sigma {vb[i]['sigma']:.6e} (D 260.8483: {va[i]['sigma']:.6e}), Delta share {vb[i]['delta']:.4f} (D 260.8483: {va[i]['delta']:.4f}), conv {vb[i]['conv']:.2e}")
print(f"  sum of the two lowest vectors' Delta shares: {vb[0]['delta'] + vb[1]['delta']:.4f} (D 260.8483: {va[0]['delta'] + va[1]['delta']:.4f}); v3+v4: {vb[2]['delta'] + vb[3]['delta']:.4f} ({va[2]['delta'] + va[3]['delta']:.4f})")
dd = db - da
for i, nm in enumerate(("lowest", "upper")):
    print(f"  sigma_{nm} slope over D 260.8483 to {db:.4f} (dD {dd:.4f}): {-math.log(vb[i]['sigma'] / va[i]['sigma']) / dd:.4f}")
print(f"  sigma_2/sigma_Delta (stopcheck's ratio) {vb[k2]['sigma'] / vb[d]['sigma']:.4f}; upper/lowest {vb[1]['sigma'] / vb[0]['sigma']:.4f} (D 260.8483: {va[1]['sigma'] / va[0]['sigma']:.4f})")
print(f"  pinned Delta component {b['step_pinned']['delta']:+.3e}")
pred = open(os.path.join(HERE, "prediction_D260.9271.txt")).read().splitlines()
for w in "AB":
    i = next(j for j, l in enumerate(pred) if l.startswith(f"window {w}"))
    D_, lo, up, ra, sh = pred[i + 2].split()
    lo, up, ra, sh = float(lo), float(up), float(ra), float(sh)
    print(f"  window {w} registered: sigma_lowest {lo:.4e} (measured {vb[0]['sigma']:.4e}, {100 * (vb[0]['sigma'] / lo - 1):+.2f}%), sigma_upper {up:.4e} ({vb[1]['sigma']:.4e}, {100 * (vb[1]['sigma'] / up - 1):+.2f}%), "
          f"ratio {ra:.3f} ({vb[1]['sigma'] / vb[0]['sigma']:.3f}), share of the lowest {sh:.3f} (measured {vb[0]['delta']:.3f}, miss {vb[0]['delta'] - sh:+.3f})")
