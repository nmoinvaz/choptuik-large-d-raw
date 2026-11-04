"""Task 4: the split extrapolation to D 85.75, 100, 200 over a set of fit choices; the spread is the uncertainty
(a spread over fit choices, not a bound). Compared with the 1/D series of Delta (hp/dd_fits_mp, as full_release.py
uses it) and with the pinned chain state at 85.7473 in the well-determined components."""
import sys, json, glob, itertools
import numpy as np, mpmath as mp
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/hp')
from b_lib import *
from b_split import Split, unit_weights, noise_dirs
d = np.load('train36.npz'); Ds, Hc = d['Ds'], d['Hc']
Zdd = Hc @ Tinv.T
qd = {D: zf(load(p)[1]) for D, p in TRUTH.items() if D >= 68}
q = np.load('g_zero67_newton_state.npz'); qd[67.742203] = zf([q['zh'], q['zl'], q['z2'], q['z3']])
Dq = np.array(sorted(qd)); Zq = np.array([qd[D] for D in Dq])
chain_p = R + 'anm-mac/run_trend_pin3_qd9/anm_pin3_D85.7473.npz'
Dc, pc, mc = load(chain_p); zc = zf(pc)
Dc = float(mc.get('D_str', Dc))
print('chain state', chain_p.split('/')[-1], 'D', Dc, 'kfreeze', mc.get('kfreeze'), {k: mc[k] for k in mc if k in ('pin', 'trend', 'F')})
targets = [Dc, 100.0, 200.0]
# well-determined components: odd fields' harmonics k <= 3, even fields' k <= 4, m_h, a_h, Delta (not p1 k >= 5, which the chain holds)
strong = np.array([(l[1] in ('m_h', 'a_h', 'Delta')) or (l[3] <= 3 and l[1] in ('p', 'm', 'p1')) or (l[3] <= 4 and l[1] in ('a', 'c', 'c0'))
                   for l in LABELS])
choices = []
for data, r, Ks, Kc, wt in itertools.product(('dd', 'dd+qd'), (4, 6), (10, 12, 14, 16), (-1, 0, 1), ('unit', 'equal')):
    if data == 'dd':
        DD, ZZ = Ds, Zdd
    else:
        DD, ZZ = np.concatenate([Ds, Dq]), np.vstack([Zdd, Zq])
    w = unit_weights(DD) if wt == 'unit' else None
    V = noise_dirs(Ds, Zdd, r, 12, unit_weights(Ds))[0]
    sp = Split(DD, ZZ, r, Ks, Kc, w=w, V=V)
    if Kc == -1 and data == 'dd+qd':
        # hold: the junk coordinates of the newest qd state
        sp.c_hold = Zq[-1] @ V
    g = [sp(D)[0] for D in targets]
    choices.append(dict(data=data, r=r, Ks=Ks, Kc=Kc, wt=wt, g=g, V=V))
print(len(choices), 'fit choices')
HOR = slice(704, 768); N07 = slice(576, 704)
# calibration: the dd-only selected fit's error per block at the qd truths, against the distance from D 61.03
spc = Split(Ds, Zdd, 4, 12, -1, w=unit_weights(Ds))
print('calibration (dd-only fit r 4, Ks 12, hold): D, ahead of 61.03, error in node 0.7, horizon data m_h a_h, Delta')
for D, zt in zip(Dq, Zq):
    e = spc(D)[0] - zt
    print(f'   {D:.3f} {D - Ds.max():5.2f}  {np.abs(e[N07]).max():.1e} {np.abs(e[HOR]).max():.1e} {abs(e[-1]):.1e}')
# Delta series reference
import dd_fits_mp as F
mp.mp.dps = 60
pts, _ = F.load_points()
DsS = F.clean(pts, sorted(x for x in pts if 10 <= x <= 67.77), verbose=False)
ser = {}
for var, deg in (('1/D', 20), ('1/D', 18), ('1/n', 20)):
    ev, _, _ = F.fit(pts, DsS, var, deg)
    ser[(var, deg)] = [float(ev(mp.mpf(D))) for D in targets]
for j, D in enumerate(targets):
    G = np.array([c['g'][j] for c in choices])
    med = np.median(G, 0)
    spread = G.max(0) - G.min(0)
    Hs = (G - med) @ T.T
    sp_strong = np.abs(Hs[:, strong]).max(); sp_junk = np.abs(Hs[:, ~strong]).max()
    # best guess: dd+qd, r 4, Ks 12, junk held at the newest qd state, unit weights
    best = [c for c in choices if (c['data'], c['r'], c['Ks'], c['Kc'], c['wt']) == ('dd+qd', 4, 12, -1, 'unit')][0]['g'][j]
    print(f'\nD {D}: spread over {len(G)} choices: max|z| {spread[:-1].max():.2e}; harmonic coords: well-determined {sp_strong:.2e}, rest {sp_junk:.2e}; node 0.7 {spread[N07].max():.2e}, horizon data {spread[HOR].max():.2e}; Delta spread {spread[-1]:.2e}')
    for dset in ('dd', 'dd+qd'):
        Gs = np.array([c['g'][j] for c in choices if c['data'] == dset])
        print(f'   {dset:6s}: max|z| spread {np.ptp(Gs, 0)[:-1].max():.2e}, Delta median {np.median(Gs[:, -1]):.15f} spread {np.ptp(Gs[:, -1]):.1e}')
    print('   Delta series: ' + ', '.join(f'{k[0]} {k[1]}: {v[j]:.15f}' for k, v in ser.items()) + f'; best-guess Delta - series(1/D 20) {best[-1] - ser[("1/D", 20)][j]:+.2e}')
    if j == 0:
        e = (best - zc) @ T.T
        print(f'   best guess - chain state (pinned): well-determined max {np.abs(e[strong][:-1]).max():.2e} (worst {LABELS[np.where(strong)[0][np.argmax(np.abs(e[strong][:-1]))]]}), Delta {e[-1]:+.2e}; held p1 k>=5 max {np.abs(e[~strong]).max():.2e}')
        print(f'   chain Delta - series(1/D 20) {zc[-1] - ser[("1/D", 20)][0]:+.2e}')
    np.save(f'far_best_D{D:.4f}.npy', best)
json.dump(dict(targets=targets), open('far.json', 'w'))
