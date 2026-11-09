# Checks of six relations that tie the #200 addendum's sources to this project (inferred, not quoted from a source,
# except where a source's own equations are checked against each other).
#   1. Kol's double-cone exponents (hep-th/0502033, Eq. 2.5), s+- = ((D-2)/2)(-1 +- i sqrt(8/(D-2) - 1)), are the roots
#      of s^2 + (D-2)s + 2(D-2) = 0. That is Kaplan-Lee-Son-Stephanov's 1/r^2 indicial form (arXiv:0905.4752, Eq. 12),
#      nu+- = -(d-2)/2 +- sqrt(alpha - alpha*), with d = D, alpha = -2(D-2), alpha* = -(D-2)^2/4, so that
#      alpha - alpha* = (D-2)(D-10)/4 and the fixed points merge at D* = 10. Kol's Eqs. (3.19)-(3.21) follow from
#      Eq. (3.16), -1/s = gamma(1 +- 2 pi i/Delta).
#   2. Kol's merger exponent at large D: lambda = -s+ = 2 + 4/n + 16/n^2 + O(n^-3), n = D - 2, so gamma -> 1/2 there
#      too, with a 1/n coefficient 4 against this project's 3.0324 (README, Proposition 5; numerical evidence).
#   3. Emparan-Herzog's fits (RMP 92, 045005, Sec. X.3), gamma ~ (1 - 1/D)/2 and (1 - 1/(D+1))/2, against this
#      project's double-double values (README, Values) at D = 20, 30, 40, 50, 60: both fits miss by more than 1e-3,
#      and their large-D deficit 1/(2D) is 0.66 of the project's 0.758/(D-2).
#   4. LeClair-Roman-Sierra (cond-mat/0211338, Eqs. 15-17): dg/ds = g^2 + theta^2 blows up at points spaced by the
#      period pi/theta, found here by integrating the flow; the gaps Delta_n = omega/sinh(t0 + n pi/theta) (Eq. 10)
#      have the ratio Delta_{n+1}/Delta_n -> e^{-pi/theta}; and theta -> 0 gives Delta_0 -> 2 omega e^{-1/g}.
#   5. Larkin-Varlamov (cond-mat/0109177): the TDGL propagator's pole (Eqs. 106, 108, gamma_GL = pi alpha/8) gives the
#      rate 8(T - Tc)/pi, the inverse of Eq. (2)'s tau_GL; below Tc the q = 0 mode grows at 8(Tc - T)/pi, a rate that
#      vanishes linearly at the threshold.
#   6. The inner equations of Proposition 5(i) with c = 1, Y_t = S, S_t = Y_s + Y^3/4, are Y_s = Y_tt - Y^3/4, the
#      gradient flow of F = int (Y_t^2/2 + Y^4/16) dt: the massless phi^4 (Ginzburg-Landau) flow, with s the flow time.
#      Under (t, s, Y) -> (a t, a^2 s, Y/a) a mass term -r Y is invariant iff r -> r/a^2, the weight of the s-shift.
# Any command-line argument applies a mutation: 8 -> 9 in Eq. (2.5), the project's coefficient in place of Kol's,
# the project's own fit in place of Emparan-Herzog's, theta^2 dropped from the flow, gamma_GL -> 2 gamma_GL, and the
# quartic 1/16 -> 1/8, so every check must then fail.
# Run: python3 -I identity_check.py [mutate]   (mpmath, sympy; exit 0 when all pass, 1 otherwise)
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
mut = len(sys.argv) > 1
ok = []

# 1. Kol's exponents are the conformality-lost indicial form with D* = 10.
eight = 9 if mut else 8
d1 = mp.mpf(0)
for D in [mp.mpf(x) for x in ('4', '5.5', '7', '9.9', '10.1', '12', '30', '200')]:
    n = D - 2
    sk = [n / 2 * (-1 + sgn * 1j * mp.sqrt(mp.mpc(eight / n - 1))) for sgn in (1, -1)]  # Eq. (2.5)
    alpha, alpha_s = -2 * n, -n ** 2 / 4
    nu = [-n / 2 + sgn * mp.sqrt(mp.mpc(alpha - alpha_s)) for sgn in (1, -1)]  # Eq. (12) of Kaplan et al.
    key = lambda z: (mp.nint(mp.im(z) * 10 ** 12), mp.re(z))  # noqa: E731
    d1 = max(d1, max(abs(a - b) for a, b in zip(sorted(sk, key=key), sorted(nu, key=key))))
    d1 = max(d1, abs((alpha - alpha_s) - n * (D - 10) / 4))
    s = max(sk, key=lambda z: mp.re(z))  # s+, the root leading at large rho when both are real
    if D < 10:  # Eqs. (3.16)-(3.20)
        g, two_pi_over_delta = -mp.re(1 / s), mp.im(1 / s) / mp.re(1 / s)
        d1 = max(d1, abs(g - mp.mpf(1) / 4), abs(abs(two_pi_over_delta) - mp.sqrt((10 - D) / (D - 2))))
    else:  # Eq. (3.21)
        d1 = max(d1, abs(mp.im(s)), abs(-1 / mp.re(s) - (1 + mp.sqrt((D - 10) / (D - 2))) / 4))
