import sys, os, json, time
HP = '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp'
sys.path.insert(0, HP)
import numpy as np
import mpmath as mp
from hpkernel.driver import make_solver, load_q, qmax
from pinning import band_coeffs, band_field
mp.mp.dps = 50
raw = '/Users/nathan/Source/choptuik-large-d-raw/'
KS = [5, 7, 9, 11, 13]
for st in sys.argv[1:]:
    z, m = load_q(raw + st)
    D = mp.mpf(m['D_str']) if 'D_str' in m else mp.mpf(repr(float(m['D'])))
    M = int(m['M'])
    t0 = time.time()
    s = make_solver(D, M, nodes=list(m['nodes']), kt=m.get('kt', 36), kc=m.get('kc', 146), ks=m.get('ks', 130), threads=2, kfreeze=3)
    s.set_segs(s.plan(np.asarray(z[0]), np.asarray(z[1]), 1e-32, 0.05))
    out = s.newton_q(*z)
    print(f'{st}: D {mp.nstr(D, 10)} newton_q {time.time() - t0:.1f} s, piv {out[6]:.1e}..{out[7]:.1e}', flush=True)
    L = len(z[0]); K = (L - 1) // (4 * M) - 1; r0 = K * 4 * M
    zero = np.zeros(L)
    h = band_coeffs(np.asarray(z[0])[:M], np.asarray(z[1])[:M], M, KS)
    for i, k in enumerate(KS):
        row = []
        for j, ab in enumerate([(1.0, 0.0), (0.0, 1.0)]):
            fh, fl = band_field([ab], [k], M)
            ch = zero.copy(); cl = zero.copy()
            ch[r0:r0 + M] = fh; cl[r0:r0 + M] = fl
            x = s.qlu_solve(ch, cl, zero, zero)
            row.append(float(np.asarray(x[0])[-1] + np.asarray(x[1])[-1]))
        print(f'  k {k:2d}: h = ({h[i][0]:+.6e}, {h[i][1]:+.6e})  dDelta/dh = ({row[0]:+.4e}, {row[1]:+.4e})', flush=True)
