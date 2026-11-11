# the pinned residual along z + t dz, dz = -J^-1 (F + e) of freeze_round.py, by block
import os, sys
sys.path.insert(0, os.path.expanduser("~/Source/choptuik-i494/hp"))
import numpy as np
import mpmath as mp
from multidouble import od_axpy
from octo_corrector import load_o, o8
from hpkernel.driver import make_solver
from renode_o import pinned, blocks
import freeze_round as fr
raw, st = sys.argv[1], sys.argv[2]
mp.mp.dps = 160
z, m = load_o(os.path.join(raw, st))
M, nodes = int(m["M"]), list(m["nodes"]); K, kf = len(nodes), 3
s = make_solver(m["D_str"], M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2, kfreeze=kf)
s.set_segs(m["segs"])
P = pinned(s, z, M, kf)
L = len(z[0]); hp = list(range(4 * M * K, 4 * M * K + M))
# e from the kernel's rows and the exact projector (as freeze_round.py), on the horizon p rows only
u = make_solver(m["D_str"], M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2, kfreeze=None)
u.set_segs(m["segs"])
N = 2 * M; th = [2 * mp.pi * j / N for j in range(M)]
Pex = [[mp.fsum(4 * mp.cos(k * (th[i] - th[j])) / N for k in range(1, kf + 1, 2)) for j in range(M)] for i in range(M)]
Phx = [[(1 if i == j else 0) - Pex[i][j] for j in range(M)] for i in range(M)]
Fs, Fu = o8(s.residual_o(list(z))), o8(u.residual_o(list(z)))
d, p1, ker = fr.mpv(Fu, hp), fr.mpv(z, range(M)), fr.mpv(Fs, hp)
ex = [x + y for x, y in zip(fr.matvec(Pex, d), fr.matvec(Phx, p1))]
e = [mp.mpf(0)] * L
for i, r in enumerate(hp):
    e[r] = ex[i] - ker[i]
F8 = P.residual_o(z)
s.newton_o(list(z))
x = o8(od_axpy(1.0, *o8(s.olu_solve(list(fr.parts8(e)))), *o8(s.olu_solve(list(F8)))))
print("|x|", float(np.abs(x[0]).max()), "x_Delta", float(x[0][-1]), flush=True)
for t in (1e-32, 1e-30, 1e-28, 1e-26, 1e-24, 1e-22, 1e-20):
    zt = o8(od_axpy(-t, *x, *z))
    Ft = P.residual_o(zt)
    ddch = int(np.count_nonzero((np.asarray(zt[0]) != np.asarray(z[0])) | (np.asarray(zt[1]) != np.asarray(z[1]))))
    print(f"  t {t:.0e}: entries whose double-double part changed {ddch} of {L}", flush=True)
    b = blocks(Ft, M, K, kf)
    top = sorted(b.items(), key=lambda kv: -kv[1])[:3]
    print(f"t {t:.0e}: max|F| {fr_max(Ft) if False else float(np.abs(np.asarray(Ft[0]) + np.asarray(Ft[1])).max()):.3e}; " + "; ".join(f"{k} {v:.2e}" for k, v in top), flush=True)
