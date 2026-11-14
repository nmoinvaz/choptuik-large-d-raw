"""where the lambda = i omega evaluation of #771 spends its time (#781): the series' tail, then D with a traceback
dump after 60 s and a hard stop after 90 s"""
import sys, time, math, faulthandler
import numpy as np
sys.path.insert(0, sys.argv[1])
import css_inf_jump as m
P = m.Problem(N=160)
x, j = P.select(log=lambda s: None)
lam = 1j * P.om
for u0, v0 in ((1.0, 0.0), (0.0, 1.0)):
    cs, res = m.pert_series(P.bgc, P.om, lam, u0, v0, P.N)
    for name, c in zip("uvw", cs):
        nz = np.abs(c[1:])
        print('data (%g, %g) %s: |c_0| %.2e, max |c_k| k >= 1 %.2e, |c_1..c_4| %s' % (
            u0, v0, name, abs(c[0]), nz.max(), ' '.join('%.1e' % a for a in nz[:4])), flush=True)
faulthandler.dump_traceback_later(60, exit=False)
t = time.time()
import signal
signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError('90 s')))
signal.alarm(90)
try:
    d = P.det(lam)
    print('D(i omega) = %r (%.1f s, nfev %d)' % (d, time.time() - t, P.last['nfev']), flush=True)
except TimeoutError as e:
    print('D(i omega): stopped after %.0f s' % (time.time() - t), flush=True)
