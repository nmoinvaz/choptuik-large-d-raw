"""#1028 reading: the scatter of M = 9's corrected r_1 over seeded starts at one (A, w/w_inf), and the issue's decision.

    python m9_seeded_std.py --seeded LOG [LOG ...] [--other LABEL=LOG ...] [--sigma_min 1.03e10] [--ref 7.7e5]
    python m9_seeded_std.py --selftest [--mutate=ddof0|thresholds|labels|dropcomp]

--seeded: the logs whose r_1 (the FIXED-A line's re, im) enter the statistic (stage 1 and the four seeded repeats). --other: listed beside them, not in the statistic (zero_repeat, unseeded).
Statistic (README of this folder, fixed before the data): the sample std (ddof 1) of each component, combined in norm as sqrt(std_re^2 + std_im^2), the definition of the fixed-x noise 7.7e5 (noise_analyze.py).
With n values the std per component lies within [sqrt(df / chi2_95), sqrt(df / chi2_05)] x the measured one at 90% (df = n - 1; Gaussian assumed); for n = 5, [0.65, 2.37].
Decision (the issue's): std_norm <= 1e6: error about std / sigma_min(J) (7.5e-5 with #1012's sigma_min 1.03e10), the 1e-4 rule is not triggered; std_norm >= 2e6: start scatter governs, error about 2.7e-4,
M = 9 not reachable at this radius in double; in between: reported, the coordinator decides.
--selftest: planted Gaussian r_1 (5 values per trial, 4000 trials): the mean of the sample variance equals the planted one within 5% (ddof 1), the 90% interval covers the planted std in 85-95% of the trials,
the thresholds' edges (0.99e6, 1.5e6, 2.01e6) decide as the issue says, the decision is 'not triggered' for a planted norm 0.5e6 in at least 80% of the trials and 'not reachable' for 3e6 in at least 80%; --mutate=ddof0 (biased variance), --mutate=thresholds (the two thresholds exchanged), --mutate=labels (the two branch labels exchanged)
and --mutate=dropcomp (the imaginary component left out of the norm) must each fail."""
import re, sys
import numpy as np

CHI2 = {1: (0.00393, 3.841), 2: (0.1026, 5.991), 3: (0.3518, 7.815), 4: (0.7107, 9.488), 5: (1.145, 11.07), 6: (1.635, 12.59), 7: (2.167, 14.07), 8: (2.733, 15.51)}   # chi2 0.05 and 0.95 quantiles
LO, HI = 1e6, 2e6


def r1_of(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"FIXED-A M \d+: A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", t)
    if not m:
        return None
    ends = {}
    for k in (3, 5, 7, 9):
        mm = re.findall(rf"r_{k} (\S+)", t[m.end():]) if k != 3 else re.findall(r"level 3 solved: \|r_3\| (\S+)", t)
        ends[k] = mm[-1] if mm else "?"
    return (float(m.group(1)), float(m.group(2))), np.array([float(m.group(3)), float(m.group(4))]), ends


def scatter(R, mut=None):
    R = np.asarray(R, float)
    ddof = 0 if mut == "ddof0" else 1
    s = R.std(axis=0, ddof=ddof)
    snorm = s[0] if mut == "dropcomp" else float(np.hypot(*s))
    return s, snorm


def decide(snorm, mut=None):
    lo, hi = (HI, LO) if mut == "thresholds" else (LO, HI)
    a, b = ("not reachable", "not triggered") if mut == "labels" else ("not triggered", "not reachable")
    if snorm <= lo:
        return a
    if snorm >= hi:
        return b
    return "between"


def interval(s, n):
    a, b = CHI2[n - 1]
    return np.sqrt((n - 1) / b) * s, np.sqrt((n - 1) / a) * s


