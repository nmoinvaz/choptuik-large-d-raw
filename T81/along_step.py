"""F(z + lam dz) along the quad-double Newton step at a state, against the linear model (1 - lam) F; and where dz is
large (blocks, fields, harmonics of p1)."""
import json, sys
import numpy as np
from hpkernel import qd_axpy
from hpkernel.driver import load_q, make_solver, qmax
zs, meta = load_q(sys.argv[1]); kf = int(sys.argv[2]) if len(sys.argv) > 2 else 13
D, M = meta["D"], meta["M"]
s = make_solver(D, M, nodes=list(meta["nodes"]), kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=6, kfreeze=kf)
s.set_segs(s.plan(zs[0], zs[1], 1e-32, 0.05))
d0, d1, d2, d3, fh, fl, pmin, pmax = s.newton_q(*zs)
F0 = fh + fl
print(f"D {D} kfreeze {kf}: |F| {np.abs(F0).max():.3e}, |dz| {np.abs(d0).max():.3e}, pivots {pmin:.2e}..{pmax:.2e}")
for lam in [1.0, 1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14]:
    z = qd_axpy(lam, d0, d1, d2, d3, *zs)
    F = s.residual_q(*z)
    Fv = F[0] + F[1]
    lin = (1 - lam) * F0
    print(f"lam {lam:.0e}: |F| {np.abs(Fv).max():.3e}, |F - (1 - lam) F0| {np.abs(Fv - lin).max():.3e}, ratio to lam^2 {np.abs(Fv - lin).max() / lam**2:.3e}")
L = len(d0); K = len(meta["nodes"])
names = ["p1", "c0"] + [f"node{i}.{f}" for i in range(K) for f in "pmac"] + ["m_h", "a_h"]
mags = [(names[i], float(np.abs(d0[i * M:(i + 1) * M]).max())) for i in range(len(names))]
print("largest |dz| by field:", sorted(mags, key=lambda t: -t[1])[:6], "Delta", float(d0[-1]))
# p1's harmonics: p1 odd on the half grid theta_j = pi j / M; sin((2k+1) theta) amplitudes by least squares
th = np.pi * np.arange(M) / M
ks = np.arange(1, 2 * M, 2)
A = np.sin(np.outer(th, ks[:M]))
c, *_ = np.linalg.lstsq(A, d0[:M], rcond=None)
print("dz p1 harmonics (k: |coef|):", [(int(k), f"{abs(v):.1e}") for k, v in zip(ks[:M], c) if abs(v) > 1e-3 * np.abs(c).max()][:12])
c0, *_ = np.linalg.lstsq(A, zs[0][:M], rcond=None)
print("state p1 harmonics:", [(int(k), f"{abs(v):.1e}") for k, v in zip(ks[:16], c0[:16])])
