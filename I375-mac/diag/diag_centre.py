import sys, time, math, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci, complex_imag_dd as cd, ddnp as dd
from ddnp import R, C
bg = ci.Background(sys.argv[1])
lam = complex(sys.argv[2])
M = bg.M
ddtf = cd.DDTestField(bg, nsub=1, tol=1e-20)
A = ddtf.matrix_dd(lam)
lnd = lambda B: cd.lu_factor(B.copy(), lb=3 * M, ub=3 * M)[2]
base = lnd(A)
print('base', base, flush=True)
rng = np.random.default_rng(5)
for eps in (1e-15, 1e-13):
    for nm, r, c in (('centre block C (rows 0..2M, cols 0..M)', slice(0, 2 * M), slice(0, M)),):
        B = A.copy()
        z = B[r, c].to_complex()
        z = z * (1 + eps * (rng.standard_normal(z.shape) + 1j * rng.standard_normal(z.shape)))
        B[r, c] = dd.from_complex(z)
        v = lnd(B) - base
        print('%s relative %.0e: dln|det| %.2e dphase %.2e' % (nm, eps, v.real, math.remainder(v.imag, 2 * math.pi)), flush=True)
# the pre-segment's tolerance: C from DOP853 at rtol 1e-11 against 1e-13
for rt in (1e-11,):
    tf2 = ci.TestField(bg, rtol=rt)
    Cm = tf2.centre(lam, bg.xs)
    x0, x1, seg = bg.segs[0]
    Cm = tf2.propagate(seg, x0, x1, Cm, lam)
    B = A.copy(); B[0:2 * M, 0:M] = dd.from_complex(Cm)
    v = lnd(B) - base
    print('centre block with the pre-segment at rtol %g: dln|det| %.2e dphase %.2e' % (rt, v.real, math.remainder(v.imag, 2 * math.pi)))
# the centre series order (kc 50 against 40) at x_s
bg2 = ci.Background(sys.argv[1], kc_series=40)
tf3 = ci.TestField(bg2)
Cm = tf3.centre(lam, bg2.xs); x0, x1, seg = bg2.segs[0]; Cm = tf3.propagate(seg, x0, x1, Cm, lam)
B = A.copy(); B[0:2 * M, 0:M] = dd.from_complex(Cm)
v = lnd(B) - base
print('centre block from kc 40 (base kc 50): dln|det| %.2e dphase %.2e' % (v.real, math.remainder(v.imag, 2 * math.pi)))
