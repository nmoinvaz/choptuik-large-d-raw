"""T84: what the nearly singular directions of the full system are, in a layout with the last node moved toward the
horizon. At a state: the quad-double Jacobian's LU (Solver.newton_q), its w weakest right singular directions
(driver.weak_subspace_q), Rayleigh-Ritz on them: per direction its singular value, its Delta component, the block
holding most of it (centre data, a node's state, the horizon data) and, for the centre block, p1's harmonics 1..13.

    python3 qd_weak.py STATE.npz [w] [threads]
"""
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
from hpkernel.driver import load_q, make_solver, weak_subspace_q  # noqa: E402
from pinning import band_coeffs  # noqa: E402

path = sys.argv[1]
w = int(sys.argv[2]) if len(sys.argv) > 2 else 24
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 2
z, m = load_q(path)
D, M, nodes = m["D"], m["M"], list(m["nodes"])
s = make_solver(D, M, nodes=nodes, kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=13)
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
st = s.newton_q(*z)
L = s.size
print(f"{os.path.basename(path)}: D {D}, nodes {nodes}, L {L}; pivots {st[6]:.1e}..{st[7]:.1e}, |F| {np.abs(st[4]).max():.1e}", flush=True)
V = weak_subspace_q(s, w)
zero = np.zeros(L)
W = np.empty_like(V)
for j in range(w):
    y = s.qlu_solve(np.ascontiguousarray(V[:, j]), zero, zero, zero, transpose=True)
    x = s.qlu_solve(*(np.ascontiguousarray(np.asarray(p)) for p in y))
    W[:, j] = np.asarray(x[0]) + np.asarray(x[1])
H = V.T @ W
ev, U = np.linalg.eigh((H + H.T) / 2)
X = V @ U
X /= np.linalg.norm(X, axis=0)
sig = 1 / np.sqrt(np.maximum(ev, 1e-300))
K = len(nodes)
names = ["centre"] + [f"node {x}" for x in nodes] + ["horizon+Delta"]
bounds = [0, 2 * M] + [2 * M + 4 * M * (i + 1) for i in range(K)] + [L]
hk = [1, 3, 5, 7, 9, 11, 13]
print(f"{'sigma':>9} {'Delta comp':>11} {'block (mass)':>22}  p1 harmonics 1..13 (|c|, of the direction's p1 part)")
for j in np.argsort(sig):
    x = X[:, j]
    mass = [float(np.sum(x[bounds[i]:bounds[i + 1]] ** 2)) for i in range(len(names))]
    b = int(np.argmax(mass))
    c = np.ravel(band_coeffs(x[:M], np.zeros(M), M, hk))
    amp = [float(np.hypot(c[2 * i], c[2 * i + 1])) for i in range(len(hk))]
    print(f"{sig[j]:9.1e} {abs(x[-1]):11.1e} {names[b]:>14s} ({mass[b]:.2f})  " + " ".join(f"{a:.1e}" for a in amp), flush=True)
