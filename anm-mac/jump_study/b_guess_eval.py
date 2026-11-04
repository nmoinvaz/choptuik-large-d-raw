"""Task 2: the split extrapolation from the double-double states (D 36-61) to the qd truths 67.74, 68.5, 69.5 (and
70.5-73 for reference). Degree choice by a holdout written before looking at the truths: fit on D <= 55.1, judge
the clean part (P z, P = 1 - V V^T) at the states D > 59.5."""
import sys, numpy as np, json
from b_lib import *
from b_split import Split, unit_weights, noise_dirs
d = np.load('train36.npz'); Ds, Hc = d['Ds'], d['Hc']
Z = Hc @ Tinv.T
w = unit_weights(Ds)
truth = {D: zf(load(p)[1]) for D, p in TRUTH.items() if D >= 68}
try:
    q = np.load('g_zero67_newton_state.npz'); mq = json.loads(str(q['meta']))
    if mq.get('conv'):
        truth[67.742203] = zf([q['zh'], q['zl'], q['z2'], q['z3']])
except FileNotFoundError:
    pass
targets = sorted(truth)
def errs(g, zt, V):
    e = g - zt
    P = e - V @ (V.T @ e) if V.shape[1] else e
    return np.abs(e[:-1]).max(), np.abs(P[:-1]).max(), abs(e[-1])
hold = Ds <= 55.1; val = Ds > 59.5
rows = []
for r in (0, 2, 4, 6):
    V = noise_dirs(Ds, Z, r, 12, w)[0] if r else np.zeros((769, 0))
    for Ks in range(8, 17):
        for Kc in (-2, -1, 0, 1, 2, 3):
            if r == 0 and Kc != -1: continue
            sp_h = Split(Ds[hold], Z[hold], r, Ks, Kc if Kc >= 0 else 0, w=w[hold], V=V)   # holdout: c by deg Kc
            vz = np.array([sp_h(D)[1] for D in Ds[val]])            # clean part only
            Pv = Z[val] - (Z[val] @ V) @ V.T
            vclean = np.abs((vz - Pv)[:, :-1]).max()
            sp = Split(Ds, Z, r, Ks, Kc, w=w, V=V)
            out = [errs(sp(D)[0], truth[D], V) for D in targets]
            rows.append(dict(r=r, Ks=Ks, Kc=Kc, val=vclean, res_w=sp.res_w, out=out))
print('targets', targets)
print(' r  Ks  Kc  holdout-clean  train-res(w) | per target: total / clean / |dDelta|')
for x in rows:
    print(f"{x['r']:2d} {x['Ks']:3d} {x['Kc']:3d}  {x['val']:.1e}  {x['res_w']:.1e} | " + ' '.join(f'{a:.1e}/{b:.1e}/{c:.0e}' for a, b, c in x['out']))
json.dump(dict(targets=targets, rows=rows), open('guess_eval.json', 'w'))
