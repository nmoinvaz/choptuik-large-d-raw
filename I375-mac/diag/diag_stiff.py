import sys, time, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci
from scipy.integrate import solve_ivp
bg = ci.Background(sys.argv[1])
tf = ci.TestField(bg)
lam = 1.3 + 0.4j
segs = bg.segs
print('omega', bg.omega, 'n', bg.n)
for (x0, x1, seg) in segs:
    rad = []
    for x in np.linspace(x0, x1, 5):
        ev = np.linalg.eigvals(tf.amat(x, seg, lam))
        rad.append((np.max(np.abs(ev)), np.max(ev.real), np.min(ev.real)))
    p, m, a, c = bg.bg_at(x1, seg)
    for rt in (1e-11, 1e-13):
        f = lambda x, y: (tf.amat(x, seg, lam) @ y.reshape(2 * bg.M, 2 * bg.M)).ravel()
        sol = solve_ivp(f, (x0, x1), np.eye(2 * bg.M, dtype=complex).ravel(), method='DOP853', rtol=rt, atol=1e-14)
        print('seg %.2f-%.2f rtol %g: nfev %d steps %d' % (x0, x1, rt, sol.nfev, len(sol.t) - 1))
    print('   |eig|max, Re max, Re min at 5 x:', ['%.0f %.0f %.0f' % r for r in rad], 'c range at x1 %.3f..%.3f' % (c.min(), c.max()))
