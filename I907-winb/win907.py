"""The step of Delta per Jacobian in windows of 100 Jacobians, and the decay rate between windows (#907).
usage: python win907.py I907_FOLDER"""
import json
import math
import os
import sys

R = sys.argv[1]
for n in ("up_10.0", "up_10.5"):
    k = [json.loads(x) for x in open(os.path.join(R, f"walk3_{n}.jsonl"), encoding="utf-8") if x.strip()][-1]
    h = k["hist"][:-1] if k["stalled"] else k["hist"]
    d = [x["dDelta"] for x in h]
    w = 100 if len(d) >= 400 else 25
    print(f"{n}: {len(d)} applied steps, windows of {w}")
    prev = None
    for i in range(0, len(d) - w + 1, w):
        m = sum(d[i:i + w]) / w
        mid = i + (w - 1) / 2
        s = f"  jac {i:3d}-{i + w - 1:3d}: mean step {m:+.4e}"
        if prev is not None:
            r = 1 - (m / prev[0]) ** (1 / (mid - prev[1]))
            s += f", decay between this window and the one before: 1 part in {1 / r:.0f} per Jacobian"
        print(s)
        prev = (m, mid)
    tot = sum(d)
    r = 1 - (d[-1] / d[0]) ** (1 / (len(d) - 1))
    print(f"  moved {tot:+.4e} in {len(d)} Jacobians; first step {d[0]:+.4e}, last {d[-1]:+.4e}, "
          f"mean decay over the whole run 1 part in {1 / r:.0f}")
