"""post hoc (#815, after the registered real fit): C with a fold part of degree K against C_even with a regular part of
the same degree in D (K // 2), plants first, then the real states; window N"""
import sys
import numpy as np
sys.path.insert(0, ".")
import lam_fold_fit as L
from scipy.optimize import minimize

def ceven(D, y, sig, m):
    extra = [(D - 259.0) ** j for j in range(m + 1)]
    f = lambda p: L.lrms(L.lin(L.wcols(D, *p) + extra, y, sig)[1])
    G = [(b, w) for b in np.linspace(0, 5, 26) for w in np.linspace(0.05, 5, 50)]
    mm = L.nm(f, [list(G[i]) for i in np.argsort([f(p) for p in G])[:4]], lambda p: True)
    c, res = L.lin(L.wcols(D, *mm.x) + extra, y, sig)
    return dict(r=float(np.max(np.abs(res))), beta=float(mm.x[0]), omega=float(abs(mm.x[1])))

pts = L.data()
b, p250 = L.pivot_law(sys.argv[1])
for w in ("N", "G"):
    D, y, sig = L.window(pts, w)
    P = L.plants(D, sig, b, p250)
    cases = [(k, P[k]) for k in ("PS", "PW", "PM")] + [("real", y)]
    print(f"window {w}")
    for K in (3, 4, 5):
        for name, v in cases:
            c = L.form(D, v, sig, "C", K); e = ceven(D, v, sig, K // 2); s = L.form(D, v, sig, "S", K)
            print(f"  K {K} {name:5s} r: S_K {s['r']:.1e}  C_K {c['r']:.1e}  C_even(deg {K//2}) {e['r']:.1e} | "
                  f"C_even/C {e['r']/c['r']:.1e}  S/C {s['r']/c['r']:.1e} | C: D* {c['Dstar']:.5f} beta {c['beta']:.4f} "
                  f"omega {c['omega']:.4f} | odd part max {c['odd_max']:.2e}, W max {c['W_max']:.2e}")
