# The production path of hp/dd_fits_mp.py (60 digits, Chebyshev LS, its clean()), with conformal-map variables added
# to its MODELS in memory: w1(n_s) maps the plane cut along e <= 1/n_s (e = 1/n) onto the unit disc, e = 0 -> 0.
# Fit on 10 <= D <= 45 (cleaned, dmax 60.1 as the README table), held out 45 < D <= 60.1; and fit on all 10-60.1.
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/hp')
import mpmath as mp
import dd_fits_mp as F
DINF = mp.mpf('1.643893746')
def w1(ns):
    ns = mp.mpf(ns)
    def f(D):
        q = mp.sqrt(1 - ns / (mp.mpf(D) - 2)); return (q - 1) / (q + 1)
    return f
def zeta(ns):
    ns = mp.mpf(ns)
    def f(D):
        u = (2 * (mp.mpf(D) - 2) - (1 + ns)) / (1 - ns); return u - mp.sqrt(u * u - 1)
    return f
args = sys.argv[1:]
dmax = float(args[0]) if args else 60.1
specs = args[1].split(';') if len(args) > 1 else ['1/D:12,14,16', 'w1:-11:10,12,14']
pts, _ = F.load_points()
Ds = sorted(d for d in pts if 10 <= d <= dmax)
t = time.time(); Ds = F.clean(pts, Ds, verbose=False); print(f'{len(Ds)} cleaned points 10-{dmax} ({time.time() - t:.0f} s)', flush=True)
fitD = [d for d in Ds if d <= 45]; hold = [d for d in Ds if d > 45]
for spec in specs:
    p = spec.split(':')
    if p[0] in F.MODELS:
        name, Ks = p[0], [int(k) for k in p[1].split(',')]
    else:
        name = f'{p[0]}({p[1]})'; F.MODELS[name] = (w1 if p[0] == 'w1' else zeta)(p[1]); Ks = [int(k) for k in p[2].split(',')]
    for K in Ks:
        t = time.time()
        ev, res, _ = F.fit(pts, fitD, name, K)
        h = max(abs(ev(d) - pts[d]) for d in hold)
        lim45 = ev(mp.mpf(10) ** 80) - DINF
        eva, resa, _ = F.fit(pts, Ds, name, K)
        lima = eva(mp.mpf(10) ** 80) - DINF
        print(f'{name:12s} K={K:2d}  fit<=45: res {mp.nstr(res, 2):>7s} held45-{dmax} {mp.nstr(h, 2):>7s} lim-Dinf {mp.nstr(lim45, 2):>8s}'
              f' | all: res {mp.nstr(resa, 2):>7s} lim-Dinf {mp.nstr(lima, 2):>8s}  ({time.time() - t:.0f} s)', flush=True)
