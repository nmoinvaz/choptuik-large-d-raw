"""T84: the quad-double LU of Solver.newton_q against the Jacobian matrix of Solver.jacobian_q at a state: for a random
right-hand side b, |J x - b| / |b| with x = qlu_solve(b), and |J^T y - b| / |b| with y = qlu_solve(b, transpose=True),
in f64 (the parts summed). The weak subspace of driver.weak_subspace_q rests on both solves.

    python3 qd_lucheck.py STATE.npz [threads]
"""
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver  # noqa: E402

path = sys.argv[1]
threads = int(sys.argv[2]) if len(sys.argv) > 2 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
st = s.newton_q(*z)
L = s.size
J = s.jacobian_q(*z)
Jm = [np.asarray(p) for p in J]
Jsum = Jm[0] + Jm[1]
zero = np.zeros(L)
rng = np.random.default_rng(2)
for trial in range(2):
    b = rng.standard_normal(L)
    x = s.qlu_solve(np.ascontiguousarray(b), zero, zero, zero)
    xs = np.asarray(x[0]) + np.asarray(x[1])
    y = s.qlu_solve(np.ascontiguousarray(b), zero, zero, zero, transpose=True)
    ys = np.asarray(y[0]) + np.asarray(y[1])
    print(f"b {trial}: |J x - b|/|b| {np.linalg.norm(Jsum @ xs - b) / np.linalg.norm(b):.2e} (|x| {np.linalg.norm(xs):.1e}); "
          f"|J^T y - b|/|b| {np.linalg.norm(Jsum.T @ ys - b) / np.linalg.norm(b):.2e} (|y| {np.linalg.norm(ys):.1e})", flush=True)
# the Newton step itself: J dz = -F
dz = np.asarray(st[0]) + np.asarray(st[1])
F = np.asarray(st[4]) + np.asarray(st[5])
print(f"Newton step: |J dz + F| / |F| {np.linalg.norm(Jsum @ dz + F) / np.linalg.norm(F):.2e}; pivots {st[6]:.1e}..{st[7]:.1e}; "
      f"J entries: max {np.abs(Jsum).max():.1e}, Delta column max {np.abs(Jsum[:, -1]).max():.1e}, Delta row max {np.abs(Jsum[-1, :]).max():.1e}", flush=True)
sv = np.linalg.svd(Jsum, compute_uv=False)
print(f"f64 singular values of J (parts summed): largest {sv[0]:.1e}, smallest five " + " ".join(f"{v:.1e}" for v in sv[-5:]), flush=True)
