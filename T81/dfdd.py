import sys, numpy as np
from hpkernel import qd_axpy
from hpkernel.driver import load_q, make_solver
zs, meta = load_q(sys.argv[1]); D, M = meta["D"], meta["M"]
mk = lambda Dx: make_solver(Dx, M, nodes=list(meta["nodes"]), kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=6, kfreeze=13)
s = mk(D); segs = s.plan(zs[0], zs[1], 1e-32, 0.05); s.set_segs(segs)
F0 = s.residual_q(*zs)
for h in (1e-6, 1e-8, 1e-10, 1e-12):
    out = []
    for Dx in (D + h, D - h):
        sx = mk(Dx); sx.set_segs(segs); out.append(sx.residual_q(*zs))
    d = qd_axpy(-1.0, *out[1], *out[0])
    print(f"h {h:.0e}: |F+| {np.abs(out[0][0]).max():.3e} |F-| {np.abs(out[1][0]).max():.3e} |F+ - F-| {np.abs(d[0]).max():.3e} "
          f"-> |dF/dD| {np.abs(d[0]).max() / (2 * h):.3e}; argmax row {int(np.abs(d[0]).argmax())} of {len(d[0])}")
