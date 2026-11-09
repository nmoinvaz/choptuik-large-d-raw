# Check of the relations that tie Pollnau-Eichhorn (Prog. Quantum Electron. 72, 100255 (2020), "PE") and Ismail et al.
# (Opt. Express 24, 16366 (2016)) to Eq. (16) of arXiv:2611.07007, beta(t) = A* Re[1/(e^{-it} + w e^{it})], w = q e^{i d}.
# The relations are inferred, not quoted from a source. sigma = (1/2) ln(1/q) is Eq. (16)'s pole distance.
#   1. Mittag-Leffler at two levels. PE Eqs. (99)-(108) sum same-sign absorptive Lorentzians (cot, Eq. (100)) to the
#      Airy distribution. The field-level counterpart sums alternating complex Lorentzians (csc). With phi = t + d/2,
#        beta = A*/(2 sqrt q) Re[e^{-id/2} sec(phi + i sigma)]
#             = A*/(2 sqrt q) sum_k (-1)^(k+1) [cos(d/2)(phi - c_k) - sin(d/2) sigma] / ((phi - c_k)^2 + sigma^2),
#      c_k = (k + 1/2) pi, so each pole pair is a dispersive Lorentzian rotated toward an absorptive one by d/2. The FP
#      field t1 t2 e^{-i x}/(1 - rho e^{-2ix}) is (t1 t2/(2i sqrt rho)) sum_q (-1)^q/(x - pi q - i sigma) likewise,
#      and the coherent field sum has the Airy shape too: |sum_q (-1)^q/(x - pi q - i sigma)|^2 equals
#      (2 sigma/sinh 2 sigma) sum_q 1/((x - pi q)^2 + sigma^2), so the cross terms add a constant factor, not zero.
#   2. The norm. <beta^2> = (A*^2/2) A_circ,FSR with R1 R2 e^{-2 alpha l} = q^2 (PE Eq. (62)), = A*^2/(2(1 - q^2)),
#      EEG's (S60), for every d.
#   3. Reading check of PE Eqs. (114), (117), (118): Delta nu_Airy/Delta nu_c = 1.001, 1.022, 1.132, 1.717 at
#      R1 = R2 = 0.9, 0.6, 0.32, 0.172 (PE Fig. 12 caption), e^{-2 pi} = 0.001867 and R = 4.32% (Eq. (114)),
#      17 - 12 sqrt 2 = 0.02944 and R = 17.2% (Eq. (118)).
#   4. The hump threshold equals the Airy breakdown only at d = 0. The Airy factor 1/D_q has min/max ((1-q)/(1+q))^2
#      for every d, so its half-maximum breakdown stays at q = 3 - 2 sqrt 2. The profile's hump threshold q_c(d) is the
#      double zero of d beta/dt, 3 - 2 sqrt 2 at d = 0 and larger at EEG's d = 0.0985.
#   5. The one-zero [1/1] form is PE's two-path reflection, Eq. (91). (1 + b u)/(1 + w u) = b/w + (1 - b/w)/(1 + w u),
#      a direct path of weight b/w plus a round-trip train. PE's reflection (r1 - r2' u)/(1 - r1 r2' u) has
#      b/w = 1/R1 >= 1. The tuned D = infinity profile's [1/1] (EEG_PROFILE.md 3.3: w = r_3, b = r_3 - r_1) has
#      |b/w| = 0.042, so it is not a passive reflection (conditional on Conjecture 1, which the tuned profile assumes).
#   6. Gain moves the pole. With round-trip amplitude rho_L = rho_c e^{g l}, PE's spectral-coherence factor
#      Lambda = 1/(1 - c g tau_c) (Eq. (146)) is the ratio of pole distances sigma_c/sigma_L, and threshold
#      (Lambda -> infinity) is rho_L -> 1, Eq. (16)'s q -> 1.
# Any command-line argument applies a mutation to each item: the (-1)^k dropped in 1, R1 R2 = q in 2, sqrt(R1 R2) -> R1 R2
# in the arcsin of 3, d = 0 in the threshold search of 4, b and w swapped in 5, the intensity gain e^{2 g l} in
# place of the amplitude gain e^{g l} in 6. Every check must then fail.   Run: python3 identity_check.py [mutate]   (mpmath; exit 0 when all pass)
import sys
import mpmath as mp

