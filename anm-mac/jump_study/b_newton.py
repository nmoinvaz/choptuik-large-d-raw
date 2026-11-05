"""Quad-double Newton (full system, kfreeze 13) at a truth D from a guess; reports the first step and the distance
to the truth state. Usage: b_newton.py D GUESS.npz [it_max] [max_halvings]
GUESS.npz holds 'g' (float64 z) or 'dz' (float64 offset added to the truth in quad-double)."""
import sys, time, json
pass
import numpy as np
from hpkernel.driver import make_solver, newton_qd, load_q, qmax, qd_axpy, qparts
from b_lib import TRUTH, T, LABELS
Dt = float(sys.argv[1]); gp = sys.argv[2]
it_max = int(sys.argv[3]) if len(sys.argv) > 3 else 8
mh = int(sys.argv[4]) if len(sys.argv) > 4 else 3
zt, m = load_q(TRUTH[Dt])
g = np.load(gp)
if 'dz' in g:
    z0 = qd_axpy(1.0, np.ascontiguousarray(g['dz']), np.zeros(len(g['dz'])), np.zeros(len(g['dz'])), np.zeros(len(g['dz'])), *zt)
else:
    z0 = qparts(g['g'], np.zeros(len(g['g'])))
D = m['D_str'] if 'D_str' in m else float(m['D'])   # the scans' D is the binary float
s = make_solver(D, int(m['M']), nodes=list(m['nodes']), kt=m.get('kt', 36), kc=m.get('kc', 146), ks=m.get('ks', 130), threads=1, kfreeze=13)
t0 = time.time()
s.set_segs(s.plan(np.asarray(z0[0]), np.asarray(z0[1]), 1e-32, 0.05))
def dist(z):
    d = qd_axpy(-1.0, *zt, *z); dd = np.asarray(d[0]) + np.asarray(d[1])
    h = T @ dd; i = np.argmax(np.abs(h[:-1]))
    return np.abs(dd[:-1]).max(), dd[-1], LABELS[i], h[i]
Ft = s.residual_q(*zt); F0 = s.residual_q(*z0)
e0 = dist(z0)
print(f'D {Dt} guess {gp}: |F(truth)| {qmax(Ft):.2e} (control, guess plan), |F(guess)| {qmax(F0):.2e}; guess - truth: max|dz| {e0[0]:.2e}, dDelta {e0[1]:+.2e}, worst {e0[2]} {e0[3]:+.2e}', flush=True)
z, hist, conv = newton_qd(s, z0, tol=1e-40, it_max=it_max, max_halvings=mh, verbose=True)
e1 = dist(z)
print(f'  {"converged" if conv else "NOT converged"} in {len(hist)} records, {time.time()-t0:.0f} s; first step |dz| {hist[0]["dz"]:.2e}; end - truth: max|dz| {e1[0]:.2e}, dDelta {e1[1]:+.2e}, worst {e1[2]} {e1[3]:+.2e}', flush=True)
out = gp.replace('.npz', f'_newton.json')
json.dump(dict(D=Dt, guess=gp, conv=conv, hist=hist, F_guess=qmax(F0), err_guess=e0[0], dDelta_guess=e0[1], err_end=e1[0], dDelta_end=e1[1]), open(out, 'w'), default=float)
np.savez(gp.replace('.npz', '_newton_state.npz'), zh=z[0], zl=z[1], z2=z[2], z3=z[3], meta=json.dumps(dict(m, conv=conv, from_guess=gp)))
