"""I902-mac post-hoc readings (not criteria; written after the runs, to describe why the verdict is "neither").

Reads the near_null.py JSONs, the vectors V_D<d>_ks<K>.npy and model.log, as sigma.py does, and prints for D 237.13,
249.01 and 253.80 at each ks K:
  g      ln g(K) - ln g(250) against the model's ln f(K), mu 1 (the model: g follows f, so the two agree)
  dF     ln max|dF_horizon(K)| - ln max|dF_horizon(250)|, the change of the horizon rows of F at z from ks 130 to K,
         against the same ln f(K) (the model: the omitted tail grows as f)
  step   Delta's pinned Newton step at z (near_null.py's step_pinned), the linear estimate of Delta's move to the
         root at ks K
  sigma_3  its Delta share, which says which mode sigma_3 by index is at each K
  h1, h3 the ks 130 vector of the smallest sigma among those with a Delta share below 0.1 whose largest component
         is of harmonic 1 (h1), or 3 (h3), followed by overlap to each K: ln sigma - ln sigma(130) against the model's
         P(K), mu 1 for h1 and mu 3 for h3. The overlap printed is the largest with one vector and, beside it, with the
         best two (the modes come in near pairs).

Run: python3 posthoc.py FOLDER
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DS = {"237": 237.13, "249": 249.01, "253": 253.80}
KS = (130, 160, 200, 250)


def model(path):
    import re
    pat = re.compile(r"^\s+D (\d+\.\d+) Re s .*mu 1: peak \d+, ln f (\S+) (\S+) (\S+) (\S+); mu 3: peak \d+, "
                     r"ln f (\S+) (\S+) (\S+) (\S+)")
    out = {}
    for line in open(path):
        mt = pat.match(line)
        if mt:
            v = [float(x) for x in mt.groups()[1:]]
            out[round(float(mt.group(1)), 2)] = {1: dict(zip(KS, v[:4])), 3: dict(zip(KS, v[4:]))}
    return out


d0 = sys.argv[1]
lnf = model(os.path.join(d0, "model.log"))
print("posthoc: readings after the runs (not criteria); ln f from model.log")
for d, D in DS.items():
    r = {K: json.load(open(os.path.join(d0, f"nn_D{d}_ks{K}.json"))) for K in KS}
    V = {K: np.load(os.path.join(d0, f"V_D{d}_ks{K}.npy")) for K in KS}
    f1, f3 = lnf[D][1], lnf[D][3]
    lg = {K: math.log(r[K]["grip"]["two"]) for K in KS}
    dF = {K: r[K]["rows"]["blocks"]["horizon"]["F"] for K in KS[1:]}
    v130 = r[130]["vectors"]
    pick = {}
    for h in (1, 3):
        pick[h] = min((i for i, v in enumerate(v130) if v["delta"] < 0.1 and v["top"][0][1] == h),
                      key=lambda i: v130[i]["sigma"])
        print(f"  D {D:.2f}: h{h} is sigma_{pick[h] + 1} at ks 130 ({v130[pick[h]]['sigma']:.3e}, Delta share "
              f"{v130[pick[h]]['delta']:.1e}, top {v130[pick[h]]['top'][0][0]} k{v130[pick[h]]['top'][0][1]})")
    for K in KS:
        line = (f"    ks {K}: g {lg[K] - lg[250]:+8.3f} (ln f {f1[K] - f1[250]:+7.2f})")
        line += (f"; dF {math.log(dF[K] / dF[250]):+7.3f} (ln f {f1[K] - f1[250]:+7.2f}), max|dF| {dF[K]:.2e}"
                 if K in dF else "; dF -")
        line += f"; step Delta {r[K]['step_pinned']['delta']:+.3e}"
        line += f"; sigma_3 Delta share {r[K]['vectors'][2]['delta']:.1e}"
        for h, fm in ((1, f1), (3, f3)):
            i0 = pick[h]
            ov = np.abs(V[K].T @ V[130][:, i0])
            o = np.argsort(-ov)
            j = int(o[0])
            ls = math.log(r[K]["vectors"][j]["sigma"] / v130[i0]["sigma"])
            P = fm[K] - fm[130]
            line += (f"; h{h} at sigma_{j + 1} (overlap {ov[j]:.2f}, two {math.hypot(ov[o[0]], ov[o[1]]):.2f}) "
                     f"{ls:+.3f} (P mu {h} {P:+.2f}" + (f", {ls / P:.2f} of it)" if K != 130 else ")"))
        print(line)
