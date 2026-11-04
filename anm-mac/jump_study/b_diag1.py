"""Task 1: which harmonic components carry the fit residual. Chebyshev in 1/n, harmonic coordinates."""
import numpy as np, sys
from b_lib import *
tr = train_files()
Ds = np.array([d for d, _ in tr])
Z = np.array([zf(load(p)[1]) for _, p in tr])
Hc = Z @ T.T
print(len(Ds), 'training states, D', Ds.min(), '..', Ds.max(), '; distinct D>=1 apart:', len(np.unique(np.round(Ds))))
truth = {D: zf(load(p)[1]) for D, p in TRUTH.items()}
# raw-monomial fit as in state_extrap.py, for comparison with the conditioned Chebyshev fit
X = 1 / (Ds - 2)
for K in (6, 8, 10, 12):
    V = np.vander(X, K + 1, increasing=True)
    C, *_ = np.linalg.lstsq(V, Z, rcond=None)
    Vc = np.polynomial.chebyshev.chebvander(2 * (X - X.min()) / (X.max() - X.min()) - 1, K)
    Cc, *_ = np.linalg.lstsq(Vc, Z, rcond=None)
    print(f'deg {K}: monomial residual {np.abs(V @ C - Z).max():.2e} (rank {np.linalg.matrix_rank(V)}), chebyshev residual {np.abs(Vc @ Cc - Z).max():.2e}')
for K in (6, 8, 10, 12):
    f = Cheb(Ds, Hc, K)
    res = Hc - f(Ds)
    rmax = np.abs(res).max(0)
    errs = []
    for Dt in (67.742203, 68.5, 69.5):
        e = np.abs(Tinv @ f(Dt)[0] - truth[Dt]); errs.append(f'{Dt}: {e[:-1].max():.1e}/{e[-1]:.1e}')
    print(f'cheb deg {K}: max residual {rmax.max():.2e}; error z/Delta at ' + ', '.join(errs))
K = 10
f = Cheb(Ds, Hc, K); res = Hc - f(Ds); rmax = np.abs(res).max(0); rrms = np.sqrt((res ** 2).mean(0))
mag = np.abs(Hc[-1])
order = np.argsort(-rmax)
print('\ntop 40 components by max fit residual (deg 10): label, max res, rms res, |value| at D', Ds[-1])
for i in order[:40]:
    print(f'  {i:4d} {LABELS[i]}  {rmax[i]:.2e} {rrms[i]:.2e}  {mag[i]:.2e}')
# summary per field and harmonic (max over cos/sin)
print('\nmax residual per field (columns k) for k with any residual > 1e-11:')
import collections
tab = collections.defaultdict(dict)
for i, (blk, name, cs, k) in enumerate(LABELS):
    tab[(blk, name)][k] = max(tab[(blk, name)].get(k, 0), rmax[i])
ks = sorted({k for v in tab.values() for k in v})
for key, v in tab.items():
    row = ' '.join(f'{k}:{v[k]:.0e}' for k in ks if k in v and v[k] > 1e-11)
    print(f'  {key[0]:>5} {key[1]:>5}  max {max(v.values()):.1e}   {row}')
# how many components exceed thresholds
for thr in (1e-8, 1e-9, 1e-10, 1e-11, 1e-12):
    print(f'components with max residual > {thr:.0e}: {(rmax > thr).sum()}')
# residual time pattern of the worst component
i0 = order[0]
print('\nworst component', LABELS[i0], 'residual vs D:')
for D, r in zip(Ds, res[:, i0]):
    print(f'  {D:.4f} {r:+.3e}')
np.savez('diag1.npz', Ds=Ds, Hc=Hc, rmax=rmax, res=res)
