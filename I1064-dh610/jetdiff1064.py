#!/usr/bin/env python3
"""jetdiff1064.py A.npz B.npz [--tol 1e-40] | --selftest [--break]: the largest relative difference per coefficient between two jets (#1064 front test). A jet npz holds z0..z7 (the eight parts of an
octo-double number, shape (orders, unknowns)); each coefficient is the exact sum of its eight parts. Relative difference |a - b| / |b| per coefficient (b = the second file; both zero is 0, a zero b with a nonzero a is inf).
Prints the largest, its order and unknown, the count above TOL (default 1e-40) and the number of coefficients. Exit 0 when the largest is at most TOL, 1 when above, 2 on a shape mismatch.
--selftest plants jets: identical (largest 0), one coefficient changed by 1e-30 relative (must be found, with its location), one changed by 1e-50 relative in its last part (below TOL), a zero coefficient against a nonzero one (inf), a
shape mismatch (exit 2 in the function); each with its expected result; --break flips one expectation and must exit 1."""
import sys
import tempfile
from fractions import Fraction

import numpy as np


def load(p):
    z = np.load(p, allow_pickle=True)
    return np.stack([z[f"z{q}"] for q in range(8)])


def exact(parts):          # parts: (8, orders, unknowns) float64 -> object array of Fraction
    out = np.empty(parts.shape[1:], dtype=object)
    for idx in np.ndindex(*parts.shape[1:]):
        out[idx] = sum((Fraction(float(parts[q][idx])) for q in range(parts.shape[0])), Fraction(0))
    return out


def diff(A, B, tol=1e-40):
    """A, B: (8, orders, unknowns). Returns (largest relative difference, location, count above tol, number of coefficients) or None on a shape mismatch."""
    if A.shape != B.shape:
        return None
    a, b = exact(A), exact(B)
    worst, loc, cnt = Fraction(0), (None, None), 0
    for idx in np.ndindex(*a.shape):
        d = abs(a[idx] - b[idx])
        if d == 0:
            continue
        r = d / abs(b[idx]) if b[idx] != 0 else float("inf")
        if r > tol:
            cnt += 1
        if r == float("inf"):
            worst, loc = r, idx
        elif worst != float("inf") and r > worst:
            worst, loc = r, idx
    return (float(worst) if worst != float("inf") else worst), loc, cnt, a.size


def selftest(brk):
    rng = np.random.default_rng(7)
    base = np.zeros((8, 3, 4))
    base[0] = rng.standard_normal((3, 4))
    base[1] = base[0] * 1e-17
    base[2] = base[0] * 1e-34
    cases = []
    cases.append(("identical jets", base, base.copy(), lambda r: r is not None and r[0] == 0 and r[2] == 0))
    ch = base.copy(); ch[2, 1, 2] += 1e-30 * abs(base[0, 1, 2])
    cases.append(("one coefficient changed by 1e-30 relative", ch, base, lambda r: r is not None and 0.9e-30 < r[0] < 1.1e-30 and r[1] == (1, 2) and r[2] == 1))
    sm = base.copy(); sm[2, 2, 1] += 1e-50 * abs(base[0, 2, 1])
    cases.append(("one coefficient changed by 1e-50 relative (below tol)", sm, base, lambda r: r is not None and 0 < r[0] < 1e-40 and r[2] == 0))
    zr = base.copy(); b0 = base.copy(); b0[:, 0, 0] = 0
    cases.append(("zero coefficient against a nonzero one", zr, b0, lambda r: r is not None and r[0] == float("inf") and r[1] == (0, 0)))
    cases.append(("shape mismatch", base, base[:, :2], lambda r: r is None))
    if brk:
        cases[1] = (cases[1][0], cases[1][1], cases[1][2], lambda r: r is not None and r[0] == 0)
    bad = 0
    for name, A, B, chk in cases:
        r = diff(A, B)
        ok = chk(r)
        print(f"  {name}: {r}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 1e-40
    A, B = load(sys.argv[1]), load(sys.argv[2])
    r = diff(A, B, tol)
    if r is None:
        print(f"shape mismatch: {A.shape} against {B.shape}")
        sys.exit(2)
    worst, loc, cnt, n = r
    print(f"largest relative difference per coefficient {worst:.4e} at order {loc[0]}, unknown {loc[1]}; {cnt} of {n} coefficients above {tol:g}")
    sys.exit(0 if worst <= tol else 1)
