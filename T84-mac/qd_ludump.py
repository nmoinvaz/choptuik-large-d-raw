"""T84: dump the quad-double Jacobian (four parts), the LU's solves of a random b (plain and transposed), the Newton
step and the residual at a state, for an exact check (qd_luexact.py, python-flint).

    python3 qd_ludump.py STATE.npz OUT.npz [threads]
"""
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel.driver import load_q, make_solver  # noqa: E402

path, out = sys.argv[1], sys.argv[2]
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
st = s.newton_q(*z)
L = s.size
J = [np.asarray(p) for p in s.jacobian_q(*z)]
zero = np.zeros(L)
b = np.random.default_rng(2).standard_normal(L)
x = [np.asarray(p) for p in s.qlu_solve(np.ascontiguousarray(b), zero, zero, zero)]
y = [np.asarray(p) for p in s.qlu_solve(np.ascontiguousarray(b), zero, zero, zero, transpose=True)]
np.savez(out, J0=J[0], J1=J[1], J2=J[2], J3=J[3], b=b, x0=x[0], x1=x[1], x2=x[2], x3=x[3], y0=y[0], y1=y[1], y2=y[2], y3=y[3],
         dz0=st[0], dz1=st[1], dz2=st[2], dz3=st[3], F0=st[4], F1=st[5], piv=np.array([st[6], st[7]]))
print(f"dumped L {L}, pivots {st[6]:.1e}..{st[7]:.1e}, |dz| {np.abs(st[0]).max():.1e}, |F| {np.abs(st[4]).max():.1e}")
