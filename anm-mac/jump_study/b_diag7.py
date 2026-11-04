"""SVD of the training fit residual: is the non-smooth part confined to a few directions?"""
import numpy as np
from b_lib import *
d = np.load('train36.npz'); Ds, Hc, TD, TH = d['Ds'], d['Hc'], d['TD'], d['TH']
Z = Hc @ Tinv.T     # z-space
for K in (10, 12, 14):
    f = Cheb(Ds, Z, K); Rz = Z - f(Ds)
    U, S, Vt = np.linalg.svd(Rz, full_matrices=False)
    print(f'deg {K}: residual max {np.abs(Rz).max():.1e}; singular values', ' '.join(f'{s:.1e}' for s in S[:16]))
K = 12
f = Cheb(Ds, Z, K); Rz = Z - f(Ds)
U, S, Vt = np.linalg.svd(Rz, full_matrices=False)
for j in range(6):
    h = T @ Vt[j]; o = np.argsort(-np.abs(h))[:6]
    print(f'  dir {j} (s {S[j]:.1e}): Delta comp {Vt[j][-1]:+.1e}; top harmonics', ', '.join(f'{LABELS[i][0]}.{LABELS[i][1]}.{LABELS[i][2]}{LABELS[i][3]} {h[i]:+.2f}' for i in o))
np.save('resid_dirs.npy', Vt[:20])
