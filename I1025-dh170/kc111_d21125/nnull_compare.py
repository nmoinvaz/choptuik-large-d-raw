#!/usr/bin/env python3
"""Compare n_null(c) of two states over the cutoff range where both counts are known exactly (#1025, t5's plateau rule).
A state's json (nnull_count.py) holds n_null at the cutoff 1e-12 sigma_max, the three largest values counted null (descending, b0 > b1 > b2) and the four
smallest kept (ascending, a0 < ... < a3). n(c) = number of singular values <= c is then exact for b2 <= c < a3: n_null for b0 <= c < a0, n_null - 1 for
b1 <= c < b0, n_null - 2 for b2 <= c < b1, n_null + 1 for a0 <= c < a1, + 2 for a1 <= c < a2, + 3 for a2 <= c < a3.
usage: nnull_compare.py A.json B.json     prints n_A(c), n_B(c), the difference and the parities on each plateau of the combined breakpoints.
       nnull_compare.py --selftest        planted spectra: identical inputs give difference 0 on every plateau; B with one more value at 2e-11 (between the
                                          two cutoffs of a planted pair) gives +1 only above 2e-11; --mutate=drop (drops that value) must fail the check.
"""
import json
import sys


def steps(j):
    b, a, n = j["sv_null_largest"], j["sv_reg_small"], j["n_null"]
    # (lower edge of c, count) from the smallest known edge up
    pts = [(b[2], n - 2), (b[1], n - 1), (b[0], n), (a[0], n + 1), (a[1], n + 2), (a[2], n + 3)]
    return pts, (b[2], a[3])


def table(A, B):
    pa, (la, ha) = steps(A)
    pb, (lb, hb) = steps(B)
    lo, hi = max(la, lb), min(ha, hb)
    edges = sorted({e for e, _ in pa + pb if lo <= e < hi} | {lo})
    cnt = lambda p, c: [n for e, n in p if e <= c][-1]
    rows = []
    for k, e in enumerate(edges):
        top = edges[k + 1] if k + 1 < len(edges) else hi
        rows.append((e, top, cnt(pa, e), cnt(pb, e)))
    return rows, (lo, hi)


def selftest(mutate=None):
    ok = True
    A = dict(n_null=50, sv_null_largest=[9e-12, 2e-12, 5e-13], sv_reg_small=[3e-11, 1e-10, 1.1e-10, 1.3e-10])
    rows, _ = table(A, A)
    same = all(a == b for _, _, a, b in rows)
    print("planted: identical states: difference 0 on %d plateaus: %s" % (len(rows), "PASS" if same else "FAIL")); ok &= same
    B = dict(n_null=51, sv_null_largest=[2e-11, 9e-12, 2e-12], sv_reg_small=[3e-11, 1e-10, 1.1e-10, 1.3e-10])
    if mutate == "drop":
        B = dict(n_null=50, sv_null_largest=[9e-12, 2e-12, 5e-13], sv_reg_small=[3e-11, 1e-10, 1.1e-10, 1.3e-10])
    rows, _ = table(A, B)
    d = {(round(e, 15)): b - a for e, _, a, b in rows}
    # B has one value at 2e-11 that A lacks: the difference must be +1 for c >= 2e-11 and 0 below, as far as both are exact
    good = all((dd == 1) == (e >= 2e-11) for e, dd in d.items() if e >= 2e-12)
    print("planted: B has one more value at 2e-11: the difference is +1 exactly for c >= 2e-11: %s" % ("PASS" if good else "FAIL")); ok &= good
    print("selftest: " + ("PASS" if ok else "FAILS"))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest(next((x.split("=", 1)[1] for x in sys.argv if x.startswith("--mutate=")), None)))
    A, B = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    rows, (lo, hi) = table(A, B)
    print("n(c) = number of singular values <= c, exact for c in [%.3e, %.3e) (both states; sigma_max %.6f and %.6f)" % (lo, hi, A["sigma_max"], B["sigma_max"]))
    print("%-24s %9s %9s %6s  %s" % ("c range", "k_c %d" % A["kc"], "k_c %d" % B["kc"], "diff", "parities"))
    span = 0.0
    import math
    tot = math.log(hi / lo)
    byd = {}
    for e, top, a, b in rows:
        w = math.log(top / e)
        byd[b - a] = byd.get(b - a, 0) + w
        mark = "  <- the convention's cutoff %.3e" % (1e-12 * A["sigma_max"]) if e <= 1e-12 * A["sigma_max"] < top else ""
        print("[%.3e, %.3e) %9d %9d %+6d  %s/%s%s" % (e, top, a, b, b - a, "odd" if a % 2 else "even", "odd" if b % 2 else "even", mark))
    print("share of the exact range (in log c) by the difference n(%d) - n(%d): " % (B["kc"], A["kc"]) + ", ".join("%+d: %.1f%%" % (d, 100 * w / tot) for d, w in sorted(byd.items())))
