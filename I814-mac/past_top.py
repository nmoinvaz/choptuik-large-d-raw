"""lam_g of the backbone past lam_gauge_fit.DMAX against the capped reference fit (c0 = 1, 1/n, REF_DEG, D >= 20)"""
import csv, sys
import mpmath as mp
sys.path.insert(0, ".")
import lam_gauge_fit as LF
mp.mp.dps = 40
pts = LF.backbone()
ts = [1 / (D - 2) for D, _ in pts]
c, _ = LF.lsq(ts, [y for _, y in pts], LF.REF_DEG, fixed0=mp.mpf(1))
rows = [r for r in csv.DictReader(x for x in open("data/lam_gauge.csv") if not x.startswith("#")) if r["role"] == "backbone"]
out = []
for r in rows:
    D = mp.mpf(r["D_str"]) if r["D_str"] else mp.mpf(float(r["D"]))
    if D > LF.DMAX:
        off = mp.mpf(r["lam_g"]) - mp.polyval(c[::-1], 1 / (D - 2))
        out.append((D, off))
print(f"{len(out)} states past D {mp.nstr(LF.DMAX, 8)}; chain lam_g minus the capped fit:")
for D, e in out:
    print(f"  D {mp.nstr(D, 10)}  {mp.nstr(e, 3)}")
