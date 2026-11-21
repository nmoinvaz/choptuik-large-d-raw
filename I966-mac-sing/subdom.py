"""#966: the type of a real singularity behind a nearer conjugate pair, by the Dlog estimator with the pair divided out.
Readings fixed in I966-mac-sing/README.md (2026-11-21 14:49:34 UTC) before this script read a real series.
    python subdom.py amp CODE JET.npz S1RE S1IM D2 [--json OUT]    amplitudes of the pair and the real point at a base
    python subdom.py planted CODE AMP.json [--mutate=move]          the planted check
    python subdom.py scan CODE AMP.json                             the amended type check (exit 0 pass, 2 not resolved)
    python subdom.py real CODE JET.npz LOCATE.json                  the estimator on Delta's series at a base
CODE: the folder holding singularity_type.py and jet_singularity.py (main 607c1df3).
Estimator: g'/g (g = df/dh, singularity_type.dlog_series) has a simple pole with residue mu - 1 at each algebraic
singularity. It is multiplied by a(h) = (1 - h/s1)(1 - h/conj s1), which cancels the pair's poles. Then, as
singularity_type.dlog_fit: Pade [L/M] for M 3..9, L M - 1..M + 1; in each, the real pole nearest the origin (Re > 0,
|Im| < 5% of the modulus, no numerator zero within 1e-6 of it), with mu = 1 + residue / a(s), skipping corrected
residues within 0.05 of 0 or +1; the median over the approximants and their spread. The spreads are over approximants
of one method, not error bars.
planted: Delta-like coefficients c_k = 2 Re(A1 b_k(mu1) / s1^k) + A2 b_k(1/2) / s2^k, b_k(mu) the coefficients of
(1 - x)^mu, with s1 = P1 - 262.3756 = -0.2946 + 0.9729i, s2 = 2.8, A1 and A2 from `amp` at 262.3756, N 31, relative
noise 1e-12. Pass: |mu - 0.5| <= 0.05 and |s - 2.8| <= 0.014 for the square-root pair (mu1 = 1/2). --mutate=move
builds the point at 2.8 + 0.5 and judges it against 2.8: it must fail. Reported, not judged: a pole pair (mu1 = -1),
the plain Dlog estimator without the division, and the division with s1 off by 0.006 (the three clusters' spread)."""
import json
import statistics
import sys

import mpmath as mp
import numpy as np

DPS = 60
S1 = complex(262.0810 - 262.3756, 0.9729)
S2 = 2.8
N = 31
NOISE = 1e-12


def st_import(code):
    sys.path.insert(0, code)
    import singularity_type as st
    return st


def b(mu, k):
    return mp.binomial(mp.mpf(mu), k) * (-1) ** k


def plant(A1, A2, s1, s2, mu1=0.5, seed=1):
    rng = np.random.default_rng(seed)
    s1 = mp.mpc(s1.real, s1.imag)
    out = []
    for k in range(1, N + 1):
        v = 2 * mp.re(mp.mpc(A1.real, A1.imag) * b(mu1, k) / s1 ** k) + A2 * b(0.5, k) / mp.mpf(s2) ** k
        out.append(v * (1 + NOISE * rng.standard_normal()))
    return out


def sub_dlog(st, c, s1, Ms=range(3, 10)):
    """(s, mu, spread of s, spread of mu, n) of the real pole nearest the origin of a(h) g'/g, or None"""
    q = st.dlog_series(c)
    s1 = mp.mpc(s1.real, s1.imag)
    a1, a2 = -2 * mp.re(1 / s1), abs(1 / s1) ** 2
    qt = [q[k] + (a1 * q[k - 1] if k >= 1 else 0) + (a2 * q[k - 2] if k >= 2 else 0) for k in range(len(q))]
    res = []
    for M in Ms:
        for L in (M - 1, M, M + 1):
            if L + M + 1 > len(qt) or L < 0:
                continue
            p, d = mp.pade(qt[:L + M + 1], L, M)
            if len(d) < 2:
                continue
            poles = mp.polyroots(d[::-1], maxsteps=200, extraprec=200)
            zeros = mp.polyroots(p[::-1], maxsteps=200, extraprec=200) if len(p) > 1 else []
            dp = [k * d[k] for k in range(1, len(d))]
            cand = []
            for z in poles:
                z = mp.mpc(z)
                if abs(z.imag) > 0.05 * abs(z) or z.real <= 0:
                    continue
                if any(abs(z - w) < 1e-6 * abs(z) for w in zeros):
                    continue
                az = mp.re(1 + a1 * z + a2 * z * z)
                if az == 0:
                    continue
                r = mp.re(mp.polyval(p[::-1], z) / mp.polyval(dp[::-1], z)) / az
                if abs(r) < 0.05 or abs(r - 1) < 0.05:
                    continue
                cand.append((z, r))
            if not cand:
                continue
            z, r = min(cand, key=lambda x: abs(x[0]))
            res.append((float(z.real), float(r) + 1.0))
    if not res:
        return None
    s = [x for x, _ in res]
    m = [x for _, x in res]
    return statistics.median(s), statistics.median(m), max(s) - min(s), max(m) - min(m), len(res)


