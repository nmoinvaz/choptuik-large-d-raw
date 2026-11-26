"""hp's d/dtheta matrices (driver.dmat_odd, form_s.dmat_even: double-double from 40-digit values; form_s.dmat_corr: the
f64 remainders from 80-digit values) against the same matrices at 120 digits: the largest error of hi + lo and of
hi + lo + c, absolute and relative to the row's largest entry, the largest |D[i,i]| of the odd matrix (0 exactly), and
the largest |D + D^T| of the odd matrix (antisymmetric exactly), at M 32 and 48.

    python3 dmat_exact_check.py HP_DIR [M ...]
"""
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import mpmath as mp  # noqa: E402

import form_s  # noqa: E402
import hpkernel.driver as drv  # noqa: E402


def exact(M, dps=120):
    with mp.workdps(dps):
        N = 2 * M
        vo, ve = mp.matrix(M, M), mp.matrix(M, M)
        for i in range(M):
            for j in range(M):
                a = b = mp.mpf(0)
                for jj, sgn in ((j, 1), (j + M, -1)):
                    if jj != i:
                        t = mp.mpf(0.5) * (-1) ** (i - jj) * mp.cot((i - jj) * mp.pi / N)
                        a += sgn * t
                        b += t
                vo[i, j], ve[i, j] = a, b
    return vo, ve


def report(name, h, l, c, X, M, odd):
    with mp.workdps(120):
        e2 = e3 = r2 = r3 = mp.mpf(0)
        d2 = d3 = s2 = s3 = mp.mpf(0)
        v2 = [[mp.mpf(float(h[i, j])) + mp.mpf(float(l[i, j])) for j in range(M)] for i in range(M)]
        v3 = [[v2[i][j] + mp.mpf(float(c[i, j])) for j in range(M)] for i in range(M)]
        for i in range(M):
            rmax = max(abs(X[i, j]) for j in range(M))
            for j in range(M):
                a2, a3 = abs(v2[i][j] - X[i, j]), abs(v3[i][j] - X[i, j])
                e2, e3 = max(e2, a2), max(e3, a3)
                r2, r3 = max(r2, a2 / rmax), max(r3, a3 / rmax)
                if odd:
                    s2 = max(s2, abs(v2[i][j] + v2[j][i]))
                    s3 = max(s3, abs(v3[i][j] + v3[j][i]))
            if odd:
                d2, d3 = max(d2, abs(v2[i][i])), max(d3, abs(v3[i][i]))
        print(f"M {M} {name}: max |hi+lo - exact| {mp.nstr(e2, 3)} (rel to row max {mp.nstr(r2, 3)}); "
              f"max |hi+lo+c - exact| {mp.nstr(e3, 3)} (rel {mp.nstr(r3, 3)})", flush=True)
        if odd:
            print(f"M {M} {name}: max |D[i,i]| hi+lo {mp.nstr(d2, 3)}, hi+lo+c {mp.nstr(d3, 3)}; "
                  f"max |D + D^T| hi+lo {mp.nstr(s2, 3)}, hi+lo+c {mp.nstr(s3, 3)}", flush=True)
            print(f"M {M} {name}: max |hi[i,i]| {max(abs(float(h[i, i])) for i in range(M)):.3e}, "
                  f"max |lo[i,i]| {max(abs(float(l[i, i])) for i in range(M)):.3e}, "
                  f"max |c[i,i]| {max(abs(float(c[i, i])) for i in range(M)):.3e}", flush=True)


for M in [int(v) for v in sys.argv[2:]] or [32, 48]:
    oh, ol = drv.dmat_odd(M)
    eh, el = form_s.dmat_even(M)
    co, ce = form_s.dmat_corr(M)
    Xo, Xe = exact(M)
    report("odd", np.asarray(oh), np.asarray(ol), np.asarray(co), Xo, M, True)
    report("even", np.asarray(eh), np.asarray(el), np.asarray(ce), Xe, M, False)
