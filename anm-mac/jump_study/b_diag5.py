"""k = 1 components: extrapolation error vs degree, cluster weighting and variable (1/n, 1/D)."""
import numpy as np
from b_lib import *
d = np.load('train36.npz'); Ds, Hc, TD, TH = d['Ds'], d['Hc'], d['TD'], d['TH']
sel = [i for i, l in enumerate(LABELS) if l[3] == 1 or l[0] == 'Delta']
names = [LABELS[i] for i in sel]
print('values at 68.5:', ' '.join(f'{LABELS[i][0]}.{LABELS[i][1]}.{LABELS[i][2]}1={TH[1][i]:+.3e}' for i in sel[:6]))
# weights: one unit of total weight per unit of D (cluster states share it)
w = np.ones(len(Ds))
for c in np.unique(np.floor(Ds)):
    m = np.floor(Ds) == c; w[m] = 1 / np.sqrt(m.sum())
for wname, ww in (('equal', None), ('per-unit-D', w)):
    for K in range(5, 13):
        f = Cheb(Ds, Hc[:, sel], K, w=ww)
        e = [np.abs(f(Dt)[0] - TH[j][sel]) for j, Dt in enumerate(TD) if Dt in (68.5, 69.5, 71.5, 73.0)]
        print(f'{wname:10s} deg {K:2d}: max k=1 error at 68.5, 69.5, 71.5, 73.0: ' + ' '.join(f'{x[:-1].max():.1e}' for x in e) + '  Delta ' + ' '.join(f'{x[-1]:.0e}' for x in e))
# which k=1 component and the residual of the fit
f = Cheb(Ds, Hc[:, sel], 8, w=w)
e = f(68.5)[0] - TH[1][sel]
for n, v in zip(names, e):
    if abs(v) > 3e-9: print('  ', n, f'{v:+.2e}')
