"""#989 rec. 2 on rpi5: the centre's scatter and the zero's standard error.
    python3 analyze989.py --centre LOG [LOG ...] --dA LOG --dw LOG [--all LOG ...]      (venv python, PYTHONPATH=. from solver/inner_stokes)
--centre: the solves under the bar (as m7_outer takes them); --all: all eight (for sigma beside it). Same J and zero as m7_outer.py --local (same formulas)."""
import sys
import numpy as np
from m7_outer import point
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from run_pert989 import stats

a = sys.argv[1:]
def grab(k):
    i = a.index(k) + 1; out = []
    while i < len(a) and not a[i].startswith("--"): out.append(a[i]); i += 1
    return out
cen = [point(f, True) for f in grab("--centre")]
allp = [point(f, True) for f in grab("--all")] if "--all" in a else cen
(_, pa, ra, ra3), (_, pw, rw, rw3) = point(grab("--dA")[0], True), point(grab("--dw")[0], True)
p0 = cen[0][1]
R = np.array([c[2] for c in cen]); r0 = R.mean(axis=0)
J = np.column_stack([(ra - r0) / (pa[0] - p0[0]), (rw - r0) / (pw[1] - p0[1])])
st = stats([tuple(c[2]) for c in cen], J=J)
sa = stats([tuple(c[2]) for c in allp])
step = -np.linalg.solve(J, r0); z = p0 + step
print(f"centre solves under the bar: n = {st['n']}; mean r_1 = {r0[0]:+.4f}{r0[1]:+.4f}i; |r_3| {min(c[3] for c in cen):.1e} to {max(c[3] for c in cen):.1e}")
print(f"sigma (sqrt of the trace of the sample covariance, ddof 1) = {st['sigma']:.4f} over the {st['n']} under the bar, {sa['sigma']:.4f} over all {sa['n']}")
print(f"covariance of r_1 (under the bar): {np.array2string(st['cov'], precision=4)}")
print(f"J (Re/Im rows; A, w/w_inf) = {np.array2string(J, precision=1)}, singular values {np.array2string(st['sv'], precision=1)}")
print(f"zero = ({z[0]:.9f}, {z[1]:.9f})   step ({step[0]:+.3e}, {step[1]:+.3e})")
print(f"standard error of the zero, J fixed: bound sigma/(sqrt(n) s_min) = {st['se_bound']:.2e};  propagated sqrt(tr(J^-1 cov J^-T)/n) = {st['se_prop']:.2e}")
print(f"r_1 spread / |r_3| (sigma / mean |r_3|) = {st['sigma'] / np.mean([c[3] for c in cen]):.1e}")
refs = {"#989 xi1 0.145 zero": (2.719313276, 0.999998856), "#977 Z14c (0.15)": (2.719234224, 1.000024742), "#974 run 4 (0.15)": (2.719236, 1.000026)}
for k, (ra_, rw_) in refs.items():
    d = np.array([z[0] - ra_, z[1] - rw_]); print(f"  vs {k}: dA {d[0]:+.2e}, dw {d[1]:+.2e}, norm {np.linalg.norm(d):.2e} = {np.linalg.norm(d) / st['se_prop']:.1f} x the propagated SE, {np.linalg.norm(d) / st['se_bound']:.1f} x the bound")
# added after the eight solves (not in the plan): a parametric bootstrap of the zero with J's own noise. r_0, r_a, r_w are each given the scatter of the
# centre solves (r_0: covariance/n, the two offsets: single solves, covariance), the zero is recomputed 20000 times (numpy default_rng(989)).
rng = np.random.default_rng(989)
cov = st["cov"]; hA = pa[0] - p0[0]; hW = pw[1] - p0[1]
Z = []
for _ in range(20000):
    r0s = r0 + rng.multivariate_normal([0, 0], cov / st["n"]); ras = ra + rng.multivariate_normal([0, 0], cov); rws = rw + rng.multivariate_normal([0, 0], cov)
    Js = np.column_stack([(ras - r0s) / hA, (rws - r0s) / hW])
    Z.append(p0 - np.linalg.solve(Js, r0s))
Z = np.array(Z); sd = Z.std(axis=0, ddof=1); med = np.median(Z, axis=0)
rb = (np.percentile(Z, 84, axis=0) - np.percentile(Z, 16, axis=0)) / 2     # robust scale: half the 16-84 percentile width (the std has heavy tails when J* is near singular)
print(f"bootstrap with J's noise (20000 draws, seed 989): std of A {sd[0]:.2e}, of w/w_inf {sd[1]:.2e}, norm {np.linalg.norm(sd):.2e}; "
      f"robust (half the 16-84 percentile width) A {rb[0]:.2e}, w/w_inf {rb[1]:.2e}, norm {np.linalg.norm(rb):.2e}; median zero ({med[0]:.9f}, {med[1]:.9f})")
# projection, not a measurement: the same bootstrap with the centre mean of kc solves and each offset the mean of ko solves of the same scatter
for kc, ko in [(8, 8), (16, 16)]:
    rng = np.random.default_rng(989); Zp = []
    for _ in range(20000):
        r0s = r0 + rng.multivariate_normal([0, 0], cov / kc); ras = ra + rng.multivariate_normal([0, 0], cov / ko); rws = rw + rng.multivariate_normal([0, 0], cov / ko)
        Zp.append(p0 - np.linalg.solve(np.column_stack([(ras - r0s) / hA, (rws - r0s) / hW]), r0s))
    Zp = np.array(Zp); sdp = Zp.std(axis=0, ddof=1); rbp = (np.percentile(Zp, 84, axis=0) - np.percentile(Zp, 16, axis=0)) / 2
    print(f"projection ({kc} centre solves, {ko} solves for each of dA and dw, same scatter): std norm {np.linalg.norm(sdp):.2e}, robust A {rbp[0]:.2e}, w/w_inf {rbp[1]:.2e}, norm {np.linalg.norm(rbp):.2e}")
if "--m7_outer" in a:   # cross-check against m7_outer.py's own printed zero and singular values (a failing check exits 1; --mutate shifts the zero)
    import re
    t = open(a[a.index("--m7_outer") + 1]).read()
    m = re.search(r"zero: A ([0-9.]+), w/w_inf ([0-9.]+)", t); s = re.search(r"singular values \[\s*([0-9.]+)\s+([0-9.]+)\]", t)
    zz = z + (1e-5 if "--mutate" in a else 0)
    ok = abs(float(m.group(1)) - zz[0]) < 6e-7 and abs(float(m.group(2)) - zz[1]) < 6e-7 and abs(float(s.group(1)) - st["sv"][0]) < 0.06 and abs(float(s.group(2)) - st["sv"][1]) < 0.06
    print(f"cross-check with m7_outer's print (zero {m.group(1)}, {m.group(2)}; singular values {s.group(1)}, {s.group(2)}): {'ok' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
