"""#1012 last stage: the slope of the corrected r_1 in (A, w/w_inf) at M = 9 from the M = 7 protocol's solves, and the error the r_1 noise induces through it.

    python m9_outer.py --centre LOG [LOG ...] --dA LOG --dw LOG [--sigma 7.7e5] [--dA_step 2e-4 --dw_step 1e-4]
    python m9_outer.py --selftest [--mutate=sign]

The arithmetic is m7_outer.py local()'s, without its |r_3| < 1e-6 bar (M = 9 cannot meet it): r_0 = the mean of the centre solves' r_1; J = [(r_a - r_0)/dA, (r_w - r_0)/dw] with r_1 as (re, im);
the zero is (A, w) of the centre point plus -J^-1 r_0; the half-range of the centre solves is m7_outer's `noise`; --sigma is the std of the corrected r_1 measured at a fixed x (noise_r5.py), a norm.
Reported: J, its singular values, the Newton step, the error noise / sigma_min(J) for both noises (and m7_outer's two-term estimate), and the SIGNIFICANCE of the offsets' responses: |r_a - r_0| / sigma
and |r_w - r_0| / sigma; a response below 3 sigma means J is not resolved at these offsets and the induced error is at least the offset itself.
--selftest plants J0 and a zero z0, draws r_1 = J0 (p - z0) + gaussian noise at a high and at a low signal-to-noise ratio, and requires: J recovered to 5% when the response is 100 sigma, the significance flag
raised and the induced-error floor equal to the offset when the response is 0.5 sigma; --mutate=sign flips the sign of one offset in the fit, which must fail the recovery."""
import re, sys
import numpy as np


def r1_of(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"FIXED-A M \d+: A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", t)
    if not m:
        sys.exit(f"{path}: no FIXED-A line")
    return np.array([float(m.group(1)), float(m.group(2))]), np.array([float(m.group(3)), float(m.group(4))])


def analyse(p0, R_centre, pa, ra, pw, rw, dA, dw, sigma=None, flip=False):
    R = np.array(R_centre)
    r0 = R.mean(axis=0)
    noise_half = 0.5 * float(np.ptp(R, axis=0).max()) if len(R) > 1 else float("nan")
    sa, sw = (-1.0 if flip else 1.0) * dA, dw
    J = np.column_stack([(ra - r0) / sa, (rw - r0) / sw])
    sv = np.linalg.svd(J, compute_uv=False)
    step = -np.linalg.solve(J, r0)
    z = p0 + step
    hmin = min(abs(dA), abs(dw))
    out = dict(r0=r0, J=J, sv=sv, step=step, zero=z, noise_half=noise_half)
    out["err_m7"] = (noise_half / sv[-1] + np.linalg.norm(step) * 2 * noise_half / (sv[-1] * hmin)) if len(R) > 1 else float("nan")
    out["err_half"] = noise_half / sv[-1]
    if sigma is not None:
        out["err_sigma"] = sigma / sv[-1]
        out["snr_A"], out["snr_w"] = np.linalg.norm(ra - r0) / sigma, np.linalg.norm(rw - r0) / sigma
        out["resolved"] = min(out["snr_A"], out["snr_w"]) >= 3.0
        out["err_floor"] = sigma / (np.linalg.norm(ra - r0) / dA) if not out["resolved"] else None   # sigma over the largest slope the (unresolved) response allows
    return out


def selftest(mut):
    rng = np.random.default_rng(1012)
    J0 = np.array([[1.2e4, -3.0e3], [2.0e3, 5.7e3]])
    p0 = np.array([2.719219, 1.000022]); z0 = p0 + np.array([3e-5, -1e-5])
    dA, dw = 2e-4, 1e-4
    ok = True
    for sig, label in ((1.0, "response 100 sigma"), (1e5, "response 0.5 sigma")):
        sg = sig * np.array([1.0, 1.0])
        # response to dA is about |J0[:,0]| dA = 2.5; choose the noise so that the ratio matches the label
        scale = np.linalg.norm(J0[:, 0]) * dA / (100.0 if sig == 1.0 else 0.5)
        noise = lambda: rng.normal(0, scale / np.sqrt(2), size=2)
        f = lambda p: J0 @ (p - z0) + noise()
        Rc = [f(p0), f(p0)]
        ra, rw = f(p0 + np.array([dA, 0])), f(p0 + np.array([0, dw]))
        out = analyse(p0, Rc, p0 + np.array([dA, 0]), ra, p0 + np.array([0, dw]), rw, dA, dw, sigma=scale, flip=mut)
        err = np.abs(out["J"] - J0).max() / np.abs(J0).max()
        if label.startswith("response 100"):
            good = err < 0.05 and out["resolved"]
        else:
            good = (not out["resolved"]) and err > 0.05
        print(f"planted ({label}): max relative error of J {err:.2e}, snr {out['snr_A']:.1f} and {out['snr_w']:.1f}, resolved {out['resolved']}  -> {'ok' if good else 'FAIL'}")
        ok = ok and good
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest("--mutate=sign" in a))
    g = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    cen = []
    i = a.index("--centre") + 1
    while i < len(a) and not a[i].startswith("--"):
        cen.append(a[i]); i += 1
    dA, dw = float(g("--dA_step", 2e-4)), float(g("--dw_step", 1e-4))
    sigma = float(g("--sigma")) if g("--sigma") else None
    pc = [r1_of(f) for f in cen]
    p0 = pc[0][0]
    pa, ra = r1_of(g("--dA")); pw, rw = r1_of(g("--dw"))
    assert abs(pa[0] - p0[0] - dA) < 1e-9 and abs(pw[1] - p0[1] - dw) < 1e-9, f"the offsets in the logs are {pa[0] - p0[0]:.2e} and {pw[1] - p0[1]:.2e}"
    out = analyse(p0, [r for _, r in pc], pa, ra, pw, rw, dA, dw, sigma)
    print(f"centre solves {len(pc)}: r_1 " + "; ".join(f"{r[0]:+.4e}{r[1]:+.4e}i" for _, r in pc) + f"; mean {out['r0'][0]:+.4e}{out['r0'][1]:+.4e}i; half-range noise {out['noise_half']:.3e}")
    print(f"dA solve r_1 {ra[0]:+.4e}{ra[1]:+.4e}i (offset {dA:g}); dw solve r_1 {rw[0]:+.4e}{rw[1]:+.4e}i (offset {dw:g})")
    print(f"J (rows re, im; columns A, w/w_inf) = {out['J'].tolist()}; singular values {out['sv'][0]:.3e}, {out['sv'][1]:.3e}")
    print(f"Newton step to the zero ({out['step'][0]:+.3e}, {out['step'][1]:+.3e}) -> zero A {out['zero'][0]:.6f}, w/w_inf {out['zero'][1]:.6f}")
    print(f"error from the centre solves' half-range: noise / sigma_min = {out['err_half']:.3e}; m7_outer's two-term estimate {out['err_m7']:.3e}")
    if sigma is not None:
        print(f"error from sigma {sigma:.2e} (the fixed-x std): sigma / sigma_min(J) = {out['err_sigma']:.3e}")
        print(f"significance of the offsets' responses (|dr| / sigma): A {out['snr_A']:.2f}, w {out['snr_w']:.2f}; J resolved at these offsets: {out['resolved']}")
        if not out["resolved"]:
            print(f"J is NOT resolved: the induced error is at least the offsets themselves (A {dA:g}, w/w_inf {dw:g}); sigma over the slope the response allows: {out['err_floor']:.3e}")


if __name__ == "__main__":
    main()
