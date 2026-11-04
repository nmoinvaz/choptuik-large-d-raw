# One series for all D > 3: Delta as a polynomial in zeta, the Joukowski variable of the n-plane cut along [n_s, 1]
# (n = D - 2; D = 3 is n = 1). zeta(D = inf) = 0, zeta(D = 3) = 1, zeta(D_s) = -1; zeta ~ (1 - n_s)/(4n) at large n,
# so analyticity in 1/n at D = inf is built in, and square-root branch points at both cut ends become regular points.
import sys, numpy as np
from numpy.polynomial import chebyshev as Ch
from data import load
DINF = 1.643893746
def zeta(D, ns):
    n = np.asarray(D, float) - 2.0
    u = (2 * n - (1 + ns)) / (1 - ns)
    return u - np.sqrt(u * u - 1)
def fit(D, y, s, ns, K, lo=0.0, hi=1.0):
    z = zeta(D, ns); a, b = lo, hi
    t = (2 * z - (a + b)) / (b - a)
    V = Ch.chebvander(t, K) / s[:, None]
    c, *_ = np.linalg.lstsq(V, y / s, rcond=None)
    ev = lambda DD: Ch.chebval((2 * zeta(DD, ns) - (a + b)) / (b - a), c)
    evz = lambda zz: Ch.chebval((2 * np.asarray(zz) - (a + b)) / (b - a), c)
    return ev, evz
if __name__ == '__main__':
    D, y, s, run = load()
    fitm = D <= 45.0; hold = D > 45.0
    lowho = D < 3.1
    print(f'{len(D)} points; fit-all, and fit on D <= 45 to predict 45 < D <= {D.max():.2f} ({hold.sum()} points);'
          f' fit on D >= 3.1 to predict 3.04375-3.1 ({lowho.sum()} points)')
    print(f"{'n_s':>6s} {'D_s':>6s} {'K':>3s} {'max|r|/s all':>12s} {'max|r| D>=8.25':>14s} {'limit-1.643893746':>17s} "
          f"{'Delta(3)':>9s} {'held>45 max':>11s} {'held<3.1 max':>12s} {'limit(fit<=45)':>15s}")
    for ns in [float(v) for v in (sys.argv[1].split(',') if len(sys.argv) > 1 else '-6,-9,-11,-13,-15,-20,-40'.split(','))]:
        for K in [int(v) for v in (sys.argv[2].split(',') if len(sys.argv) > 2 else '16,20,24,28,32'.split(','))]:
            ev, evz = fit(D, y, s, ns, K)
            r = ev(D) - y
            ev2, evz2 = fit(D[fitm], y[fitm], s[fitm], ns, K)
            h = np.abs(ev2(D[hold]) - y[hold]).max()
            ev3, _ = fit(D[~lowho], y[~lowho], s[~lowho], ns, K)
            hl = np.abs(ev3(D[lowho]) - y[lowho]).max()
            print(f'{ns:6.1f} {ns + 2:6.1f} {K:3d} {np.abs(r / s).max():12.1e} {np.abs(r[D >= 8.25]).max():14.1e} '
                  f'{evz(0.0) - DINF:+17.2e} {evz(1.0):9.5f} {h:11.1e} {hl:12.1e} {evz2(0.0) - DINF:+15.2e}', flush=True)
