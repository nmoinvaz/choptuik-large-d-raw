"""The zeta polynomial is a dispersion relation. With x = cos(theta) the affine image of t in [n_s, 1] and the identity
(1/pi) int_{-1}^{1} sqrt(1 - x^2) U_{k-1}(x) / (u - x) dx = zeta^k (zeta = u - sqrt(u^2 - 1)),
    Delta(n) = a_0 + (1/pi) int_{n_s}^{1} rho(t) dt / (n - t),   rho(t) = sum_{k>=1} a_k sin(k theta(t)),
a_k the monomial coefficients in zeta. rho is minus the imaginary part of Delta on the upper lip of the cut. Checks:
the identity by quadrature at D = 5 and 20; the first moment (1/pi) int rho dt = a_1 (1 - n_s)/4 (the 1/n coefficient);
then where rho changes sign (a positive or negative measure would allow Stieltjes-type bounds) and how stable rho is
across fit choices (K, n_s)."""
import numpy as np, mpmath as mp
from flint import arb
import common as C, arbfit as AF
D, H, L, s, _ = C.data()
mp.mp.dps = 40
def monomial(c, K):
    # T*_k(z) = T_k(2z - 1) as monomial coefficient lists, in arb
    T = [[arb(1)], [arb(-1), arb(2)]]
    for k in range(1, K):
        a = T[k]; b = T[k - 1]; nxt = [arb(0)] * (k + 2)
        for i, v in enumerate(a):
            nxt[i + 1] += 4 * v; nxt[i] -= 2 * v
        for i, v in enumerate(b): nxt[i] -= v
        T.append(nxt)
    m = [arb(0)] * (K + 1)
    for k in range(K + 1):
        for i, v in enumerate(T[k]): m[i] += c[k] * v
    return m
fits = {}
for K, ns in ((28, -9.0), (28, -11.0), (32, -9.0), (32, -11.0)):
    ev, info = AF.fit_zpoly(D, H, L, s, K, ns0=ns); a = monomial(info['coef'], K)
    am = [mp.mpf(v.mid().str(50, radius=False)) for v in a]
    rho = lambda th, am=am: mp.fsum(am[k] * mp.sin(k * th) for k in range(1, len(am)))
    tof = lambda th, ns=ns: ((1 - ns) * mp.cos(th) + 1 + ns) / 2           # t (an n value) on the cut
    # identity check by quadrature: Delta(n) = a0 + (1/pi) int_0^pi rho(theta) sin(theta) (1 - ns)/2 / (n - t) d theta
    chk = []
    for Dq in (5.0, 20.0):
        n = mp.mpf(Dq) - 2
        I = mp.quad(lambda th: rho(th) * mp.sin(th) * (1 - ns) / 2 / (n - tof(th)), mp.linspace(0, mp.pi, 9))
        ser = ev(np.array([Dq])); ser = mp.mpf(ser[0][0]) + mp.mpf(ser[1][0])
        chk.append(f'D={Dq:g}: {float(am[0] + I / mp.pi - ser):+.1e}')
    mom = float(am[1] * (1 - ns) / 4)
    th = np.linspace(1e-4, np.pi - 1e-4, 4001); rv = np.array([float(rho(mp.mpf(x))) for x in th])
    sc = np.where(np.diff(np.sign(rv)) != 0)[0]
    Dz = [float(tof(mp.mpf(th[i]))) + 2 for i in sc]
    fits[(K, ns)] = (th, rv, ns)
    print(f'K={K} ns={ns:g}: identity {chk}; first moment {mom:.5f} (1/n coefficient); max|a_k| {max(abs(float(v)) for v in am):.1e}')
    print(f'   rho changes sign {len(sc)} times, at D = {np.round(Dz, 2)}; rho near D = 3 end (theta = 0.05): {float(rho(mp.mpf(0.05))):+.3e},'
          f' near D_s end (theta = pi - 0.05): {float(rho(mp.pi - mp.mpf(0.05))):+.3e}; max |rho| {np.abs(rv).max():.2e} at D = {float(tof(mp.mpf(th[np.argmax(np.abs(rv))]))) + 2:.2f}')
# stability of rho as a function of D on the common part of the cuts [-7, 3]: compare fits
print('rho(D) on the cut, by fit (D = t + 2):')
Dg = [-6.0, -4.0, -2.0, 0.0, 1.0, 2.0, 2.5, 2.9, 2.99]
print('   D      ' + ' '.join(f'{d:>10g}' for d in Dg))
for (K, ns), (th, rv, ns_) in fits.items():
    tD = ((1 - ns) * np.cos(th) + 1 + ns) / 2 + 2
    vals = [np.interp(d, tD[::-1], rv[::-1]) for d in Dg]
    print(f'   K{K} ns{ns:g} ' + ' '.join(f'{v:10.3e}' for v in vals))
