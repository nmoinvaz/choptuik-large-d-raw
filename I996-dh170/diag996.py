#!/usr/bin/env python3
"""#996: why does amp_trunc_hiermodel.py M 18 1000 1.0 stop at M = 9 with "ValueError: matrix is numerically singular" (mp.qr_solve in S_at), while M = 3, 5, 7 run?
mp.qr_solve(A, y) factors the augmented matrix [A | y] with mpmath's householder, which raises when the squared norm of a column's remaining part is not above
the context's eps. So the error says either that A has a dependent column or that y is inside the span of A to better than about sqrt(eps). This script builds the
model, forms the A and y of the first S_at call the failing run reaches (S_at(1, 1)) by the script's own routines, factors A alone (mp.qr), and prints norm(y),
the least-squares residual of the fit and eps, for the M given.
    python diag996.py M         (from any directory; the worktree's solver/proof is put on sys.path)"""
import sys
import mpmath as mp

WT = "/home/nathan/Source/choptuik-large-d-996/solver"
sys.path.insert(0, WT + "/proof")
sys.path.insert(0, WT + "/inner_amp")
import amp_trunc_hiermodel as T  # noqa: E402

M = int(sys.argv[1])
a = T.AmpHierModel(1.0, 3, 1000, M)
orig = mp.qr_solve
seen = {}


def spy(A, y):
    seen["A"], seen["y"] = A, y
    return orig(A, y)


mp.qr_solve = spy
try:
    a.run()
    print(f"M {M}: run to K 3 went through")
except ValueError as e:
    print(f"M {M}: ValueError {e}")
A, y = seen["A"], seen["y"]
print(f"A {A.rows} x {A.cols}, mp.prec {mp.mp.prec}, eps {mp.nstr(mp.mp.eps, 3)}")
Q, R = mp.qr(A)                # A alone
dmin = min(abs(R[i, i]) for i in range(A.cols))
print(f"smallest |R_ii| of A alone {mp.nstr(dmin, 3)} (A itself is {'singular' if dmin * dmin <= mp.mp.eps else 'not singular'} by the same test)")
c = mp.lu_solve(R[:A.cols, :A.cols], (Q.H * y)[:A.cols, 0])
res = mp.norm(y - A * c)
print(f"norm(y) {mp.nstr(mp.norm(y), 6)}, least-squares residual {mp.nstr(res, 6)}, residual squared {mp.nstr(res * res, 3)} against eps {mp.nstr(mp.mp.eps, 3)}: "
      f"{'<= eps, so the augmented column is declared singular' if res * res <= mp.mp.eps else '> eps'}")
