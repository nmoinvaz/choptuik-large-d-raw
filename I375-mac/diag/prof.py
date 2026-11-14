import sys, time, cProfile, pstats, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci, complex_imag_dd as cd, ddnp as dd
from ddnp import R, C
bg = ci.Background(sys.argv[1])
st = cd.DDState(bg)
M = bg.M
I2 = np.eye(2 * M)
Y0 = C(R(I2.copy()), R(np.zeros((2 * M, 2 * M))))
lam = 1.3 + 0.4j
t = time.time()
bgs, ts = cd.taylor_series(st, 0.6, st.node[3], None, lam, 32)
print('bg series K32: %.2fs' % (time.time() - t), flush=True)
pr = cProfile.Profile(); pr.enable()
t = time.time()
bgs, ts = cd.taylor_series(st, 0.6, st.node[3], Y0, lam, 32)
print('full series K32 nc64: %.2fs' % (time.time() - t), flush=True)
pr.disable()
h = cd.step_size(bgs, ts, 32, 1e-20)
print('h at tol 1e-20: %.4g' % h)
for tl in (1e-12, 1e-14, 1e-16):
    print("h at tol %g: %.4g" % (tl, cd.step_size(bgs, ts, 32, tl)))
pstats.Stats(pr).sort_stats('cumtime').print_stats(12)
t = time.time()
H, tail = cd.horizon_dd(st, bg, lam, 0.7)
print('horizon: %.2fs tail %.1e' % (time.time() - t, tail))