ok.append(d1 < mp.mpf('1e-25'))
print(f"1. Kol (2.5) = Kaplan et al. (12), D* = 10:      max deviation {mp.nstr(d1, 3)}")

# 2. The merger's lambda = -s+ at large n: 2 + 4/n + 16/n^2.
c1_claim = mp.mpf('3.0324') if mut else 4


def lam_kol(n):
    return n / 2 * (1 - mp.sqrt(1 - 8 / n))


ns = [mp.mpf(10) ** k for k in (6, 7, 8)]
c1 = [(lam_kol(n) - 2) * n for n in ns]
c2 = [((lam_kol(n) - 2) * n - 4) * n for n in ns]
d2 = max(max(abs(c - c1_claim) for c in c1), max(abs(c - 16) for c in c2) * mp.mpf('1e-4'))
ok.append(d2 < mp.mpf('1e-3'))
print(f"2. Kol: lambda = 2 + 4/n + 16/n^2 + ...:          1/n coefficient {mp.nstr(c1[-1], 8)}, "
      f"1/n^2 {mp.nstr(c2[-1], 6)}, deviation {mp.nstr(d2, 3)}")

# 3. Emparan-Herzog's gamma fits against the project's values (README, Values table).
vals = {20: '0.4737106', 30: '0.48079268', 40: '0.484776464', 50: '0.487364941', 60: '0.4891910657'}


def proj_fit(D):
    # The project's leading behaviour with one more term fitted to D = 60 (used only as the mutation).
    n = mp.mpf(D) - 2
    c2 = (mp.mpf(vals[60]) - (mp.mpf(1) / 2 - mp.mpf('0.7581') / 58)) * 58 ** 2
    return mp.mpf(1) / 2 - mp.mpf('0.7581') / n + c2 / n ** 2


miss = []
for D, g in vals.items():
    fa = proj_fit(D) if mut else (1 - mp.mpf(1) / D) / 2
    fb = proj_fit(D) if mut else (1 - mp.mpf(1) / (D + 1)) / 2
    miss.append(min(abs(fa - mp.mpf(g)), abs(fb - mp.mpf(g))))
ratio = (mp.mpf(1) / 2) / mp.mpf('0.7581')
ok.append(min(miss) > mp.mpf('1e-3'))
print(f"3. Emparan-Herzog fits vs README values, D 20-60: smallest miss {mp.nstr(min(miss), 3)} "
      f"(must exceed 1e-3); deficit ratio 0.5/0.7581 = {mp.nstr(ratio, 4)}")

# 4. The Russian-doll flow: blow-ups spaced by pi/theta, gap ratio e^{-pi/theta}, the BCS limit.
theta, g0 = mp.mpf('0.3'), mp.mpf('0.2')


def beta(g):
    return g ** 2 + (0 if mut else theta ** 2)  # Eq. (15); the mutation drops theta^2


def blowups(count):
    # Integrate the flow in the angle phi = atan(g/theta), which stays regular where g has a pole:
    # dphi/ds = theta beta(g)/(theta^2 + g^2) with g = theta tan(phi). The poles of g are the crossings of phi through
    # pi/2 + k pi, located by bisection on the integrated phi. Without theta^2 in beta, phi tends to pi after the first
    # pole and never reaches 3 pi/2, so the second crossing is not found within the search window.
    def f(s, y):
        g = theta * mp.tan(y[0])
        return [theta * beta(g) * mp.cos(y[0]) ** 2 / theta ** 2]

    sol = mp.odefun(f, 0, [mp.atan(g0 / theta)])
    out, k, smax = [], 0, 3 * count * mp.pi / theta
    while len(out) < count:
        target = mp.pi / 2 + k * mp.pi
        lo, hi = (out[-1] if out else mp.mpf(0)), (out[-1] if out else mp.mpf(0)) + mp.mpf(1)
        while sol(hi)[0] < target:
            lo, hi = hi, hi + 1
            if hi > smax:
                return out
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if sol(mid)[0] < target else (lo, mid)
        out.append((lo + hi) / 2)
        k += 1
    return out


