"""#903 p_min question: the answer's table, from near_null.py's JSONs and vectors in this folder.

One row per base run at its own order (tags k135, k142, k150, k160): order, D, near_null's LU pivot floor (the chain's
p_min), the weak pair (the two smallest, harmonic 3: sigma_1 and its top harmonic), the Delta mode (the vector of
largest Delta share: its sigma and share), the fall per unit D of the pair and of the Delta mode from the same chain's
previous base in the table, and the weak pair's overlap with order 160's at D 229, on the span of its two smallest
(sqrt(o_1^2 + o_2^2)).

Run: python3 pmin_table.py FOLDER
"""
import glob
import json
import os
import re
import sys

import numpy as np

d0 = sys.argv[1]
pat = re.compile(r"nn_(k135|k142|k150|k160)_D([\d.]+)_ks(\d+)\.json$")
rows = []
for p in glob.glob(os.path.join(d0, "nn_*.json")):
    mt = pat.search(os.path.basename(p))
    if not mt or int(mt.group(3)) != int(mt.group(1)[1:]):
        continue
    r = json.load(open(p))
    V = np.load(p.replace("nn_", "V_").replace(".json", ".npy"))
    rows.append((int(mt.group(3)), float(r["D"]), r, V))
rows.sort(key=lambda t: (t[0], t[1]))
ref = next((V for K, D, r, V in rows if K == 160 and D == 229.0), None)
print("| order | D | p_min (LU pivot floor) | weak pair σ₁ (harmonic) | fall per unit D | Δ mode σ (Δ share) "
      "| fall per unit D | overlap with order 160's pair at D 229 |")
print("|---|---|---|---|---|---|---|---|")
prev = {}
for K, D, r, V in rows:
    v = r["vectors"]
    i = int(np.argmax([x["delta"] for x in v]))
    pr = prev.get(K)
    fp = fd = "–"
    if pr and abs(D - pr[0] - 1) < 1e-9:
        fp, fd = f"{pr[1] / v[0]['sigma']:.3g}", f"{pr[2] / v[i]['sigma']:.3g}"
    ov = f"{np.hypot(*(ref[:, :2].T @ V[:, 0])):.3f}" if ref is not None else "–"
    print(f"| {K} | {D:.4f} | {r['pivots'][0]:.2e} | {v[0]['sigma']:.3e} (k{v[0]['top'][0][1]}) | {fp} | "
          f"{v[i]['sigma']:.3e} ({v[i]['delta']:.2f}) | {fd} | {ov} |")
    prev[K] = (D, v[0]["sigma"], v[i]["sigma"])
