import sys, time, numpy as np, math
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci
from flint import acb_mat, acb, ctx
ctx.prec = 320
bg = ci.Background(sys.argv[1])
lam = 1.3 + 0.4j
tf = ci.TestField(bg, rtol=1e-13)
A = tf.matrix(lam)
N = A.shape[0]
def lnd_arb(B):
    t = time.time()
    m = acb_mat([[acb(complex(B[i, j]).real, complex(B[i, j]).imag) for j in range(N)] for i in range(N)])
    d = m.det()
    return complex(d.log().real.mid(), d.log().imag.mid()) if False else (d, time.time() - t)
d, tt = lnd_arb(A)
print('N', N, 'arb det', d.mid().str(5) if hasattr(d,'mid') else d, 'rad', d.rad(), '%.1fs' % tt)
print('numpy lndet', tf.lndet(lam))
lg = d.log()
print('arb lndet', float(lg.real.mid()), float(lg.imag.mid()))
rng = np.random.default_rng(1)
for eps in (1e-16, 1e-20, 1e-24):
    P = A * (1 + eps * (rng.standard_normal(A.shape) + 1j * rng.standard_normal(A.shape)))
    dp, _ = lnd_arb(P)
    lp = dp.log()
    print('eps %g: dln|det| %.3e dphase %.3e' % (eps, float(lp.real.mid()) - float(lg.real.mid()),
          math.remainder(float(lp.imag.mid()) - float(lg.imag.mid()), 2 * math.pi)), flush=True)
# blockwise: perturb only one block row at 1e-20
M = bg.M; L = len(bg.X)
names = ['centre'] + ['seg%d' % b for b in range(1, L)] + ['horizon']
for bi, nm in enumerate(names):
    P = A.copy()
    r = slice(2 * M * bi, 2 * M * (bi + 1))
    P[r] = P[r] * (1 + 1e-20 * (rng.standard_normal(P[r].shape) + 1j * rng.standard_normal(P[r].shape)))
    dp, _ = lnd_arb(P); lp = dp.log()
    print('rows %s at 1e-20: dln|det| %.3e dphase %.3e' % (nm, float(lp.real.mid()) - float(lg.real.mid()),
          math.remainder(float(lp.imag.mid()) - float(lg.imag.mid()), 2 * math.pi)), flush=True)