mp.mp.dps = 30
mut = len(sys.argv) > 1
ok = []


def beta(t, q, d, A=1):
    return A * mp.re(1 / (mp.exp(-1j * t) + q * mp.exp(1j * d) * mp.exp(1j * t)))


# 1. Mittag-Leffler at the field level (csc/sec), against PE's intensity level (cot)
q, d = mp.mpf('0.0551'), mp.mpf('0.0985')
sig = mp.log(1 / q) / 2


def ml_sum(t, q, d, alt=True):
    phi, s = t + d / 2, mp.log(1 / q) / 2
    term = lambda k: ((-1) ** (int(k) + 1) if alt else -1) * (mp.cos(d / 2) * (phi - (k + mp.mpf(1) / 2) * mp.pi)
                                                             - mp.sin(d / 2) * s) / ((phi - (k + mp.mpf(1) / 2) * mp.pi) ** 2 + s ** 2)
    # symmetric partial sums pair k with -k-1; nsum accelerates them
    pair = lambda m: term(m) + term(-m - 1)
    return mp.nsum(pair, [0, mp.inf]) / (2 * mp.sqrt(q))


ts = [mp.mpf(j) / 5 for j in range(-8, 9)]
d1a = max(abs(beta(t, q, d) - mp.re(mp.exp(-1j * d / 2) * mp.sec(t + d / 2 + 1j * sig)) / (2 * mp.sqrt(q))) for t in ts)
d1b = max(abs(beta(t, q, d) - ml_sum(t, q, d, alt=not mut)) for t in ts)
rho = mp.mpf('0.3')
sr = mp.log(1 / rho) / 2
ft = lambda x: mp.exp(-1j * x) / (1 - rho * mp.exp(-2j * x))
sgn = lambda m: 1 if mut else (-1) ** int(m)
fs = lambda x: (1 / (x - 1j * sr) + mp.nsum(lambda m: sgn(m) * (1 / (x - mp.pi * m - 1j * sr)
                                                                + 1 / (x + mp.pi * m - 1j * sr)), [1, mp.inf])) \
    / (2j * mp.sqrt(rho))
d1c = max(abs(ft(x) - fs(x)) for x in [mp.mpf(j) / 7 for j in range(-5, 6)])
# PE Eq. (101)/(108) for comparison: same-sign absorptive Lorentzians give the Airy distribution exactly
airy = lambda x: (1 - rho ** 2) / ((1 - rho) ** 2 + 4 * rho * mp.sin(x) ** 2)
lor = lambda x: mp.nsum(lambda m: (2 * sr) / ((2 * sr) ** 2 + (2 * x - 2 * mp.pi * m) ** 2), [-mp.inf, mp.inf]) * 2
d1d = max(abs(airy(x) - lor(x)) for x in [mp.mpf(j) / 7 for j in range(-5, 6)])
# the coherent sum of the alternating field terms against the incoherent sum of their intensities
d1e = max(abs(abs(fs(x) * 2j * mp.sqrt(rho)) ** 2 - 2 * lor(x) / mp.sinh(2 * sr)) for x in [mp.mpf(j) / 7 for j in range(-5, 6)])
ok.append(d1a < mp.mpf('1e-25') and d1b < mp.mpf('1e-20') and d1c < mp.mpf('1e-20') and d1d < mp.mpf('1e-20')
          and d1e < mp.mpf('1e-20'))