def fmt(e):
    return "none" if e is None else (f"s {e[0]:.4f} (spread {e[2]:.1e}), mu {e[1]:+.4f} (spread {e[3]:.1e}), "
                                     f"{e[4]} approximants")


def amp(argv):
    code, jet, s1re, s1im, D2 = argv[0], argv[1], float(argv[2]), float(argv[3]), float(argv[4])
    sys.path.insert(0, code)
    from jet_singularity import load_jet, row_series
    mp.mp.dps = DPS
    Z, m = load_jet(jet)
    c, _ = row_series(Z, "delta")
    c = np.array([float(x) for x in c])
    s1, s2 = complex(s1re, s1im), D2 - m["D"]
    k = np.arange(1, len(c) + 1)
    u = np.array([complex(b(0.5, int(j))) / s1 ** j for j in k])
    v = np.array([float(b(0.5, int(j))) / s2 ** j for j in k])
    w = 1 / np.abs(c)
    X = np.column_stack([2 * u.real, -2 * u.imag, v]) * w[:, None]
    (ar, ai, a2), *_ = np.linalg.lstsq(X, c * w, rcond=None)
    fit = 2 * (ar * u.real - ai * u.imag) + a2 * v
    rel = np.abs(fit - c) / np.abs(c)
    A1 = complex(ar, ai)
    print(f"D0 {m['D']:.4f}, s1 {s1.real:+.4f}{s1.imag:+.4f}i, s2 {s2:.4f}: A1 {A1.real:+.4e}{A1.imag:+.4e}i "
          f"(|A1| {abs(A1):.4e}), A2 {a2:+.4e}, |A2|/|A1| {abs(a2) / abs(A1):.4e}; relative misfit of c_k: median "
          f"{np.median(rel):.2e}, max {rel.max():.2e}, k 26..31 {', '.join(f'{x:.1e}' for x in rel[-6:])}")
    if "--json" in argv:
        json.dump(dict(D0=m["D"], s1=[s1.real, s1.imag], s2=s2, A1=[A1.real, A1.imag], A2=a2,
                       ratio=abs(a2) / abs(A1), misfit_median=float(np.median(rel)), misfit_max=float(rel.max())),
                  open(argv[argv.index("--json") + 1], "w"), indent=1)
    return 0


