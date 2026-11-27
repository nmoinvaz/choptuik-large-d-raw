"""#1098: where is Delta(D) singular in e = 1/(D - 2)? Rational fits [L/M] (weighted least squares, Levenberg-Marquardt
from the linearized start, as hp/ladder_pade.py's rat_fit, returning the denominator too) to the ladder records, and
the poles of each accepted fit's denominator; a pole that recurs across the accepted fits is reported as a singularity
estimate. Checked first on planted truths with known singularities (hp/ladder_fit.py's T1-T3), at the ladder's own D and
sigma, with Gaussian noise.

    python3 delta_singularities.py real LADDER_FOLDER...        (from main's hp/, for ladder_fit's readers)
    python3 delta_singularities.py planted LADDER_FOLDER... --truth=T1|T2|T3 [--seed=1]

Accepted fit: chi^2 <= the chi^2(dof) 0.99 quantile and every |residual|/sigma <= 4, with dof >= 2. A pole cluster: poles
of different fits within 25% of their modulus of one another; reported when it holds poles of at least half the accepted
fits, with its median position (e and n = 1/e) and spread. Truths (e): T1 poles at about -0.077 and -0.2 (n about -13
and -5); T2 adds a pair at 0.02 exp(+-2 pi i/3); T3 adds a square-root branch point at -0.03.
"""
import sys

import mpmath as mp
from scipy.stats import chi2 as CHI2

sys.argv = [sys.argv[0], "sing"] + sys.argv[1:]
import ladder_fit as LF  # noqa: E402

mp.mp.dps = 50
args = LF.args
mode = sys.argv[2]
folders = [a for a in sys.argv[3:] if not a.startswith("--")]


def rat_fit(xs, ys, w, L, M):
    N = len(xs)
    lo, hi = min(xs), max(xs)
    xm = hi

    def T(x):
        u = (2 * x - (lo + hi)) / (hi - lo)
        r = [mp.mpf(1), u]
        for _ in range(L - 1):
            r.append(2 * u * r[-1] - r[-2])
        return r[:L + 1]
    Ts = [T(x) for x in xs]
    us = [x / xm for x in xs]
    A = mp.matrix(N, L + 1 + M)
    b = mp.matrix(N, 1)
    for i in range(N):
        for k in range(L + 1):
            A[i, k] = w[i] * Ts[i][k]
        for j in range(M):
            A[i, L + 1 + j] = -w[i] * ys[i] * us[i] ** (j + 1)
        b[i] = w[i] * ys[i]
    try:
        p = mp.lu_solve(A.T * A, A.T * b)
    except ZeroDivisionError:
        return None

    def resid(p):
        r = mp.matrix(N, 1)
        J = mp.matrix(N, L + 1 + M)
        for i in range(N):
            P = mp.fsum(p[k] * Ts[i][k] for k in range(L + 1))
            Q = 1 + mp.fsum(p[L + 1 + j] * us[i] ** (j + 1) for j in range(M))
            r[i] = w[i] * (P / Q - ys[i])
            for k in range(L + 1):
                J[i, k] = w[i] * Ts[i][k] / Q
            for j in range(M):
                J[i, L + 1 + j] = -w[i] * P * us[i] ** (j + 1) / Q ** 2
        return r, J
    lam = mp.mpf("1e-6")
    r, J = resid(p)
    c2 = mp.fsum(v ** 2 for v in r)
    for _ in range(80):
        JTJ = J.T * J
        g = J.T * r
        Ad = JTJ + lam * mp.diag([JTJ[k, k] for k in range(L + 1 + M)])
        try:
            dp = mp.lu_solve(Ad, -g)
        except ZeroDivisionError:
            return None
        pn = p + dp
        rn, Jn = resid(pn)
        cn = mp.fsum(v ** 2 for v in rn)
        if cn < c2:
            rel = (c2 - cn) / max(c2, mp.mpf("1e-300"))
            p, r, J, c2 = pn, rn, Jn, cn
            lam = max(lam / 10, mp.mpf("1e-20"))
            if rel < mp.mpf("1e-14"):
                break
        else:
            lam *= 10
            if lam > 1e12:
                break
    q = [mp.mpf(1)] + [p[L + 1 + j] for j in range(M)]          # Q(u) = sum q_j u^j, u = x / xm
    try:
        roots = mp.polyroots(list(reversed(q)), maxsteps=200, extraprec=200) if M else []
    except Exception:
        return None
    poles = [complex(rt * xm) for rt in roots]
    pf = [p[k] for k in range(L + 1 + M)]

    def ev(x):
        P = mp.fsum(pf[k] * T(x)[k] for k in range(L + 1))
        Q = 1 + mp.fsum(pf[L + 1 + j] * (x / xm) ** (j + 1) for j in range(M))
        return P / Q
    return dict(chi2=float(c2), maxres=float(max(abs(v) for v in r)), poles=poles, ev=ev)


