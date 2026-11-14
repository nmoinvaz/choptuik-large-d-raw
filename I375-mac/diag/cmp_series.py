import sys, time, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci, complex_imag_dd as cd, ddnp as dd
from ddnp import R, C
bg = ci.Background(sys.argv[1])
st = cd.DDState(bg)
M = bg.M
rng = np.random.default_rng(0)
Y = dd.from_complex(rng.standard_normal((2 * M, 64)) + 1j * rng.standard_normal((2 * M, 64)))
bgs = cd.bg_series(st, 0.6, st.node[3], 32)
for kc, gG in ((1.0, 1.0), (1.1, 1.0), (1.0, 0.0)):
    t = time.time(); P, Q = cd.test_series(st, 0.6, bgs, Y, 1.3 + 0.4j, 32, kc, gG); t1 = time.time() - t
    t = time.time(); Z = cd.test_series2(st, 0.6, bgs, Y, 1.3 + 0.4j, 32, kc, gG); t2 = time.time() - t
    worst = 0.0
    for k in range(33):
        for blk, ref in ((slice(0, M), P[k]), (slice(M, 2 * M), Q[k])):
            dz = dd.csub(Z[k][blk], ref)
            worst = max(worst, dd.maxabs(dz) / dd.maxabs(ref))
    print('kcoup %g gG %g: old %.2fs new %.2fs; largest double-double difference per order and block, relative: %.1e'
          % (kc, gG, t1, t2, worst), flush=True)
