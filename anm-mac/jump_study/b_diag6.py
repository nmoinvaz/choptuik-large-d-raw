"""Junk harmonics: smoothness of the qd truths 68.5-73 and of the dd training data; truth fit vs training."""
import numpy as np
from b_lib import *
d = np.load('train36.npz'); Ds, Hc, TD, TH = d['Ds'], d['Hc'], d['TD'], d['TH']
idx = {l: i for i, l in enumerate(LABELS)}
q = TD >= 68.4   # the qd-converged truths
comps = [('ctr','p1',cs,k) for k in (5, 7, 9, 11, 13) for cs in 'cs'] + [('ctr','c0','s',12), ('n0.3','p','s',13), ('n0.3','m','c',11), ('ctr','p1','c',1)]
for c in comps:
    i = idx[c]
    y = TH[q, i]; x = 1 / (TD[q] - 2)
    out = []
    for deg in (1, 2, 3, 4):
        V = np.vander(x - x.mean(), deg + 1); C, *_ = np.linalg.lstsq(V, y, rcond=None)
        r = np.abs(V @ C - y).max()
        # back-extrapolate to the dd data at D 59-61 and 67.74
        xb = 1 / (Ds - 2); g = np.vander(xb - x.mean(), deg + 1) @ C
        m = Ds > 59.5
        xt = 1 / (67.742203 - 2); g67 = np.vander(np.array([xt - x.mean()]), deg + 1) @ C
        out.append(f'd{deg}: res {r:.0e} dd-fit@60 {np.abs(Hc[m, i] - g[m]).max():.1e} full1@67.7 {abs(TH[0, i]-g67[0]):.1e}')
    print(f'{str(c):28s} |v| {abs(y[0]):.2e}  ' + ' | '.join(out))
