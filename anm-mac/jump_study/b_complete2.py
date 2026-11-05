"""The horizon completion with the Jacobian block (horizon rows x m_h, a_h columns) taken at a converged state
(the truth at D_J, a nearby D, or the guess itself) instead of at the guess, chord iterations on the guess at D
(Delta from the 1/D series). Saves the completed state. Usage: b_complete2.py D GUESS.npz D_J [rcond]"""
import sys, os, json, time
import numpy as np, mpmath as mp
from hpkernel.driver import make_solver, load_q, qmax, qd_axpy, qparts
from b_lib import TRUTH
Dt, gp, DJ = float(sys.argv[1]), sys.argv[2], float(sys.argv[3])
RC = float(sys.argv[4]) if len(sys.argv) > 4 else None
rows, cols = list(range(640, 768)), list(range(704, 768))
zt, m = load_q(TRUTH[Dt])
g = np.load(gp)['g'].copy()
mp.mp.dps = 80
v = mp.mpf(json.load(open('series.json'))['fits']['1/D 20'][str(Dt)])
parts = []
for _ in range(4):
    p = float(v); parts.append(p); v -= p
z = [g, np.zeros(769), np.zeros(769), np.zeros(769)]
for i in range(4): z[i][-1] = parts[i]
z = tuple(np.ascontiguousarray(a) for a in z)
z0 = np.zeros(769)
def mk(D, zz):
    s = make_solver(D, 32, nodes=[0.3, 0.4, 0.5, 0.6, 0.7], kt=36, kc=146, ks=130, threads=1, kfreeze=13)
    s.set_segs(s.plan(np.asarray(zz[0]), np.asarray(zz[1]), 1e-32, 0.05)); return s
s = mk(float(m['D']), z)
cache = f'Jh_truth_D{DJ:.4f}.npz'
t0 = time.time()
if os.path.exists(cache):
    J = np.load(cache)['J']
else:
    zJ, mJ = load_q(TRUTH[DJ])
    sJ = s if DJ == Dt else mk(float(mJ['D']), zJ)
    Jp = sJ.jacobian_q(*zJ, 0)
    J = (np.asarray(Jp[0]) + np.asarray(Jp[1]))[np.ix_(rows, list(range(704, 769)))]
    np.savez(cache, J=J)
J = J[:, :64]
Jg = np.load(gp.replace('.npz', '_Jh.npz'))['J'][:, :64] if os.path.exists(gp.replace('.npz', '_Jh.npz')) else None
sc = np.abs(J).max(0); Js = J / sc
print(f'D {Dt}: J block from the truth at D {DJ} ({time.time()-t0:.0f} s); scaled singular values {np.linalg.svd(Js, compute_uv=False)[[0, -1]]}'
      + (f'; |J_guess - J_truth| / |J_truth| {np.abs(Jg - J).max() / np.abs(J).max():.1e}' if Jg is not None and DJ == Dt else ''), flush=True)
def F(z):
    f = s.residual_q(*z); return np.asarray(f[0]) + np.asarray(f[1])
def ehor(z):
    d = qd_axpy(-1.0, *zt, *z); dv = np.asarray(d[0]) + np.asarray(d[1]); return np.abs(dv[704:768]).max(), np.abs(dv[:-1]).max()
f = F(z)
print(f'  start: |F| {np.abs(f).max():.2e} (horizon rows {np.abs(f[rows]).max():.2e}); horizon data - truth {ehor(z)[0]:.2e}', flush=True)
for k in range(10):
    du = np.linalg.lstsq(Js, -f[rows], rcond=RC)[0] / sc
    d = np.zeros(769); d[cols] = du
    zn = qd_axpy(1.0, d, z0, z0, z0, *z); fn = F(zn)
    print(f'  chord {k}: |du| {np.abs(du).max():.2e}, |F| {np.abs(fn).max():.2e} (horizon rows {np.abs(fn[rows]).max():.2e}, others {np.abs(fn[:640]).max():.2e}); horizon data - truth {ehor(zn)[0]:.2e}', flush=True)
    if np.linalg.norm(fn[rows]) >= 0.999 * np.linalg.norm(f[rows]):
        break
    z, f = zn, fn
out = gp.replace('.npz', f'_c2J{DJ:.1f}.npz')
np.savez(out, zh=z[0], zl=z[1], z2=z[2], z3=z[3]); print('  saved', out, flush=True)
