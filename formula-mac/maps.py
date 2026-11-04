# Which map helps, on D >= 10 (cleaned as dd_fits_mp.clean, in float64): polynomial (Chebyshev LS) in
#   1/D, 1/n; one cut at the negative-D singularity, w1 = (sqrt(1 - e/e_s) - 1)/(sqrt(1 - e/e_s) + 1), e = 1/n, e_s = 1/n_s;
#   one cut at D = 3 only, w3 = (1 - sqrt(1 - e))/(1 + sqrt(1 - e)); both cuts, zeta(n_s) (Joukowski).
# Fit on 10-45: held-out max on 45-60.1 and on 45-67.77, and the limit; fit on all: residual and limit.
import sys, numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
from jouk import zeta, DINF
D, y, s, run = load(); m = D >= 10; D, y = D[m], y[m]
def pfit(t, y, K, tf):
    a, b = t[tf].min(), t[tf].max(); V = Ch.chebvander((2 * t[tf] - a - b) / (b - a), K)
    c, *_ = np.linalg.lstsq(V, y[tf], rcond=None)
    return lambda tt: Ch.chebval((2 * np.asarray(tt) - a - b) / (b - a), c)
# cleaning as dd_fits_mp.clean: degree-18 fit in 1/D (here zeta(-13) deg 14, which reaches the same floor), drop points
# off the median of their four neighbours by > 1e-15
t0 = zeta(D, -13.0); ev = pfit(t0, y, 14, np.ones(len(D), bool)); r = ev(t0) - y
keep = np.ones(len(D), bool)
for i in range(len(D)):
    nb = np.sort(np.r_[r[max(0, i - 2):i], r[i + 1:i + 3]]); med = np.median(nb)
    if abs(r[i] - med) > 1e-15: keep[i] = False
print(f'clean drops {np.sum(~keep)} of {len(D)}')
D, y = D[keep], y[keep]
fitm = D <= 45; h60 = (D > 45) & (D <= 60.1); h68 = D > 45
w1 = lambda d, ns: (lambda q: (q - 1) / (q + 1))(np.sqrt(1 - ns / (d - 2)))     # 1 - e/e_s = 1 - n_s/n
w3 = lambda d: (lambda q: (1 - q) / (1 + q))(np.sqrt(1 - 1 / (d - 2)))
V = [('1/D', lambda d: 1 / d), ('1/n', lambda d: 1 / (d - 2)), ('w3 (D=3 cut)', w3)]
for ns in [float(v) for v in (sys.argv[1] if len(sys.argv) > 1 else '-9,-11,-13,-16,-25').split(',')]:
    V.append((f'w1 ns={ns:g}', (lambda ns: lambda d: w1(d, ns))(ns)))
    V.append((f'zeta ns={ns:g}', (lambda ns: lambda d: zeta(d, ns))(ns)))
Ks = [int(k) for k in (sys.argv[2] if len(sys.argv) > 2 else '10,12,14,16,18').split(',')]
print(f'{len(D)} points; per K: res(all) / lim(all)-Dinf / held 45-60.1 / held 45-67.77 / lim(fit<=45)-Dinf')
for nm, tf in V:
    t = tf(D); out = []
    for K in Ks:
        ea = pfit(t, y, K, np.ones(len(D), bool)); e4 = pfit(t, y, K, fitm)
        out.append(f'K{K}: {np.abs(ea(t) - y).max():.0e} {float(ea(0.0)) - DINF:+.0e} {np.abs(e4(t[h60]) - y[h60]).max():.0e} '
                   f'{np.abs(e4(t[h68]) - y[h68]).max():.0e} {float(e4(0.0)) - DINF:+.0e}')
    print(f'{nm:14s} ' + ' | '.join(out))
