import sys, time, numpy as np
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-xf-checks/solver/matter')
import complex_imag as ci
st = sys.argv[1]
t = time.time()
bg = ci.Background(st)
print('D', bg.D, 'X', bg.X, 'xs', bg.xs, 'pre', bg.pre, 'bg setup %.1fs' % (time.time() - t), flush=True)
lam = 1.3 + 0.4j
for rt in (1e-9, 1e-11, 1e-13):
    tf = ci.TestField(bg, rtol=rt)
    t = time.time()
    A = tf.matrix(lam)
    tA = time.time() - t
    M = bg.M
    out = []
    for b in range(1, len(bg.X)):
        Phi = A[2*M*b:2*M*(b+1), M+2*M*(b-1):M+2*M*b]
        s = np.linalg.svd(Phi, compute_uv=False)
        out.append('%.1e..%.1e' % (s[-1], s[0]))
    l1 = tf.lndet(lam); l2 = tf.lndet(lam + 1e-5)
    sv = np.linalg.svd(A, compute_uv=False)
    print('rtol %g: matrix %.1fs; segment sv %s; M sv %.1e..%.1e (next %.1e); lndet %s; d(lam+1e-5) %s' % (
        rt, tA, out, sv[-1], sv[0], sv[-2], l1, l2 - l1), flush=True)
