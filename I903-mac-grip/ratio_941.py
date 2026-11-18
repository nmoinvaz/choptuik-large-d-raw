"""#941's discrepancy: sigma_Delta / sigma_pair on dh610's order-160 states, at order 160 and at order 200.

dh370 (#941) reads 176-304 at order 160; xfchecks's #941 comment read 0.33 at order 200. Per base (D 229, 230, 231)
and order (160, and 200 where run), from near_null.py's JSONs and vectors here: the Delta mode is the vector of
largest Delta share; the harmonic-3 pair is the two order-160 smallest (sigma_1, sigma_2, top harmonic 3), and at
order 200 the two vectors whose span holds most of order-160's pair (largest sqrt(o_1^2 + o_2^2) per vector).
Printed: each label's index, sigma, Delta share and top harmonic, the pair's span overlap with order 160's, and
sigma_Delta / sigma_pair (the pair's smaller sigma).

Check (can fail): the labels are unambiguous at every row: the Delta mode's share is at least 0.5 and is not in the
pair, each pair member's overlap with order 160's pair span is at least 0.9. Control --mutate=labels takes the pair at
order 200 as its sigma_1, sigma_2 (the order-160 rule applied blindly), which must fail.

Run: python3 ratio_941.py FOLDER [--mutate=labels]. Exit 1 when the check fails.
"""
import json
import os
import sys

import numpy as np

d0 = sys.argv[1]
mut = "--mutate=labels" in sys.argv
ok = True
print("| D | order | Δ mode: index, σ, Δ share, top | pair: indices, σ, top | pair overlap with order 160's | σ_Δ / σ_pair |")
print("|---|---|---|---|---|---|")
for D in ("229.0000", "230.0000", "231.0000"):
    ref = np.load(os.path.join(d0, f"V_k160_D{D}_ks160.npy"))[:, :2]
    for K in (160, 200):
        pj = os.path.join(d0, f"nn_k160_D{D}_ks{K}.json")
        if not os.path.exists(pj):
            continue
        v = json.load(open(pj))["vectors"]
        V = np.load(os.path.join(d0, f"V_k160_D{D}_ks{K}.npy"))
        span = np.hypot(*(ref.T @ V))                  # each vector's overlap with order 160's pair span
        i = int(np.argmax([x["delta"] for x in v]))
        pair = [0, 1] if (K == 160 or mut) else sorted(int(j) for j in np.argsort(-span)[:2])
        good = v[i]["delta"] >= 0.5 and i not in pair and all(span[j] >= 0.9 for j in pair)
        ok &= good
        sp = min(v[j]["sigma"] for j in pair)
        top = lambda x: f"{x['top'][0][0]} k{x['top'][0][1]}"
        print(f"| {D} | {K} | σ{i + 1}, {v[i]['sigma']:.3e}, {v[i]['delta']:.2f}, {top(v[i])} | "
              + ", ".join(f"σ{j + 1} {v[j]['sigma']:.3e} {top(v[j])}" for j in pair)
              + f" | {', '.join(f'{span[j]:.3f}' for j in pair)} | {v[i]['sigma'] / sp:.3g}{'' if good else ' (ambiguous)'} |")
print(f"check{' (--mutate=labels)' if mut else ''}: {'pass' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
