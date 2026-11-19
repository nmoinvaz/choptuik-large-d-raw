"""#1002: the M = 7 zero at each radius from sampled centre, dA and dw solves, its standard error with J's noise, and the radius comparison.

    python3 analyze1002.py --r145 CENTRE... --dA145 LOG... --dw145 LOG... --r150 CENTRE... --dA150 LOG... --dw150 LOG... [--mc]   (venv python, PYTHONPATH=. from solver/inner_stokes)
    python3 analyze1002.py --selftest [--mutate=jterm|zero|combine]

Per radius: the solves with |r_3| printed under 1e-6 of each of the three groups; r_0, r_a, r_w the group means of r_1 and Sigma_0, Sigma_a, Sigma_w their sample covariances (ddof 1), n_0, n_a, n_w the counts.
J = [(r_a - r_0)/hA, (r_w - r_0)/hW] with hA = 2e-4, hW = 1e-4, zero z = p_0 - J^-1 r_0 (p_0 = (2.719219, 1.000022)): m7_outer.py --local's formula with group means.
Standard error with J's noise, to first order: dz = J^-1 [ c_0 e_0 + c_a e_a + c_w e_w ], c_a = s_A/hA, c_w = s_W/hW, c_0 = -(1 + c_a + c_w), s = J^-1 r_0
(z moves by -J^-1 e_0 through the step and by J^-1 dJ s through J, dJ = [(e_a - e_0)/hA, (e_w - e_0)/hW]), so Cov z = J^-1 (c_0^2 Sigma_0/n_0 + c_a^2 Sigma_a/n_a + c_w^2 Sigma_w/n_w) J^-T.
SE = sqrt(trace Cov z); components (SE_A, SE_w) are the diagonal. --mc adds a parametric bootstrap (each group mean drawn from N(mean, Sigma/n), 20000 draws, numpy default_rng(1002)) with its std and robust scale.
Radius comparison: Delta = z(0.145) - z(0.15), combined SE = sqrt(SE_145^2 + SE_150^2) (quadrature sum), d = |Delta| / combined; per component and Mahalanobis beside it.
Verdict (fixed before the run): resolved if d > 3, absent if d < 1, else undecided; the w component reported separately with its own d_w."""
import sys
import numpy as np

P0 = np.array([2.719219, 1.000022]); HA, HW = 2e-4, 1e-4
BAR = 1e-6


def zero_se(r0s, ras, rws, mc=False, cov_fallback=None, mutate=""):
    R0, RA, RW = (np.array(x, float) for x in (r0s, ras, rws))
    n0, na, nw = len(R0), len(RA), len(RW)
    r0, ra, rw = R0.mean(0), RA.mean(0), RW.mean(0)

    def cov(R):
        return np.cov(R.T, ddof=1) if len(R) > 1 else (cov_fallback if cov_fallback is not None else np.full((2, 2), np.nan))
    S0, Sa, Sw = cov(R0), cov(RA), cov(RW)
    J = np.column_stack([(ra - r0) / HA, (rw - r0) / HW])
    Ji = np.linalg.inv(J)
    s = Ji @ r0
    z = P0 - s
    ca, cw = s[0] / HA, s[1] / HW
    c0 = -(1 + ca + cw)
    if mutate == "jterm":
        c0, ca, cw = -1.0, 0.0, 0.0
    C = Ji @ (c0**2 * S0 / n0 + ca**2 * Sa / na + cw**2 * Sw / nw) @ Ji.T
    out = dict(z=z, C=C, se=float(np.sqrt(np.trace(C))), se_c=np.sqrt(np.diag(C)), n=(n0, na, nw), J=J, sv=np.linalg.svd(J, compute_uv=False),
               r0=r0, S0=S0, Sa=Sa, Sw=Sw, c=(c0, ca, cw))
    # centre only, J fixed (#1000's two forms)
    out["se_bound_Jfixed"] = float(np.sqrt(np.trace(S0)) / (np.sqrt(n0) * out["sv"][-1]))
    out["se_prop_Jfixed"] = float(np.sqrt(np.trace(Ji @ S0 @ Ji.T) / n0))
    if mc:
        rng = np.random.default_rng(1002)
        Z = []
        for _ in range(20000):
            r0s_ = r0 + rng.multivariate_normal([0, 0], S0 / n0); ras_ = ra + rng.multivariate_normal([0, 0], Sa / na); rws_ = rw + rng.multivariate_normal([0, 0], Sw / nw)
            Js = np.column_stack([(ras_ - r0s_) / HA, (rws_ - r0s_) / HW])
            Z.append(P0 - np.linalg.solve(Js, r0s_))
        Z = np.array(Z)
        out["mc_std"] = Z.std(0, ddof=1)
        out["mc_rob"] = (np.percentile(Z, 84, axis=0) - np.percentile(Z, 16, axis=0)) / 2
    return out


