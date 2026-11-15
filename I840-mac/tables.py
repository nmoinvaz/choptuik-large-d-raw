#!/usr/bin/env python3
"""#840: the README's tables from this folder's step_spread JSONs. Run from I840-mac/: python3 tables.py
Per D: the state's max|F|, the unperturbed dDelta and smallest pivot, per horizon seed dDelta, the smallest pivot and
max|F|, and the Delta control (its move, dDelta and |dDelta| / move, which is 1 if Newton's step returns the move; the
move's sign is not in the JSON).
Then the power diagnostic: p = log10(dev(rel) / dev(rel / 10)), dev = dDelta(seed 1) - dDelta(unperturbed), at D 240.1244
from ss_D240 (1e-65) and pw_D240_r66, pw_D240_r67 (the same signs)."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, name + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


print("| D | state max\\|F\\| | unperturbed dΔ | its smallest pivot | seed | seed dΔ | seed's smallest pivot | "
      "pivot / unperturbed | seed max\\|F\\| |")
print("|---|---|---|---|---|---|---|---|---|")
for n in ("ss_D240", "ss_D245", "ss_D250", "ss_D252"):
    r = load(n)
    u = r["runs"][0]
    for s in [x for x in r["runs"] if x["blocks"] == ["m_h", "a_h"]]:
        print(f"| {float(r['D_str']):.4f} | {u['F']:.2e} | {u['dDelta']:+.3e} | {u['piv'][0]:.3e} | {s['seed']} | "
              f"{s['dDelta']:+.3e} | {s['piv'][0]:.3e} | {s['piv'][0] / u['piv'][0]:.3g} | {s['F']:.3e} |")
print()
print("| D | Delta move | dΔ after it | \\|dΔ\\| / move | max\\|F\\| after it |")
print("|---|---|---|---|---|")
for n in ("ss_D240", "ss_D245", "ss_D250", "ss_D252"):
    r = load(n)
    d = next(x for x in r["runs"] if x["blocks"] == ["Delta"])
    print(f"| {float(r['D_str']):.4f} | {d['move']:.4e} | {d['dDelta']:+.4e} | {abs(d['dDelta']) / d['move']:.3e} | "
          f"{d['F']:.3e} |")
print()
pw = [("1e-65", load("ss_D240")), ("1e-66", load("pw_D240_r66")), ("1e-67", load("pw_D240_r67"))]
devs = []
for rel, r in pw:
    if r is None:
        print(f"rel {rel}: no JSON")
        continue
    s = next(x for x in r["runs"] if x["blocks"] == ["m_h", "a_h"] and x["seed"] == 1)
    dev = s["dDelta"] - r["runs"][0]["dDelta"]
    devs.append((rel, dev, s))
    print(f"rel {rel}: move {s['move']:.4e}, seed 1 dDelta {s['dDelta']:+.6e}, dev {dev:+.6e}, max|dz| {s['dz']:.4e}, "
          f"smallest pivot {s['piv'][0]:.6e}, max|F| {s['F']:.4e}")
ps = []
for (r1, d1, _), (r2, d2, _) in zip(devs, devs[1:]):
    p = math.log10(abs(d1 / d2)) if d1 * d2 > 0 else float("nan")
    ps.append(p)
    print(f"p({r1} -> {r2}) = log10(dev ratio) = {p:.4f}{'' if d1 * d2 > 0 else ' (sign changed)'}")
if len(ps) == 2:
    rule = ("quadratic" if all(1.8 <= p <= 2.2 for p in ps) else
            "linear" if all(0.8 <= p <= 1.2 for p in ps) else "neither")
    print(f"reading (registered): {rule}")
    for rel, dev, st in devs:
        x = float(rel)
        # the step's quadratic part, max|dz| / rel^2, against the move per unit rel: they are equal at rel_eq
        q, m = st["dz"] / x ** 2, st["move"] / x
        print(f"rel {rel}: max|dz| / rel^2 {q:.4e}, dDelta / rel^2 {dev / x ** 2:.4e}, move / rel {m:.4f}; the "
              f"quadratic part equals the move at rel {m / q:.2e}")

# the spread against D from sum.json (step_spread.py sum): the pairwise slopes of ln(spread), the fit over the first
# three D, the unperturbed pivot against #805's p_min, and the spread / rel^2 (rel 1e-65; a quadratic coefficient only where the response is quadratic, read at
# D 240.1244 alone)
s = load("sum")
if s:
    import numpy as np
    D = np.array([r["D"] for r in s["rows"]])
    sp = np.array([r["spread"] for r in s["rows"]])
    print()
    for a in range(len(D) - 1):
        print(f"slope of ln(spread), D {D[a]:.4f} -> {D[a + 1]:.4f}: {np.log(sp[a + 1] / sp[a]) / (D[a + 1] - D[a]):.4f}")
    print(f"slope of ln(spread) over the first three D: {np.polyfit(D[:3], np.log(sp[:3]), 1)[0]:.4f}; over all four "
          f"{s['slope']:.4f} (sum)")
    for r in s["rows"]:
        print(f"D {r['D']:.4f}: unperturbed pivot / p_min {r['piv0'] / r['p_min']:.6f}, spread / rel^2 "
              f"{r['spread'] / 1e-130:.3e}")
