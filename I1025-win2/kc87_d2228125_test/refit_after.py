#!/usr/bin/env python3
"""refit_after.py: the refit that the order allowed only AFTER the reading of the registered test (predict_check.py printed its classification first).
Reads every scan row of the low, neg, fine and test folders of D 22.28125 (four decimals), writes joint/ln_table4.txt (lambda to four decimals; the driver's table prints three and merges -0.1990 with -0.1985),
and fits the zero and the pole model of ../kc87_d2228125_fine/fit_zero_pole.py (same functions, imported) to the hybrid ln|det| at -0.20 .. -0.08 including the three new points, with lc on a 1e-5 grid in the sign-change bracket (-0.1985, -0.1965).
Exploratory, as before: an estimator over a model class, not an enclosure."""
import sys, glob, json, importlib.util
import numpy as np
base = 'D:/choptuik-i935-raw/I1025-win2/'
sys.argv = [sys.argv[0]]
spec = importlib.util.spec_from_file_location('fz', base + 'kc87_d2228125_fine/fit_zero_pole.py'); fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
rows = {}
for d in ('kc87_d2228125_low', 'kc87_d2228125_neg', 'kc87_d2228125_fine', 'kc87_d2228125_test'):
    for f in sorted(glob.glob(base + d + '/scan_D22.28125_p*.jsonl')):
        for l in open(f):
            if l.strip():
                r = json.loads(l); rows[round(r['lam'], 4)] = r
ls = sorted(rows)
with open(base + 'kc87_d2228125_test/joint/ln_table4.txt', 'w') as o:
    o.write('lambda  hybrid  f64  ln|det| hybrid  ln|det| f64  slope(to next, per unit lambda)\n')
    for i, l in enumerate(ls):
        r = rows[l]
        sl = (rows[ls[i + 1]]['ln'] - r['ln']) / (ls[i + 1] - l) if i + 1 < len(ls) else float('nan')
        o.write('%+.4f  %+d  %+d  %.4f  %.4f  %.1f\n' % (l, r['sign'], r['f64_sign'], r['ln'], r['f64_ln'], sl))
sel = [l for l in ls if -0.2001 <= l <= -0.0799]
x = np.array(sel); y = np.array([rows[l]['ln'] for l in sel])
print(len(x), 'points', ' '.join('%+.4f' % v for v in x))
for kind in ('zero', 'pole'):
    out = None
    for lc in np.arange(-0.19849, -0.19651, 1e-5):
        c, rms, r = fz.fit(kind, lc, x, y)
        if out is None or rms < out[0]:
            out = (rms, lc, c, r)
    print('%s: best lc %.5f rms %.5f a %.4f s %.3f q %.2f residuals %s' % (kind, out[1], out[0], out[2][0], out[2][1], out[2][2], ' '.join('%+.3f' % v for v in out[3])))
# the zero fit's lc range at rms <= 0.01 and <= 0.03
oks = {}
for tol in (0.01, 0.03):
    ok = [lc for lc in np.arange(-0.19849, -0.19651, 1e-5) if fz.fit('zero', lc, x, y)[1] <= tol]
    print('zero rms <= %.2f: lc in [%.5f, %.5f]' % (tol, min(ok), max(ok)) if ok else 'zero rms <= %.2f: none' % tol)
