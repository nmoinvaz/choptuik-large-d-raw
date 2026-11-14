import sys, time, math, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci, complex_imag_dd as cd, ddnp as dd
from ddnp import R, C
bg = ci.Background(sys.argv[1], ks_series=int(sys.argv[3]) if len(sys.argv) > 3 else 100)
lam = complex(sys.argv[2])
M = bg.M; L = len(bg.X)
ddtf = cd.DDTestField(bg, nsub=1, tol=1e-20)
Add = ddtf.matrix_dd(lam)
Ad = ddtf.tf.matrix(lam)
def lnd(A):
    return cd.lu_factor(A.copy(), lb=3 * M, ub=3 * M)[2]
base = lnd(Add)
print("dd", base, "double (dd LU)", lnd(dd.from_complex(Ad)), "horizon tail", ddtf.last_tail, ddtf.last_times, flush=True)
names = ['centre'] + ['seg%d' % b for b in range(1, L)] + ['horizon']
for bi, nm in enumerate(names):
    B = Add.copy()
    r = slice(2 * M * bi, 2 * M * (bi + 1))
    B[r] = dd.from_complex(Ad[r])
    v = lnd(B) - base
    blk = Ad[r] - Add[r].to_complex()
    print('double %s in the dd matrix: dln|det| %.3e dphase %.3e; max |block diff| %.1e (max entry %.1e)' % (
        nm, v.real, math.remainder(v.imag, 2 * math.pi), np.max(np.abs(blk)), np.max(np.abs(Ad[r]))), flush=True)
