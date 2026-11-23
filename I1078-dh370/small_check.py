"""#1078: the check of mode_scale.py's --small=K output: logdet_lu(A, small=K) must return the K smallest |pivots| with the index of the unknown (column) each belongs to.

A planted 200 x 200 matrix: a well-conditioned dense matrix whose rows and columns are permuted in blocks so that, after the LU with partial pivoting, the pivot at the
planted index is small. Simplest planted case: A = diag-dominant lower-triangular-in-effect matrix with known diagonal d_k (no row interchanges needed when the diagonal
dominates), so U_kk = d_k up to the elimination; here the matrix is upper triangular with the diagonal d: U_kk = d_k exactly, and pivot k belongs to unknown k.
Exit 0 iff the K smallest returned (index, value) pairs equal the planted ones. --mutate=shift shifts the returned indices by one: it must exit 1."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.getcwd()))
import mode_scale as MS  # noqa: E402

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
n, K = 200, 5
rng = np.random.default_rng(3)
d = rng.uniform(0.5, 2.0, n)
planted = {17: 1e-9, 63: -2e-9, 120: 3e-9, 5: 4e-9, 199: -5e-9}
for i, v in planted.items():
    d[i] = v
A = np.triu(rng.uniform(-0.3, 0.3, (n, n)), 1) + np.diag(d)
r = MS.logdet_lu(A, small=K)
got = [(i + (1 if MUT == "shift" else 0), v) for i, v in r[4]]
want = sorted(((i, v) for i, v in planted.items()), key=lambda t: abs(t[1]))
ok = [g[0] for g in got] == [w[0] for w in want] and all(abs(g[1] - w[1]) <= 1e-12 * abs(w[1]) for g, w in zip(got, want))
print(f"small_check{' --mutate=shift' if MUT else ''}: {'PASS' if ok else 'FAIL'}; returned {got}; planted {want}")
sys.exit(0 if ok else 1)
