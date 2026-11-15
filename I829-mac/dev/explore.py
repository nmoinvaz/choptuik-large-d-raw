import sys, glob, os, json
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-829/hp")
import mpmath as mp, numpy as np
import lam_gauge as LG
mp.mp.dps = 80
RAW = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/raw-wt/I603-win2/chain_nsr"
def dser(p):
    z = np.load(p); ks = sorted(k for k in z.files if k[0]=="z" and k[1:].isdigit())
    m = json.loads(str(z["meta"]))
    return mp.mpf(m["D_str"]), [mp.fsum(mp.mpf(float(z[k][n][-1])) for k in ks) for n in range(z[ks[0]].shape[0])], m
def sdelta(p):
    parts, meta = LG.load(p)
    return mp.mpf(meta["D_str"]), mp.fsum(mp.mpf(float(q[-1])) for q in parts), meta
jets = sorted(glob.glob(RAW+"/jet_pin3_D*.npz"))
sts = sorted(glob.glob(RAW+"/anm_pin3_D*.npz"))
S = {}
for p in sts:
    D, d, meta = sdelta(p); S[float(D)] = (D, d)
print("states", len(S), "range", min(S), max(S))
_, _, m0 = dser(jets[-1]); print("jet meta keys", sorted(m0)[:30])
Dst = mp.mpf("259.9033")
Ds = sorted(S)
for p in jets:
    Db, c, m = dser(p)
    if float(Db) < 258.78: continue
    i = Ds.index(float(Db))
    out = []
    for j in (i+1, i+2):
        if j < len(Ds):
            D, d = S[Ds[j]]; h = D - Db
            v = mp.fsum(x*h**k for k, x in enumerate(c))
            last = abs(c[-1]*h**24)
            out.append("h %.4f diff %.1e last %.1e" % (h, abs(v-d), last))
    print("%.4f s1 %.4f z0-state %.1e z0 %s |z24 s1^24| %.2e | %s" % (Db, Dst-Db, abs(c[0]-S[float(Db)][1]), mp.nstr(c[0], 15), abs(c[24]*(Dst-Db)**24), " ; ".join(out)))