def selftest(mut):
    rng = np.random.default_rng(1028)
    ok = True
    edges = [(0.99e6, "not triggered"), (1.5e6, "between"), (2.01e6, "not reachable")]       # the issue's thresholds, deterministic
    bad = [(v, w, decide(v, mut)) for v, w in edges if decide(v, mut) != w]
    print(f"threshold edges {[(v, w) for v, w in edges]}: " + ("ok" if not bad else f"FAIL {bad}"))
    ok = ok and not bad
    for sig_norm, want in ((0.5e6, "not triggered"), (3e6, "not reachable")):
        sc = sig_norm / np.sqrt(2.0)                        # per component
        var, cover, dec = [], 0, 0
        N = 4000
        for _ in range(N):
            R = rng.normal(0, sc, size=(5, 2))
            s, sn = scatter(R, mut)
            var.append(s[1] ** 2)
            lo, hi = interval(s[1], 5)
            cover += lo <= sc <= hi
            dec += decide(sn, mut) == want
        bias = np.mean(var) / sc ** 2
        good = abs(bias - 1) < 0.05 and 0.85 < cover / N < 0.95 and dec / N >= 0.80
        # dropcomp leaves the norm at one component: its decision share at the planted norm falls (3e6 branch) and the bias check cannot see it, so test the norm directly as well
        _, sn1 = scatter(rng.normal(0, sc, size=(2000, 2)), mut)
        good = good and abs(sn1 / sig_norm - 1) < 0.06
        print(f"planted norm {sig_norm:.1e}: mean s^2 / sigma^2 {bias:.3f}, 90% interval covers {cover / N:.3f}, decision '{want}' in {dec / N:.3f} of the trials, large-sample norm / planted {sn1 / sig_norm:.3f} -> {'ok' if good else 'FAIL'}")
        ok = ok and good
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest(next((x.split("=")[1] for x in a if x.startswith("--mutate=")), None)))
    seeded, other = [], []
    i = 0
    while i < len(a):
        if a[i] == "--seeded":
            i += 1
            while i < len(a) and not a[i].startswith("--"):
                seeded.append(a[i]); i += 1
        elif a[i] == "--other":
            i += 1
            while i < len(a) and not a[i].startswith("--"):
                other.append(a[i]); i += 1
        else:
            i += 2 if a[i] in ("--sigma_min", "--ref") else 1
    g = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
    smin, ref = g("--sigma_min", 1.03e10), g("--ref", 7.7e5)
    rows, vals = [], []
    for p in seeded:
        r = r1_of(p)
        name = p.replace("\\", "/").split("/")[-1].replace("hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4", "")
        rows.append((name, r))
        if r is not None:
            vals.append(r[1])
    print("| run | (A, w/w_inf) | r_1 re | r_1 im | r_1 - stage 1 | end r_3, r_5, r_7, r_9 |\n|---|---|---|---|---|---|")
    base = next((r[1] for _, r in rows if r is not None), None)
    for name, r in rows + [(o.split("=", 1)[0], r1_of(o.split("=", 1)[1])) for o in other]:
        if r is None:
            print(f"| {name} | no FIXED-A line (capped or failed) | | | | |")
            continue
        d = r[1] - base
        print(f"| {name} | {r[0][0]:.6f}, {r[0][1]:.6f} | {r[1][0]:+.4e} | {r[1][1]:+.4e} | {d[0]:+.2e} {d[1]:+.2e}i ({np.linalg.norm(d):.2e}) | {r[2][3]}, {r[2][5]}, {r[2][7]}, {r[2][9]} |")
    n = len(vals)
    if n < 2:
        sys.exit("fewer than two seeded values: no scatter")
    s, sn = scatter(vals)
    lo, hi = interval(s, n)
    print(f"\nseeded values n = {n}: std per component {s[0]:.3e} (re), {s[1]:.3e} (im); in norm {sn:.3e} (the fixed-x noise: {ref:.1e}, same definition)")
    print(f"90% interval of the true std per component (df {n - 1}, Gaussian assumed): re [{lo[0]:.2e}, {hi[0]:.2e}], im [{lo[1]:.2e}, {hi[1]:.2e}]; norm of the interval ends [{np.hypot(*lo):.2e}, {np.hypot(*hi):.2e}]")
    print(f"error implied: std_norm / sigma_min(J) = {sn / smin:.2e} (sigma_min {smin:.2e}; #1012: 7.5e-5 at 7.7e5, 2.7e-4 at 2.79e6)")
    print(f"decision (<= {LO:.0e} not triggered, >= {HI:.0e} not reachable): {decide(sn)}")


if __name__ == "__main__":
    main()
