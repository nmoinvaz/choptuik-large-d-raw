# notes/QUAD_DOUBLE.md 13.12 reads the Chebyshev decay of Delta over D 70.63-73.27 (degree 16; relative coefficients
# 1, 1.4e-3, 1.2e-5, 1.1e-7, 9.8e-10, 8.7e-12, 7.1e-14; 'a decay of 113 per order', R_D = 75) as the formula's pole
# at D = -3.2. Test: the same Chebyshev analysis of model functions whose singularities are known. If models with
# different nearest singularities give the same coefficients at these orders, the measurement cannot name it.
import numpy as np, json
from numpy.polynomial import chebyshev as Ch
import mpmath as mp
import common as C, forms as F
mp.mp.dps = 50
lo, hi = 70.63, 73.27; mid, half = (lo + hi) / 2, (hi - lo) / 2
MEAS = [1, 1.4e-3, 1.2e-5, 1.1e-7, 9.8e-10, 8.7e-12, 7.1e-14]
def cheb_coefs(f, deg=16, N=64):
    # Chebyshev interpolation at N Chebyshev points in mpmath (exact for the model; no noise floor)
    xs = [mp.cos(mp.pi * (k + mp.mpf(1) / 2) / N) for k in range(N)]
    fv = [f(mid + half * x) for x in xs]
    c = []
    for j in range(deg + 1):
        c.append(2 * sum(fv[k] * mp.cos(j * mp.pi * (k + mp.mpf(1) / 2) / N) for k in range(N)) / N)
    c[0] /= 2
    return [abs(v) for v in c]
_J = json.load(open('/Users/nathan/Source/choptuik-large-d/solver/data/formula_coefficients.json'))
a = [mp.mpf(v) for v in _J['a']]; b = [mp.mpf(1)] + [mp.mpf(v) for v in _J['b']]
Rf = lambda D: (lambda e: sum(ai * e ** i for i, ai in enumerate(a)) / sum(bi * e ** i for i, bi in enumerate(b)))(1 / (mp.mpf(D) - 2))
D_, H_, L_, s_, _ = C.data()
ev, info = F.fit_zeta_poly_arb(D_, H_, L_, s_, 28, ns0=-11.0); cz = info['coef']
def Zf(D):
    import arbfit as AF
    hl = AF.zpoly_eval(cz, np.array([float(D)]), 28, -11.0); return mp.mpf(hl[0][0]) + mp.mpf(hl[1][0])
models = {
    'measured (QUAD_DOUBLE 13.12)': None,
    'README formula R (poles -3.24, -11.0; order-6 pole at D = 2)': Rf,
    'zeta-poly K28 cut [-9, 3] fitted to the data (no poles)': Zf,
    '1.644 + 10.37/(D - 2) (pole at D = 2)': lambda D: 1.644 + 10.37 / (mp.mpf(D) - 2),
    '1.644 + 10.37/(D + 3.2) (pole at D = -3.2)': lambda D: 1.644 + 10.37 / (mp.mpf(D) + 3.2),
    '1.644 + 10.37/(D + 11) (pole at D = -11)': lambda D: 1.644 + 10.37 / (mp.mpf(D) + 11),
    '1.644 + c sqrt(D - 3) - ... : 1.644 + 10.37/sqrt((D-3)(D-2)) (branch at D = 3)': lambda D: 1.644 + 10.37 / mp.sqrt((mp.mpf(D) - 3) * (mp.mpf(D) - 2)),
}
print(f'window {lo}-{hi}, centre {mid}, half-width {half}; distance to D = 3: {mid - 3:.2f}, D = 2: {mid - 2:.2f}, '
      f'D = -3.2: {mid + 3.2:.2f}, D = -11: {mid + 11:.2f}')
print(f"{'model':80s} " + ' '.join(f'c{k}/c0'.rjust(8) for k in range(1, 7)) + '  ratios c_{k-1}/c_k, k = 3..6   R_D from k=4-6')
for nm, f in models.items():
    if f is None:
        c = MEAS
    else:
        cc = cheb_coefs(f); c = [float(v / cc[0]) for v in cc[:7]]
    rat = [c[k - 1] / c[k] for k in range(3, 7)]
    rho = np.exp(-np.polyfit(range(4, 7), np.log(c[4:7]), 1)[0]); R = half * (rho + 1 / rho) / 2
    print(f'{nm:80s} ' + ' '.join(f'{v:8.1e}' for v in c[1:7]) + '  ' + ' '.join(f'{v:6.1f}' for v in rat) + f'   {R:6.1f}')
