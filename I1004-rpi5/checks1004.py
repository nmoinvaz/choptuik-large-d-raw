"""#1004 checks beside the pre-registered analysis (run from solver/inner_stokes, venv python, PYTHONPATH=.:<this dir>):
the 24 new centre solves against #1000's eight; the leave-one-out of the largest outlier; r_1's deviation against |r_3| (exploratory, not in the plan);
the projection of #1002 against what 32 solves gave."""
import glob, sys
import numpy as np
from m7_outer import point
import analyze1002 as an

L = "logs/hier_nb_M7_rpi5_rtol14"
def grp(pat):
    return [point(f, True) for f in sorted(glob.glob(pat))]
old = grp(f"{L}_xi0145_s98?.log"); new = grp(f"{L}_xi0145_zero_s10[567]?.log")
dA, dw = grp(f"{L}_xi0145_dA_s100?.log"), grp(f"{L}_xi0145_dw_s101?.log")
c150, a150, w150 = grp(f"{L}_xi0150_zero_s102?.log"), grp(f"{L}_xi0150_dA_s103?.log"), grp(f"{L}_xi0150_dw_s104?.log")
r = lambda g: [tuple(p[2]) for p in g]
def sg(g):
    R = np.array(r(g)); return float(np.sqrt(np.trace(np.cov(R.T, ddof=1))))
for name, g in (("#1000's 8 (seeds 980-987)", old), ("the 24 new (1050-1073)", new), ("all 32", old + new)):
    R = np.array(r(g)); print(f"{name}: n {len(g)}, mean r_1 {R.mean(0)[0]:+.4f}{R.mean(0)[1]:+.4f}i, sigma {sg(g):.3f}, |r_3| median {np.median([p[3] for p in g]):.1e}")
o32 = an.zero_se(r(old + new), r(dA), r(dw)); o150 = an.zero_se(r(c150), r(a150), r(w150))
print(f"all 32: zero ({o32['z'][0]:.9f}, {o32['z'][1]:.9f}) SE {o32['se']:.2e}; projection of #1002 for 32: SE 4.70e-6, combined 4.97e-6; measured combined {np.hypot(o32['se'], o150['se']):.2e}")
# the largest outlier
allp = old + new
R = np.array(r(allp)); mu = R.mean(0); S = np.cov(R.T, ddof=1)
md = [float(np.sqrt((x - mu) @ np.linalg.solve(S, x - mu))) for x in R]
i = int(np.argmax(md)); seed = sorted(glob.glob(f"{L}_xi0145_s98?.log")) + sorted(glob.glob(f"{L}_xi0145_zero_s10[567]?.log"))
print(f"largest Mahalanobis distance from the 32's mean: {md[i]:.2f} ({seed[i].split('/')[-1]}, r_1 {R[i][0]:+.4f}{R[i][1]:+.4f}i, |r_3| {allp[i][3]:.1e}); next {sorted(md)[-2]:.2f}; for 32 Gaussian points the expected max is about 2.9")
keep = [p for j, p in enumerate(allp) if j != i]
o31 = an.zero_se(r(keep), r(dA), r(dw)); c = an.combine(o31, o150)
print(f"without it (31 solves): zero ({o31['z'][0]:.9f}, {o31['z'][1]:.9f}), SE {o31['se']:.2e}; d = {c['d']:.2f}, d_w {c['d_comp'][1]:+.2f}, Mahalanobis {c['maha']:.2f}")
# exploratory: r_1's deviation against |r_3|
dev = np.linalg.norm(R - np.median(R, axis=0), axis=1); r3 = np.array([p[3] for p in allp])
from math import sqrt
rk = lambda x: np.argsort(np.argsort(x))
rho = float(np.corrcoef(rk(dev), rk(r3))[0, 1])
print(f"exploratory: Spearman correlation of |r_1 - median| with |r_3| over the 32: {rho:+.2f}; deviation / |r_3| median {np.median(dev / r3):.1e}")
lo = [p for p in allp if p[3] < np.median(r3)]; hi = [p for p in allp if p[3] >= np.median(r3)]
print(f"  |r_3| below the median ({len(lo)} solves): sigma {sg(lo):.3f}, mean {np.array(r(lo)).mean(0).round(3)}; at or above ({len(hi)}): sigma {sg(hi):.3f}, mean {np.array(r(hi)).mean(0).round(3)}")
# exploratory (not in the plan): the same analysis with the 0.145 groups cut to |r_3| below a value (0.15's solves are all below 1e-7)
print("\nexploratory cut on |r_3| at 0.145 (all three groups), 0.15 as measured:")
print("| cut | n centre, dA, dw | zero (A, w/w_inf) | SE | d | d_w | Mahalanobis |\n|---|---|---|---|---|---|---|")
for cut in (1e-6, 3e-7, 2e-7, 1.5e-7, 1.0e-7):
    cs, as_, ws = ([tuple(p[2]) for p in g if p[3] < cut] for g in (old + new, dA, dw))
    if min(len(cs), len(as_), len(ws)) < 2:
        print(f"| {cut:.1e} | {len(cs)}, {len(as_)}, {len(ws)} | too few | | | | |"); continue
    o = an.zero_se(cs, as_, ws); c = an.combine(o, o150)
    print(f"| {cut:.1e} | {len(cs)}, {len(as_)}, {len(ws)} | ({o['z'][0]:.9f}, {o['z'][1]:.9f}) | {o['se']:.2e} | {c['d']:.2f} | {c['d_comp'][1]:+.2f} | {c['maha']:.2f} |")
