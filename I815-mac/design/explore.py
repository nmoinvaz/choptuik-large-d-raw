import json, sys
import mpmath as mp
sys.path.insert(0, ".")
import lam_gauge_fit as LF
mp.mp.dps = 40
pts = LF.backbone()
allf = LF.fits(pts, fixed0=mp.mpf(1))
Rs = []
for f in allf:
    if not f["sel"]:
        continue
    sel = [(D, y) for D, y in pts if D >= f["Dlo"]]
    tf = (lambda D: 1 / (D - 2)) if f["var"] == "n" else (lambda D: 1 / D)
    c, _ = LF.lsq([tf(D) for D, _ in sel], [y for _, y in sel], f["d"], mp.mpf(1))
    Rs.append((lambda D, c=c, tf=tf: mp.polyval(c[::-1], tf(D))))
ts = [1 / (D - 2) for D, _ in pts]
c, _ = LF.lsq(ts, [y for _, y in pts], LF.REF_DEG, fixed0=mp.mpf(1))
R = lambda D: mp.polyval(c[::-1], 1 / (D - 2))
data = json.load(open(sys.argv[0].replace("explore.py", "data.json") if False else "%s/data.json" % "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/i815"))
Dstar = mp.mpf("259.9033")
print(len(Rs), "kept c0 = 1 fits")
for o in data:
    D = mp.mpf(o["D_str"]); r0 = R(D)
    sp = max(abs(Rf(D) - r0) for Rf in Rs)
    d = mp.mpf(o["lam_g"]) - r0
    o.update(delta=float(d), spread=float(sp))
    if o["D"] > 244.6:
        print(f"{o['D']:9.4f} delta {float(d):+.3e} spread {float(sp):.1e} d*pmin {float(d)*o['p_min']:+.2e} d/sqrt(D*-D) {float(d/mp.sqrt(Dstar-D)):+.3e}")
json.dump(data, open("/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/i815/data2.json", "w"), indent=0)
