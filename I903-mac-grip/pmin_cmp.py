"""#903 p_min question: is order 160's fast-falling pivot floor from D 228 the wall's weak direction or a new one?

Reads near_null.py's JSONs and vectors (--save_v, six columns) in this folder: nn_k160_D<d>.0000_ks160 (dh610's
order-160 chain), nn_k135_D<d>.1312_ks135 (macm3's order-135 chain, 0.13 in D above), nn_k160_D229.0000_ks200 (the
order-160 state at D 229 summed to order 200) and, from I902-mac (argument 2), #902's order-130 states at D 249.01
and 253.80. For each d of 227..231 with both runs it prints:
  sigma_1..6 at order 160 and order 135, the gap sigma_2 / sigma_1 at each, and near_null's LU pivot floor;
  v_1(160): its Delta share and top harmonic, and |V(135)^T v_1(160)|, the overlap with each order-135 vector, with the
  largest named (its index, sigma, Delta share, harmonic); the overlap of the two smallest, |v_1(135) . v_1(160)|, and on the span of order 135's two smallest (a near pair);
  the Delta mode (the vector of largest Delta share) at each order and its sigma.
Order 150 (dh170's I903-dh170/chain_k150, nn_k150_D<d>.0000_ks150) at D 226 and 227, added at the coordinator's
request: its sigma_1..6, gap and pivot floor, and v_1(150) against the six of order 160 at D 229 and of order 135 at
D 227.13 (the largest named; the two smallest together, sqrt of the sum of their two squared overlaps, as the weak
modes come in near pairs). Then at D 229: v_1(160) followed into the order-200 run at the same z (largest overlap; its sigma there, the ratio to
order 160), and v_1(160) of every d against the order-130 Delta modes of #902 (D 249.01, 253.80).
Overlaps are in z's raw coordinates (near_null's), of unit f64 vectors, so 1 is the same direction. Calibration printed
with them: v_1(160) at d against d - 1 (same chain, the next base), and the Delta mode at order 135 at d against d - 1.

Run: python3 pmin_cmp.py FOLDER I902_FOLDER
"""
import json
import os
import sys

import numpy as np


def get(d0, name):
    fj, fv = os.path.join(d0, f"nn_{name}.json"), os.path.join(d0, f"V_{name}.npy")
    if not (os.path.exists(fj) and os.path.exists(fv)):
        return None
    return json.load(open(fj)), np.load(fv)


def ident(r, i):
    v = r["vectors"][i]
    return f"sigma_{i + 1} {v['sigma']:.3e} (Delta {v['delta']:.2f}, {v['top'][0][0]} k{v['top'][0][1]})"


def dmode(r):
    return int(np.argmax([v["delta"] for v in r["vectors"]]))


d0, d902 = sys.argv[1], sys.argv[2]
runs = {d: (get(d0, f"k160_D{d}.0000_ks160"), get(d0, f"k135_D{d}.1312_ks135")) for d in range(227, 232)}
old = {D: get(d902, f"D{D}_ks130") for D in ("249", "253")}
print("pmin_cmp: order 160 (dh610, D d) against order 135 (macm3, D d + 0.1312); overlaps |u . v| of unit vectors")
prev = None
for d, (a, b) in runs.items():
    if a is None:
        print(f"  D {d}: order 160 not run yet")
        prev = None
        continue
    ra, Va = a
    sa = [v["sigma"] for v in ra["vectors"]]
    line = (f"  D {d}: order 160 sigma_1-6 " + ", ".join(f"{x:.2e}" for x in sa) + f", gap {sa[1] / sa[0]:.3g}, "
            f"LU pivot floor {ra['pivots'][0]:.2e}; v_1 Delta {ra['vectors'][0]['delta']:.2f}, "
            f"{ra['vectors'][0]['top'][0][0]} k{ra['vectors'][0]['top'][0][1]}; Delta mode {ident(ra, dmode(ra))}")
    if prev is not None:
        line += f"; v_1 against D {d - 1}'s v_1 {abs(Va[:, 0] @ prev[:, 0]):.3f}"
    print(line)
    prev = Va
    for D, o in old.items():
        if o is not None:
            ov = np.abs(o[1].T @ Va[:, 0])
            i = dmode(o[0])
            print(f"    v_1(160) against order 130 at D {D}: its Delta mode {ident(o[0], i)} {ov[i]:.3f}, best "
                  f"{ov.max():.3f} ({ident(o[0], int(ov.argmax()))})")
    if b is None:
        print(f"    order 135 at D {d}.1312 not run yet")
        continue
    rb, Vb = b
    sb = [v["sigma"] for v in rb["vectors"]]
    ov = np.abs(Vb.T @ Va[:, 0])
    j = int(ov.argmax())
    print(f"    order 135 sigma_1-6 " + ", ".join(f"{x:.2e}" for x in sb) + f", gap {sb[1] / sb[0]:.3g}, LU pivot floor "
          f"{rb['pivots'][0]:.2e}; v_1 {ident(rb, 0)}; Delta mode {ident(rb, dmode(rb))}")
    print(f"    v_1(160) against order 135's six: " + ", ".join(f"{x:.3f}" for x in ov)
          + f"; largest {ident(rb, j)}; smallest against smallest |v_1(135) . v_1(160)| {ov[0]:.3f}, on the span of order 135's two smallest "
          f"{np.hypot(ov[0], ov[1]):.3f}; Delta modes "
          f"{abs(Vb[:, dmode(rb)] @ Va[:, dmode(ra)]):.3f}; sigma_1(160) / sigma_1(135) {sa[0] / sb[0]:.3g}")
    pb = runs.get(d - 1, (None, None))[1]
    if pb is not None:
        print(f"    calibration: order 135's Delta mode against D {d - 1}.1312's "
              f"{abs(pb[1][:, dmode(pb[0])] @ Vb[:, dmode(rb)]):.3f}")
for d in (226, 227):
    e = get(d0, f"k150_D{d}.0000_ks150")
    if e is None:
        print(f"  order 150 (dh170) at D {d}: not run yet")
        continue
    re_, Ve = e
    se = [v["sigma"] for v in re_["vectors"]]
    print(f"  order 150 (dh170) at D {d}: sigma_1-6 " + ", ".join(f"{x:.2e}" for x in se) + f", gap {se[1] / se[0]:.3g}, "
          f"LU pivot floor {re_['pivots'][0]:.2e}; v_1 {ident(re_, 0)}; Delta mode {ident(re_, dmode(re_))}")
    for name, o in (("order 160 at D 229", runs[229][0]), ("order 135 at D 227.1312", runs[227][1])):
        if o is None:
            print(f"    v_1(150) against {name}: not run yet")
            continue
        ov = np.abs(o[1].T @ Ve[:, 0])
        j = int(ov.argmax())
        print(f"    v_1(150) against {name}'s six: " + ", ".join(f"{x:.3f}" for x in ov) + f"; largest {ident(o[0], j)}; "
              f"two smallest together {np.hypot(ov[0], ov[1]):.3f}")
c = get(d0, "k160_D229.0000_ks200")
if c is not None and runs[229][0] is not None:
    ra, Va = runs[229][0]
    ov = np.abs(c[1].T @ Va[:, 0])
    j = int(ov.argmax())
    print(f"  D 229 at order 200 (same z): v_1(160) {ident(ra, 0)} is {ident(c[0], j)} there (overlap {ov[j]:.3f}), "
          f"ratio {c[0]['vectors'][j]['sigma'] / ra['vectors'][0]['sigma']:.3g}; order 200's v_1 {ident(c[0], 0)}")
