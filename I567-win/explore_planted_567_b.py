import sys, math, numpy as np
import flex_trend_567 as f
from scipy.optimize import minimize
j, t5, p8 = f.load(sys.argv[1])
D, _ = f.all75(j, p8)
u = (D - 228.0) / 10.0
def gp_deg(deg):
    def fp(Dtr, ytr, Dte):
        uu, ut = (Dtr - 228.0) / 10.0, (Dte - 228.0) / 10.0
        H = np.column_stack([uu ** k for k in range(deg + 1)]); Ht = np.column_stack([ut ** k for k in range(deg + 1)])
        best = None
        for l in (1, 2, 4, 8):
            for sf in (0.01, 0.1, 1.0):
                for sn in (0.002, 0.005, 0.01):
                    p = [math.log(sf), math.log(l), math.log(sn)]; v = f._reml(p, uu, ytr, H)
                    if best is None or v < best[0]: best = (v, p)
        res = minimize(f._reml, best[1], args=(uu, ytr, H), method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8, maxiter=300))
        p = res.x if res.fun < best[0] else best[1]
        sf, l, sn = math.exp(p[0]), math.exp(p[1]), math.exp(p[2])
        K = sf * sf * f._mat52(np.abs(uu[:, None] - uu[None, :]), l) + (sn * sn + 1e-10) * np.eye(len(uu)); Ki = np.linalg.inv(K)
        beta = np.linalg.solve(H.T @ Ki @ H, H.T @ Ki @ ytr)
        ks = sf * sf * f._mat52(np.abs(ut[:, None] - uu[None, :]), l)
        return Ht @ beta + ks @ (Ki @ (ytr - H @ beta))
    return fp
def expo(Dtr, ytr, Dte):
    B = lambda d: np.column_stack([np.ones_like(d), (d - 228.0) / 10.0, np.exp(-((d - 228.0) / 10.0 + 1.0) / 1.2)])
    c = np.linalg.lstsq(B(Dtr), ytr, rcond=None)[0]; return B(Dte) @ c
M = {"G3": gp_deg(3), "G4": gp_deg(4), "G5": gp_deg(5), "poly3": lambda a, b, c: t5.fit_predict(a, b, c, ("poly", 3)), "poly4": lambda a, b, c: t5.fit_predict(a, b, c, ("poly", 4)), "expo": expo}
names = list(M)
yt = -230.0 - 20.0 * u + 3.0 * np.exp(-(u + 1.0) / 1.2)
print("P_E = -230 - 20 u + 3 exp(-(u+1)/1.2): range of the exp term over the data", float((3*np.exp(-(u+1)/1.2)).min()), float((3*np.exp(-(u+1)/1.2)).max()))
R = {n: {w: [] for w in f.WIN} for n in names}
for s in range(20):
    rng = np.random.default_rng(78000 + s); y = yt + rng.normal(0, 0.004, len(D))
    tab = f.rms_table(D, y, M, names)
    for w in f.WIN:
        for n in names: R[n][w].append(tab[w][n])
fl = {w: np.median(R["expo"][w]) for w in f.WIN}
print("floors (expo)", {w: round(float(v), 4) for w, v in fl.items()})
for n in names:
    print(f"   {n:6s}", {w: f"{np.median(R[n][w]):.4f} ({np.median(R[n][w])/(1.5*fl[w]):.1f}x)" for w in f.WIN})
