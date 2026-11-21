"""#966: the exponent of a real singularity behind a nearer conjugate pair, on a conformally mapped series. Protocol
fixed in I966-mac-sing/README.md (2026-11-21 14:57:55 UTC) before any planted or real run.
    python confmap.py unit CODE                          a code test: one square-root point, no pair (not the protocol)
    python confmap.py scan CODE AMP.json                 the planted check (exit 0 pass, 2 not resolved)
    python confmap.py real CODE JET.npz LOCATE.json      the mapped estimator on Delta's series at a base
CODE: the folder with singularity_type.py and jet_singularity.py (main 607c1df3) and subdom.py.
Map: h = phi(w) = c + R (w - a)/(1 - a w), R = s2 - c, a = c/R: the unit disk onto |h - c| < R, 0 -> 0, 1 -> s2. c on a
grid of 0.001 maximizes min(|w(s1)|, |w(P2)|, 1/a). The series d_k of f(phi(w)) follows from c_1..c_N exactly
(phi(0) = 0); singularity_type.dlog_fit on d gives w* and mu, and s = phi(w*). A Moebius (Euler-type) map of the
series' variable; the exponent is unchanged by a conformal map."""
import json
import sys

import mpmath as mp

DPS = 60
P2_ABS = complex(258.3606, 2.2688)


def choose_c(s1, s2, p2):
    def w_of(h, c):
        R = s2 - c
        a = c / R
        u = (h - c) / R
        return (u + a) / (1 + a * u)
    best = None
    i = 1
    while True:
        c = i * 0.001
        R = s2 - c
        if c >= R:
            break
        m = min(abs(w_of(s1, c)), abs(w_of(p2, c)), R / c)
        if best is None or m > best[1]:
            best = (c, m, abs(w_of(s1, c)), abs(w_of(p2, c)), R / c)
        i += 1
    return best


def phi_series(c, s2, N):
    """coefficients phi_1..phi_N of phi(w) = c + R (w - a)/(1 - a w) (phi_0 = 0)"""
    c, s2 = mp.mpf(c), mp.mpf(s2)
    R = s2 - c
    a = c / R
    # (w - a)/(1 - a w) = -a + sum_{k>=1} (1 - a^2) a^(k-1) w^k
    return [mp.mpf(0)] + [R * (1 - a * a) * a ** (k - 1) for k in range(1, N + 1)]


def phi(w, c, s2):
    R = s2 - c
    a = c / R
    return c + R * (w - a) / (1 - a * w)


def compose(cs, ph):
    """d_1..d_N of f(phi(w)) with f = sum_k c_k h^k (cs = c_1..c_N), phi = ph (ph[0] = 0)"""
    N = len(cs)
    d = [mp.mpf(0)] * (N + 1)
    pw = [mp.mpf(0)] * (N + 1)
    pw[0] = mp.mpf(1)                          # phi^0
    for k in range(1, N + 1):
        new = [mp.mpf(0)] * (N + 1)            # phi^k = phi^(k-1) * phi, truncated at w^N
        for i in range(N + 1):
            if pw[i] == 0:
                continue
            for j in range(1, N + 1 - i):
                new[i + j] += pw[i] * ph[j]
        pw = new
        for n in range(N + 1):
            d[n] += cs[k - 1] * pw[n]
    return d[1:]


def mapped(st, cs, s1, s2, p2=None):
    """(s, mu, spread of w*, spread of mu, n, c, w images) of the mapped Dlog estimate, or None"""
    p2 = p2 if p2 is not None else complex(P2_ABS.real - 262.3756, P2_ABS.imag)
    cb = choose_c(s1, s2, p2)
    d = compose(cs, phi_series(cb[0], s2, len(cs)))
    e = st.dlog_fit(d)
    if e is None:
        return None, cb
    return (float(phi(e[0], cb[0], s2)), e[1], e[2], e[3], e[4]), cb


def fmt(e):
    return "none" if e is None else (f"s {e[0]:.4f}, mu {e[1]:+.4f} (spreads in w {e[2]:.1e}, in mu {e[3]:.1e}), "
                                     f"{e[4]} approximants")


def setup(code):
    sys.path.insert(0, code)
    import singularity_type as st
    import subdom as sd
    mp.mp.dps = DPS
    return st, sd


def unit(argv):
    st, sd = setup(argv[0])
    s1 = sd.S1
    import numpy as np
    rng = np.random.default_rng(1)              # the plants' relative noise 1e-12, or the Pade matrices are exactly singular
    cs = [sd.b(0.5, k) / mp.mpf(sd.S2) ** k * (1 + sd.NOISE * rng.standard_normal()) for k in range(1, sd.N + 1)]
    e, cb = mapped(st, cs, s1, sd.S2)
    ok = e is not None and abs(e[0] - sd.S2) < 1e-6 and abs(e[1] - 0.5) < 1e-6
    print(f"code test: one square-root point at {sd.S2} (noise 1e-12), no pair, map c {cb[0]:.3f}: mapped {fmt(e)}; plain "
          f"{sd.fmt(st.dlog_fit(cs))}: {'ok' if ok else 'WRONG'}")
    return 0 if ok else 1


