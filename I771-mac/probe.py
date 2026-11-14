import sys, time, math, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-771/solver/matter')
import css_inf_jump as m
P = m.Problem()
x, j = P.select()
print('bg', x, j, 'A', x[0] * x[1], flush=True)
om = P.om
for lam in (2.05, 1.5 + 0.3j, 3.0, 0.5 + 7.9j, 0.53 + 7.93j, 0.5365223424 + 7.9320241697j, 2.0 + 1e-6, 2.0 - 1e-6):
    t = time.time(); d = P.det(lam)
    print('lam %-28s D %.6e%+.6ei |D| %.2e (%.1fs, nfev %d, bg jump %.1e)' % (lam, d.real, d.imag, abs(d), time.time() - t, P.last['nfev'], P.last['jump_bg']), flush=True)
