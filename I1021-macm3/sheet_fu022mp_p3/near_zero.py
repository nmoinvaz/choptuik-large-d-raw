"""macm3b #1076 (my own analysis, not part of dh370's run.sh): the lines-mode pairs of sheet_check.py re-read from the same rules
(last record per point, valued as the script reads it, pairs along lines of constant wf with dA <= 0.25 and of constant A with dwf <= 0.1),
then the pairs that touch the cell of pass 3's new zero. python near_zero.py CACHE"""
import json, sys
import numpy as np
rk = lambda x: round(x, 9)
last = {}
for line in open(sys.argv[1]):
    r = json.loads(line); last[(rk(r["A"]), rk(r["wf"]))] = r
valued = lambda r: ((isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))) and np.isfinite(r["re"]) and np.isfinite(r["F3re"])
pts = {k: complex(r["F3re"], r["F3im"]) for k, r in last.items() if valued(r)}
byA, byW = {}, {}
for k in pts:
    byA.setdefault(k[0], []).append(k); byW.setdefault(k[1], []).append(k)
runs = []
for ks in byW.values():
    ks = sorted(ks, key=lambda k: k[0]); runs += [[p, q] for p, q in zip(ks[:-1], ks[1:]) if q[0] - p[0] <= 0.25 + 1e-9]
for ks in byA.values():
    ks = sorted(ks, key=lambda k: k[1]); runs += [[p, q] for p, q in zip(ks[:-1], ks[1:]) if q[1] - p[1] <= 0.1 + 1e-9]
pairs = {(p, q): (abs(pts[q] - pts[p]), float(np.hypot(q[0] - p[0], q[1] - p[1]))) for p, q in runs}
med = float(np.median([d / L for d, L in pairs.values()]))
print(f"all: {len(pts)} valued points, {len(pairs)} pairs, median {med:.3g}, largest |dF3| {max(d for d, L in pairs.values()):.3g}")
a0, a1, w0, w1 = 3.5217206, 3.5373456, 0.20654321, 0.21279321
inn = lambda k, e=1e-9: a0 - e <= k[0] <= a1 + e and w0 - e <= k[1] <= w1 + e
inside = [k for k in pts if inn(k)]
touch = {pq: v for pq, v in pairs.items() if inn(pq[0]) or inn(pq[1])}
print(f"cell A {a0}-{a1}, wf {w0}-{w1} (the new zero's cell, closed): {len(inside)} valued points, {len(touch)} pairs with an end in it, "
      f"largest |dF3| {max(d for d, L in touch.values()):.3g}, largest |dF3|/length {max(d / L for d, L in touch.values()):.3g} (median of all {med:.3g}), "
      f"flagged {sum(1 for d, L in touch.values() if d > 0.1 or (d > 0.02 and d / L > 20 * med))}")
zA, zw = 3.5265378505668146, 0.2114823267002827
near = sorted(pts, key=lambda k: np.hypot(k[0] - zA, k[1] - zw))[:6]
print("the 6 valued points nearest the zero (A, wf, distance, F3):")
for k in near:
    print(f"  ({k[0]:.9g}, {k[1]:.9g}) {np.hypot(k[0] - zA, k[1] - zw):.2e} F3 {pts[k]:.4f}")
