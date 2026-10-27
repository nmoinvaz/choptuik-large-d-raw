"""The quad-double tangent dz/dD at a converged state: its size by field, p1's harmonics, dDelta/dD, and the
residual of the predicted state at D + dD."""
import sys, numpy as np
from hpkernel import qd_axpy
from hpkernel.driver import load_q, make_solver, tangent_q
zs, meta = load_q(sys.argv[1]); D, M = meta["D"], meta["M"]
mk = lambda Dx: make_solver(Dx, M, nodes=list(meta["nodes"]), kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=6, kfreeze=13)
s = mk(D); s.set_segs(s.plan(zs[0], zs[1], 1e-32, 0.05))
F = s.residual_q(*zs); print(f"D {D}: |F| {np.abs(F[0]).max():.2e}")
for h in (1e-8, 1e-10, 1e-12):
    t = tangent_q(s, mk, D, zs, h=h)
    print(f"h {h:.0e}: |t| {np.abs(t[0]).max():.3e}, dDelta/dD {t[0][-1]:.6e}, |t p1| {np.abs(t[0][:M]).max():.3e}, |t rest| {np.abs(t[0][M:-1]).max():.3e}")
th = np.pi * np.arange(M) / M; ks = np.arange(1, 2 * M, 2); A = np.sin(np.outer(th, ks[:M]))
c, *_ = np.linalg.lstsq(A, t[0][:M], rcond=None)
print("tangent p1 harmonics:", [(int(k), f"{v:.2e}") for k, v in zip(ks[:16], c[:16])])
for dD in (1e-6, 1e-5, 1e-4, 1e-3):
    zp = qd_axpy(dD, *t, *zs); sp = mk(D + dD); sp.set_segs(s.get_segs())
    try:
        Fp = sp.residual_q(*zp); print(f"dD {dD:.0e}: predicted |F| {np.abs(Fp[0]).max():.3e}")
    except ValueError as e:
        print(f"dD {dD:.0e}: {e}")
