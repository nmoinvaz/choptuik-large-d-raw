#!/usr/bin/env python3
"""#1021 cost estimate for a double-double hier_nb at M = 5: the time of inner_nb.conv (the harmonic convolution that
rhs calls six times per right-hand side) in complex128 against the same loop in double-double complex (hi/lo parts of
re and im; Dekker's two_prod, Knuth's two_sum, the accurate dd add). Accuracy check against exact rational sums
(fractions) of one random input: the dd result must agree to 1e-30 relative, complex128 to only about 1e-16;
--mutate=nolo drops the low parts (the check must then fail, exit 1). Prints the time ratio per call for L = 5 and 7.
    python bench_dd.py [--mutate=nolo]"""
import sys
import time
from fractions import Fraction

import numba as nb
import numpy as np

MUT = 1 if "--mutate=nolo" in sys.argv else 0


@nb.njit(cache=False)
def conv(a, b, space, L):                     # inner_nb.conv, verbatim
    n = 2 * L + 1
    out = np.zeros(n, np.complex128)
    for k in range(n):
        if space[k] == 0.0:
            continue
        lo = max(0, k + L - (n - 1))
        hi = min(n - 1, k + L)
        s = 0j
        for i in range(lo, hi + 1):
            s += a[i] * b[k + L - i]
        out[k] = s
    return out


@nb.njit(inline="always")
def two_sum(a, b):
    s = a + b
    bb = s - a
    return s, (a - (s - bb)) + (b - bb)


@nb.njit(inline="always")
def split(a):
    t = 134217729.0 * a
    h = t - (t - a)
    return h, a - h


@nb.njit(inline="always")
def two_prod(a, b):
    p = a * b
    ah, al = split(a)
    bh, bl = split(b)
    return p, ((ah * bh - p) + ah * bl + al * bh) + al * bl


@nb.njit(inline="always")
def dd_add(ah, al, bh, bl):
    s, e = two_sum(ah, bh)
    t, f = two_sum(al, bl)
    e += t
    s, e = two_sum(s, e)
    e += f
    return two_sum(s, e)


@nb.njit(inline="always")
def dd_mul(ah, al, bh, bl):
    p, e = two_prod(ah, bh)
    e += ah * bl + al * bh
    return two_sum(p, e)


@nb.njit(cache=False)
def conv_dd(a, b, space, L, mut):
    """a, b: (n, 4) arrays of re hi, re lo, im hi, im lo; out likewise"""
    n = 2 * L + 1
    out = np.zeros((n, 4))
    for k in range(n):
        if space[k] == 0.0:
            continue
        lo = max(0, k + L - (n - 1))
        hi = min(n - 1, k + L)
        sr, srl, si, sil = 0.0, 0.0, 0.0, 0.0
        for i in range(lo, hi + 1):
            j = k + L - i
            p1, p1l = dd_mul(a[i, 0], a[i, 1], b[j, 0], b[j, 1])
            p2, p2l = dd_mul(a[i, 2], a[i, 3], b[j, 2], b[j, 3])
            p3, p3l = dd_mul(a[i, 0], a[i, 1], b[j, 2], b[j, 3])
            p4, p4l = dd_mul(a[i, 2], a[i, 3], b[j, 0], b[j, 1])
            rr, rrl = dd_add(p1, p1l, -p2, -p2l)
            ii, iil = dd_add(p3, p3l, p4, p4l)
            sr, srl = dd_add(sr, srl, rr, rrl)
            si, sil = dd_add(si, sil, ii, iil)
        out[k, 0], out[k, 1], out[k, 2], out[k, 3] = sr, srl * (1 - mut), si, sil * (1 - mut)
    return out


def exact(a, b, L):                          # rational convolution of the dd inputs (exact)
    n = 2 * L + 1
    F = lambda x: Fraction(float(x))
    A = [(F(a[i, 0]) + F(a[i, 1]), F(a[i, 2]) + F(a[i, 3])) for i in range(n)]
    B = [(F(b[i, 0]) + F(b[i, 1]), F(b[i, 2]) + F(b[i, 3])) for i in range(n)]
    out = []
    for k in range(n):
        lo, hi = max(0, k + L - (n - 1)), min(n - 1, k + L)
        sr = sum(A[i][0] * B[k + L - i][0] - A[i][1] * B[k + L - i][1] for i in range(lo, hi + 1))
        si = sum(A[i][0] * B[k + L - i][1] + A[i][1] * B[k + L - i][0] for i in range(lo, hi + 1))
        out.append((sr, si))
    return out


def main():
    rng = np.random.default_rng(1021)
    ok = True
    for L in (5, 7):
        n = 2 * L + 1
        a, b = rng.standard_normal((n, 4)), rng.standard_normal((n, 4))
        a[:, 1] *= 1e-17; a[:, 3] *= 1e-17; b[:, 1] *= 1e-17; b[:, 3] *= 1e-17
        space = np.ones(n)
        ac, bc = a[:, 0] + 1j * a[:, 2], b[:, 0] + 1j * b[:, 2]
        d, c, ex = conv_dd(a, b, space, L, MUT), conv(ac, bc, space, L), exact(a, b, L)
        err_dd = max(abs((Fraction(d[k, 0]) + Fraction(d[k, 1]) - ex[k][0])) + abs(Fraction(d[k, 2]) + Fraction(d[k, 3]) - ex[k][1]) for k in range(n))
        err_c = max(abs(Fraction(c[k].real) - ex[k][0]) + abs(Fraction(c[k].imag) - ex[k][1]) for k in range(n))
        scale = max(abs(ex[k][0]) + abs(ex[k][1]) for k in range(n))
        e_dd, e_c = float(err_dd / scale), float(err_c / scale)
        ok = ok and e_dd < 1e-30
        N = 200000
        t = time.perf_counter()
        for _ in range(N):
            conv(ac, bc, space, L)
        tc = (time.perf_counter() - t) / N
        t = time.perf_counter()
        for _ in range(N):
            conv_dd(a, b, space, L, MUT)
        td = (time.perf_counter() - t) / N
        print(f"L {L}: complex128 {tc * 1e6:.2f} us/call, double-double {td * 1e6:.2f} us/call, ratio {td / tc:.1f}; "
              f"relative error against the exact sum: dd {e_dd:.1e}, complex128 {e_c:.1e}")
    print(f"accuracy check{' --mutate=nolo' if MUT else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
