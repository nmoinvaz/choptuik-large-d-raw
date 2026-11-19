# glue (read only, no computation of the solver): tables for #997 step (a) from the saved series and the run logs, for the three runs of 2026-11-19 beyond the first two:
# run 1 (M 128 at D 3.15, target 3.14) against the first run (M 160) per order, and run 2 (M 256 at D 3.0475, target 3.0465).
# usage (from the raw-743 worktree root, python -I): python I997-win2/tab997.py > I997-win2/tab997.txt
import re
import numpy as np
from mpmath import mp, mpf
mp.dps = 40
X = 'I997-win2/'


def log(p):
    d = {}
    for l in open(p, errors='replace'):
        m = re.match(r'\s+z_(\d+): \|z\| ([\d.e+-]+), \|rhs\| ([\d.e+-]+), (\d+) products, converged (\w+), (\d+) \+ (\d+) s', l)
        if m:
            d[int(m.group(1))] = (float(m.group(2)), int(m.group(4)), m.group(5), int(m.group(6)), int(m.group(7)))
    return d


def delta(p):
    z = np.load(p, allow_pickle=True)
    return [mpf(float(a)) + mpf(float(b)) for a, b in zip(z['delta_hi'], z['delta_lo'])], z


def psums(dk, h, ref):
    s = mpf(0)
    out = []
    for k, d in enumerate(dk):
        s += d * mpf(h) ** k
        out.append((k, d * mpf(h) ** k, s - ref if ref is not None else None))
    return out


a160, za = delta(X + 'series/series_D3.15_M160_N20.npz')
a128, zb = delta(X + 'series_M128/series_D3.15_M128_N20.npz')
l160, l128 = log(X + 'series/run.log'), log(X + 'series_M128/run.log')
print('===== run 1: D 3.15, M 128 against M 160 (the first run), target D 3.14')
print('Newton Delta(3.14): M 128 2.928976393761668, M 160 2.928976301580259, difference %.4e' % (2.928976393761668 - 2.928976301580259))
print('k | Delta_k M128 | Delta_k M160 | rel diff | |z_k| M128 | |z_k| M160 | growth M128 | growth M160')
for k in range(21):
    rel = abs(a128[k] - a160[k]) / abs(a160[k])
    if k == 0:
        print('%d | %.6e | %.6e | %.2e |' % (k, a128[k], a160[k], rel))
    else:
        g1 = (l128[k][0] / l128[k - 1][0]) if k > 1 else float('nan')
        g2 = (l160[k][0] / l160[k - 1][0]) if k > 1 else float('nan')
        print('%d | %.6e | %.6e | %.2e | %.3e | %.3e | %.4g | %.4g' % (k, a128[k], a160[k], rel, l128[k][0], l160[k][0], g1, g2))
print('partial sums of Delta_k h^k at h = -0.01 minus Newton Delta(3.14) of M 128 (k, term, error):')
for k, t, e in psums(a128, '-0.01', mpf('2.928976393761668')):
    if k in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20):
        print('  %2d %s %s' % (k, mp.nstr(t, 4), mp.nstr(e, 4)))
print('ratios Delta_k / Delta_(k-1), M 128 | M 160:')
print('  ' + ' '.join('%d:%.3g|%.3g' % (k, a128[k] / a128[k - 1], a160[k] / a160[k - 1]) for k in range(1, 21)))

a256, zc = delta(X + 'series_D30475/series_D3.0475_M256_N20.npz')
l256 = log(X + 'series_D30475/run.log')
print()
print('===== run 2: D 3.0475, M 256, target D 3.0465 (h = -0.001): the target Newton did not run, the prediction is non-finite on its own plan (31 steps)')
print('k | Delta_k | Delta_k/Delta_(k-1) | |z_k| | growth |z_k|/|z_(k-1)| | products | solve+product s')
print('0 | %.6e' % a256[0])
for k in range(1, 21):
    g = (l256[k][0] / l256[k - 1][0]) if k > 1 else float('nan')
    print('%d | %.6e | %.4g | %.3e | %.4g | %d | %d + %d' % (k, a256[k], a256[k] / a256[k - 1], l256[k][0], g, l256[k][1], l256[k][3], l256[k][4]))
print('terms Delta_k h^k at h = -0.001 (arithmetic only, there is no Newton Delta at the target):')
for k, t, e in psums(a256, '-0.001', None):
    print('  %2d %s' % (k, mp.nstr(t, 4)))
print('terms |z_k| |h|^k at h = -0.001 (largest part norm):')
print('  ' + ' '.join('%d:%.2e' % (k, l256[k][0] * 1e-3 ** k) for k in range(1, 21)))