def combine(a, b, mutate=""):
    D = a["z"] - b["z"]
    C = a["C"] + b["C"]
    comb = np.sqrt(a["se"] ** 2 + b["se"] ** 2)
    if mutate == "combine":
        comb = a["se"] + b["se"]
    return dict(D=D, norm=float(np.linalg.norm(D)), comb=float(comb), d=float(np.linalg.norm(D) / comb), d_comp=D / np.sqrt(np.diag(C)),
                maha=float(np.sqrt(D @ np.linalg.solve(C, D))))


def verdict(d):
    return "resolved" if d > 3 else ("absent" if d < 1 else "undecided")


def selftest(a):
    mut = [t for t in a if t.startswith("--mutate=")]
    mut = mut[0].split("=")[1] if mut else ""
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + label); ok = ok and cond
    # planted: a known J, a known zero, known noise; the delta-method SE must match the parametric bootstrap, and the zero must be recovered
    J0 = np.array([[3500.0, 3800.0], [2650.0, 11300.0]]); ztrue = P0 + np.array([2.5e-4, -1e-4])
    rng = np.random.default_rng(1)
    Sg = np.array([[0.03, 0.015], [0.015, 0.04]])
    def sample(r_mean, n):
        return rng.multivariate_normal(r_mean, Sg, size=n)
    r0t = -J0 @ (ztrue - P0)    # r_1 at p_0 is J (p_0 - z)
    big = 200000
    R0, RA, RW = sample(r0t, big), sample(r0t + J0[:, 0] * HA, big), sample(r0t + J0[:, 1] * HW, big)
    o = zero_se(R0, RA, RW, mutate="zero" if mut == "zero" else "")
    zz = o["z"] + (np.array([3e-5, 0]) if mut == "zero" else 0)
    chk("planted: the zero is recovered to 1e-6 from 200000 solves per group (its SE is 2e-5 at n = 8)", np.linalg.norm(zz - ztrue) < 1e-6)
    n = 8
    R0, RA, RW = sample(r0t, n), sample(r0t + J0[:, 0] * HA, n), sample(r0t + J0[:, 1] * HW, n)
    o = zero_se(R0, RA, RW, mc=True, mutate="jterm" if mut == "jterm" else "")
    chk(f"planted n = 8: delta-method SE {o['se']:.3e} within 15% of the bootstrap robust scale {np.linalg.norm(o['mc_rob']):.3e}", abs(o["se"] / np.linalg.norm(o["mc_rob"]) - 1) < 0.15)
    chk(f"J terms matter in the planted case: SE {o['se']:.2e} with J's noise against {o['se_prop_Jfixed']:.2e} with J fixed differ by more than 20%", abs(o["se"] / o["se_prop_Jfixed"] - 1) > 0.20)
    # two radii: combination rule on hand numbers
    A = dict(z=np.array([0.0, 0.0]), C=np.diag([9e-10, 1e-10]), se=np.sqrt(1e-9))
    B = dict(z=np.array([6e-5, 0.0]), C=np.diag([9e-10, 1e-10]), se=np.sqrt(1e-9))
    c = combine(A, B, mutate=mut)
    chk("combine: |Delta| 6e-5 over sqrt(2e-9) = 4.47e-5 gives d = 1.342", abs(c["d"] - 6e-5 / np.sqrt(2e-9)) < 1e-9)
    chk("verdicts: 3.01 resolved, 2.99 undecided, 0.99 absent, 1.0 undecided", [verdict(x) for x in (3.01, 2.99, 0.99, 1.0)] == ["resolved", "undecided", "absent", "undecided"])
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest(a)
    from m7_outer import point
    keys = ("--r145", "--dA145", "--dw145", "--r150", "--dA150", "--dw150")
    def grab(k):
        i = a.index(k) + 1; out = []
        while i < len(a) and not a[i].startswith("--"): out.append(a[i]); i += 1
        return out
    res = {}
    for rad, kc, ka, kw in (("0.145", "--r145", "--dA145", "--dw145"), ("0.15", "--r150", "--dA150", "--dw150")):
        groups = []
        for k in (kc, ka, kw):
            pts = [point(f, True) for f in grab(k)]
            use = [p for p in pts if p[3] < BAR]
            print(f"xi1 {rad} {k[2:]}: {len(use)} of {len(pts)} under the bar, |r_3| {min(p[3] for p in use):.1e} to {max(p[3] for p in use):.1e}" if use else f"xi1 {rad} {k[2:]}: none under the bar")
            groups.append([tuple(p[2]) for p in use])
        # a group with fewer than 2 solves takes the covariance of the centre group
        fb = np.cov(np.array(groups[0]).T, ddof=1) if len(groups[0]) > 1 else None
        o = zero_se(*groups, mc="--mc" in a, cov_fallback=fb)
        res[rad] = o
        print(f"xi1 {rad}: n (centre, dA, dw) = {o['n']}; centre mean r_1 = {o['r0'][0]:+.4f}{o['r0'][1]:+.4f}i")
        print(f"  covariances of r_1: centre {np.array2string(o['S0'], precision=4)}, dA {np.array2string(o['Sa'], precision=4)}, dw {np.array2string(o['Sw'], precision=4)}")
        print(f"  J (Re/Im rows; A, w/w_inf) = {np.array2string(o['J'], precision=1)}, singular values {np.array2string(o['sv'], precision=1)}")
        print(f"  zero ({o['z'][0]:.9f}, {o['z'][1]:.9f})   coefficients c0, ca, cw = {o['c'][0]:+.3f}, {o['c'][1]:+.3f}, {o['c'][2]:+.3f}")
        print(f"  standard error with J's noise: {o['se']:.2e} (A {o['se_c'][0]:.2e}, w/w_inf {o['se_c'][1]:.2e});  centre only, J fixed: bound {o['se_bound_Jfixed']:.2e}, propagated {o['se_prop_Jfixed']:.2e}")
        if "mc_std" in o:
            print(f"  bootstrap: std A {o['mc_std'][0]:.2e}, w {o['mc_std'][1]:.2e}, norm {np.linalg.norm(o['mc_std']):.2e}; robust A {o['mc_rob'][0]:.2e}, w {o['mc_rob'][1]:.2e}, norm {np.linalg.norm(o['mc_rob']):.2e}")
    if "--check_m7" in a:   # the formula against m7_outer.py --local's own print: centre = all counted centre solves, offsets = the first counted dA and dw, per radius (--mutate shifts the zero)
        import re
        ok = True
        for rad, kc, ka, kw in (("0.145", "--r145", "--dA145", "--dw145"), ("0.15", "--r150", "--dA150", "--dw150")):
            cen = [point(f, True) for f in grab(kc)]; cen = [tuple(p[2]) for p in cen if p[3] < BAR]
            oa = [point(f, True) for f in grab(ka)]; oa = [tuple(p[2]) for p in oa if p[3] < BAR][:1]
            ow = [point(f, True) for f in grab(kw)]; ow = [tuple(p[2]) for p in ow if p[3] < BAR][:1]
            zz = zero_se(cen, oa, ow, cov_fallback=np.eye(2))["z"] + (1e-5 if "--mutate" in a else 0)
            t = open(a[a.index("--check_m7") + 1 + (0 if rad == "0.145" else 1)]).read()
            m = re.search(r"zero: A ([0-9.]+), w/w_inf ([0-9.]+)", t)
            good = abs(float(m.group(1)) - zz[0]) < 6e-7 and abs(float(m.group(2)) - zz[1]) < 6e-7
            ok = ok and good
            print(f"check against m7_outer (xi1 {rad}): its zero {m.group(1)}, {m.group(2)}; formula {zz[0]:.6f}, {zz[1]:.6f}: {'ok' if good else 'FAIL'}")
        if not ok:
            return 1
    c = combine(res["0.145"], res["0.15"])
    print(f"\nDelta = Z(0.145) - Z(0.15) = (A {c['D'][0]:+.3e}, w/w_inf {c['D'][1]:+.3e}), |Delta| {c['norm']:.3e}; combined SE (quadrature) {c['comb']:.3e}")
    print(f"d = |Delta| / combined SE = {c['d']:.2f} -> {verdict(c['d'])}   (Mahalanobis {c['maha']:.2f}; per component A {c['d_comp'][0]:+.2f}, w/w_inf {c['d_comp'][1]:+.2f})")
    print(f"w/w_inf alone: {c['D'][1]:+.3e} over its combined SE {np.hypot(res['0.145']['se_c'][1], res['0.15']['se_c'][1]):.3e} = {c['d_comp'][1]:+.2f} -> {verdict(abs(c['d_comp'][1]))}")


if __name__ == "__main__":
    sys.exit(main())