def scan(argv):
    st, sd = setup(argv[0])
    a = json.load(open(argv[1]))
    A1 = complex(*a["A1"])
    r0 = a["ratio"]
    sign = 1.0 if a["A2"] >= 0 else -1.0
    judge = lambda e: e is not None and abs(e[1] - 0.5) <= 0.05 and abs(e[0] - sd.S2) <= 0.005 * sd.S2
    cb = choose_c(sd.S1, sd.S2, complex(P2_ABS.real - 262.3756, P2_ABS.imag))
    print(f"map for s2 {sd.S2}: c {cb[0]:.3f}; images: pair |w| {cb[2]:.4f}, P2 {cb[3]:.4f}, infinity {cb[4]:.4f}, real point 1")
    jstar = None
    for j in range(0, 41):
        A2 = sign * abs(A1) * r0 / 2 ** j
        e = st.dlog_fit(sd.plant(A1, A2, sd.S1, sd.S2, 0.5))
        print(f"j {j:2d}, |A2|/|A1| {r0 / 2 ** j:.4e}: plain Dlog, square-root pair: {sd.fmt(e)} -> "
              f"{'meets' if judge(e) else 'FAILS'} the bars", flush=True)
        if not judge(e):
            jstar = j
            break
    if jstar is None:
        print("the plain Dlog meets the bars at every j up to 40: type not resolved at N 31")
        return 2
    ok = True
    for j in (jstar, jstar + 1, jstar + 2):
        A2 = sign * abs(A1) * r0 / 2 ** j
        for name, mu1 in (("square-root pair", 0.5), ("pole pair", -1.0)):
            e, _ = mapped(st, sd.plant(A1, A2, sd.S1, sd.S2, mu1), sd.S1, sd.S2)
            em, _ = mapped(st, sd.plant(A1, A2, sd.S1, sd.S2 + 0.5, mu1), sd.S1, sd.S2)
            good, moved = judge(e), judge(em)
            ok &= good and not moved
            print(f"j {j:2d}, |A2|/|A1| {r0 / 2 ** j:.4e}, {name}: mapped {fmt(e)} -> {'PASS' if good else 'FAIL'}; "
                  f"--mutate=move {fmt(em)} -> {'fails (as required)' if not moved else 'PASSES (control did not fire)'}",
                  flush=True)
        if j == jstar:                         # reported, not judged
            A2 = sign * abs(A1) * r0 / 2 ** j
            base = sd.plant(A1, A2, sd.S1, sd.S2, 0.5)
            p2r = complex(P2_ABS.real - 262.3756, P2_ABS.imag)
            withp2 = [x + 2 * mp.re(mp.mpc(A1.real, A1.imag) * sd.b(0.5, k) / mp.mpc(p2r.real, p2r.imag) ** k)
                      for k, x in enumerate(base, 1)]
            for label, cs, s1u, s2u in (("P2 added", withp2, sd.S1, sd.S2), ("map with s2 + 0.01", base, sd.S1, sd.S2 + 0.01),
                                        ("map with s1 + 0.006", base, sd.S1 + 0.006, sd.S2)):
                e, _ = mapped(st, cs, s1u, s2u)
                print(f"      reported, not judged ({label}): mapped {fmt(e)} -> {'would pass' if judge(e) else 'would fail'}")
    print(f"conformal-map type check (j* = {jstar}): {'PASS: the mapped estimator may read the type' if ok else 'FAIL: type not resolved at N 31'}")
    return 0 if ok else 2


def real(argv):
    st, sd = setup(argv[0])
    from jet_singularity import load_jet, row_series
    Z, m = load_jet(argv[1])
    cs, _ = row_series(Z, "delta")
    r = json.load(open(argv[2]))[0]
    p = next((q for q in r["pade"] if q["D_im"] > 0.05), None)
    q = next((q for q in r["pade"] if q["D_im"] <= 0.05), None)
    if p is None or q is None:
        print(f"D0 {m['D']:.4f}: no pair or no real stable pole in locate")
        return 1
    D0 = m["D"]
    s1, s2 = complex(p["D_re"] - D0, p["D_im"]), q["D_re"] - D0
    e, cb = mapped(st, cs, s1, s2, complex(P2_ABS.real - D0, P2_ABS.imag))
    print(f"D0 {D0:.4f}: pair {p['D_re']:.4f} +- {p['D_im']:.4f}i, real pole {q['D_re']:.4f}; map c {cb[0]:.3f} (pair |w| "
          f"{cb[2]:.4f}, P2 {cb[3]:.4f}, infinity {cb[4]:.4f}); mapped {fmt(e)}" + (f"; D* {D0 + e[0]:.4f}" if e else ""))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd in ("unit", "scan", "real"):
        sys.exit({"unit": unit, "scan": scan, "real": real}[cmd](sys.argv[2:]))
    sys.exit(__doc__)
