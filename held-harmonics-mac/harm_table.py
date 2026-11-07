import glob, json, os, sys
import numpy as np
R = '/Users/nathan/Source/choptuik-large-d-raw/'
H = '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp/data/states/'
OUT = '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics/'
M = 32
th = np.pi * np.arange(M) / M
KS = list(range(1, 15, 2))


def coeffs(f):
    return [((2 / M) * np.sum(f * np.cos(k * th)), (2 / M) * np.sum(f * np.sin(k * th))) for k in KS]


def load(p):
    d = np.load(p); m = json.loads(str(d['meta']))
    parts = [d['zh'], d['zl']] + ([d['z2'], d['z3']] if 'z2' in d else [])
    z = sum(parts[::-1])
    return float(m['D']), z, m


groups = {
    'dd_full': sorted(glob.glob(H + '*.npz')) + sorted(glob.glob(R + 'T12-win/scratch/t12/*.npz'))[::6]
    + sorted(glob.glob(R + 'T13-win/scratch/t13/*.npz'))[::4],
    'qd_full': sorted(glob.glob(R + 'T84-mac/*_full.npz')) + [R + 'T81/conv_pin7_D72.8000_D72.800000.npz',
                                                              R + 'T81/conv_pin5_D73.0000_D73.000000.npz'],
    'T75': sorted(glob.glob(R + 'T75/pin7_D*.npz'))[::40] + [R + 'T75/pin7_D73.2657.npz'],
    'chain': sorted(glob.glob(R + 'anm-mac/run_trend_pin3/*.npz')) + sorted(glob.glob(R + 'anm-mac/run_trend_pin3_qd3/*.npz'))
    + sorted(glob.glob(R + 'anm-mac/run_trend_pin3_qd7/*.npz'))[::4],
}
rows = []
for g, fs in groups.items():
    for p in fs:
        D, z, m = load(p)
        if int(m['M']) != M or list(m['nodes']) != [0.3, 0.4, 0.5, 0.6, 0.7]:
            continue
        c = coeffs(z[:M])
        rows.append((g, D, c, z[-1], os.path.relpath(p, R) if p.startswith(R) else p))
rows.sort(key=lambda r: r[1])
print('group D | sqrt(n) * (a_k, b_k) for k = ' + ' '.join(str(k) for k in KS))
for g, D, c, dl, p in rows:
    n = D - 2
    print(f'{g:8s} {D:9.4f} | ' + ' '.join(f'{a*np.sqrt(n):+.6e} {b*np.sqrt(n):+.6e}' for a, b in c))
np.save(OUT + 'harm_rows.npy', np.array([(r[1],) + tuple(x for ab in r[2] for x in ab) for r in rows]))
json.dump([(r[0], r[1], r[4]) for r in rows], open(OUT + 'harm_rows.json', 'w'))
