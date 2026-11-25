"""T1-like probe: one octo-double Newton step of the full system (kfreeze None) at a stored chain state."""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from hpkernel.driver import make_solver
from octo_corrector import load_o, omax, D_of, o8
from pinning import band_coeffs
from multidouble import od_axpy

p = sys.argv[1]
thr = int(sys.argv[2]) if len(sys.argv) > 2 else 2
z, meta = load_o(p)
M = meta["M"]; K = len(meta["nodes"])
D = D_of(meta)
sf = make_solver(D, M, nodes=meta["nodes"], kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr, kfreeze=(int(sys.argv[4]) if len(sys.argv) > 4 else None))
sf.set_segs(meta["segs"])
F0 = sf.residual_o(list(z)); print("F0", omax(F0), flush=True)
t = time.time()
d, Fh, Fl, pmin, pmax = sf.newton_o(list(z))
print(f"newton_o {time.time()-t:.1f}s  |F| {np.abs(np.asarray(Fh)+np.asarray(Fl)).max():.3e} pivots {pmin:.3e} .. {pmax:.3e}", flush=True)
d = o8(d)
dv = np.asarray(d[0]) + np.asarray(d[1])
print(f"|dz| {np.abs(dv).max():.3e}  dDelta {dv[-1]:.3e}", flush=True)
co = band_coeffs(dv[:M], np.zeros(M), M, list(range(1, 32, 2)))
print("dp1 harmonics:", " ".join(f"{k}:{abs(a)+abs(b):.1e}" for k, (a, b) in zip(range(1, 32, 2), co)), flush=True)
blk = lambda v, b: np.abs(v[2*M + 4*M*b: 2*M + 4*M*(b+1)]).max()
print("dz per node:", " ".join(f"{blk(dv, b):.1e}" for b in range(K)), " c0", f"{np.abs(dv[M:2*M]).max():.1e}",
      " mh", f"{np.abs(dv[2*M+4*M*K:3*M+4*M*K]).max():.1e}", " ah", f"{np.abs(dv[3*M+4*M*K:4*M+4*M*K]).max():.1e}", flush=True)
for lam in (1.0, 0.5, 0.25, 1e-3):
    zt = o8(od_axpy(lam, *d, *z))
    F = sf.residual_o(list(zt))
    Fv = np.asarray(F[0]) + np.asarray(F[1])
    print(f"lam {lam}: |F| {np.abs(Fv).max():.3e}  per block " + " ".join(f"{np.abs(Fv[b*4*M:(b+1)*4*M]).max():.1e}" for b in range(K+1)), flush=True)
np.savez(sys.argv[3] if len(sys.argv) > 3 else "probe2_step.npz", *d)
