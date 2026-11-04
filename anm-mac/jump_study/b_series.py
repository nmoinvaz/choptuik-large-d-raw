"""Delta from the 1/D and 1/n series fitted on the double-double points 10 <= D <= 67.77 (hp/dd_fits_mp, as
hp/full_release.py and hp/chain_vs_series.py use them), at the targets; written to series.json."""
import sys, json
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/hp')
import mpmath as mp
import dd_fits_mp as F
mp.mp.dps = 60
targets = [67.742203, 68.5, 69.5, 70.5, 73.0, 79.765722, 85.74734, 100.0, 200.0]
pts, _ = F.load_points()
Ds = F.clean(pts, sorted(d for d in pts if 10 <= d <= 67.77), verbose=False)
out = {}
for var, deg in (('1/D', 16), ('1/D', 18), ('1/D', 20), ('1/n', 18), ('1/n', 20)):
    ev, res, _ = F.fit(pts, Ds, var, deg)
    out[f'{var} {deg}'] = {str(D): mp.nstr(ev(mp.mpf(D)), 30) for D in targets}
    print(var, deg, f'residual {float(res):.1e}', ' '.join(f'{D}: {mp.nstr(ev(mp.mpf(D)), 18)}' for D in targets), flush=True)
json.dump(dict(n_points=len(Ds), fits=out), open('series.json', 'w'), indent=1)
