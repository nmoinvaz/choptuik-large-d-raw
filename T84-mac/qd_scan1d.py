"""T84: the residual along the weakest direction with Delta content, through a state: |F(z + t v)| for t from -1e-5
to 1e-5 (log-spaced), in quad-double, with v from Rayleigh-Ritz on the quad-double Jacobian's weak subspace (the
direction of smallest sigma among those with |Delta component| > 0.1). A simple root crosses zero linearly in t, a
double root touches it, a positive minimum means no real root along v. Also the residual's component along J v.

    python3 qd_scan1d.py STATE.npz [threads]
"""
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from hpkernel import qd_axpy  # noqa: E402
from hpkernel.driver import load_q, make_solver, qmax, weak_subspace_q  # noqa: E402

path = sys.argv[1]
threads = int(sys.argv[2]) if len(sys.argv) > 2 else 2
z, m = load_q(path)
D, M = m["D"], m["M"]
s = make_solver(D, M, nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
st = s.newton_q(*z)
L = s.size
V = weak_subspace_q(s, 24)
zero = np.zeros(L)
W = np.empty_like(V)
for j in range(V.shape[1]):
    y = s.qlu_solve(np.ascontiguousarray(V[:, j]), zero, zero, zero, transpose=True)
    x = s.qlu_solve(*(np.ascontiguousarray(np.asarray(p)) for p in y))
    W[:, j] = np.asarray(x[0]) + np.asarray(x[1])
H = V.T @ W
ev, U = np.linalg.eigh((H + H.T) / 2)
X = V @ U
X /= np.linalg.norm(X, axis=0)
sig = 1 / np.sqrt(np.maximum(ev, 1e-300))
cand = [j for j in range(len(sig)) if ev[j] > 0 and abs(X[-1, j]) > 0.1]
j = min(cand, key=lambda k: sig[k])
v = np.ascontiguousarray(X[:, j])
print(f"{os.path.basename(path)}: D {D}, |F(z)| {qmax(st[4:6]):.2e}, Newton |dz| {np.abs(st[0]).max():.1e}; direction: sigma {sig[j]:.1e}, "
      f"Delta component {X[-1, j]:+.3f}, Newton step along it {float(v @ (st[0] + st[1])):+.2e}", flush=True)
F0 = s.residual_q(*z)
f0 = np.asarray(F0[0]) + np.asarray(F0[1])
print(f"{'t':>10} {'max|F|':>10} {'|F|_2':>10} {'F . F0/|F0| (2-norm projection)':>34}")
for t in [0.0] + [sg * 10.0 ** e for e in range(-5, -15, -1) for sg in (1, -1)]:
    zt = qd_axpy(t, v, zero, zero, zero, *z)
    F = s.residual_q(*zt)
    f = np.asarray(F[0]) + np.asarray(F[1])
    print(f"{t:+10.0e} {np.abs(f).max():10.2e} {np.linalg.norm(f):10.2e} {float(f @ f0) / np.linalg.norm(f0):+34.2e}", flush=True)