mp.mp.dps = 20  # the ODE integration only needs a modest precision
bs = blowups(2)
mp.mp.dps = 30
d4a = abs(bs[1] - bs[0] - mp.pi / theta) if len(bs) > 1 else mp.inf
# Check that the integrated angle reproduces Eq. (16), g = theta tan(theta s + atan(g0/theta)), at a sample point.
s_test = mp.mpf('0.7')
g_eq16 = theta * mp.tan(theta * s_test + mp.atan(g0 / theta))
h = mp.mpf('1e-8')
g_dot = (theta * mp.tan(theta * (s_test + h) + mp.atan(g0 / theta)) - g_eq16) / h
d4b = abs(g_dot - (g_eq16 ** 2 + theta ** 2)) / abs(g_dot)
t0 = mp.atan(theta / g0) / theta  # Eq. (11): tan(theta t0) = theta/g, 0 < t0 < pi/(2 theta)
omega = 1
gaps = [omega / mp.sinh(t0 + k * mp.pi / theta) for k in range(4)]
d4c = abs(gaps[3] / gaps[2] - mp.exp(-mp.pi / theta)) / mp.exp(-mp.pi / theta)
gs = mp.mpf('0.05')
th_small = mp.mpf('1e-6')
t0s = mp.atan(th_small / gs) / th_small
d4d = abs(omega / mp.sinh(t0s) / (2 * omega * mp.exp(-1 / gs)) - 1)
ok.append(d4a < mp.mpf('1e-10') and d4b < mp.mpf('1e-6') and d4c < mp.mpf('1e-10') and d4d < mp.mpf('1e-6'))
print(f"4. LeClair et al.: pole spacing - pi/theta {mp.nstr(d4a, 3)}; Eq. (16) residual {mp.nstr(d4b, 3)}; "
      f"gap ratio {mp.nstr(d4c, 3)}; BCS limit {mp.nstr(d4d, 3)}")

# 5. TDGL: the pole of L(0, Omega) = 1/(-i gamma_GL Omega + eps_0) is at Omega = -i eps_0/gamma_GL.
alpha, Tc = mp.mpf('1.7'), mp.mpf('2.3')
gam = (2 if mut else 1) * mp.pi * alpha / 8
d5 = mp.mpf(0)
for T in (Tc * mp.mpf('1.01'), Tc * mp.mpf('1.2'), Tc * mp.mpf('0.95')):
    eps0 = alpha * Tc * (T - Tc) / Tc
    Om = mp.findroot(lambda w: -1j * gam * w + eps0, mp.mpc(0, -1))
    rate = -mp.im(Om)  # decay rate above Tc, minus the growth rate below
    d5 = max(d5, abs(rate - 8 * (T - Tc) / mp.pi))
    if T > Tc:
        d5 = max(d5, abs(1 / rate - mp.pi / (8 * (T - Tc))))  # Eq. (2), hbar = k_B = 1
ok.append(d5 < mp.mpf('1e-20'))
print(f"5. Larkin-Varlamov: pole rate = 8(T - Tc)/pi:     max deviation {mp.nstr(d5, 3)}")

# 6. The c = 1 heat form is the massless phi^4 gradient flow; the mass and the s-shift both have weight 2.
t, s, a, r, s0 = sp.symbols('t s a r s0', positive=True)
Y = sp.Function('Y')
q4 = sp.Rational(1, 8) if mut else sp.Rational(1, 16)
Sfun = sp.diff(Y(s, t), t)  # Y_t = c S with c = 1
eq_heat = sp.diff(Sfun, t) - (sp.diff(Y(s, t), s) + Y(s, t) ** 3 / 4)  # S_t - (Y_s + Y^3/4) = 0
Ys_from_heat = sp.solve(eq_heat, sp.diff(Y(s, t), s))[0]
Lag = sp.diff(Y(s, t), t) ** 2 / 2 + q4 * Y(s, t) ** 4
dF = sp.diff(Lag, Y(s, t)) - sp.diff(sp.diff(Lag, sp.diff(Y(s, t), t)), t)  # functional derivative dF/dY
d6a = sp.simplify(Ys_from_heat - (-dF))
# Scaling: Ytilde(s, t) = y(s/a^2, t/a)/a. With y0, ys, ytt the values of y, y_sigma and y_tautau at
# (sigma, tau) = (s/a^2, t/a), the chain rule gives Ytilde_s = ys/a^3 and Ytilde_tt = ytt/a^3. Ytilde solves
# Y_s = Y_tt - Y^3/4 - r' Y, given that y solves it with r, iff r' = r/a^2. The quartic of the flow sets the cubic.
y0, ytt, rp = sp.symbols('y0 ytt rp')
cubic = 4 * q4 * 4  # 1 when the quartic is Y^4/16, the coefficient of Y^3/4 in -dF/dY
ys = ytt - cubic * y0 ** 3 / 4 - r * y0  # the unscaled equation
res = ys / a ** 3 - (ytt / a ** 3 - (y0 / a) ** 3 / 4 - rp * y0 / a)
rsol = sp.solve(sp.simplify(res), rp)
d6b = sp.simplify(rsol[0] - r / a ** 2) if rsol else 1
# The s-shift: Ytilde(s + s0, t) rescaled is y(s/a^2 + s0/a^2, t/a)/a, so s0 -> a^2 s0, the inverse weight of r.
d6b = d6b if d6b != 0 else sp.simplify((a ** 2 * s0) * (r / a ** 2) - s0 * r)
ok.append(d6a == 0 and d6b == 0)
print(f"6. heat form = massless phi^4 flow; r -> r/a^2:   residuals {d6a}, {d6b}")

print("all pass" if all(ok) else f"FAIL: {[i + 1 for i, x in enumerate(ok) if not x]}")
sys.exit(0 if all(ok) else 1)
