# All double-double Delta points 3.04375 <= D <= 67.77: delta_dd.csv (continuation, D >= 8.25, and best low-D) plus the
# resolved best rows of delta_dd_lowD.csv; the unresolved M48 rows (4.25-8.2) are dropped. err: Delta_err, or |dM| for
# low-D rows, floored at 1e-15; M80 rows at 3.72-3.8 get 1.2e-9 (README: M 80 -> 96 is 1.2e-9).
import csv, numpy as np
R = '/Users/nathan/Source/choptuik-large-d/hp/data/'
def load(clean=False):
    pts = {}
    for r in csv.DictReader(open(R + 'delta_dd.csv')):
        if 'unresolved' in r['run']:
            continue
        D = round(float(r['D']), 6); v = float(r['Delta_hi']) + float(r['Delta_lo'])
        if r['run'].startswith('lowD'):
            err = float(r['Delta_err']) if r['Delta_err'] else (1.2e-9 if r['run'] == 'lowD-M80' else 1e-12)
        else:
            err = float(r['Delta_err'])
        pts[D] = (v, max(err, 1e-15), r['run'])
    for r in csv.DictReader(open(R + 'delta_dd_lowD.csv')):
        if r['best'] == '1' and r['resolved'] == '1':
            D = round(float(r['D']), 6)
            if D not in pts:
                c = r['change_from_lower_M']; err = abs(float(c)) if c else 1.2e-9
                pts[D] = (float(r['Delta_hi']) + float(r['Delta_lo']), max(err, 1e-15), 'lowDcsv-M' + r['M'])
    Ds = np.array(sorted(pts)); y = np.array([pts[d][0] for d in Ds]); s = np.array([pts[d][1] for d in Ds])
    run = [pts[d][2] for d in Ds]
    return Ds, y, s, run
if __name__ == '__main__':
    D, y, s, run = load(); print(len(D), D.min(), D.max(), (D < 8.25).sum(), 'below 8.25')
    print(D[D < 8.3])
