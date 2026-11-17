"""#903 p_min question: the horizon series' own terms at u0, by order, at a stored state and several orders.

series_order.py found the base series' terms at u0 growing with the order at D 229 (term norm 8.06 at order 0,
1.71e9 at order 160), so this prints that profile directly. For each order K it builds the solver at K and reads
Solver.series (double-double, scaled; model.rs horizon_state sums c_kk sigma^kk t^kk at t = u0 / sigma) at the stored
z, and prints, per field (p, m, a, c) and for all four, the term norm ||c_kk sigma^kk|| t^kk at every tenth order and
the last, and the growth factor per order over the last 20 orders, exp(mean of the differences of ln norm). Above 1
the terms at u0 grow at the top and the truncated sum is dominated by its last terms; below 1 they fall.

Check (can fail): the series depends on the order only through where the recursion stops, so the coefficients up to
the smaller order must agree bit for bit between two orders at the same z. Control --mutate=order compares the
smaller order's coefficients against the larger one's shifted by one order, which must fail.

Run: python3 series_profile.py RAWDIR STATE K1 [K2 ...] [--mutate=order]. Exit 1 when the check fails.
"""
import math
import os
import sys

import numpy as np

HP = "/Users/nathan/Source/choptuik-large-d-902/hp"
sys.path.insert(0, HP)
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
mut = "--mutate=order" in sys.argv
raw, st, Ks = args[0], args[1], [int(k) for k in args[2:]]
z, m = load_o(os.path.join(raw, st))
zh, zl = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z[:2]]
M, nodes = int(m["M"]), list(m["nodes"])
D = m.get("D_str", repr(float(m["D"])))
print(f"{st}: D {float(m['D']):.4f}, the state's order {m.get('ks')}, u0 {1 - nodes[-1]:.6g}")
ser = {}
for K in Ks:
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=K, threads=3,
                    kfreeze=int(m.get("kfreeze", 3)))
    h, l = s.series(zh, zl, 1, True)
    h, l = np.asarray(h).reshape(-1, 4, M), np.asarray(l).reshape(-1, 4, M)
    ser[K] = (h, l)
    t = (1 - nodes[-1]) / s.series_scale(1)
    w = np.exp(math.log(t) * np.arange(K + 1))
    nf = np.sqrt((h ** 2).sum(axis=2)) * w[:, None]
    na = np.sqrt((nf ** 2).sum(axis=1))
    lg = np.diff(np.log(na[-21:]))
    print(f"  order {K}: t = u0 / sigma {t:.6f}; growth per order over the last 20 {math.exp(lg.mean()):.4f}; term norm "
          "(all four; p, m, a, c) at order:")
    for kk in sorted(set(list(range(0, K + 1, 10)) + [K])):
        print(f"    {kk:4d}  {na[kk]:.3e}  (" + ", ".join(f"{x:.2e}" for x in nf[kk]) + ")")
ok = True
for a, b in zip(Ks, Ks[1:]):
    k0 = min(a, b)
    ha, hb = ser[a][0], ser[b][0]
    la, lb = ser[a][1], ser[b][1]
    if mut:
        same = np.array_equal(ha[:k0], hb[1:k0 + 1]) and np.array_equal(la[:k0], lb[1:k0 + 1])
    else:
        same = np.array_equal(ha[:k0 + 1], hb[:k0 + 1]) and np.array_equal(la[:k0 + 1], lb[:k0 + 1])
    ok &= same
    print(f"  orders 0..{k0} at order {a} and order {b}{' (shifted, --mutate=order)' if mut else ''}: "
          f"{'equal bit for bit' if same else 'NOT equal'}")
print(f"check: {'pass' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
