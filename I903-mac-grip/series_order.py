"""#903 p_min question: where by horizon-series order a weak direction of near_null.py lives.

The horizon block sums the series of p, m, a, c at u0 = 1 - (last node) to order K (model.rs horizon_state: Horner of
the scaled coefficients c_kk sigma^kk at t = u0 / sigma). The series is a function of the horizon data m_h, a_h and
Delta only. For a direction v of z (a column of near_null's --save_v), the change of order kk's term at u0 along v is
    n_kk = || d/de [c_kk sigma^kk](z + e v) || t^kk,
the norm over the four fields and the M grid values, by a central difference of Solver.series (double-double, scaled)
at z + e v and z - e v (z's double-double parts plus e v by multidouble's dd_add). Printed per vector: the share of
sum_kk n_kk^2 in the top tenth of the orders (kk > K - K/10), the orders by which the cumulative share reaches 0.5 and
0.99, and the base series' own term norms b_kk = ||c_kk sigma^kk|| t^kk read the same way. A direction "lives in the
top orders" (the truncation's) when its top-tenth share is above 0.5, and not when it is below 0.01 (written before
the runs).

Checks (each can fail):
  linear   the shares from e = 1e-12 and e = 1e-14 agree to 1e-6 (the difference is linear and resolved); control
           --mutate=eps takes the second at e = 1e-31, below double-double resolution, and the check must fail
  selftest planted n_kk (all in the top tenth; geometric 0.5^kk; flat) give top shares 1, below 1e-6 and 0.1 to 1e-12

Run: python3 series_order.py RAWDIR STATE K NN.json V.npy [--mutate=eps], or python3 series_order.py --selftest.
Exit 1 when a check fails.
"""
import json
import math
import os
import sys

import numpy as np

HP = "/Users/nathan/Source/choptuik-large-d-902/hp"


def reduce(n2, K):
    """n2[kk] = n_kk^2: (top-tenth share, order at 0.5 cumulative, order at 0.99, centroid)"""
    tot = n2.sum()
    c = np.cumsum(n2) / tot
    top = n2[K - K // 10 + 1:].sum() / tot
    return float(top), int(np.searchsorted(c, 0.5)), int(np.searchsorted(c, 0.99)), float((np.arange(len(n2)) * n2).sum() / tot)


def selftest():
    K, ok = 160, True
    k = np.arange(K + 1)
    for name, n2, want in [("top", np.where(k > K - K // 10, 1.0, 0.0), lambda t: abs(t - 1) < 1e-12),
                           ("geometric", 0.25 ** k, lambda t: t < 1e-6),
                           ("flat", np.ones(K + 1), lambda t: abs(t - 16 / 161) < 1e-12)]:
        top, h, q, cen = reduce(n2, K)
        good = want(top)
        ok &= good
        print(f"planted {name}: top-tenth share {top:.3e}, half at {h}, 0.99 at {q}, centroid {cen:.1f}: "
              f"{'pass' if good else 'FAIL'}")
    print(f"series_order selftest: {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    sys.path.insert(0, HP)
    from hpkernel.driver import make_solver
    from multidouble import dd_add
    from octo_corrector import load_o
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mut = "--mutate=eps" in sys.argv
    raw, st, K, fj, fv = args[0], args[1], int(args[2]), args[3], args[4]
    z, m = load_o(os.path.join(raw, st))
    zh, zl = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z[:2]]
    M, nodes = int(m["M"]), list(m["nodes"])
    D = m.get("D_str", repr(float(m["D"])))
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=K, threads=3,
                    kfreeze=int(m.get("kfreeze", 3)))
    V = np.load(fv)
    rec = json.load(open(fj))
    sig = s.series_scale(1)
    lt = math.log((1.0 - nodes[-1]) / sig)
    w = np.exp(lt * np.arange(K + 1))
    zero = np.zeros_like(zh)

    def ser(h, l):
        a, b = s.series(np.ascontiguousarray(h), np.ascontiguousarray(l), 1, True)
        return np.asarray(a), np.asarray(b)

    def n2(v, eps):
        ph, pl = ser(*dd_add(zh, zl, eps * v, zero))
        mh, ml = ser(*dd_add(zh, zl, -eps * v, zero))
        dh, dl = dd_add(ph, pl, -mh, -ml)
        d = ((np.asarray(dh) + np.asarray(dl)) / (2 * eps)).reshape(-1, 4, M)
        if d.shape[0] != K + 1:
            sys.exit(f"series_order.py: {d.shape[0]} orders, not K + 1 = {K + 1}")
        return (d ** 2).sum(axis=(1, 2)) * w ** 2

    bh, bl = ser(zh, zl)
    b = (np.asarray(bh) + np.asarray(bl)).reshape(-1, 4, M)
    print(f"{st}: D {float(m['D']):.4f}, order {K}, u0 / sigma {math.exp(lt):.6f}; top tenth = orders {K - K // 10 + 1}"
          f"..{K}")
    top, h, q, cen = reduce((b ** 2).sum(axis=(1, 2)) * w ** 2, K)
    bn = np.sqrt((b ** 2).sum(axis=(1, 2))) * w
    print(f"  base series: top-tenth share {top:.3e}, half at {h}, 0.99 at {q}, centroid {cen:.1f}; term norm at order 0 "
          f"{bn[0]:.2e}, {K // 2} {bn[K // 2]:.2e}, {K} {bn[K]:.2e}")
    ok = True
    for i in range(V.shape[1]):
        v = V[:, i]
        r1, r2 = reduce(n2(v, 1e-12), K), reduce(n2(v, 1e-31 if mut else 1e-14), K)
        lin = abs(r1[0] - r2[0]) <= 1e-6 * max(r1[0], 1e-300) or abs(r1[0] - r2[0]) < 1e-12
        ok &= lin
        vi = rec["vectors"][i]
        hz = np.linalg.norm(v[-1 - 2 * M:])
        read = "top orders" if r1[0] > 0.5 else ("not top" if r1[0] < 0.01 else "mixed")
        print(f"  sigma_{i + 1} {vi['sigma']:.3e} (Delta share {vi['delta']:.1e}, top {vi['top'][0][0]} k{vi['top'][0][1]}; "
              f"|v| on m_h, a_h, Delta {hz:.2f}): top-tenth share {r1[0]:.3e} ({read}), half at {r1[1]}, 0.99 at {r1[2]}, "
              f"centroid {r1[3]:.1f}; at e 1e-{31 if mut else 14} {r2[0]:.3e}: {'linear' if lin else 'NOT linear'}")
    print(f"check linear{' (--mutate=eps, must FAIL)' if mut else ''}: {'pass' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if (selftest() if "--selftest" in sys.argv else main()) else 1)
