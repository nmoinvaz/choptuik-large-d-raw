"""Which unknowns carry the horizon rows' quadratic term: G(t) = F(z - t u) - F(z) for u a random unit vector inside
one block of z, the nonlinearity |G(2t) - 2 G(t)| / |G(2t)| at t, at near_null's plan. Scratch probe for #501."""
import os
import sys

import numpy as np

HP = sys.argv[1]
sys.path.insert(0, HP)
from hpkernel.driver import make_solver  # noqa: E402
from multidouble import od_axpy  # noqa: E402
from near_null import layout  # noqa: E402
from octo_corrector import load_o  # noqa: E402

raw, st, t = sys.argv[2], sys.argv[3], float(sys.argv[4])
z, m = load_o(os.path.join(raw, st))
z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
M, nodes = int(m["M"]), list(m["nodes"])
D = m.get("D_str", repr(float(m["D"])))
s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2,
                kfreeze=int(m.get("kfreeze", 3)))
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
L = len(z[0])
zero = np.zeros(L)
F0 = [np.asarray(p) for p in s.residual_o(z)]
rng = np.random.default_rng(3)


def G(u, tt):
    zp = [np.ascontiguousarray(p) for p in od_axpy(-tt, *([np.ascontiguousarray(u)] + [zero] * 7), *z)]
    d = od_axpy(-1.0, *F0, *[np.asarray(p) for p in s.residual_o(zp)])
    return np.asarray(d[0]) + np.asarray(d[1])


blocks = layout(M, len(nodes)) + [("Delta", L - 1, 0)]
for name, o, _ in blocks:
    n = 1 if name == "Delta" else M
    u = np.zeros(L)
    u[o:o + n] = rng.standard_normal(n)
    u /= np.linalg.norm(u)
    g1, g2 = G(u, t), G(u, 2 * t)
    nl = np.abs(g2 - 2 * g1).max() / np.abs(g2).max()
    i = int(np.argmax(np.abs(g2 - 2 * g1)))
    print(f"{name:<9} |z| {np.linalg.norm(z[0][o:o + n]):.2e}: max|G| {np.abs(g1).max():.2e}, nonlinearity {nl:.1e} "
          f"(row {i}, residual block {i // (4 * M)})", flush=True)