def data():
    pts = LF.full_points(folders)
    L_ = sorted(pts)
    sig = [pts[d][1] for d in L_]
    if mode == "real":
        ys = [pts[d][0] for d in L_]
    else:
        import random
        rng = random.Random(int(args.get("seed", "1")))
        ys = [LF.truth(args["truth"], d) + mp.mpf(rng.gauss(0, 1)) * mp.mpf(s) for d, s in zip(L_, sig)]
    return L_, ys, sig


L_, ys, sig = data()
xs = [1 / (mp.mpf(d) - 2) for d in L_]
w = [1 / mp.mpf(s) for s in sig]
N = len(xs)
print(f"{mode} {args.get('truth', '')}: {N} points, e {float(min(xs)):.2e} to {float(max(xs)):.2e}")
acc = []
for M in range(1, 6):
    for L in range(1, N - M - 2):
        f = rat_fit(xs, ys, w, L, M)
        if f is None:
            continue
        dof = N - L - 1 - M
        if dof < 2 or f["chi2"] > CHI2.ppf(0.99, dof) or f["maxres"] > 4:
            continue
        acc.append((L, M, f))
        print(f"  [{L}/{M}] chi2 {f['chi2']:.2f} (dof {dof}), poles in e: "
              + ", ".join(f"{p.real:+.4f}{p.imag:+.4f}i" for p in sorted(f["poles"], key=abs)))
print(f"{len(acc)} accepted fits")
# --taylor=K: the Taylor coefficients a_0..a_K of every accepted fit at e = 0 (median and range)
if "taylor" in args:
    K = int(args["taylor"])
    cs = [mp.taylor(f["ev"], 0, K) for _, _, f in acc]
    for k in range(K + 1):
        v = sorted(c[k] for c in cs)
        print(f"  a_{k}: median {mp.nstr(v[len(v) // 2], 25)}, range {mp.nstr(v[-1] - v[0], 3)} over {len(v)} fits")
# --predict=D1,D2,...: every accepted fit's value there (median and range), against --compare=delta_all.csv rows
if "predict" in args:
    import csv
    tab = {}
    if "compare" in args:
        for r in csv.DictReader(open(args["compare"])):
            tab[round(float(r["D"]), 6)] = (mp.fsum(mp.mpf(r[f"Delta_q{i}"] or 0) for i in range(4)), r["err"], r["kind"])
    for Dp in [float(v) for v in args["predict"].split(",")]:
        x = 1 / (mp.mpf(Dp) - 2)
        vals = sorted(f["ev"](x) for _, _, f in acc)
        med = vals[len(vals) // 2]
        t = tab.get(round(Dp, 6))
        cmp = "" if t is None else (f"; table {mp.nstr(t[0], 20)} ({t[2]}, err {t[1]}): median - table "
                                    f"{mp.nstr(med - t[0], 3)}")
        print(f"  predict D {Dp:g}: median {mp.nstr(med, 20)}, range {mp.nstr(vals[-1] - vals[0], 3)} over "
              f"{len(vals)} fits{cmp}")
# clusters of poles across the accepted fits
allp = [(i, p) for i, (_, _, f) in enumerate(acc) for p in f["poles"] if abs(p) < 1.0]
clusters = []
for i, p in sorted(allp, key=lambda t: abs(t[1])):
    for c in clusters:
        if abs(p - c["c"]) <= 0.25 * abs(c["c"]):
            c["m"].append((i, p))
            c["c"] = sorted(c["m"], key=lambda t: abs(t[1]))[len(c["m"]) // 2][1]
            break
    else:
        clusters.append(dict(c=p, m=[(i, p)]))
for c in sorted(clusters, key=lambda c: abs(c["c"])):
    fits = {i for i, _ in c["m"]}
    if len(fits) * 2 < len(acc):
        continue
    re = sorted(p.real for _, p in c["m"])
    im = sorted(p.imag for _, p in c["m"])
    med = complex(re[len(re) // 2], im[len(im) // 2])
    print(f"  SINGULARITY e {med.real:+.5f}{med.imag:+.5f}i (|e| {abs(med):.5f}, n {1 / med:.3f}), in {len(fits)} of "
          f"{len(acc)} fits; spread re {re[0]:+.4f}..{re[-1]:+.4f}, im {im[0]:+.4f}..{im[-1]:+.4f}")
