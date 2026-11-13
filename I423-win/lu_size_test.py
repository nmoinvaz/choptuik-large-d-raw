#!/usr/bin/env python3
"""#423: does scipy.linalg.lu_factor of an F-ordered float64 matrix crash on this machine above 4 GiB (the 48x141 Jacobian is 23857^2 = 4.24 GiB; the 32x141 one, 15905^2 = 1.9 GiB, factors)?
usage: OPENBLAS_NUM_THREADS=2 python -X faulthandler lu_size_test.py N [SEED]       the same call as rt_mpsolve.LUdd: lu_factor(A.T, overwrite_a=True, check_finite=False) on a C-order A.
Planted check that the factors are right when it does not crash: r = A.T x0 is formed before the factorization, and lu_solve with the factors must return x0 to about cond * 1e-16."""
import sys
import time

import numpy as np
import scipy
import scipy.linalg as sl

n = int(sys.argv[1])
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
A = rng.standard_normal((n, n))
print(f"n {n}: matrix {A.nbytes / 2**30:.2f} GiB ({A.nbytes} bytes; 2^32 = {2**32}), scipy {scipy.__version__}, numpy {np.__version__}", flush=True)
x0 = rng.standard_normal(n)
r = A.T @ x0
t = time.time()
f, piv = sl.lu_factor(A.T, overwrite_a=True, check_finite=False)
print(f"lu_factor done in {time.time() - t:.0f} s, in place: {np.shares_memory(f, A)}", flush=True)
z = sl.lu_solve((f, piv), r, check_finite=False)
print(f"lu_solve: max|z - x0| = {np.abs(z - x0).max():.2e}", flush=True)
print("lu test done", flush=True)