def planted(argv):
    st = st_import(argv[0])
    mp.mp.dps = DPS
    a = json.load(open(argv[1]))
    A1, A2 = complex(*a["A1"]), a["A2"]
    move = "--mutate=move" in argv
    s2b = S2 + (0.5 if move else 0.0)
    judge = lambda e: e is not None and abs(e[1] - 0.5) <= 0.05 and abs(e[0] - S2) <= 0.005 * S2
    c = plant(A1, A2, S1, s2b)
    e = sub_dlog(st, c, S1)
    ok = judge(e)
    print(f"plant: pair (mu1 +0.5) at s1 {S1.real:+.4f}{S1.imag:+.4f}i, A1 {A1.real:+.3e}{A1.imag:+.3e}i; real "
          f"square-root point at {s2b} (judged against {S2}), A2 {A2:+.3e} (|A2|/|A1| {a['ratio']:.3e}); N {N}"
          + (" (--mutate=move)" if move else ""))
    print(f"  divided-out Dlog: {fmt(e)} -> {'PASS' if ok else 'FAIL'}")
    c_pole = plant(A1, A2, S1, s2b, mu1=-1.0)
    e_pole = sub_dlog(st, c_pole, S1)
    print(f"  reported, not judged: pole pair (mu1 -1): {fmt(e_pole)} -> {'would pass' if judge(e_pole) else 'would fail'}")
    print(f"  reported, not judged: plain Dlog (no division): {fmt(st.dlog_fit(c))}")
    e_off = sub_dlog(st, c, S1 + 0.006)
    print(f"  reported, not judged: division with s1 + 0.006: {fmt(e_off)} -> {'would pass' if judge(e_off) else 'would fail'}")
    print(f"planted check{' (--mutate=move)' if move else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def scan(argv):
    """the amended type check (README, fixed 2026-11-21 14:53:52 UTC): the plant's |A2|/|A1| = ratio / 2^j until the
    plain Dlog fails the bars on the square-root-pair plant (j*); then at j*, j* + 1, j* + 2 the divided-out estimator
    must pass for the square-root pair and the pole pair, and --mutate=move (point at 3.3) must fail at each"""
    st = st_import(argv[0])
    mp.mp.dps = DPS
    a = json.load(open(argv[1]))
    A1 = complex(*a["A1"])
    r0 = a["ratio"]
    sign = 1.0 if a["A2"] >= 0 else -1.0
    judge = lambda e: e is not None and abs(e[1] - 0.5) <= 0.05 and abs(e[0] - S2) <= 0.005 * S2
    jstar = None
    for j in range(0, 41):
        A2 = sign * abs(A1) * r0 / 2 ** j
        e_sq = st.dlog_fit(plant(A1, A2, S1, S2, 0.5))
        e_po = st.dlog_fit(plant(A1, A2, S1, S2, -1.0))
        print(f"j {j:2d}, |A2|/|A1| {r0 / 2 ** j:.4e}: plain Dlog, square-root pair: {fmt(e_sq)} -> "
              f"{'meets' if judge(e_sq) else 'FAILS'} the bars; pole pair: {fmt(e_po)} -> {'meets' if judge(e_po) else 'fails'}",
              flush=True)
        if not judge(e_sq):
            jstar = j
            break
    if jstar is None:
        print("the plain Dlog meets the bars at every j up to 40: no plant reproduces its failure on the data; "
              "type not resolved at N 31")
        return 2
    ok = True
    for j in (jstar, jstar + 1, jstar + 2):
        A2 = sign * abs(A1) * r0 / 2 ** j
        for name, mu1 in (("square-root pair", 0.5), ("pole pair", -1.0)):
            e = sub_dlog(st, plant(A1, A2, S1, S2, mu1), S1)
            em = sub_dlog(st, plant(A1, A2, S1, S2 + 0.5, mu1), S1)
            good, moved = judge(e), judge(em)
            ok &= good and not moved
            print(f"j {j:2d}, |A2|/|A1| {r0 / 2 ** j:.4e}, {name}: divided-out Dlog {fmt(e)} -> {'PASS' if good else 'FAIL'}; "
                  f"--mutate=move {fmt(em)} -> {'fails (as required)' if not moved else 'PASSES (control did not fire)'}",
                  flush=True)
    print(f"type check (j* = {jstar}): {'PASS: the estimator may read the type' if ok else 'FAIL: type not resolved at N 31'}")
    return 0 if ok else 2


def real(argv):
    code, jet, loc = argv[0], argv[1], argv[2]
    st = st_import(code)
    from jet_singularity import load_jet, row_series
    mp.mp.dps = DPS
    Z, m = load_jet(jet)
    c, _ = row_series(Z, "delta")
    r = json.load(open(loc))[0]
    p = next((q for q in r["pade"] if q["D_im"] > 0.05), None)
    if p is None:
        print(f"D0 {m['D']:.4f}: no stable pole off the axis to divide out")
        return 1
    s1 = complex(p["D_re"] - m["D"], p["D_im"])
    e = sub_dlog(st, c, s1)
    re_ = [q for q in r["pade"] if q["D_im"] <= 0.05]
    print(f"D0 {m['D']:.4f}: pair divided out at {p['D_re']:.4f} +- {p['D_im']:.4f}i; divided-out Dlog: {fmt(e)}"
          + (f"; D* {m['D'] + e[0]:.4f}" if e else "")
          + (f"; locate's real stable pole {re_[0]['D_re']:.4f} (n {re_[0]['n']})" if re_ else "; no real stable pole in locate"))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "amp":
        sys.exit(amp(sys.argv[2:]))
    if cmd == "planted":
        sys.exit(planted(sys.argv[2:]))
    if cmd == "scan":
        sys.exit(scan(sys.argv[2:]))
    if cmd == "real":
        sys.exit(real(sys.argv[2:]))
    sys.exit(__doc__)
