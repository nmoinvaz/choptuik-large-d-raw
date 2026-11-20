#!/usr/bin/env python3
"""#1057: the two-mode fit (twomode949.py's own `fit`, `pair`, `share`, `crossing`, unchanged) on the last N states INCLUDING the ones track949.py leaves unclassified (no vector with a
Delta share above 0.5), read straight from the state records with row949.picks. Outside the #949 pipeline: a diagnostic, labelled as such in every post.

    crossing1057.py NAME1 NAME2 ...    states in increasing D, e.g. c3b_ks293_D260.6706 c3b_ks293_D260.8483"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twomode949 as tm  # noqa: E402
from row949 import picks  # noqa: E402

D, sd, s2, sh, sh2 = [], [], [], [], []
for name in sys.argv[1:]:
    rec = json.load(open(os.path.join(HERE, name + ".json")))
    d, k2 = picks(rec)
    D.append(float(rec["D"])); sd.append(rec["vectors"][d]["sigma"]); s2.append(rec["vectors"][k2]["sigma"])
    sh.append(rec["vectors"][d]["delta"]); sh2.append(rec["vectors"][k2]["delta"])
th, rms = tm.fit(D, sd, s2)
x = np.array(D) - D[-1]
print(f"states {len(D)}: D {D[0]:.4f} to {D[-1]:.4f}: s1 {th[1]:.4f}, s2 {th[3]:.4f}, gamma {th[4]:.4f} (gap {(1 + th[4]) / (1 - th[4]):.3f}), D_c {tm.crossing(th, D[-1]):.3f}, rms of ln sigma {rms:.2e}")
print("fitted share of the lowest vector / measured share of the picked vector / measured share of the second:", ", ".join(f"{s:.3f}/{m:.3f}/{m2:.3f}" for s, m, m2 in zip(tm.share(th, x), sh, sh2)))
a, b = tm.pair(th, x)
print("fitted sigma_lowest, sigma_upper / measured:", ", ".join(f"{float(p):.3e},{float(q):.3e}/{u:.3e},{v:.3e}" for p, q, u, v in zip(a, b, sd, s2)))
