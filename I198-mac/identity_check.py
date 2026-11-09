# Check of four identities and two asymptotic laws that tie the #198 addendum's cavity sources to Eq. (16) of arXiv:2611.07007
# (inferred, not quoted from a source). B is Eq. (16)'s real form with A* = 1 and delta = 0,
#   B(t; q) = Re[e^{it}/(1 + q e^{2it})] = (1 + q) cos t / (1 + q^2 + 2q cos 2t).
#   1. B = (1+q)/(1-q)^2 * cos t * A(t + pi/2), with the Airy distribution A(phi) = 1/(1 + F sin^2 phi) and the
#      coefficient of finesse F = 4q/(1-q)^2 (Sanchez-Soto et al., Eqs. (3.1)-(3.2), with r^2 = q).
#   2. B has an interior maximum on (0, pi/2) iff F > 1 iff q > 3 - 2 sqrt 2, and (3 - 2 sqrt 2)^2 = 17 - 12 sqrt 2
#      is the reflectivity product at which the Airy FWHM breaks down (Pollnau-Eichhorn, Eq. (118)).
#   3. The Airy transmission is a sum of Lorentzians,
#      (1-q)^2/(1+q^2-2q cos 2phi) = (1-q)/(1+q) sum_m a/((phi-m pi)^2+a^2), whose half-width a = (1/2) ln(1/q) is
#      the pole distance of Eq. (16) (Sanchez-Soto et al., Eq. (3.7); Pollnau-Eichhorn, Eqs. (99)-(108)). The sum
#      over all m is evaluated by mpmath's nsum (series acceleration).
#   4. The Lorentzian linewidth equals the free spectral range, 2a = pi, at q = e^{-pi} (Pollnau-Eichhorn, Eq. (114),
#      R1 R2 = e^{-2 pi}).
#   5. A pole smeared over a one-sided spread of round-trip phase with a density that is finite at the edge (the
#      paraxial Gaussian beam of the angular Airy function, Marques et al. Eq. (3)) has coefficients
#      c_k = w^k [1 + b s0/(1 + 2iks0)], and |r_{k+1} - r_k| falls like k^-3 (r_k = c_{k+1}/c_k).
#   6. A spread of round-trip loss with a density that vanishes linearly at the edge has c_k = w^k [1 + b/((k+1)(k+2))],
#      and |r_{k+1} - r_k| falls like k^-4, the law EEG_PROFILE.md 8.5 reads from the tuned profile.
#   The exponents are measured between k = 200 and 400 and must be within 0.05 of 3 and 4.
# Any command-line argument applies a mutation: q -> -q in 1, F -> F/2 in 2, a -> 2a in 3, pi -> pi/2 in 4, the
# linear-edge density in 5 and the finite-edge density in 6, so every check must then fail. Run: python3 identity_check.py [mutate]   (mpmath; exit 0 when all pass)
import sys
import mpmath as mp

mp.mp.dps = 30
mut = len(sys.argv) > 1
ok = []


def B(t, q):
    return mp.re(mp.exp(1j * t) / (1 + q * mp.exp(2j * t)))


def airy(phi, F):
    return 1 / (1 + F * mp.sin(phi) ** 2)


# 1. the delta = 0 profile is the single-pass carrier times the Airy distribution
q = mp.mpf('0.0551')
F = 4 * q / (1 - q) ** 2
qq = -q if mut else q
d1 = max(abs(B(mp.mpf(j) / 7, q) - (1 + qq) / (1 - qq) ** 2 * mp.cos(mp.mpf(j) / 7)
             * airy(mp.mpf(j) / 7 + mp.pi / 2, 4 * qq / (1 - qq) ** 2)) for j in range(-20, 21))
ok.append(d1 < mp.mpf('1e-25'))
print(f"1. B = (1+q)/(1-q)^2 cos t A(t+pi/2):       max deviation {mp.nstr(d1, 3)}")


# 2. the hump threshold of the delta = 0 profile is F = 1, q = 3 - 2 sqrt 2
def has_interior_max(q, Fscale):
    # The claimed criterion. B = (1+q)/(1-q)^2 c/(1 + F c^2) with c = cos t has dB/dc = (1 - F)/(1+F)^2 at c = 1.
    return Fscale * 4 * q / (1 - q) ** 2 > 1


