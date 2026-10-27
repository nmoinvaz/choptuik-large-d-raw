"""Full Newton steps in quad-double from a state, with the natural monotonicity quantity |dbar| = |J_k^-1 F(z_k+1)|
(the simplified Newton correction with the old LU) against |dz_k|."""
import sys, numpy as np
from hpkernel import qd_axpy
from hpkernel.driver import load_q, make_solver
zs, meta = load_q(sys.argv[1]); kf = int(sys.argv[2]); n = int(sys.argv[3])
D, M = meta["D"], meta["M"]
s = make_solver(D, M, nodes=list(meta["nodes"]), kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=6, kfreeze=kf)
s.set_segs(s.plan(zs[0], zs[1], 1e-32, 0.05))
z = zs
for it in range(n):
    d0, d1, d2, d3, fh, fl, pmin, pmax = s.newton_q(*z)
    zn = qd_axpy(1.0, d0, d1, d2, d3, *z)
    F = s.residual_q(*zn)
    b = s.qlu_solve(*F)
    dz, db = np.abs(d0).max(), np.abs(b[0]).max()
    dD = qd_axpy(-1.0, *zs, *zn)
    print(f"it {it}: |F| {np.abs(fh + fl).max():.3e} -> {np.abs(F[0]).max():.3e}, |dz| {dz:.3e}, |dbar| {db:.3e} (ratio {db / dz:.2e}), "
          f"Delta {zn[0][-1]:.17f} {zn[1][-1]:+.4e}, Delta - Delta0 {dD[0][-1] + dD[1][-1]:+.3e}", flush=True)
    z = zn
