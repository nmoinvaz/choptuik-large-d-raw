#!/usr/bin/env python3
"""#1025 win2b, the finer D 18.5 scan at k_c 55: information beside the coordinator's reading (not part of it). The reading is a near miss (no robust change, an interior ln|det| minimum without a
change). This script fits the 21 ln|det| values with a model of a root pair just off the real axis, ln|det| = a + ln((l - l0)^2 + e^2) + b (l - l0) + c (l - l0)^2 (det proportional to (l - l0)^2 + e^2 times a
smooth factor), and compares it with a quartic and a quadratic polynomial. A planted-truth control first: the model is fitted to synthetic data of known (l0, e) plus 1e-4 noise and must recover them.
usage: fine_dip_fit.py SCAN.jsonl"""
import json, sys
import numpy as np
from scipy.optimize import least_squares


def model(p, x):
    a, l0, e, b, c = p
    return a + np.log((x - l0) ** 2 + e ** 2) + b * (x - l0) + c * (x - l0) ** 2


def fit(x, y):
    best = None
    for e0 in (0.003, 0.01, 0.03):
        for l00 in np.linspace(x.min(), x.max(), 7)[1:-1]:
            r = least_squares(lambda p: model(p, x) - y, [y.mean(), l00, e0, 0.0, 0.0])
            if best is None or r.cost < best.cost:
                best = r
    return best


x = np.array([1.660 + 0.002 * i for i in range(21)])
rng = np.random.default_rng(1)
true = [-1597.0, 1.6840, 0.0130, 4.9, -13.0]
ys = model(true, x) + 1e-4 * rng.standard_normal(x.size)
r = fit(x, ys)
ok = abs(r.x[1] - true[1]) < 2e-4 and abs(abs(r.x[2]) - true[2]) < 1e-3
print(f"planted truth: l0 {true[1]}, e {true[2]} -> fitted l0 {r.x[1]:.5f}, e {abs(r.x[2]):.5f}, max |residual| {np.abs(r.fun).max():.1e} -> {'ok' if ok else 'WRONG'}")
ys2 = model([-1597.0, 1.6840, 0.0040, 4.9, -13.0], x) + 1e-4 * rng.standard_normal(x.size)
r2 = fit(x, ys2)
ok2 = abs(abs(r2.x[2]) - 0.0040) < 1e-3
print(f"planted truth: l0 1.6840, e 0.0040 -> fitted l0 {r2.x[1]:.5f}, e {abs(r2.x[2]):.5f} -> {'ok' if ok2 else 'WRONG'}")
if not (ok and ok2):
    sys.exit(1)
P = sorted((json.loads(l) for l in open(sys.argv[1]) if l.strip()), key=lambda r: r["lam"])
xs = np.array([r["lam"] for r in P]); y = np.array([r["ln"] for r in P])
b = fit(xs, y)
a, l0, e, bb, c = b.x
print(f"data ({len(P)} points, {xs[0]:.3f} to {xs[-1]:.3f}): fit ln|det| = a + ln((l-l0)^2+e^2) + b(l-l0) + c(l-l0)^2: a {a:.3f}, l0 {l0:.5f}, e {abs(e):.5f}, b {bb:.3f}, c {c:.3f}; "
      f"max |residual| {np.abs(b.fun).max():.2e}, rms {np.sqrt((b.fun ** 2).mean()):.2e}")
for deg in (2, 4):
    co = np.polyfit(xs - 1.68, y, deg)
    print(f"polynomial of degree {deg} in (l - 1.68): max |residual| {np.abs(np.polyval(co, xs - 1.68) - y).max():.2e}")
print(f"the model's complex roots of det: {l0:.5f} +- {abs(e):.5f} i (a model fit, not a root search; the k_c 63 root is 1.6772091, {l0 - 1.6772091:+.5f} from l0)")