qc = 3 - 2 * mp.sqrt(2)
d2a = abs(qc ** 2 - (17 - 12 * mp.sqrt(2)))
fs = mp.mpf('0.5') if mut else 1
tests = []
for qt in [qc * mp.mpf('0.98'), qc * mp.mpf('1.02'), mp.mpf('0.0551'), mp.mpf('0.3')]:
    # dB/dt > 0 just right of t = 0 means t = 0 is a local minimum, so the maximum is interior.
    numeric = mp.diff(lambda t: B(t, qt), mp.mpf('1e-3')) > 0
    tests.append(numeric == has_interior_max(qt, fs))
ok.append(d2a < mp.mpf('1e-25') and all(tests))
print(f"2. interior maximum iff F > 1 (q_c = {mp.nstr(qc, 8)}); (3-2sqrt2)^2 - (17-12sqrt2) = {mp.nstr(d2a, 3)};"
      f" sign tests {tests}")

# 3. the Airy distribution is the sum of Lorentzians whose half-width is the pole distance of Eq. (16)
a = mp.log(1 / q) / 2
aa = 2 * a if mut else a
d3 = 0
for j in range(-10, 11):
    phi = mp.mpf(j) / 9
    lhs = (1 - q) ** 2 / (1 + q ** 2 - 2 * q * mp.cos(2 * phi))
    s = mp.nsum(lambda m: aa / ((phi - m * mp.pi) ** 2 + aa ** 2), [-mp.inf, mp.inf])
    d3 = max(d3, abs(lhs - (1 - q) / (1 + q) * s))
ok.append(d3 < mp.mpf('1e-20'))
print(f"3. Airy = (1-q)/(1+q) sum of Lorentzians, a = {mp.nstr(a, 8)}: max deviation {mp.nstr(d3, 3)}")

# 4. Lorentzian linewidth = free spectral range at q = e^{-pi}
pp = mp.pi / 2 if mut else mp.pi
qL = mp.exp(-pp)
d4 = abs(mp.log(1 / qL) - mp.pi)
ok.append(d4 < mp.mpf('1e-25'))
print(f"4. 2a = pi at q = e^(-pi) = {mp.nstr(mp.exp(-mp.pi), 8)}: deviation {mp.nstr(d4, 3)}")
print(f"   Eq. (16) at the paper's q = 0.0551: F = {mp.nstr(F, 6)}, 2a = {mp.nstr(2 * a, 6)},"
      f" Lorentzian finesse pi/(2a) = {mp.nstr(mp.pi / (2 * a), 6)}")



# 5, 6. the decay of the ratio differences for a pole smeared by a one-sided spread
def exponent(c):
    def d(k):
        return abs(c(k + 2) / c(k + 1) - c(k + 1) / c(k))
    return -mp.log(d(400) / d(200)) / mp.log(2)


w = mp.mpf('0.0551') * mp.exp(1j * mp.mpf('0.0985'))
s0, b = mp.mpf('0.5'), mp.mpf('0.3')
finite_edge = lambda k: w ** k * (1 + b * s0 / (1 + 2j * k * s0))
linear_phase = lambda k: w ** k * (1 + b * s0 ** 2 / (1 + 2j * k * s0) ** 2)
linear_loss = lambda k: w ** k * (1 + b / ((k + 1) * (k + 2)))
finite_loss = lambda k: w ** k * (1 + b / (k + 1))
p5 = exponent(linear_phase if mut else finite_edge)
p6 = exponent(finite_loss if mut else linear_loss)
pl = exponent(linear_phase)
ok.append(abs(p5 - 3) < mp.mpf('0.05'))
ok.append(abs(p6 - 4) < mp.mpf('0.05'))
print(f"5. phase spread, finite-edge density: |r_(k+1) - r_k| ~ k^-{mp.nstr(p5, 5)} (expected 3)")
print(f"6. loss spread, linear-edge density:  |r_(k+1) - r_k| ~ k^-{mp.nstr(p6, 5)} (expected 4);"
      f" phase spread with a linear edge gives k^-{mp.nstr(pl, 5)}")

print("all pass" if all(ok) else f"FAIL {ok}")
sys.exit(0 if all(ok) else 1)
