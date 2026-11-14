"""D(lambda) at the box's corners and left edge, and the conjugation symmetry (#781, setting A, N 160)"""
import sys, time, math, json
sys.path.insert(0, sys.argv[1])
import css_inf_jump as m
P = m.Problem(N=160)
x, j = P.select(log=lambda s: None)
print('bg f0 %.16f omega %.16f jump %.1e' % (x[0], x[1], j), flush=True)
om = P.om
for lam in (0.05 + 9j, 0.05 - 9j, 5 + 9j, 5 - 9j, 5.0, 0.05, 0.05 + 1j * om, 0.05 - 1j * om, 0.05 + 4.2j, 0.05 - 4.2j,
            2.5 + 6j, 2.5 - 6j):
    t = time.time()
    try:
        d = P.det(lam)
        print('lam %-22s D %+.6e %+.6ei |D| %.2e arg %+.4f (%.1fs, nfev %d)' % (
            lam, d.real, d.imag, abs(d), math.atan2(d.imag, d.real), time.time() - t, P.last['nfev']), flush=True)
    except Exception as e:
        print('lam %-22s %s: %s (%.1fs)' % (lam, type(e).__name__, e, time.time() - t), flush=True)
