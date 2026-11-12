"""Linearity of G(z - t w) = F(z - t w) - F(z) in t, by residual block, at near_null's plan: the planted residual must
scale with t if it is -t J w. Scratch probe for #501."""
import os
import sys

import numpy as np

HP = sys.argv[1]
sys.path.insert(0, HP)
from hpkernel.driver import make_solver  # noqa: E402
from multidouble import od_axpy  # noqa: E402
from octo_corrector import load_o  # noqa: E402

raw, st = sys.argv[2], sys.argv[3]
z, m = load_o(os.path.join(raw, st))
z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
M, nodes = int(m["M"]), list(m["nodes"])
D = m.get("D_str", repr(float(m["D"])))
s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2,
                kfreeze=int(m.get("kfreeze", 3)))
s.set_segs(s.plan(z[0], z[1], 1e-32, 0.05))
L = len(z[0])
K = len(nodes)
zero = np.zeros(L)
g = np.random.default_rng(2).standard_normal(L)
w = g / np.linalg.norm(g)
F0 = [np.asarray(p) for p in s.residual_o(z)]
F0b = [np.asarray(p) for p in s.residual_o(z)]
print("residual_o(z) twice, max diff of the eight-part sums:",
      float(np.abs(od_axpy(-1.0, *F0b, *F0)[0]).max()), flush=True)


def G(t):
    zp = [np.ascontiguousarray(p) for p in od_axpy(-t, *([np.ascontiguousarray(w)] + [zero] * 7), *z)]
    Fp = [np.asarray(p) for p in s.residual_o(zp)]
    d = od_axpy(-1.0, *F0, *Fp)
    return np.asarray(d[0]) + np.asarray(d[1])


def blocks(v):
    out = []
    for b in range(K + 1):
        out.append(float(np.abs(v[4 * M * b:4 * M * (b + 1)]).max()))
    out.append(float(np.abs(v[4 * M * (K + 1):]).max()))
    return out


for t in [float(x) for x in sys.argv[4].split(",")]:
    g1, g2 = G(t), G(2 * t)
    lin = np.abs(g2 - 2 * g1).max() / np.abs(g2).max()
    print(f"t {t:.0e}: max|G| {np.abs(g1).max():.3e}, |G(2t) - 2 G(t)| / |G(2t)| {lin:.1e}; by block (rows of 4M): "
          + " ".join(f"{x:.1e}" for x in blocks(g1)), flush=True)
    # by row within the block whose linearity is worst
    r = np.abs(g2 - 2 * g1) / (np.abs(g2) + 1e-300)
    i = int(np.argmax(np.abs(g2 - 2 * g1)))
    print(f"   worst row {i} (block {i // (4 * M)}, field {(i % (4 * M)) // M}, j {i % M}): G(t) {g1[i]:.3e}, "
          f"G(2t) {g2[i]:.3e}", flush=True)
