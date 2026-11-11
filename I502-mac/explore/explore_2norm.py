#!/usr/bin/env python3
"""#502 exploration: why near_null_eq.py does not use the 2-norm (doubly stochastic) equilibration.

    python3 explore_2norm.py J0.npz

J0.npz holds J0, the f64 leading part of the octo-double Jacobian of the 0.3-0.7 state (dumpJ.py). After Ruiz's
max-norm iteration (tol 1e-12), B = |D_r J D_c|^2 is balanced by Ruiz's iteration in the 2-norm (rows and columns of
D_r J D_c divided by the square roots of their 2-norms): its largest |1 - 2-norm| is printed every 2e5 iterations to
1e6. Then the Hessian of Newton's method for the same balancing, on the convex potential
f(u, w) = sum_ij B_ij e^(u_i + w_j) - sum u - sum w at u = w = 0, with u_0 held: its smallest eigenvalues.
"""
import sys

import numpy as np

A = np.abs(np.load(sys.argv[1])["J0"])
L = A.shape[0]
dr, dc = np.ones(L), np.ones(L)
for it in range(1000):
    B = A * dr[:, None] * dc[None, :]
    r, c = B.max(axis=1), B.max(axis=0)
    if max(np.abs(1 - r).max(), np.abs(1 - c).max()) < 1e-12:
        break
    dr /= np.sqrt(r)
    dc /= np.sqrt(c)
print(f"max-norm stage: {it} iterations", flush=True)
B2 = (A * dr[:, None] * dc[None, :]) ** 2
er, ec = np.ones(L), np.ones(L)
for it in range(1000001):
    r2 = er ** 2 * (B2 @ ec ** 2)
    c2 = ec ** 2 * (er ** 2 @ B2)
    if it % 200000 == 0:
        err = max(np.abs(1 - np.sqrt(r2)).max(), np.abs(1 - np.sqrt(c2)).max())
        print(f"2-norm Ruiz iteration {it}: largest |1 - 2-norm| {err:.3e}, D_c {(dc * ec).min():.2e}..{(dc * ec).max():.2e}",
              flush=True)
    er /= r2 ** 0.25
    ec /= c2 ** 0.25
r, c = B2.sum(axis=1), B2.sum(axis=0)
H = np.block([[np.diag(r), B2], [B2.T, np.diag(c)]])
H[0, :] = 0
H[:, 0] = 0
H[0, 0] = 1
ev = np.linalg.eigvalsh(H)
print("Newton's Hessian at the max-norm stage, u_0 held: smallest eigenvalues " + ", ".join(f"{x:.2e}" for x in ev[:4])
      + f"; largest {ev[-1]:.2e}")
