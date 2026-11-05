"""The horizon completion: hold the extrapolated centre and node states, solve the horizon data (m_h, a_h) and
Delta by Gauss-Newton least squares on the horizon block's rows (640-767), the quad-double Jacobian's columns
704-768 computed once at the guess (chord iterations), then the full-system quad-double Newton (newton_qd) from the
completed guess. Usage: b_complete.py D GUESS.npz [--withDelta] [--Delta_series] [--it N] [--no_newton]
Default: complete m_h, a_h only. --withDelta: Delta as a column too (truncated SVD, rcond 1e-6).
--Delta_series: first set Delta to the 1/D degree-20 series value (series.json, b_series.py).
The Jacobian block is cached in GUESS_Jh.npz."""
import sys, time, json
import numpy as np
from hpkernel.driver import make_solver, newton_qd, load_q, qmax, qd_axpy, qparts
from b_lib import TRUTH, T, LABELS
args = [a for a in sys.argv[1:] if not a.startswith('--')]
Dt = float(args[0]); gp = args[1]
it_max = int(sys.argv[sys.argv.index('--it') + 1]) if '--it' in sys.argv else 8
cols = list(range(704, 769 if '--withDelta' in sys.argv else 768)); rows = list(range(640, 768))
RC = float(sys.argv[sys.argv.index('--rcond') + 1]) if '--rcond' in sys.argv else (1e-6 if '--withDelta' in sys.argv else None)
have_truth = Dt in TRUTH
if have_truth:
    zt, m = load_q(TRUTH[Dt]); Dv = m['D_str'] if 'D_str' in m else float(m['D'])
else:
    Dv = Dt
G = np.load(gp)
z = qparts(G['g'], np.zeros(769)) if 'g' in G else (G['zh'], G['zl'], G['z2'], G['z3'])
z0 = np.zeros(769)
if '--Delta_series' in sys.argv:
    import mpmath as mp
    mp.mp.dps = 80
    v = mp.mpf(json.load(open('series.json'))['fits']['1/D 20'][str(Dt)])
    parts = []
    for _ in range(4):
        p = float(v); parts.append(p); v -= p
    z = tuple(np.array(np.asarray(z[i]), dtype=float) for i in range(4))
    for i in range(4):
        z[i][-1] = parts[i]
    z = tuple(np.ascontiguousarray(a) for a in z)
s = make_solver(Dv, 32, nodes=[0.3, 0.4, 0.5, 0.6, 0.7], kt=36, kc=146, ks=130, threads=1, kfreeze=13)
s.set_segs(s.plan(np.asarray(z[0]), np.asarray(z[1]), 1e-32, 0.05))
def dist(z):
    if not have_truth:
        return float('nan'), float('nan'), float('nan')
    d = qd_axpy(-1.0, *zt, *z); dv = np.asarray(d[0]) + np.asarray(d[1])
    return np.abs(dv[:-1]).max(), np.abs(dv[704:768]).max(), dv[-1]
def F(z):
    f = s.residual_q(*z); return np.asarray(f[0]) + np.asarray(f[1])
t0 = time.time()
f = F(z); e = dist(z)
print(f'D {Dt} {gp}: |F| {np.abs(f).max():.2e} (horizon rows {np.abs(f[rows]).max():.2e}, other {np.abs(f[:640]).max():.2e}); '
      f'guess - truth: max {e[0]:.2e}, horizon data {e[1]:.2e}, Delta {e[2]:+.2e}', flush=True)
import os
cache = gp.replace('.npz', '_Jh.npz')
if os.path.exists(cache):
    J = np.load(cache)['J'][:, :len(cols)]
else:
    Jp = s.jacobian_q(*z, 0)
    J = (np.asarray(Jp[0]) + np.asarray(Jp[1]))[np.ix_(rows, list(range(704, 769)))]
    np.savez(cache, J=J); J = J[:, :len(cols)]
sc = np.abs(J).max(0); Js = J / sc
sv = np.linalg.svd(Js, compute_uv=False)
print(f'  Jacobian (horizon rows x completed columns) {J.shape}, {time.time()-t0:.0f} s; scaled singular values {sv.max():.1e}..{sv.min():.1e}', flush=True)
for k in range(8):
    du = np.linalg.lstsq(Js, -f[rows], rcond=RC)[0] / sc
    dfull = np.zeros(769); dfull[cols] = du
    zn = qd_axpy(1.0, dfull, z0, z0, z0, *z)
    fn = F(zn); e = dist(zn)
    print(f'  chord {k}: |du| {np.abs(du).max():.2e} (dDelta {du[-1] if len(cols) == 65 else 0:+.2e}); |F| {np.abs(fn).max():.2e} (horizon rows {np.abs(fn[rows]).max():.2e}, '
          f'|F_hor|_2 {np.linalg.norm(fn[rows]):.2e}); - truth: horizon data {e[1]:.2e}, Delta {e[2]:+.2e}', flush=True)
    if np.linalg.norm(fn[rows]) >= np.linalg.norm(f[rows]) * 0.999:
        if k == 0:
            print('  the completion made no progress; no Newton', flush=True); sys.exit(1)
        break
    z, f = zn, fn
tag = gp.replace('.npz', f'_compl_rc{RC}' + ('_wD' if '--withDelta' in sys.argv else '') + ('_sD' if '--Delta_series' in sys.argv else ''))
np.savez(tag + '.npz', zh=z[0], zl=z[1], z2=z[2], z3=z[3])
if '--no_newton' in sys.argv:
    sys.exit(0)
zc = z
zf_, hist, conv = newton_qd(s, zc, tol=1e-40, it_max=it_max, max_halvings=3, verbose=True)
e = dist(zf_)
print(f'  newton_qd {"converged" if conv else "NOT converged"} in {len(hist)} records, {time.time()-t0:.0f} s; first step |dz| {hist[0]["dz"]:.2e}; end - truth: max {e[0]:.2e}, Delta {e[2]:+.2e}', flush=True)
np.savez(tag + '_newton_state.npz', zh=zf_[0], zl=zf_[1], z2=zf_[2], z3=zf_[3], meta=json.dumps(dict(D=Dv, conv=conv)))
json.dump(dict(D=Dt, conv=conv, hist=hist), open(tag + '_newton.json', 'w'), default=float)
