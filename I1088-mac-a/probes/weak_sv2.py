"""The weakest singular values of the full system's octo-double Jacobian at a stored chain state (#1086's T1 gain):
make_solver with kfreeze K (13: p1's harmonics 1-13 free, 15 and up zero; none: all free), the state's segments and
orders, Solver.newton_o for the LU, then octo_corrector.junk_subspace_o's subspace iteration on (J^T J)^-1 with every
direction kept (delta_max 2). Prints each sigma with its direction's Delta component and the p1 harmonic it lies on most.

    python3 weak_sv.py STATE.npz THREADS KFREEZE W ITERS [W2]

W2 > 0: a second subspace iteration of W2 directions on the complement of the first's directions with sigma below
the f64 Rayleigh-Ritz's resolution (eigenvalue of (J^T J)^-1 above 1e-12 of the largest), deflated each iteration, so
that the weaker spectrum (the Delta mode) is resolved: the first iteration's eigenvalues span 1e34 to 5e49 at D 245.6
and f64 resolves only the top 1e16 of that (weak_sv_k13.log printed a negative one on dh370).
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from hpkernel.driver import make_solver
from octo_corrector import load_o, D_of, junk_subspace_o
from pinning import band_coeffs

p, thr, kf, w, iters = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
z, meta = load_o(p)
M, K = meta["M"], len(meta["nodes"])
s = make_solver(D_of(meta), M, nodes=meta["nodes"], kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr,
                kfreeze=None if kf == "none" else int(kf))
s.set_segs(meta["segs"])
t = time.time()
d, Fh, Fl, pmin, pmax = s.newton_o(list(z))
print(f"D {meta['D']}, kfreeze {kf}, ks {meta['ks']}: newton_o {time.time() - t:.0f} s, max|F| "
      f"{np.abs(np.asarray(Fh) + np.asarray(Fl)).max():.3e}, pivots {pmin:.3e} .. {pmax:.3e}", flush=True)
zero = np.zeros(s.size)
eD = np.zeros(s.size); eD[-1] = 1.0
g = np.asarray(s.olu_solve([eD] + [zero] * 7, True)[0])          # row Delta of J^-1: dDelta = -g . F
print(f"Delta's gain: sum |dDelta/dF_i| {np.abs(g).sum():.3e}, max {np.abs(g).max():.3e} at row {int(np.argmax(np.abs(g)))}"
      f" (block {int(np.argmax(np.abs(g))) // (4 * M)}); first-order dDelta of this state's F: {-(g @ (np.asarray(Fh) + np.asarray(Fl))):.3e}", flush=True)
t = time.time()
V, sk, sd = junk_subspace_o(s, w, delta_max=2.0, iters=iters)
print(f"subspace iteration ({w} directions, {iters} iterations): {time.time() - t:.0f} s", flush=True)
# Rayleigh-Ritz again on V to pair each sigma with its vector


def apply(v):
    y = s.olu_solve([np.ascontiguousarray(v)] + [zero] * 7, True)
    return np.asarray(s.olu_solve([np.ascontiguousarray(np.asarray(y[0]))] + [zero] * 7, False)[0])


W = np.column_stack([apply(V[:, j]) for j in range(V.shape[1])])
H = V.T @ W
ev, U = np.linalg.eigh((H + H.T) / 2)
X = V @ U
order = np.argsort(-ev)
W2 = int(sys.argv[6]) if len(sys.argv) > 6 else 0
if W2:
    keep = [j for j in order if ev[j] > 1e-12 * ev.max()]
    Vd = np.linalg.qr(X[:, keep])[0]
    rng = np.random.default_rng(1)
    V2 = np.linalg.qr(rng.standard_normal((s.size, W2)))[0]
    for _ in range(iters + 2):
        V2 = V2 - Vd @ (Vd.T @ V2)
        V2 = np.column_stack([apply(V2[:, j]) for j in range(W2)])
        V2 = V2 - Vd @ (Vd.T @ V2)
        V2 = np.linalg.qr(V2)[0]
    W2m = np.column_stack([apply(V2[:, j]) for j in range(W2)])
    W2m = W2m - Vd @ (Vd.T @ W2m)
    H2 = V2.T @ W2m
    ev2, U2 = np.linalg.eigh((H2 + H2.T) / 2)
    X2 = V2 @ U2
    print(f"deflated: {len(keep)} directions removed, {W2} more:", flush=True)
    X = np.column_stack([X[:, keep], X2])
    ev = np.r_[ev[keep], ev2]
    order = np.argsort(-ev)
for j in order:
    x = X[:, j] / np.linalg.norm(X[:, j])
    sig = 1 / np.sqrt(ev[j])
    co = band_coeffs(x[:M], np.zeros(M), M, list(range(1, 32, 2)))
    amps = [abs(a) + abs(b) for a, b in co]
    k = 2 * int(np.argmax(amps)) + 1
    print(f"  sigma {sig:.3e}  |Delta comp| {abs(x[-1]):.2e}  p1 part {np.linalg.norm(x[:M]):.2e} (harmonic {k} "
          f"{max(amps):.1e})  horizon data {np.linalg.norm(x[2 * M + 4 * M * K:-1]):.2e}", flush=True)
