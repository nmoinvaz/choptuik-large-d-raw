"""T84: the quad-double Jacobian against finite differences at a state, along the LU's weakest Delta-carrying
direction v (as qd_scan1d.py) and along a random direction: |J v| from Solver.jacobian_q against
(F(z + t v) - F(z)) / t, and the p1-harmonic content of v above kfreeze 13.

    python3 qd_jvcheck.py STATE.npz [threads]
"""
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
from hpkernel import qd_axpy  # noqa: E402
from hpkernel.driver import load_q, make_solver, qmax, weak_subspace_q  # noqa: E402
from pinning import band_coeffs  # noqa: E402

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
j = min((k for k in range(len(sig)) if ev[k] > 0 and abs(X[-1, k]) > 0.1), key=lambda k: sig[k])
v = np.ascontiguousarray(X[:, j])
J = s.jacobian_q(*z)
Jm = np.asarray(J[0]) + np.asarray(J[1])
rng = np.random.default_rng(1)
r = rng.standard_normal(L); r /= np.linalg.norm(r)
F0 = s.residual_q(*z)
f0 = np.asarray(F0[0]) + np.asarray(F0[1])
hk = list(range(1, 32, 2))
for name, d in (("weak v", v), ("random", np.ascontiguousarray(r))):
    jv = Jm @ d
    t = 1e-10
    F = s.residual_q(*qd_axpy(t, d, zero, zero, zero, *z))
    fd = (np.asarray(F[0]) + np.asarray(F[1]) - f0) / t
    c = np.ravel(band_coeffs(d[:M], np.zeros(M), M, hk))
    amp = [float(np.hypot(c[2 * i], c[2 * i + 1])) for i in range(len(hk))]
    big = sum(a * a for a, k in zip(amp, hk) if k > 13)
    print(f"{name}: |J d|_2 {np.linalg.norm(jv):.2e}, |FD|_2 {np.linalg.norm(fd):.2e}, |J d - FD|_2 {np.linalg.norm(jv - fd):.2e}; "
          f"mass of d in p1 {float(np.sum(d[:M] ** 2)):.2f}, of which harmonics > 13: {big:.2f}; Delta comp {d[-1]:+.2f}", flush=True)
    print("   p1 harmonics 1..31: " + " ".join(f"{a:.1e}" for a in amp), flush=True)
print(f"sigma of v by the LU: {sig[j]:.1e}; J's smallest pivot {st[6]:.1e}", flush=True)
