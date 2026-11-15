# multipoint quadratic Hermite-Pade on the plant: P f^2 + Q f + R = 0 matched to order K at several bases
import sys, os, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-829/hp")
import mpmath as mp
import fold_mirror as F
mp.mp.dps = int(os.environ.get("DPS", "80"))
pl = F.Plant(0.0, float(os.environ.get("CONT", "0.3")), float(os.environ.get("NOISE", "1e-30")))
bases = [mp.mpf(x) for x in sys.argv[1].split(",")]
K = int(sys.argv[2]); degs = tuple(int(x) for x in sys.argv[3].split(","))
Dc, W = F.DSTAR, mp.mpf("0.3")
def cond_rows(kind):
    l, m, n = degs
    rows, rhs = [], []
    for i, Db in enumerate(bases):
        c = pl.series(Db, 829 + i)
        ch = [c[k] * W ** k for k in range(F.N + 1)]
        xb = (Db - Dc) / W
        if kind == "QP":
            g1, g0 = F.smul(ch, ch, F.N + 1), ch          # multiplies P, Q
        else:
            g1, g0 = [(k + 1) * ch[k + 1] for k in range(F.N)], ch   # multiplies Q1 (f'), Q0
        for k in range(K):
            row = []
            for gg, deg in ((g1, l), (g0, m)):
                for ii in range(deg + 1):
                    row.append(mp.fsum(mp.binomial(ii, j) * xb ** (ii - j) * gg[k - j] for j in range(0, min(ii, k) + 1)))
            for ii in range(n + 1):
                row.append(mp.binomial(ii, k) * xb ** (ii - k) if ii >= k else mp.mpf(0))
            rows.append(row)
    nu = l + m + n + 3
    assert len(rows) >= nu - 1, (len(rows), nu - 1)
    A = mp.matrix([r[1:] for r in rows]); b = mp.matrix([-r[0] for r in rows])   # first unknown (p_0 / q1_0) = 1
    x = mp.lu_solve(A, b) if A.rows == A.cols else mp.qr_solve(A, b)[0]
    v = [mp.mpf(1)] + [x[i] for i in range(nu - 1)]
    return v[:l + 1], v[l + 1:l + m + 2], v[l + m + 2:]
def to_h(p, Db):   # p(x), x = (D - Dc)/W = xb + h/W  ->  coefficients in h
    xb = (Db - Dc) / W
    s = F.pshift(p, xb)
    return [s[j] / W ** j for j in range(len(s))]
t = time.time()
anchor = max(bases)
cA = pl.series(anchor, 829 + bases.index(anchor))
targets = F.GRID
for kind in ("QP", "DA"):
    P, Q, R = (to_h(p, anchor) for p in cond_rows(kind))
    if kind == "QP":
        q = F.QPade.__new__(F.QPade)
        q.P, q.Q, q.R, q.Db = P, Q, R, anchor
        q.disc = [a - b for a, b in zip(*[x + [mp.mpf(0)] * 200 for x in (F.smul(Q, Q), [4 * v for v in F.smul(P, R)])])]
        while len(q.disc) > 1 and q.disc[-1] == 0: q.disc.pop()
        d0 = F.peval(q.disc, 0); q.ok = d0 > 0
        r0 = [(-F.peval(Q, 0) + sg * mp.sqrt(abs(d0))) / (2 * F.peval(P, 0)) for sg in (1, -1)]
        q.sig = 1 if abs(r0[0] - cA[0]) < abs(r0[1] - cA[0]) else -1
        q.bad = [r.real for r in F.proots(q.disc) + F.proots(P) if abs(r.imag) < 1e-9]
        em = [q.value(D, -1) for D in targets]
        em = [float(abs(v - pl.value(D, -1))) if v is not None else None for v, D in zip(em, targets)]
        ep = [float(abs(q.value(D, 1) - pl.value(D))) if q.value(D, 1) is not None else 9 for D in targets]
        print("QP res0 %.1e" % float(min(abs(x - cA[0]) for x in r0)), "mirror err max %.1e at 259.64 %.1e 259.77 %.1e" % (max(x for x in em if x is not None), em[0], em[13]), "plus max %.1e" % max(ep), "undefined", sum(x is None for x in em))
    else:
        a = F.DApprox.__new__(F.DApprox)
        a.Q1, a.Q0, a.R, a.Db, a.c0 = [W * x for x in P], Q, R, anchor, cA[0]
        a.zeros = [complex(z) for z in F.proots(a.Q1)]
        hs = float(F.DSTAR - anchor)
        z0 = min(a.zeros, key=lambda z: abs(z - hs))
        a.hstar = mp.re(F.polish(a.Q1, z0.real)); others = [z for z in a.zeros if z is not z0]
        dn = min(abs(z - complex(a.hstar)) for z in others)
        a.rho = min(F.RHO, mp.mpf(0.45 * dn)); a.zc = [mp.mpc(z) for z in others] + [mp.mpc(a.hstar)]
        dQ1 = [k * a.Q1[k] for k in range(1, len(a.Q1))]
        mu = -F.peval(a.Q0, a.hstar) / F.peval(dQ1, a.hstar)
        sh = a.sheets(targets)
        em = [float(abs(mp.re(sh[D][-1]) - pl.value(D, -1))) for D in targets]
        im = max(float(abs(mp.im(sh[D][-1]))) for D in targets)
        ep = [float(abs(mp.re(sh[D][1]) - pl.value(D))) for D in targets]
        print("DA D* %.8f mu %.8f rho %.3f dnext %.3f" % (float(anchor + a.hstar), float(mu), float(a.rho), dn), "mirror err max %.1e at 259.64 %.1e 259.77 %.1e" % (max(em), em[0], em[13]), "im %.1e" % im, "plus max %.1e" % max(ep))
print("time %.1f" % (time.time() - t))
