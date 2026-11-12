"""Run near_null.main on a mock solver (numpy, f64, M = 4, K = 1) to exercise the new code paths. Scratch for #501."""
import sys

import numpy as np

HP = sys.argv[1]
sys.path.insert(0, HP)
import near_null  # noqa: E402

M, K = 4, 1
L = 4 * M + 4 * M * K + 1
rng = np.random.default_rng(5)
A = rng.standard_normal((L, L)) + 5 * np.eye(L)
z0 = rng.standard_normal(L)
b = A @ z0 + 1e-3 * rng.standard_normal(L)


def F(x):
    return A @ x - b + 0.0 * x * x


class S:
    size = L

    def plan(self, *a):
        return [[0.3, 1.0]]

    def set_segs(self, segs):
        self.segs = segs

    def newton_o(self, z):
        x = np.asarray(z[0]) + np.asarray(z[1])
        self.A = A
        dz = -np.linalg.solve(A, F(x))
        return (dz,) + tuple(np.zeros(L) for _ in range(7)), F(x), np.zeros(L), 1e-3, 1e3

    def olu_solve(self, bb, transpose=False):
        v = np.asarray(bb[0]) + np.asarray(bb[1])
        x = np.linalg.solve(A.T if transpose else A, v)
        return (x,) + tuple(np.zeros(L) for _ in range(7))

    def jacobian_o(self, z):
        return [A] + [np.zeros((L, L)) for _ in range(7)]

    def residual_o(self, z):
        x = np.asarray(z[0]) + np.asarray(z[1])
        return (F(x),) + tuple(np.zeros(L) for _ in range(7))


near_null.make_solver = lambda *a, **k: S()
near_null.load_o = lambda p: ((z0.copy(),) + tuple(np.zeros(L) for _ in range(7)),
                              dict(M=M, nodes=[0.3], D=10.0, segs=[[0.3, 1.0]], kfreeze=3))
sys.argv = ["near_null.py", "raw", "st", "--its=4", "--k=2"] + sys.argv[2:]
print("exit", near_null.main())
