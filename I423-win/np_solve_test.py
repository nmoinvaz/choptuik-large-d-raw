#!/usr/bin/env python3
"""#423 side task 2: numpy's own OpenBLAS (the wheel's ILP64 build) on the same random matrix as lu_size_test.py: np.linalg.solve(A, b) with b = A x0, which must return x0.
usage: OPENBLAS_NUM_THREADS=2 python -X faulthandler np_solve_test.py N [SEED]
Same generator and order as lu_size_test.py (default_rng(seed 1): A = standard_normal((n, n)), then x0 = standard_normal(n)). Prints the threadpoolctl lines first (version, architecture, threading layer, threads),
then the seconds of the solve and max|x - x0|."""
import sys
import time

import numpy as np
import threadpoolctl

n = int(sys.argv[1])
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
for p in threadpoolctl.threadpool_info():
    print(f"threadpool: {p['internal_api']} {p['version']}, architecture {p['architecture']}, threading layer {p['threading_layer']}, threads {p['num_threads']}, {p['filepath'].rsplit(chr(92), 1)[-1]}", flush=True)
A = rng.standard_normal((n, n))
x0 = rng.standard_normal(n)
print(f"n {n}: matrix {A.nbytes / 2**30:.2f} GiB ({A.nbytes} bytes), numpy {np.__version__}", flush=True)
b = A @ x0
print("matvec A @ x0 done", flush=True)
t = time.time()
x = np.linalg.solve(A, b)
print(f"np.linalg.solve done in {time.time() - t:.0f} s: max|x - x0| = {np.abs(x - x0).max():.2e}", flush=True)
print("np solve test done", flush=True)
