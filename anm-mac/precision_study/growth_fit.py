"""Growth per unit D of three quantities in the quad-double chain's records (anm-mac/run_trend_pin3_qd*/anm_run.jsonl):
(1) the double-double residual of the accepted quad-double states (the value floor, eps_dd times the mass-mode growth G),
(2) the double-double jet's order-1 error, fix1[0] (the quad-double model's order-1 residual of the jet's z_1, 2-norm),
(3) the second-order prediction error with fix1, F_pred / a^2 of the attempts. Least-squares slope of log10 against D,
with a bootstrap over bases for its spread (a spread over resamples, not a confidence interval).
    python growth_fit.py RAWDIR"""
import glob, json, math, os, sys
import numpy as np
raw = sys.argv[1]
recs = []
for f in sorted(glob.glob(os.path.join(raw, "anm-mac", "run_trend_pin3_qd*", "anm_run.jsonl"))):
    for l in open(f):
        r = json.loads(l); r["_f"] = f.split("/")[-2]; recs.append(r)
floor, slope1, sec = [], [], []
for r in recs:
    if r.get("fix1"):
        slope1.append((r["D0"], r["fix1"][0]))
    for a in r.get("attempts", []):
        if a["accepted"] and a["F_final"] == a["F_final"]:
            floor.append((a["D"], a["F_final"]))
        if r.get("fix1") and a["F_pred"] == a["F_pred"]:
            sec.append((r["D0"], a["F_pred"] / a["a"] ** 2, a["a"]))
        for (aa, Fp) in a.get("screens", []):
            if r.get("fix1"):
                sec.append((r["D0"], Fp / aa ** 2, aa))
rng = np.random.default_rng(1)
def fit(name, pts):
    x = np.array([p[0] for p in pts]); y = np.log10([p[1] for p in pts])
    b = np.polyfit(x, y, 1)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(x), len(x))
        if np.ptp(x[i]) > 0.5:
            bs.append(np.polyfit(x[i], y[i], 1)[0])
    lo, hi = np.percentile(bs, [5, 95])
    print(f"{name}: {len(x)} points, D {x.min():.2f}-{x.max():.2f}, growth {10 ** b[0]:.3f}x per unit D "
          f"(bootstrap 5-95%: {10 ** lo:.3f}-{10 ** hi:.3f}); value at D 82.16 {10 ** np.polyval(b, 82.16):.2e}, scatter "
          f"(rms of log10 residual) {np.sqrt(np.mean((y - np.polyval(b, x)) ** 2)):.2f}")
    return b
b1 = fit("(1) dd residual of accepted qd states (value floor)", floor)
b2 = fit("(2) jet order-1 error, fix1[0]", slope1)
b3 = fit("(3) fix1 prediction error F_pred / a^2", sec)
G = lambda D: 0.7 ** (-(D - 3.0))
print(f"mass-mode growth G = 0.7^-(n-1): {1 / 0.7:.3f}x per unit D; G^2: {1 / 0.49:.3f}x")
for D in (82.16, 86.36):
    print(f"  D {D}: eps_dd G = {2.0 ** -106 * G(D):.2e}")
