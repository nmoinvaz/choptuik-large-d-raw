"""#903 grip, closing: how fast the Delta mode falls with D along each fixed-order chain, at its own order and at ks 200.

From near_null.py's JSONs and vectors here (tags k135, k142): at each base the Delta mode at the own order is the
vector of largest Delta share, and at ks 200 the vector of largest overlap with it (lift.py's rule). Printed per chain
and order: sigma_Delta at each base, the fall per unit D between consecutive bases, exp(-(d ln sigma / dD)), and the
least-squares fall over all the chain's bases from D 229, with the largest |residual| of ln sigma from that line. The
same for the harmonic-3 pair (sigma_1 at the own order). Compare #941 (dh370): order 240's converged Delta mode falls
1.51 per unit D.

Check (can fail): planted, sigma = 3e-14 * 2^-(D - 229) at the k135 bases' D is read as a fall of 2 to 1e-9 with
residual below 1e-9; its control --mutate=planted multiplies one sigma by 10 and must fail that bar.

Run: python3 fall_rate.py FOLDER [--mutate=planted]. Exit 1 when the check fails.
"""
import glob
import json
import math
import os
import re
import sys

import numpy as np

d0 = sys.argv[1]
mut = "--mutate=planted" in sys.argv
pat = re.compile(r"nn_(k135|k142)_D([\d.]+)_ks(\d+)\.json$")


def fit(D, s):
    D, y = np.asarray(D), np.log(np.asarray(s))
    A = np.c_[D, np.ones_like(D)]
    c = np.linalg.lstsq(A, y, rcond=None)[0]
    return math.exp(-c[0]), float(np.abs(y - A @ c).max())


rows = {}
for p in glob.glob(os.path.join(d0, "nn_*.json")):
    m = pat.search(os.path.basename(p))
    if m and float(m.group(2)) >= 229:
        rows.setdefault((m.group(1), m.group(2)), {})[int(m.group(3))] = p
for tag in ("k135", "k142"):
    bases = sorted((float(d), runs) for (t, d), runs in rows.items() if t == tag and len(runs) == 2)
    Ds, sd_own, sd_200, sp = [], [], [], []
    for D, runs in bases:
        own = min(runs)
        a, b = json.load(open(runs[own])), json.load(open(runs[200]))
        i = int(np.argmax([v["delta"] for v in a["vectors"]]))
        Va, Vb = (np.load(r.replace("nn_", "V_").replace(".json", ".npy")) for r in (runs[own], runs[200]))
        j = int(np.abs(Vb.T @ Va[:, i]).argmax())
        Ds.append(D); sd_own.append(a["vectors"][i]["sigma"]); sd_200.append(b["vectors"][j]["sigma"])
        sp.append(a["vectors"][0]["sigma"])
    print(f"{tag} (own order {own}), bases D " + ", ".join(f"{D:.4f}" for D in Ds))
    for name, s in ((f"Delta mode at {own}", sd_own), ("Delta mode at 200", sd_200), (f"pair at {own}", sp)):
        steps = [math.exp(-math.log(s[k + 1] / s[k]) / (Ds[k + 1] - Ds[k])) for k in range(len(s) - 1)]
        r, res = fit(Ds, s)
        print(f"  {name}: sigma " + ", ".join(f"{x:.3e}" for x in s) + "; fall per unit D between bases "
              + ", ".join(f"{x:.3f}" for x in steps) + f"; least squares {r:.3f} (largest |residual| in ln {res:.3f})")
for (t, d), runs in sorted(rows.items()):     # equal D on both chains: the ks 200 grip and the own-order one
    other = rows.get(("k142", d))
    if t == "k135" and other and 200 in runs and 200 in other:
        a, b = (json.load(open(r[200])) for r in (runs, other))
        print(f"D {d}: g at ks 200 on order 135's root {a['grip']['two']:.10e}, on order 142's {b['grip']['two']:.10e}, "
              f"relative difference {abs(a['grip']['two'] / b['grip']['two'] - 1):.1e}; Delta's pinned step at 200 "
              f"{a['step_pinned']['delta']:+.3e} and {b['step_pinned']['delta']:+.3e}")
Dp = [229.1312, 239.1312, 244.1312, 249.1312, 254.7003]
sp = [3e-14 * 2.0 ** -(D - 229) for D in Dp]
if mut:
    sp[2] *= 10
r, res = fit(Dp, sp)
ok = abs(r - 2) < 1e-9 and res < 1e-9
print(f"check{' (--mutate=planted)' if mut else ''}: planted fall 2 read as {r:.12f}, residual {res:.2e}: "
      f"{'pass' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