print(f"1. sec form {mp.nstr(d1a, 3)}; alternating pole-pair sum {mp.nstr(d1b, 3)}; FP field as csc sum"
      f" {mp.nstr(d1c, 3)}; PE Eq. (108) cot sum {mp.nstr(d1d, 3)}; coherent/incoherent factor {mp.nstr(d1e, 3)}")

# 2. the norm is the FSR-integrated generic Airy distribution, PE Eq. (62)
A = mp.mpf('3.8455')
msq = mp.quad(lambda t: beta(t, q, d, A) ** 2, [0, mp.pi / 2, mp.pi, 3 * mp.pi / 2, 2 * mp.pi]) / (2 * mp.pi)
RR = q if mut else q ** 2
acirc_fsr = mp.quad(lambda x: 1 / ((1 - mp.sqrt(RR)) ** 2 + 4 * mp.sqrt(RR) * mp.sin(x) ** 2), [-mp.pi / 2, mp.pi / 2]) / mp.pi
d2 = max(abs(msq - A ** 2 / 2 * acirc_fsr), abs(acirc_fsr - 1 / (1 - RR)), abs(msq - A ** 2 / (2 * (1 - q ** 2))))
ok.append(d2 < mp.mpf('1e-20'))
print(f"2. <beta^2> = (A*^2/2) A_circ,FSR(R1R2 = q^2) = A*^2/(2(1-q^2)): {mp.nstr(msq, 10)}, max deviation {mp.nstr(d2, 3)}")


# 3. reading check of PE Eqs. (114), (117), (118)
def ratio117(R):
    rr = R * R  # R1 = R2 = R
    s = rr if mut else mp.sqrt(rr)
    return 4 * mp.asin((1 - s) / (2 * mp.sqrt(s))) / (-mp.log(rr))


quoted = [('0.9', '1.001'), ('0.6', '1.022'), ('0.32', '1.132'), ('0.172', '1.717')]
got = [(R, mp.nstr(ratio117(mp.mpf(R)), 4)) for R, _ in quoted]
c3 = all(g == v for (_, g), (_, v) in zip(got, quoted))
c3 = c3 and mp.nstr(mp.exp(-2 * mp.pi), 4) == '0.001867' and mp.nstr(100 * mp.exp(-mp.pi), 3) == '4.32'
c3 = c3 and mp.nstr(17 - 12 * mp.sqrt(2), 4) == '0.02944' and mp.nstr(100 * (3 - 2 * mp.sqrt(2)), 3) == '17.2'
ok.append(c3)
print(f"3. Eq. (117) at R = 0.9, 0.6, 0.32, 0.172: {[g for _, g in got]} (PE Fig. 12: 1.001, 1.022, 1.132, 1.717);"
      f" e^(-2pi) = {mp.nstr(mp.exp(-2 * mp.pi), 4)}, 17-12sqrt2 = {mp.nstr(17 - 12 * mp.sqrt(2), 4)}")


# 4. hump threshold q_c(d) against the Airy half-maximum breakdown
def dbeta(t, q, d):
    return mp.diff(lambda x: beta(x, q, d), t)


def hump_threshold(d, guess):
    # q_c: d beta/dt has a double zero at some t, so solve d beta/dt = d2 beta/dt2 = 0 for (t, q)
    f = lambda t, qq: [mp.diff(lambda x: beta(x, qq, d), t, 1), mp.diff(lambda x: beta(x, qq, d), t, 2)]
    t0, q0 = mp.findroot(f, guess)
    return q0, t0


qc0, _ = hump_threshold(mp.mpf(0), (mp.mpf('0.0'), mp.mpf('0.17')))
dd = mp.mpf(0) if mut else d
qcd, tcd = hump_threshold(dd, (mp.mpf('0.0'), mp.mpf('0.17')) if mut else (mp.mpf('-0.357'), mp.mpf('0.2133')))
airy_ratio = lambda q, d: (min(1 / (1 + q * q + 2 * q * mp.cos(2 * t + d)) for t in [0, mp.pi / 2 - d / 2, -d / 2])
                           / max(1 / (1 + q * q + 2 * q * mp.cos(2 * t + d)) for t in [0, mp.pi / 2 - d / 2, -d / 2]))
