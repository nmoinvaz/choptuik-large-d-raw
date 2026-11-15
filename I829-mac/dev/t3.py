# two-base forms by weighted least squares (more conditions than unknowns), on the plant with noise
import sys, os, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-829/hp")
import mpmath as mp
import fold_mirror as F
mp.mp.dps = 80
pl = F.Plant(0.0, float(os.environ.get("CONT", "0.3")), float(os.environ.get("NOISE", "1e-30")))
W = mp.mpf(os.environ.get("W", "0.3"))
def forms_ls(inputs, deg, kind):
    l, m, n = deg
    kmax = F.N + 1 if kind == "QP" else F.N
    rows = []
    for (Db, c) in inputs:
        ch = [c[k] * W ** k for k in range(F.N + 1)]
        xb = (Db - F.DSTAR) / W
        g1 = F.smul(ch, ch, F.N + 1) if kind == "QP" else [(k + 1) * ch[k + 1] for k in range(F.N)]
        for k in range(kmax):
            row = []
            for g, d in ((g1, l), (ch, m)):
                for i in range(d + 1):
                    row.append(mp.fsum(mp.binomial(i, j) * xb ** (i - j) * g[k - j] for j in range(min(i, k) + 1)))
            for i in range(n + 1):
                row.append(mp.binomial(i, k) * xb ** (i - k) if i >= k else mp.mpf(0))
            sc = max(abs(v) for v in row)
            rows.append([v / sc for v in row])
    j0 = l + 1
    A = mp.matrix([r[:j0] + r[j0 + 1:] for r in rows])
    x, res = mp.qr_solve(A, mp.matrix([-r[j0] for r in rows]))
    v = [x[i] for i in range(j0)] + [mp.mpf(1)] + [x[i] for i in range(j0, l + m + n + 2)]
    xa = (inputs[0][0] - F.DSTAR) / W
    toh = lambda p: [y / W ** j for j, y in enumerate(F.pshift(p, xa))]
    P, Q, R = toh(v[:l + 1]), toh(v[l + 1:l + m + 2]), toh(v[l + m + 2:])
    if kind == "DA":
        P = [W * y for y in P]
    return (P, Q, R), res
if __name__ == '__main__':
    bases = [mp.mpf(x) for x in sys.argv[1].split(",")]
    inputs = [(Db, pl.series(Db, 829 + i)) for i, Db in enumerate(bases)]
    for dstr in sys.argv[2:]:
        deg = tuple(int(x) for x in dstr.split(","))
        for kind in ("DA", "QP"):
            t = time.time()
            try:
                polys, res = forms_ls(inputs, deg, kind)
            except Exception as ex:
                print(kind, deg, "solve:", ex); continue
            Db, c0 = inputs[0][0], inputs[0][1][0]
            if kind == "QP":
                q = F.QPade(polys, Db, c0)
                mv = [q.value(D, -1) for D in F.GRID]
                em = [float(abs(v - pl.value(D, -1))) if v is not None else 9 for v, D in zip(mv, F.GRID)]
                print("QP", deg, "res %.1e" % float(res), "D* %s" % (mp.nstr(Db + q.hstar, 12) if q.hstar is not None else None), "mirror 259.64 %.1e 259.70 %.1e 259.80 %.1e max %.1e" % (em[0], em[6], em[16], max(em)), "%.0fs" % (time.time() - t))
            else:
                a = F.DApprox(polys, Db, c0)
                if a.why: print("DA", deg, "why", a.why); continue
                try:
                    sh = a.sheets(F.GRID)
                except RuntimeError as ex:
                    print("DA", deg, ex); continue
                em = [float(abs(mp.re(sh[D][-1]) - pl.value(D, -1))) for D in F.GRID]
                print("DA", deg, "res %.1e" % float(res), "D* %s mu %s" % (mp.nstr(Db + a.hstar, 12), mp.nstr(a.mu, 10)), "mirror 259.64 %.1e 259.70 %.1e 259.80 %.1e max %.1e" % (em[0], em[6], em[16], max(em)), "%.0fs" % (time.time() - t))

