"""#964: the affine zero of ALL the solves of a radius, accepted or not (m7_outer.py --fit and --local use only |r_3| < 1e-6).
Prints a separate labelled line: it is what a looser bar would give, and not a result until the bar is justified.
Under --schur r_1 is corrected for r_3 to first order, so this line shows the effect of the bar and not the raw r_1.

    python3 affine_all.py LOG [LOG ...]       run from solver/inner_stokes/ (imports m7_outer.point)
    python3 affine_all.py --selftest [--mutate=sign]   planted affine r_1 with a known zero, recovered to 1e-9
"""
import sys
import numpy as np


def affine_zero(pts):
    """pts: [(p (2,), r (2,) as Re, Im)]; least-squares r = r0 + J (p - pref); returns zero, J singular values, residuals"""
    P = np.array([t[0] for t in pts]); Y = np.array([t[1] for t in pts])
    pref = P.mean(axis=0)
    X = np.column_stack([np.ones(len(P)), P - pref])
    C, *_ = np.linalg.lstsq(X, Y, rcond=None)
    J = C[1:].T
    z = pref - np.linalg.solve(J, C[0])
    return z, np.linalg.svd(J, compute_uv=False), np.linalg.norm(Y - X @ C, axis=1)


def selftest(mut):
    rng = np.random.default_rng(1)
    z0 = np.array([2.7192, 1.00002]); J0 = np.array([[1.2e4, -3.0e3], [2.0e3, 5.7e3]])
    P = np.array([[2.719219, 1.000022], [2.719419, 1.000022], [2.719219, 1.000122], [2.719219, 1.000022]])
    Y = (P - z0) @ J0.T
    if mut:
        Y = Y * np.array([1.0, -1.0])      # the zero is unchanged by a row sign, so also shift the model off
        Y = Y + np.array([0.0, 0.5])
    z, sv, res = affine_zero([(p, y) for p, y in zip(P, Y)])
    err = np.abs(z - z0).max()
    print(f"planted zero {z0}, recovered {z}, max error {err:.1e}, residuals {res.max():.1e}")
    ok = err < 1e-9
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest(any(a == "--mutate=sign" for a in sys.argv)))
    import m7_outer
    pts = [m7_outer.point(f, True) for f in sys.argv[1:]]
    for (_, p, r, r3), f in zip(pts, sys.argv[1:]):
        print(f"  {p[0]:.9f} {p[1]:.9f}   r_1 {r[0]:+.4f}{r[1]:+.4f}i   |r_3| {r3:.1e}{'' if r3 < 1e-6 else '  (above the bar)'}   ({f})")
    z, sv, res = affine_zero([(t[1], t[2]) for t in pts])
    print(f"NOT ACCEPTED by the 1e-6 bar: affine zero of all {len(pts)} solves: A {z[0]:.6f}, w/w_inf {z[1]:.6f}; "
          f"J singular values {np.array2string(sv, precision=1)}; residuals {np.array2string(res, precision=3)}")
