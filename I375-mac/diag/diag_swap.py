import sys, time, numpy as np, math
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci
from flint import acb_mat, acb, ctx
ctx.prec = 256
bg = ci.Background(sys.argv[1])
lam = complex(sys.argv[2]) if len(sys.argv) > 2 else 1.3 + 0.4j
A11 = ci.TestField(bg, rtol=1e-11).matrix(lam)
A13 = ci.TestField(bg, rtol=1e-13).matrix(lam)
N = A11.shape[0]; M = bg.M; L = len(bg.X)
def lnd(B):
    m = acb_mat([[acb(B[i, j].real, B[i, j].imag) for j in range(N)] for i in range(N)])
    lg = m.det().log()
    return complex(float(lg.real.mid()), float(lg.imag.mid()))
base = lnd(A13)
d11 = lnd(A11) - base
print('lam', lam, 'arb ln det rtol13', base, ' rtol11 - rtol13:', d11.real, math.remainder(d11.imag, 2*math.pi))
names = ['centre'] + ['seg%d' % b for b in range(1, L)] + ['horizon']
for bi, nm in enumerate(names[:-1]):
    B = A13.copy(); r = slice(2 * M * bi, 2 * M * (bi + 1)); B[r] = A11[r]
    d = lnd(B) - base
    print('only %s at rtol 1e-11: dln|det| %.2e dphase %.2e  (max rel entry change %.1e)' % (
        nm, d.real, math.remainder(d.imag, 2*math.pi), np.max(np.abs(A11[r] - A13[r])) / np.max(np.abs(A13[r]))), flush=True)
