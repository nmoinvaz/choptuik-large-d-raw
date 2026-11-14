#!/usr/bin/env python3
"""#752: the stored D 117 state's pinned octo-double residual on this machine's kernel, of the state itself and of its
projection (ElimO, switch 0: Reseeder.project at its quad-double rounding, then refine_o 3), by block. On win both
were 1.75e-64 (#742's N.log and M.log: the base polish converged at step 0). Run from the worktree's hp/.
usage: python3 base_resid.py RAW [--threads 4]"""
import json
import sys
import time

import mpmath as mp
import numpy as np

sys.path.insert(0, ".")
from hpkernel.driver import make_solver, qmax  # noqa: E402
from octo_corrector import ElimO, PinnedO, load_o, o8, omax, q4_of_o  # noqa: E402
from pinning import PinnedQ, PinnedSolver, band_field  # noqa: E402
from reseed import Reseeder  # noqa: E402
import hpkernel  # noqa: E402

mp.mp.dps = 50
raw = sys.argv[1]
threads = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 4
path = f"{raw}/I742-win/L/anm_pin13_D117.0000.npz"
z8, m = load_o(path)
M, nodes, kf = int(m["M"]), list(m["nodes"]), int(m["kfreeze"])
D = mp.mpf(m["D_str"])
print(f"kernel {hpkernel.__file__}; state {path}, D {D}, kfreeze {kf}, plan {sum(len(s) - 1 for s in m['segs'])} steps", flush=True)
s = make_solver(D, M, nodes=nodes, kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=threads, kfreeze=kf, horizon_alpha=0)
s.set_segs(m["segs"])
h = band_field([], [], M, parts=2)
sp = PinnedSolver(s, M, h[0], h[1], h_rest=h[2:])
so = PinnedO(s, sp.ch, sp.cl, c8=sp.c8)
K = len(nodes)


def blocks(F):
    v = np.asarray(F[0]) + np.asarray(F[1])
    out = {}
    for b in range(K + 1):
        for f, nm in enumerate("pmac"):
            out[f"{b}{nm}"] = float(np.abs(v[4 * M * b + M * f:4 * M * b + M * (f + 1)]).max())
    return sorted(out.items(), key=lambda kv: -kv[1])[:5]


F = so.residual_o(z8)
print(f"  F(z) of the state itself: max {omax(F):.3e}; largest blocks {blocks(F)}", flush=True)
print(f"  pinned quad-double max|F| of its rounding (the switch's test value): {qmax(PinnedQ(s, sp.ch, sp.cl).residual_q(*q4_of_o(z8))):.3e}", flush=True)
rs = Reseeder(dict(M=M, nodes=nodes, kt=m["kt"], kc=m["kc"], ks=m["ks"]), D, threads=threads, horizon_alpha=0, qd=True, od=3)
el = ElimO(so, rs, switch=0.0)
t0 = time.time()
zp = el.project(z8)
dz = np.asarray(zp[0]) - np.asarray(z8[0]) + (np.asarray(zp[1]) - np.asarray(z8[1]))
print(f"  projection: {el.counts}, rung max|R| {' -> '.join(f'{r:.2e}' for r in rs.last_o)}, {time.time() - t0:.1f} s", flush=True)
print(f"  P(z) - z: max {float(np.abs(dz).max()):.3e} (m_h {float(np.abs(dz[2 * M + 4 * M * K:2 * M + 4 * M * K + M]).max()):.3e}, "
      f"a_h {float(np.abs(dz[2 * M + 4 * M * K + M:2 * M + 4 * M * K + 2 * M]).max()):.3e})", flush=True)
Fp = so.residual_o(zp)
print(f"  F(P(z)): max {omax(Fp):.3e}; largest blocks {blocks(Fp)}", flush=True)
print(json.dumps(dict(F=omax(F), Fp=omax(Fp), disp=float(np.abs(dz).max()), rung=list(rs.last_o))), flush=True)
