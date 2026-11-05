"""Task 1c: guess error per component at the truth states (training D 36-61, kfreeze-13 states only)."""
import numpy as np, collections
from b_lib import *
tr = train_files(dmin=36.0)
Ds = np.array([d for d, _ in tr]); Hc = np.array([T @ zf(load(p)[1]) for _, p in tr])
TH = {D: T @ zf(load(p)[1]) for D, p in TRUTH.items()}
np.savez('train36.npz', Ds=Ds, Hc=Hc, TD=np.array(list(TH)), TH=np.array(list(TH.values())))
print(len(Ds), 'states', Ds.min(), Ds.max())
for K in (4, 5, 6, 7, 8, 9, 10, 12):
    f = Cheb(Ds, Hc, K)
    out = []
    for Dt in TH:
        e = np.abs(Tinv @ (f(Dt)[0] - TH[Dt])); out.append(f'{Dt:.2f}: {e[:-1].max():.1e}/{e[-1]:.0e}')
    print(f'deg {K:2d} res {np.abs(Hc - f(Ds)).max():.1e} | ' + ' '.join(out))
K = 8
f = Cheb(Ds, Hc, K)
for Dt in (67.742203, 68.5, 69.5):
    e = f(Dt)[0] - TH[Dt]
    tab = collections.defaultdict(dict)
    for i, (blk, name, cs, k) in enumerate(LABELS):
        tab[(blk, name)][k] = max(tab[(blk, name)].get(k, 0), abs(e[i]))
    print(f'\nD {Dt}, deg {K}: harmonic-space error per field (k: err) for err > 1e-10; z-space max {np.abs(Tinv @ e)[:-1].max():.2e}')
    for key, v in tab.items():
        row = ' '.join(f'{k}:{v[k]:.0e}' for k in sorted(v) if v[k] > 1e-10)
        print(f'  {key[0]:>5} {key[1]:>5} max {max(v.values()):.1e}  {row}')
