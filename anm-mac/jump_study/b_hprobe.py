"""Which part of the guess error throws the residual: |F(truth + eps * e_X)| for the guess error e restricted to
each block X (centre, nodes, horizon data, Delta), at D 68.5, full system (kfreeze 13). Residuals only."""
import sys, json
import numpy as np
from hpkernel.driver import make_solver, load_q, qmax, qd_axpy
from b_lib import TRUTH, T, LABELS, M, FIELDS
Dt = float(sys.argv[1]); gp = sys.argv[2]
zt, m = load_q(TRUTH[Dt])
g = np.load(gp)['g']
e = g - (((np.asarray(zt[3]) + zt[2]) + zt[1]) + zt[0])
s = make_solver(float(m['D']), 32, nodes=list(m['nodes']), kt=36, kc=146, ks=130, threads=1, kfreeze=13)
s.set_segs(s.plan(np.asarray(zt[0]), np.asarray(zt[1]), 1e-32, 0.05))
L = len(e); z0 = np.zeros(L)
blocks = {'ctr': range(0, 64)}
for i, x in enumerate([0.3, 0.4, 0.5, 0.6, 0.7]):
    blocks[f'n{x}'] = range(64 + 128 * i, 64 + 128 * (i + 1))
blocks['hor'] = range(704, 768); blocks['Delta'] = [768]; blocks['all'] = range(769)
def Fnorm(dz):
    z = qd_axpy(1.0, np.ascontiguousarray(dz), z0, z0, z0, *zt)
    F = s.residual_q(*z); Fv = np.asarray(F[0]) + np.asarray(F[1])
    return np.abs(Fv).max(), np.abs(Fv[:640]).max(), np.abs(Fv[640:768]).max()
print(f'D {Dt}: |F(truth)| {Fnorm(z0)[0]:.1e}; guess error per block (max |e|):', ', '.join(f'{k} {np.abs(e[list(v)]).max():.1e}' for k, v in blocks.items()), flush=True)
for k, v in blocks.items():
    ek = np.zeros(L); ek[list(v)] = e[list(v)]
    row = []
    for eps in (1.0, 1e-1, 1e-2, 1e-3, 1e-4):
        a, b, c = Fnorm(eps * ek)
        row.append(f'{eps:.0e}: {a:.1e} (hor rows {c:.1e})')
    print(f'  {k:6s} ' + ' | '.join(row), flush=True)
