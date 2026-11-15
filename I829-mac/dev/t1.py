import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-829/hp")
import mpmath as mp
import fold_mirror as F
mp.mp.dps = F.DPS
RAW = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/raw-wt"
import os; pl = F.Plant(0.0, float(os.environ.get("CONT", "0.3")), float(os.environ.get("NOISE", "1e-30")))
for Dbs in sys.argv[1:]:
    Db = mp.mpf(Dbs)
    c = pl.series(Db, 1)
    for h in ("0.01", "-0.05"):
        h = mp.mpf(h); print("series check h", h, mp.nstr(abs(mp.fsum(x*h**k for k, x in enumerate(c)) - pl.value(Db+h)), 3))
    t = time.time()
    targets = [F.GRID[0], F.GRID[13], F.GRID[-1]]
    pst = [(D, pl.value(D)) for D, _ in F.states(RAW) if abs(D - Db) > 1e-9][::4]
    res = F.run_base(c, Db, targets, pst)
    for m in ("M1", "M2"):
        for e in res[m]:
            if e["why"]:
                print(m, e["deg"], "why:", e["why"]); continue
            em = [float(abs(mp.re(e["grid"][str(D)][1]) - pl.value(D, -1))) if e["grid"][str(D)][1] is not None else None for D in targets]
            ep = max(float(abs(mp.re(e["plus"][str(D)]) - v)) if e["plus"][str(D)] is not None else 9 for D, v in pst)
            im = [float(abs(mp.im(e["grid"][str(D)][1]))) if e["grid"][str(D)][1] is not None else None for D in targets]
            cf = e.get("coeffs")
            print(m, e["deg"], "D* %.6f" % e["Dstar"] if e.get("Dstar") else "", "mu %.6f" % e["mu"] if "mu" in e else "",
                  "mirror err", ["%.1e" % x if x is not None else None for x in em], "plus %.1e" % ep, "im", ["%.0e" % x for x in im if x is not None],
                  "a1 %.6f" % float(mp.re(cf[2])) if cf else "")
    print("time %.1f s" % (time.time() - t), flush=True)