qa = 3 - 2 * mp.sqrt(2)
c4 = abs(qc0 - qa) < mp.mpf('1e-15') and abs(airy_ratio(qa, d) - mp.mpf(1) / 2) < mp.mpf('1e-25') \
    and abs(airy_ratio(qa, 0) - mp.mpf(1) / 2) < mp.mpf('1e-25') and qcd - qa > mp.mpf('0.03')
ok.append(c4)
print(f"4. q_c(0) = {mp.nstr(qc0, 12)} (3-2sqrt2 = {mp.nstr(qa, 12)}); q_c({mp.nstr(dd, 4)}) = {mp.nstr(qcd, 8)}"
      f" at t = {mp.nstr(tcd, 6)}; Airy min/max at 3-2sqrt2 is 1/2 for d = 0 and d = 0.0985")

# 5. the [1/1] form as PE's two-path reflection, Eq. (91)
r1 = mp.mpf('0.055085') * mp.exp(1j * mp.mpf('0.09879'))
r3 = mp.mpf('0.057203') * mp.exp(1j * mp.mpf('0.07881'))
w, b = (r3 - r1, r3) if mut else (r3, r3 - r1)
u = mp.mpf('0.4') * mp.exp(0.7j)
d5a = abs((1 + b * u) / (1 + w * u) - (b / w + (1 - b / w) / (1 + w * u)))
R1, r2p = mp.mpf('0.6'), mp.mpf('0.7')
bw_pe = (-r2p / mp.sqrt(R1)) / (-mp.sqrt(R1) * r2p)
c5 = d5a < mp.mpf('1e-25') and abs(bw_pe - 1 / R1) < mp.mpf('1e-25') and abs(b / w) < 1
ok.append(c5)
print(f"5. two-path identity {mp.nstr(d5a, 3)}; PE reflection b/w = 1/R1 = {mp.nstr(bw_pe, 6)} (R1 = 0.6);"
      f" tuned [1/1]: |b| = {mp.nstr(abs(b), 4)}, |b/w| = {mp.nstr(abs(b / w), 4)}, arg(b/w) = {mp.nstr(mp.arg(b / w), 4)}")

# 6. gain moves the pole: Lambda = sigma_c / sigma_L, threshold at rho_L = 1
rho_c, gl = mp.mpf('0.8'), mp.mpf('0.15')  # round-trip amplitude factor and single-pass amplitude gain g*l
tRT_over_tauc = -2 * mp.log(rho_c)  # PE Eq. (23): t_RT/tau_c = -ln(R1 R2 (1-L)) = -2 ln rho_c
cg_tRT = 2 * gl  # c g t_RT = 2 g l
Lam = 1 / (1 - cg_tRT / tRT_over_tauc)  # PE Eq. (146)
rho_L = rho_c * mp.exp(2 * gl if mut else gl)  # the mutation applies the intensity gain to the amplitude
sig_ratio = mp.log(1 / rho_c) / mp.log(1 / rho_L)
gl_th = -mp.log(rho_c)  # gain at which rho_L = 1
Lam_near = 1 / (1 - 2 * (gl_th * (1 - mp.mpf('1e-12'))) / tRT_over_tauc)
c6 = abs(Lam - sig_ratio) < mp.mpf('1e-25') and Lam_near > mp.mpf('1e11')
ok.append(c6)
print(f"6. Lambda = {mp.nstr(Lam, 10)}, sigma_c/sigma_L = {mp.nstr(sig_ratio, 10)}; Lambda at 1 - 1e-12 of threshold"
      f" gain = {mp.nstr(Lam_near, 4)}")

print("all pass" if all(ok) else f"FAIL {ok}")
sys.exit(0 if all(ok) else 1)
