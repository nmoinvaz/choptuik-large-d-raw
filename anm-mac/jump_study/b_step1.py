"""One quad-double Newton step (Solver.newton_q, full system) from truth + eps * e_X: the step |dz| and the distance
of z + dz from the truth (the linear model leaves ~0; the quadratic term along the weak directions leaves more).
Usage: b_step1.py D GUESS.npz block:eps [block:eps ...]"""
import sys, time
import numpy as np
from hpkernel.driver import make_solver, load_q, qmax, qd_axpy
from b_lib import TRUTH, T, LABELS
Dt = float(sys.argv[1]); gp = sys.argv[2]
zt, m = load_q(TRUTH[Dt])
ztf = ((np.asarray(zt[3]) + zt[2]) + zt[1]) + zt[0]
e = np.load(gp)['g'] - ztf
s = make_solver(float(m['D']), 32, nodes=list(m['nodes']), kt=36, kc=146, ks=130, threads=1, kfreeze=13)
s.set_segs(s.plan(np.asarray(zt[0]), np.asarray(zt[1]), 1e-32, 0.05))
L = len(e); z0 = np.zeros(L)
blocks = {'ctr': range(0, 64), 'nodes': range(64, 704), 'n0.7': range(576, 704), 'hor': range(704, 768), 'Delta': [768], 'all': range(769), 'interior': range(704)}
for a in sys.argv[3:]:
    k, eps = a.split(':'); eps = float(eps)
    ek = np.zeros(L); ek[list(blocks[k])] = e[list(blocks[k])]
    z = qd_axpy(eps, np.ascontiguousarray(ek), z0, z0, z0, *zt)
    t0 = time.time()
    d0, d1, d2, d3, fh, fl, pmin, pmax = s.newton_q(*z)
    zn = qd_axpy(1.0, *(np.ascontiguousarray(np.asarray(p)) for p in (d0, d1, d2, d3)), *z)
    dist = qd_axpy(-1.0, *zt, *zn); dv = np.asarray(dist[0]) + np.asarray(dist[1])
    h = T @ dv; i = np.argmax(np.abs(h))
    print(f'{k}:{eps:.0e}: |e| {eps*np.abs(ek).max():.1e}, |F| {qmax((fh, fl)):.1e}, step |dz| {np.abs(np.asarray(d0)).max():.2e}, after the step |z - truth| {np.abs(dv[:-1]).max():.2e} '
          f'(worst {LABELS[i]} {h[i]:+.1e}), dDelta {dv[-1]:+.1e}, piv {pmin:.1e}, {time.time()-t0:.0f} s', flush=True)
