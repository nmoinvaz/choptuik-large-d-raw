# Numerical check of four identities used in the #172 addendum (inferred, not quoted from a source).
#   1. d/dt artanh(c sin t), c = 2 sqrt(q)/(1+q)  = 2 sqrt(q) * B(t; q, 0)       (Rozali-Way oscillaton)
#   2. d/dt arctan(k sin t), k = 2 sqrt(q)/(1-q)  = 2 sqrt(q) * B(t; q, pi)      (sine-Gordon breather centre)
#   3. Re[e^{-i phi}/(1 - r1 r2 e^{-2 i phi})] at phi = -t = Re[e^{it}/(1 + w e^{2it})], w = -r1 r2  (Fabry-Perot)
#   4. B(t; q, delta) = [(1 + P_q(phi)) cos t - Q_q(phi) sin t]/2, phi = 2t + delta + pi, with the Poisson
#      kernel P_r = (1 - r^2)/(1 - 2r cos + r^2) (DLMF 1.15.12) and the conjugate kernel Q_r = 2r sin/(...)
# B is Eq. (16)'s real form with A* = 1. Any command-line argument flips the sign of q (1, 2, 4) or of w (3),
# so every check must then fail. Run: python3 identity_check.py [mutate]
import sys
import mpmath as mp

mp.mp.dps = 30
s = -1 if len(sys.argv) > 1 else 1


def B(t, q, d):
    return (mp.cos(t) + q * mp.cos(t + d)) / (1 + q**2 + 2 * q * mp.cos(2 * t + d))


def P(r, x):
    return (1 - r**2) / (1 - 2 * r * mp.cos(x) + r**2)


def Q(r, x):
    return 2 * r * mp.sin(x) / (1 - 2 * r * mp.cos(x) + r**2)


q = mp.mpf('0.3')
d = mp.mpf('0.7')
c = 2 * mp.sqrt(q) / (1 + q)
k = 2 * mp.sqrt(q) / (1 - q)
r1r2 = mp.mpc('0.4', '0.2')
w = -r1r2
dev = [0, 0, 0, 0]
for j in range(-20, 21):
    t = mp.mpf(j) / 7
    d1 = mp.diff(lambda u: mp.atanh(c * mp.sin(u)), t) - 2 * mp.sqrt(q) * B(t, s * q, 0)
    d2 = mp.diff(lambda u: mp.atan(k * mp.sin(u)), t) - 2 * mp.sqrt(q) * B(t, s * q, mp.pi)
    phi = -t
    d3 = mp.re(mp.exp(-1j * phi) / (1 - r1r2 * mp.exp(-2j * phi))) - mp.re(mp.exp(1j * t) / (1 + s * w * mp.exp(2j * t)))
    x = 2 * t + d + mp.pi
    d4 = B(t, s * q, d) - ((1 + P(q, x)) * mp.cos(t) - Q(q, x) * mp.sin(t)) / 2
    dev = [max(dev[0], abs(d1)), max(dev[1], abs(d2)), max(dev[2], abs(d3)), max(dev[3], abs(d4))]
print('max deviations (oscillaton, breather, Fabry-Perot, Poisson):', [mp.nstr(x, 3) for x in dev])
ok = all(x < 1e-20 for x in dev)
print('all pass' if ok else 'FAIL')
sys.exit(0 if ok else 1)
