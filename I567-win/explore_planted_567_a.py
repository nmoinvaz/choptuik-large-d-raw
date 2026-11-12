import sys, math, numpy as np
import flex_trend_567 as f
from scipy.interpolate import make_smoothing_spline
j, t5, p8 = f.load(sys.argv[1])
D, _ = f.all75(j, p8)
T = f.truths(D)
def gp_deg(deg):
    def fp(Dtr, ytr, Dte):
        u, ut = (Dtr - 228.0) / 10.0, (Dte - 228.0) / 10.0
        H = np.column_stack([u ** k for k in range(deg + 1)]); Ht = np.column_stack([ut ** k for k in range(deg + 1)])
        best = None
        for l in (1, 2, 4, 8):
            for sf in (0.01, 0.1, 1.0):
                for sn in (0.002, 0.005, 0.01):
                    p = [math.log(sf), math.log(l), math.log(sn)]; v = f._reml(p, u, ytr, H)
                    if best is None or v < best[0]: best = (v, p)
        from scipy.optimize import minimize
        res = minimize(f._reml, best[1], args=(u, ytr, H), method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8, maxiter=300))
        p = res.x if res.fun < best[0] else best[1]
        sf, l, sn = math.exp(p[0]), math.exp(p[1]), math.exp(p[2])
        K = sf * sf * f._mat52(np.abs(u[:, None] - u[None, :]), l) + (sn * sn + 1e-10) * np.eye(len(u)); Ki = np.linalg.inv(K)
        beta = np.linalg.solve(H.T @ Ki @ H, H.T @ Ki @ ytr)
        ks = sf * sf * f._mat52(np.abs(ut[:, None] - u[None, :]), l)
        return Ht @ beta + ks @ (Ki @ (ytr - H @ beta))
    return fp
def spl_poly(Dtr, ytr, Dte):
    s = make_smoothing_spline(Dtr, ytr); return np.array([float(s(x, extrapolate=True)) for x in Dte])
M = f.methods(t5)
M.update({"G2": gp_deg(2), "G3": gp_deg(3), "G4": gp_deg(4), "Spoly": spl_poly})
names = ["G2", "G3", "G4", "S", "Spoly", "poly3", "poly4", "lnD3"]
print("planted-only exploration (no real sum values): median rms over 20 seeds at noise 0.004, per window; floors = the true form")
for k, yt in T.items():
    R = {n: {w: [] for w in f.WIN} for n in names}
    for s in range(20):
        rng = np.random.default_rng(77000 + s); y = yt + rng.normal(0, 0.004, len(D))
        tab = f.rms_table(D, y, M, names)
        for w in f.WIN:
            for n in names: R[n][w].append(tab[w][n])
    fl = {w: np.median(R[f.TRUE_FORM[k]][w]) for w in f.WIN}
    print(f"-- truth {k} (true form {f.TRUE_FORM[k]}), floors", {w: round(float(v), 4) for w, v in fl.items()})
    for n in names:
        print(f"   {n:6s}", {w: f"{np.median(R[n][w]):.4f} ({np.median(R[n][w])/(1.5*fl[w]):.1f}x)" for w in f.WIN})
