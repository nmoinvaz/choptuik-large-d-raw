# The recommended representation (fallback series): Delta = sum_{k=0}^{28} c_k T_k(2 zeta - 1), zeta the Joukowski
# variable of the n-plane cut [n_s, 1], n_s = -9 (D_s = -7), fitted at 256 bits on all 1214 cleaned points.
# Writes rec_coefficients.json (c_k to 30 digits) and prints its residuals by range, its agreement with the M48 thin
# points it never saw (in units of their estimated error), Dinf, Delta(3), and values at the README table's D.
import json, numpy as np
import common as C, arbfit as AF
D, H, L, s, _ = C.data(); K, NS = 28, -9.0
ev, info = AF.fit_zpoly(D, H, L, s, K, ns0=NS)
hl = ev(D); r = (hl[0] - H) + (hl[1] - L)
for a, b in [(3.0, 3.1), (3.1, 4.01), (4.01, 8.3), (8.3, 30), (30, 68)]:
    m = (D >= a) & (D < b); print(f'{a:g}-{b:g}: {m.sum():4d} pts  max|r| {np.abs(r[m]).max():.1e}  max|r|/sigma {np.abs(r[m] / s[m]).max():.1f}')
print(f'all: max|r|/sigma {np.abs(r / s).max():.2f}  chi2/dof {np.sum((r / s) ** 2) / (len(D) - K - 1):.3f}')
tD, tv, te = C.thin_m48(); th = ev(tD); rt = (th[0] - tv) + th[1]
print('M48 thin points (not fitted): ' + ' '.join(f'{d:g}:{x / e:+.1f}' for d, x, e in zip(tD, rt, te)) + '  (in units of their est. error)')
print(f"Dinf {info['Dinf']:.12f}  Delta(3) {info['D3']:.5f}")
for d in (4, 5, 6, 7, 8, 10, 20, 60, 70, 100, 1000):
    v = ev(np.array([float(d)])); print(f'  D={d}: {v[0][0] + v[1][0]:.13f}')
json.dump(dict(form='Delta(D) = sum_k c_k T_k(2 zeta - 1); zeta = u - sqrt(u^2 - 1); u = (2 (D - 2) - (1 + n_s)) / (1 - n_s)',
               n_s=NS, K=K, c=[v.mid().str(30, radius=False) for v in info['coef']], Dinf=info['Dinf'], Delta3=info['D3'],
               data='hp/data/delta_dd.csv + delta_dd_lowD.csv, 1214 points after hp/dd_fits_mp.clean'),
          open('rec_coefficients.json', 'w'), indent=1)
