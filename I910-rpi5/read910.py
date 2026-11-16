#!/usr/bin/env python3
"""#910: the issue's acceptance from fineA.jsonl and fineB.jsonl.  python3 read910.py FOLDER
Per sweep: the points (least |F|, Jacobians used, the cap 60 reached, Delta held, smallest singular value) and the
minimum's location, the vertex of the parabola through the sweep's three lowest points (|F| against Delta, exact through
the three). Rule: the locations differ by at most 0.002 -> agree, the mean is the prior-free estimate with half the
difference as spread; by more than 0.004 -> the minimum depends on the branch; between -> reported."""
import json, os, sys
import numpy as np
R = sys.argv[1]
CAP = 60
def pts(f):
    r = [json.loads(l) for l in open(os.path.join(R, f)) if l.strip()][-1]
    return sorted(r["points"], key=lambda p: p["target"])
loc = {}
for name in ("A", "B"):
    P = pts(f"fine{name}.jsonl")
    print(f"### sweep {name}\n\n| Delta | least \\|F\\| | Jacobians | cap reached | Delta held | smallest sv |\n|---|---|---|---|---|---|")
    for p in P:
        print(f"| {p['target']:.3f} | {p['F']:.4e} | {p['jac']} | {'yes' if p['jac'] >= CAP else 'no'} | {p['held']} | {p['s_low'][0]:.2e} |")
    low = sorted(sorted(P, key=lambda p: p["F"])[:3], key=lambda p: p["target"])
    x = np.array([p["target"] for p in low]); y = np.array([p["F"] for p in low])
    c2, c1, c0 = np.polyfit(x - x[1], y, 2)
    v = x[1] - c1 / (2 * c2) if c2 > 0 else float("nan")
    adj = round((x[2] - x[0]) / 0.001) == 2
    loc[name] = v
    print(f"\nthree lowest: Delta {', '.join(f'{t:.3f}' for t in x)} (|F| {', '.join(f'{t:.4e}' for t in y)}), "
          f"{'adjacent' if adj else 'NOT adjacent'}; parabola curvature {'positive' if c2 > 0 else 'NOT positive'}; "
          f"vertex Delta {v:.6f}, parabola minimum |F| {c0 - c1 * c1 / (4 * c2):.4e}\n" if c2 > 0 else
          f"\nthree lowest: Delta {', '.join(f'{t:.3f}' for t in x)}, curvature not positive, no minimum\n")
    held = all(p["held"] for p in P)
    print(f"Delta held at every point: {held}; points at the cap: {[p['target'] for p in P if p['jac'] >= CAP] or 'none'}; "
          f"Jacobians {min(p['jac'] for p in P)} to {max(p['jac'] for p in P)}\n")
d = abs(loc["A"] - loc["B"])
print(f"locations: A {loc['A']:.6f}, B {loc['B']:.6f}, difference {d:.6f}")
if d <= 0.002:
    print(f"reading by the frozen rule: LOCATION AGREES; prior-free estimate {(loc['A'] + loc['B']) / 2:.6f} +- {d / 2:.6f} (half the difference, an estimator spread)")
elif d > 0.004:
    print("reading by the frozen rule: LOCATION DIFFERS; the minimum depends on the branch")
else:
    print("reading by the frozen rule: between 0.002 and 0.004, reported")
