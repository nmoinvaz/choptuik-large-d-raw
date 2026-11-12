#!/usr/bin/env python3
"""#534: the second harmonic of ln sigma_1 and ln sigma_2 against the first, by window of D. Analysis only.
usage: python second_harmonic_534.py --raw=<raw worktree with I533-win2, I525-win2, ...> planted --scenario=S0|S1A|S1B|S2 [--seeds=N] [--out=FILE]
       python second_harmonic_534.py --raw=... summarize FILE...        (the planted verdict; needs S0, S1A, S1B, S2)
       python second_harmonic_534.py --raw=... data --verdict=FILE      (the real series; refuses unless FILE says VERDICT: PASS)
Model. The chirp of #533 is fitted to all 51 states (trend of degree 3 in u = (D - 228) / 10, one sinusoid, period P0 + p1 x + p2 x^2,
x = D - 228, #533's Fitter.fit_free): it gives the phase phi(D). In each window (D < 216, 216 <= D < 228, D >= 228) the series is then fitted by
least squares as
  y = quadratic in the window + A1 cos phi + B1 sin phi + A2 cos 2 phi + B2 sin 2 phi
with phi fixed. a_k = hypot(A_k, B_k), delta_k = atan2(-B_k, A_k) (a_k cos(k phi + delta_k)), ratio rho = a2 / a1, relative phase
theta = delta2 - 2 delta1 (wrapped to (-pi, pi]; it does not change if phi's origin is shifted). Errors: the delta method on the least-squares
covariance (s^2 (X^T X)^-1, s^2 the window's residual variance).
Planted truth (the same code, the whole pipeline including the global chirp fit): at the D of the data, y = cubic trend
+ a1 cos(phi_true + 0.7) + rho_w a1 cos(2 phi_true + 1.4 + 1.0) + white noise 0.006, a1 = 0.11, phi_true from P0 2.62, p1 +0.0165, p2 +0.0003.
Scenarios: S0 rho = 0, 0, 0; S1 rho = 0.066, 0.066, 0.066 (set A calibrates, set B tests); S2 rho = 0.03, 0.066, 0.12.
Rules (fixed on the issue before the real series was read): R1 coverage of rho +- 2 SE in 88% to 99% per window (S0: at least 88%);
R2 bias: S1 and S2 |median rho_hat - rho| <= 0.5 rho, S0 median <= 0.05; R3a size of the agreement statistic Q on S1B at most 10%
at the 95th percentile of S1A, R3b size on S0 at most 15%, R3c power on S2 at least 50% for the agreement statement to be resolving.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

SCEN = {"S0": (0.0, 0.0, 0.0), "S1A": (0.066,) * 3, "S1B": (0.066,) * 3, "S2": (0.03, 0.066, 0.12),
        "S0A": (0.0, 0.0, 0.0), "S0B": (0.0, 0.0, 0.0)}
SEED0 = {"S0": 1000, "S1A": 2000, "S1B": 3000, "S2": 4000, "S0A": 5000, "S0B": 6000}
A1, NOISE, TRUE_THETA, DELTA1, THETA2, DEG = 0.11, 0.006, (2.62, 0.0165, 0.0003), 0.7, 1.0, 2
EDGES = (216.0, 228.0)
NAMES = ("D < 216", "216 <= D < 228", "D >= 228")


def load_pp(raw):
    sys.path.insert(0, os.path.join(raw, "I533-win2"))
    import period_p2_533 as pp
    return pp


def masks(D):
    return [D < EDGES[0], (D >= EDGES[0]) & (D < EDGES[1]), D >= EDGES[1]]


def wrap(x):
    return (x + math.pi) % (2 * math.pi) - math.pi


def ratio_phase(b4):
    a1, a2 = math.hypot(b4[0], b4[1]), math.hypot(b4[2], b4[3])
    return a2 / a1, wrap(math.atan2(-b4[3], b4[2]) - 2 * math.atan2(-b4[1], b4[0])), a1, a2


def window_fit(pp, D, y, theta, mask, deg=DEG):
    DEG = deg
    Dw, yw = D[mask], y[mask]
    ph = pp.phase(Dw, *theta)
    xc = (Dw - Dw.mean()) / (0.5 * (Dw.max() - Dw.min()))
    X = np.column_stack([xc ** k for k in range(DEG + 1)] + [np.cos(ph), np.sin(ph), np.cos(2 * ph), np.sin(2 * ph)])
    beta = np.linalg.lstsq(X, yw, rcond=None)[0]
    e = yw - X @ beta
    dof = len(yw) - X.shape[1]
    s2 = float(e @ e) / dof
    C = s2 * np.linalg.pinv(X.T @ X)
    k = DEG + 1
    b4, C4 = beta[k:k + 4], C[k:k + 4, k:k + 4]
    rho, th, a1, a2 = ratio_phase(b4)
    g_r, g_t = np.zeros(4), np.zeros(4)
    for j in range(4):
        d = np.zeros(4)
        d[j] = 1e-6 * max(1.0, abs(b4[j]))
        rp, tp, _, _ = ratio_phase(b4 + d)
        rm, tm, _, _ = ratio_phase(b4 - d)
        g_r[j] = (rp - rm) / (2 * d[j])
        g_t[j] = wrap(tp - tm) / (2 * d[j])
    return dict(n=int(mask.sum()), rho=rho, se_rho=math.sqrt(max(g_r @ C4 @ g_r, 0)), theta=th,
                se_theta=math.sqrt(max(g_t @ C4 @ g_t, 0)), a1=a1, a2=a2, rms=math.sqrt(s2 * dof / len(yw)),
                fitted=X @ beta, X=X, beta=beta, dof=dof, s2=s2, C4=C4, b4=b4)


def pipeline(pp, F, D, y, theta=None):
    if theta is None:
        best, f0 = F.fit_free(y)
        theta = best["theta"]
    return theta, [window_fit(pp, D, y, theta, m) for m in masks(D)]


def qstat(rows):
    r = np.array([w["rho"] for w in rows])
    s = np.array([w["se_rho"] for w in rows])
    wt = 1.0 / s ** 2
    rb = float((wt * r).sum() / wt.sum())
    return float((wt * (r - rb) ** 2).sum()), rb


def planted_y(pp, D, rho_by_window, rng):
    ph = pp.phase(D, *TRUE_THETA)
    u = (D - 228.0) / 10.0
    y = 0.08 * u + 0.05 * u ** 2 - 0.087 * u ** 3 + A1 * np.cos(ph + DELTA1)
    rv = np.zeros(len(D))
    for m, r in zip(masks(D), rho_by_window):
        rv[m] = r
    y = y + rv * A1 * np.cos(2 * ph + 2 * DELTA1 + THETA2)
    return y + rng.normal(0, NOISE, len(D))


def cmd_planted(pp, scen, nseeds, out):
    D, _ = pp.collect51()
    F = pp.Fitter(D, 3)
    recs, t0 = [], time.time()
    for s in range(nseeds):
        rng = np.random.default_rng(SEED0[scen] + s)
        y = planted_y(pp, D, SCEN[scen], rng)
        theta, rows = pipeline(pp, F, D, y)
        q, rb = qstat(rows)
        recs.append(dict(seed=SEED0[scen] + s, theta=[float(x) for x in theta], q=q, rho_bar=rb,
                         rho=[w["rho"] for w in rows], se_rho=[w["se_rho"] for w in rows],
                         th=[w["theta"] for w in rows], se_th=[w["se_theta"] for w in rows], rms=[w["rms"] for w in rows]))
        if (s + 1) % 10 == 0 or s == 0:
            print(f"{scen}: {s + 1}/{nseeds} seeds, {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(scenario=scen, rho_true=SCEN[scen], n=[int(m.sum()) for m in masks(D)], records=recs), open(out, "w"))
    print(f"{scen}: wrote {out} ({nseeds} seeds, {time.time() - t0:.0f} s)")


def cmd_summarize(files):
    R = {}
    for f in files:
        d = json.load(open(f))
        R[d["scenario"]] = d
    need = {"S0", "S1A", "S1B", "S2"}
    if not need <= set(R):
        sys.exit(f"missing scenarios {need - set(R)}")
    ok = True
    print(f"states per window {R['S0']['n']}; seeds per scenario {[(k, len(R[k]['records'])) for k in sorted(R)]}")
    print("\nR1/R2: coverage of rho +- 2 SE (88% to 99%) and bias of the median (S1, S2: |median - rho| <= 0.5 rho; S0: median <= 0.05)")
    print("| scenario | window | rho true | median rho_hat | median SE | coverage of +-2 SE | R1 | R2 |\n|---|---|---|---|---|---|---|---|")
    for k in ("S0", "S1B", "S2"):
        rec = R[k]["records"]
        for w in range(3):
            rt = R[k]["rho_true"][w]
            r = np.array([x["rho"][w] for x in rec])
            s = np.array([x["se_rho"][w] for x in rec])
            cov = float(np.mean(np.abs(r - rt) <= 2 * s))
            med = float(np.median(r))
            r1 = (0.88 <= cov <= 0.99) if k != "S0" else cov >= 0.88
            r2 = (med <= 0.05) if k == "S0" else (abs(med - rt) <= 0.5 * rt)
            ok = ok and r1 and r2
            print(f"| {k} | {NAMES[w]} | {rt:.3f} | {med:.3f} | {np.median(s):.3f} | {100 * cov:.0f}% | {'pass' if r1 else 'FAIL'} | {'pass' if r2 else 'FAIL'} |")
    qa = np.array([x["q"] for x in R["S1A"]["records"]])
    crit = float(np.percentile(qa, 95))
    size1 = float(np.mean([x["q"] > crit for x in R["S1B"]["records"]]))
    size0 = float(np.mean([x["q"] > crit for x in R["S0"]["records"]]))
    power = float(np.mean([x["q"] > crit for x in R["S2"]["records"]]))
    r3a, r3b, r3c = size1 <= 0.10, size0 <= 0.15, power >= 0.50
    ok = ok and r3a and r3b
    print(f"\nR3: the agreement statistic Q (inverse-variance spread of the three rho): critical value {crit:.2f} = 95th percentile of S1A")
    print(f"size on S1B (equal rho = 0.066) {100 * size1:.0f}% (R3a: at most 10%: {'pass' if r3a else 'FAIL'}); "
          f"on S0 (equal rho = 0) {100 * size0:.0f}% (R3b: at most 15%: {'pass' if r3b else 'FAIL'})")
    print(f"power on S2 (rho 0.03, 0.066, 0.12) {100 * power:.0f}% (R3c: at least 50% for the agreement statement to be resolving: "
          f"{'pass' if r3c else 'NOT RESOLVING'})")
    cov_t = ", ".join(f"{100 * np.mean([abs(wrap(x['th'][w] - THETA2)) <= 2 * x['se_th'][w] for x in R['S1B']['records']]):.0f}%" for w in range(3))
    print(f"\ntheta (relative phase, planted {THETA2} rad), S1B: median "
          + ", ".join(f"{np.median([x['th'][w] for x in R['S1B']['records']]):.2f}" for w in range(3)) + f"; coverage of +-2 SE per window: {cov_t} (information, no rule)")
    print(f"\nVERDICT: {'PASS' if ok else 'FAIL'} (R1, R2, R3a, R3b); agreement statement "
          f"{'resolving' if r3c else 'NOT resolving (power below 50%)'}; Q critical value {crit:.3f}")
    return ok


def cmd_summarize2(files):
    """v2 rules (R1 for S0 replaced by a calibrated detection threshold on z = rho_hat / SE; everything else as v1), on fresh S0A, S0B seeds."""
    R = {}
    for f in files:
        d = json.load(open(f))
        R[d["scenario"]] = d
    need = {"S0A", "S0B", "S1A", "S1B", "S2"}
    if not need <= set(R):
        sys.exit(f"missing scenarios {need - set(R)}")
    ok = True
    z = lambda k, w: np.array([x["rho"][w] / x["se_rho"][w] for x in R[k]["records"]])
    zc = [float(np.percentile(z("S0A", w), 95)) for w in range(3)]
    print(f"states per window {R['S1A']['n']}; seeds per scenario {[(k, len(R[k]['records'])) for k in sorted(R)]}")
    print(f"\nR1' (replaces R1 for S0): detection threshold z_crit = 95th percentile of z = rho_hat / SE on S0A, per window: {', '.join(f'{c:.2f}' for c in zc)}")
    print("| scenario | window | rho true | median rho_hat | median SE | coverage of +-2 SE | detection rate (z > z_crit) | R1 / R1' | R2 |\n|---|---|---|---|---|---|---|---|---|")
    for k in ("S0B", "S1B", "S2"):
        rec = R[k]["records"]
        for w in range(3):
            rt = R[k]["rho_true"][w]
            r = np.array([x["rho"][w] for x in rec])
            s = np.array([x["se_rho"][w] for x in rec])
            cov = float(np.mean(np.abs(r - rt) <= 2 * s))
            det = float(np.mean(z(k, w) > zc[w]))
            med = float(np.median(r))
            if k == "S0B":
                r1 = det <= 0.10
            else:
                r1 = 0.88 <= cov <= 0.99
            r2 = (med <= 0.05) if k == "S0B" else (abs(med - rt) <= 0.5 * rt)
            ok = ok and r1 and r2
            print(f"| {k} | {NAMES[w]} | {rt:.3f} | {med:.3f} | {np.median(s):.3f} | {100 * cov:.0f}% | {100 * det:.0f}% | {'pass' if r1 else 'FAIL'} | {'pass' if r2 else 'FAIL'} |")
    qa = np.array([x["q"] for x in R["S1A"]["records"]])
    crit = float(np.percentile(qa, 95))
    size1 = float(np.mean([x["q"] > crit for x in R["S1B"]["records"]]))
    size0 = float(np.mean([x["q"] > crit for x in R["S0B"]["records"]]))
    power = float(np.mean([x["q"] > crit for x in R["S2"]["records"]]))
    r3a, r3b, r3c = size1 <= 0.10, size0 <= 0.15, power >= 0.50
    ok = ok and r3a and r3b
    print(f"\nR3: Q critical value {crit:.2f} = 95th percentile of S1A; size on S1B {100 * size1:.0f}% (R3a, at most 10%: {'pass' if r3a else 'FAIL'}); "
          f"on S0B {100 * size0:.0f}% (R3b, at most 15%: {'pass' if r3b else 'FAIL'}); power on S2 {100 * power:.0f}% (R3c, at least 50%: {'pass' if r3c else 'NOT RESOLVING'})")
    print(f"\nVERDICT: {'PASS' if ok else 'FAIL'} (R1, R1', R2, R3a, R3b); agreement statement {'resolving' if r3c else 'NOT resolving (power below 50%)'}; "
          f"Q critical value {crit:.3f}; z_crit {', '.join(f'{c:.3f}' for c in zc)}")
    return ok


def cmd_data(pp, verdict, boot=1000):
    import re
    txt = open(verdict).read()
    vline = [ln for ln in txt.splitlines() if ln.startswith("VERDICT:")]
    if not vline or not vline[0].startswith("VERDICT: PASS"):
        sys.exit(f"{verdict} does not say VERDICT: PASS; the real series is not read")
    zc = [float(x) for x in re.search(r"z_crit ([\d.]+), ([\d.]+), ([\d.]+)", vline[0]).groups()]
    qcrit = float(re.search(r"Q critical value ([\d.]+);", vline[0]).group(1))
    resolving = "agreement statement resolving" in vline[0]
    D, Y = pp.collect51()
    F = pp.Fitter(D, 3)
    ms = masks(D)
    print(f"{len(D)} states D {D[0]:.2f} to {D[-1]:.2f}; windows {[int(m.sum()) for m in ms]}; planted verdict file {verdict}: z_crit {zc}, Q critical value {qcrit}, "
          f"agreement statement {'resolving' if resolving else 'NOT resolving'}; {boot} bootstrap trials")
    rec = {}
    for i in (1, 2):
        y = Y[:, i - 1]
        best, f0 = F.fit_free(y)
        print(f"\n=== ln sigma_{i}: global chirp (p2 chirp, cubic trend) P0 {best['theta'][0]:.3f}, p1 {best['theta'][1]:+.4f}, p2 {best['theta'][2]:+.5f}, rms {math.sqrt(best['ss'] / len(D)):.4f}")
        for tag, th in (("phase of the p2 chirp (the main)", best["theta"]), ("sensitivity: phase of the p2 = 0 chirp", f0["theta"])):
            rows = [window_fit(pp, D, y, th, m) for m in ms]
            q, rb = qstat(rows)
            print(f"\n{tag}: P0 {th[0]:.3f}, p1 {th[1]:+.4f}, p2 {th[2]:+.5f}")
            print("| window | states | rms | a1 | a2 | ratio rho +- SE | z = rho/SE (z_crit) | second harmonic | theta +- SE (rad) | bootstrap rho 16-50-84% | bootstrap theta 16-50-84% |\n|---|---|---|---|---|---|---|---|---|---|---|")
            for w, (m, wf) in enumerate(zip(ms, rows)):
                rng = np.random.default_rng(7000 + 10 * i + w)
                bs_r, bs_t = [], []
                for _ in range(boot):
                    yb = y.copy()
                    yb[m] = wf["fitted"] + rng.normal(0, math.sqrt(wf["s2"]), int(m.sum()))
                    wb = window_fit(pp, D, yb, th, m)
                    bs_r.append(wb["rho"])
                    bs_t.append(wrap(wb["theta"] - wf["theta"]) + wf["theta"])
                pr, pt = np.percentile(bs_r, [16, 50, 84]), np.percentile(bs_t, [16, 50, 84])
                zz = wf["rho"] / wf["se_rho"]
                det = "detected" if zz > zc[w] else "not detected"
                print(f"| {NAMES[w]} | {wf['n']} | {wf['rms']:.4f} | {wf['a1']:.4f} | {wf['a2']:.4f} | {wf['rho']:.3f} +- {wf['se_rho']:.3f} | {zz:.2f} ({zc[w]:.2f}) | {det} | {wf['theta']:+.2f} +- {wf['se_theta']:.2f} | "
                      f"{pr[0]:.3f} {pr[1]:.3f} {pr[2]:.3f} | {pt[0]:+.2f} {pt[1]:+.2f} {pt[2]:+.2f} |", flush=True)
                if tag.startswith("phase of the p2 chirp"):
                    rec[f"sigma_{i}_w{w}"] = dict(n=wf["n"], rho=wf["rho"], se_rho=wf["se_rho"], theta=wf["theta"], se_theta=wf["se_theta"], z=zz, detected=bool(zz > zc[w]),
                                                  a1=wf["a1"], a2=wf["a2"], rms=wf["rms"], boot_rho=[float(x) for x in pr], boot_theta=[float(x) for x in pt])
            verdict_txt = "the windows' ratios DISAGREE (Q above the critical value)" if q > qcrit else "the windows' ratios AGREE within their errors (Q at or below the critical value)"
            print(f"Q = {q:.2f} against the critical value {qcrit:.2f} (95th percentile on S1A), inverse-variance mean ratio {rb:.3f}: {verdict_txt}"
                  + ("" if resolving else "; NOT resolving"), flush=True)
            if tag.startswith("phase of the p2 chirp"):
                rec[f"sigma_{i}_Q"] = dict(q=q, rho_bar=rb, crit=qcrit, agree=bool(q <= qcrit))
        wg = window_fit(pp, D, y, best["theta"], np.ones(len(D), bool), deg=3)
        print(f"\nall 51 states with a cubic trend (the cross-check with #525's M2h by-product, 0.0074 against 0.112, ratio 0.066): a1 {wg['a1']:.4f}, a2 {wg['a2']:.4f}, "
              f"ratio {wg['rho']:.3f} +- {wg['se_rho']:.3f}, theta {wg['theta']:+.2f} +- {wg['se_theta']:.2f}")
    json.dump(rec, open("results_534.json", "w"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("cmd", choices=["planted", "summarize", "summarize2", "data"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--scenario", default="S1A")
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--out", default=None)
    ap.add_argument("--verdict", default=None)
    a = ap.parse_args()
    pp = load_pp(a.raw)
    if a.cmd == "planted":
        cmd_planted(pp, a.scenario, a.seeds, a.out or f"planted_534_{a.scenario}.json")
    elif a.cmd == "summarize":
        sys.exit(0 if cmd_summarize(a.files) else 1)
    elif a.cmd == "summarize2":
        sys.exit(0 if cmd_summarize2(a.files) else 1)
    else:
        if not a.verdict:
            sys.exit("data needs --verdict=<the planted summary file>")
        cmd_data(pp, a.verdict)
