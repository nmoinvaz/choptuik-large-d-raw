"""newton_qd (full system) from truth + eps * e_X, e = guess - truth restricted to block X (as b_step1.py).
Usage: b_newton2.py D GUESS.npz block:eps [it_max]"""
import sys, time
import numpy as np
from hpkernel.driver import make_solver, newton_qd, load_q, qmax, qd_axpy
from b_lib import TRUTH, T, LABELS
Dt = float(sys.argv[1]); gp = sys.argv[2]; k, eps = sys.argv[3].split(':'); eps = float(eps)
it_max = int(sys.argv[4]) if len(sys.argv) > 4 else 6
zt, m = load_q(TRUTH[Dt])
e = np.load(gp)['g'] - (((np.asarray(zt[3]) + zt[2]) + zt[1]) + zt[0])
blocks = {'ctr': range(0, 64), 'nodes': range(64, 704), 'n0.7': range(576, 704), 'hor': range(704, 768), 'Delta': [768], 'all': range(769), 'interior': range(704)}
ek = np.zeros(769); ek[list(blocks[k])] = e[list(blocks[k])]
z0 = np.zeros(769)
s = make_solver(float(m['D']), 32, nodes=list(m['nodes']), kt=36, kc=146, ks=130, threads=1, kfreeze=13)
s.set_segs(s.plan(np.asarray(zt[0]), np.asarray(zt[1]), 1e-32, 0.05))
z = qd_axpy(eps, np.ascontiguousarray(ek), z0, z0, z0, *zt)
t0 = time.time()
print(f'D {Dt}: start = truth + {eps:.1e} x guess error in {k} (|e| {eps*np.abs(ek).max():.1e})', flush=True)
zn, hist, conv = newton_qd(s, z, tol=1e-40, it_max=it_max, max_halvings=3, verbose=True)
d = qd_axpy(-1.0, *zt, *zn); dv = np.asarray(d[0]) + np.asarray(d[1])
print(f'  {"converged" if conv else "NOT converged"} in {len(hist)} records, {time.time()-t0:.0f} s; end - truth max {np.abs(dv[:-1]).max():.1e}, Delta {dv[-1]:+.1e}', flush=True)
