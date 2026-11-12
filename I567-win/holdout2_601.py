#!/usr/bin/env python3
"""#601: #533's chirp hold-outs for ln sigma_1 and ln sigma_2 with the second harmonic in the waveform. Analysis only.
usage: python holdout2_601.py --raw=<raw worktree with I533-win2, I525-win2, ...> planted --scenario=P1|P2|P3 [--seeds=N] [--out=FILE]
       python holdout2_601.py --raw=... summarize FILE...        (the planted verdict; needs P1 and P2, P3 is information)
       python holdout2_601.py --raw=... data --verdict=FILE      (the real series; refuses unless FILE's VERDICT line says PASS)
Model. y = trend(u) + A1 cos phi + B1 sin phi + A2 cos 2 phi + B2 sin 2 phi, u = (D - 228) / 10, trend of degree 3, phi(D) = 2 pi int_228^D dD' / P(D'),
P = P0 + p1 x + p2 x^2 (x = D - 228); the six linear parameters by least squares, (P0, p1, p2) by Nelder-Mead from the single-harmonic fits of #533's Fitter
(its grid best, then p2 = 0, +-0.0005). rho = a2 / a1, theta = delta2 - 2 delta1 (a_k cos(k phi + delta_k)), as in #534.
Hold-outs exactly as #533: H1 fits D <= 232.7 (42 states) and predicts D 233.13 to 237.13 (9); H2 fits D >= 214 (43) and predicts D 210.13 to 213.63 (8). Three models for
each: the p2 chirp (free P0, p1, p2), the p2 = 0 chirp, and the control p1 = p2 = 0 (a constant period, P0 on a grid then polished). The single-harmonic results are
those of #533's own holdouts() on the same series.
Planted truth (the same code, the whole pipeline, the 51 D of the data): y = cubic trend + a1 cos(phi_true + 0.7) + rho a1 cos(2 phi_true + 1.4 + theta_true) + white noise, a1 = 0.11,
rho = 0.065, phi_true from P0 2.62, p1 +0.0165, p2 +0.0003. P1: theta_true 0 (sigma_1-like), noise 0.003. P2: theta_true pi (sigma_2-like), noise 0.003. P3: as P1 at noise 0.006
(information, no rule). 200 seeds per scenario.
Rules (fixed on the issue before the real series was read), on P1 and P2:
  PR1 recovery, the 2-harmonic fit to all 51 states: median |P0 - 2.62| <= 0.02, median |p1 - 0.0165| <= 0.003, median rho_hat in [0.049, 0.081], median |theta_hat - theta_true| <= 0.25 rad.
  PR2 the 2-harmonic p2 chirp predicts at most 0.014 (rms) in at least 80% of seeds, in H1 and in H2.
  PR3 the 2-harmonic control p1 = p2 = 0 predicts worse (larger rms) than the 2-harmonic p2 chirp in at least 90% of seeds, in H1 and in H2.
  PR4 the median prediction rms of the 2-harmonic p2 chirp is below that of the 1-harmonic p2 chirp, in H1 and in H2.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

SEED0 = {"P1": 11000, "P2": 12000, "P3": 13000}
SCEN = {"P1": dict(theta=0.0, noise=0.003), "P2": dict(theta=math.pi, noise=0.003), "P3": dict(theta=0.0, noise=0.006)}
A1, RHO, TRUE, DELTA1, DEG, LIMIT = 0.11, 0.065, (2.62, 0.0165, 0.0003), 0.7, 3, 0.014
HOLD = (("H1", lambda D: D <= 232.7, lambda D: D > 232.7), ("H2", lambda D: D >= 214.0, lambda D: D < 214.0))


def load_pp(raw):
    sys.path.insert(0, os.path.join(raw, "I533-win2"))
    import period_p2_533 as pp
    return pp


def wrap(x):
    return (x + math.pi) % (2 * math.pi) - math.pi


def cols2(pp, D, ph):
    u = (D - pp.D0) / 10.0
    return np.column_stack([u ** k for k in range(DEG + 1)] + [np.cos(ph), np.sin(ph), np.cos(2 * ph), np.sin(2 * ph)])


def ss2(pp, th, D, y):
    ph = pp.phase(D, th[0], th[1], th[2])
    if ph is None:
        return 1e9
    X = cols2(pp, D, ph)
    e = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
    return float(e @ e)


def lin2(pp, D, y, th):
    X = cols2(pp, D, pp.phase(D, *th))
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ beta
    return beta, float(e @ e)


def predict2(pp, Dte, D, y, th):
    beta, _ = lin2(pp, D, y, th)
    return cols2(pp, Dte, pp.phase(Dte, *th)) @ beta


def harmonics(beta):
    k = DEG + 1
    A1_, B1_, A2_, B2_ = beta[k:k + 4]
    return math.hypot(A2_, B2_) / math.hypot(A1_, B1_), wrap(math.atan2(-B2_, A2_) - 2 * math.atan2(-B1_, A1_))


def fit2(pp, D, y, starts, free_p2=True):
    best = None
    for s in starts:
        for p2 in ((s[2], 0.0, 0.0005, -0.0005) if free_p2 else (0.0,)):
            if free_p2:
                x, f = pp.nm(lambda th: ss2(pp, th, D, y), [s[0], s[1], p2], [0.03, 0.004, 0.0004])
                x = np.array(x)
            else:
                x2, f = pp.nm(lambda th: ss2(pp, [th[0], th[1], 0.0], D, y), [s[0], s[1]], [0.03, 0.004])
                x = np.array([x2[0], x2[1], 0.0])
            if best is None or f < best["ss"]:
                best = dict(theta=x, ss=f)
    return best


def fit2_const(pp, D, y):
    grid = np.arange(1.5, 3.5001, 0.01)
    ssg = [ss2(pp, [P, 0.0, 0.0], D, y) for P in grid]
    P0 = float(grid[int(np.argmin(ssg))])
    x, f = pp.nm(lambda th: ss2(pp, [th[0], 0.0, 0.0], D, y), [P0], [0.02])
    return dict(theta=np.array([x[0], 0.0, 0.0]), ss=f)


def holdouts2(pp, D, y):
    out = {}
    for tag, trf, tef in HOLD:
        tr, te = trf(D), tef(D)
        Dtr, ytr = D[tr], y[tr]
        F = pp.Fitter(Dtr, DEG)
        b1, f01 = F.fit_free(ytr)
        cst1 = F.const(ytr)
        starts = [b1["theta"], f01["theta"]]
        models = {"p2 chirp": fit2(pp, Dtr, ytr, starts), "p2 = 0 chirp": fit2(pp, Dtr, ytr, starts, free_p2=False), "p1 = p2 = 0": fit2_const(pp, Dtr, ytr)}
        row = {"2h": {}, "1h": {}}
        for name, fit in models.items():
            e = y[te] - predict2(pp, D[te], Dtr, ytr, fit["theta"])
            row["2h"][name] = (math.sqrt(float(np.mean(e ** 2))), float(np.max(np.abs(e))), [float(v) for v in fit["theta"]])
        for name, th in (("p2 chirp", b1["theta"]), ("p2 = 0 chirp", f01["theta"]), ("p1 = p2 = 0", cst1["theta"])):
            e = y[te] - pp.predict(D[te], Dtr, ytr, DEG, th)
            row["1h"][name] = (math.sqrt(float(np.mean(e ** 2))), float(np.max(np.abs(e))), [float(v) for v in th])
        out[tag] = (row, int(tr.sum()), int(te.sum()))
    return out


def full_fit(pp, D, y):
    F = pp.Fitter(D, DEG)
    b1, f01 = F.fit_free(y)
    best = fit2(pp, D, y, [b1["theta"], f01["theta"]])
    beta, ss = lin2(pp, D, y, best["theta"])
    rho, th = harmonics(beta)
    return dict(theta=[float(v) for v in best["theta"]], rho=rho, th=th, rms=math.sqrt(ss / len(D)), rms1=math.sqrt(b1["ss"] / len(D)))


def planted_y(pp, D, theta_true, noise, rng):
    ph = pp.phase(D, *TRUE)
    u = (D - 228.0) / 10.0
    y = 0.3 - 1.1 * u + 0.15 * u ** 2 - 0.09 * u ** 3 + A1 * np.cos(ph + DELTA1) + RHO * A1 * np.cos(2 * ph + 2 * DELTA1 + theta_true)
    return y + rng.normal(0, noise, len(D))


def cmd_planted(pp, scen, nseeds, out):
    D, _ = pp.collect51()
    recs, t0 = [], time.time()
    for s in range(nseeds):
        rng = np.random.default_rng(SEED0[scen] + s)
        y = planted_y(pp, D, SCEN[scen]["theta"], SCEN[scen]["noise"], rng)
        ff = full_fit(pp, D, y)
        ho = holdouts2(pp, D, y)
        recs.append(dict(seed=SEED0[scen] + s, full=ff, ho={t: {k: {m: v[:2] for m, v in rr.items()} for k, rr in r[0].items()} for t, r in ho.items()}))
        if (s + 1) % 10 == 0 or s == 0:
            print(f"{scen}: {s + 1}/{nseeds} seeds, {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(scenario=scen, params=SCEN[scen], recs=recs), open(out, "w"))
    print(f"{scen}: wrote {out} ({nseeds} seeds, {time.time() - t0:.0f} s)")


def cmd_summarize(files):
    R = {}
    for f in files:
        d = json.load(open(f))
        R[d["scenario"]] = d
    if not {"P1", "P2"} <= set(R):
        sys.exit("needs P1 and P2")
    ok = True
    print(f"seeds per scenario {[(k, len(R[k]['recs'])) for k in sorted(R)]}; rules on P1 and P2 (noise 0.003), P3 (noise 0.006) is information")
    print("\n| scenario | median P0 err | median p1 err | median rho_hat | median theta err | PR1 |\n|---|---|---|---|---|---|")
    for k in sorted(R):
        rc = R[k]["recs"]
        th_true = R[k]["params"]["theta"]
        e0 = np.median([abs(r["full"]["theta"][0] - TRUE[0]) for r in rc])
        e1 = np.median([abs(r["full"]["theta"][1] - TRUE[1]) for r in rc])
        rh = np.median([r["full"]["rho"] for r in rc])
        et = np.median([abs(wrap(r["full"]["th"] - th_true)) for r in rc])
        pr1 = e0 <= 0.02 and e1 <= 0.003 and 0.049 <= rh <= 0.081 and et <= 0.25
        if k in ("P1", "P2"):
            ok = ok and pr1
        print(f"| {k} | {e0:.4f} | {e1:.4f} | {rh:.3f} | {et:.3f} | {'pass' if pr1 else 'FAIL'}{'' if k in ('P1', 'P2') else ' (info)'} |")
    print("\n| scenario | hold-out | 2h chirp: median rms | share <= 0.014 (PR2) | 1h chirp: median rms | 2h control: median rms | share control worse (PR3) | PR2 | PR3 | PR4 |\n|---|---|---|---|---|---|---|---|---|---|")
    for k in sorted(R):
        rc = R[k]["recs"]
        for h in ("H1", "H2"):
            c2 = np.array([r["ho"][h]["2h"]["p2 chirp"][0] for r in rc])
            c1 = np.array([r["ho"][h]["1h"]["p2 chirp"][0] for r in rc])
            k2 = np.array([r["ho"][h]["2h"]["p1 = p2 = 0"][0] for r in rc])
            s2, s3 = float(np.mean(c2 <= LIMIT)), float(np.mean(k2 > c2))
            p2_, p3_, p4_ = s2 >= 0.80, s3 >= 0.90, np.median(c2) < np.median(c1)
            if k in ("P1", "P2"):
                ok = ok and p2_ and p3_ and p4_
            print(f"| {k} | {h} | {np.median(c2):.4f} | {100 * s2:.0f}% | {np.median(c1):.4f} | {np.median(k2):.4f} | {100 * s3:.0f}% | {'pass' if p2_ else 'FAIL'} | {'pass' if p3_ else 'FAIL'} | {'pass' if p4_ else 'FAIL'} |")
    print(f"\nVERDICT: {'PASS' if ok else 'FAIL'} (PR1 to PR4 on P1 and P2)")
    return ok


def cmd_data(pp, verdict):
    vline = [ln for ln in open(verdict).read().splitlines() if ln.startswith("VERDICT:")]
    if not vline or not vline[0].startswith("VERDICT: PASS"):
        sys.exit(f"{verdict} does not say VERDICT: PASS; the real series is not read")
    D, Y = pp.collect51()
    print(f"{len(D)} states D {D[0]:.2f} to {D[-1]:.2f}; planted verdict file {verdict}; limit {LIMIT} (rms prediction error)")
    rec = {}
    allok = True
    for i in (1, 2):
        y = Y[:, i - 1]
        ff = full_fit(pp, D, y)
        print(f"\n=== ln sigma_{i}: the 2-harmonic chirp over all 51 states: P0 {ff['theta'][0]:.3f}, p1 {ff['theta'][1]:+.4f}, p2 {ff['theta'][2]:+.5f}, rho {ff['rho']:.3f}, theta {ff['th']:+.2f}, rms {ff['rms']:.4f} (1 harmonic: {ff['rms1']:.4f})")
        print("| hold-out | model | 2 harmonics: rms (max) | 1 harmonic: rms (max) | meets 0.014 (2h) | control worse (2h) |\n|---|---|---|---|---|---|")
        ho = holdouts2(pp, D, y)
        for tag, (row, ntr, nte) in ho.items():
            for name in ("p2 chirp", "p2 = 0 chirp", "p1 = p2 = 0"):
                a, b = row["2h"][name], row["1h"][name]
                extra = ""
                if name == "p2 chirp":
                    meets = a[0] <= LIMIT
                    worse = row["2h"]["p1 = p2 = 0"][0] > a[0]
                    allok = allok and meets and worse
                    extra = f"{'yes' if meets else 'NO'} | {'yes' if worse else 'NO'} ({row['2h']['p1 = p2 = 0'][0]:.4f} against {a[0]:.4f})"
                    rec[f"sigma_{i}_{tag}"] = dict(n_fit=ntr, n_pred=nte, rms2=a[0], max2=a[1], rms1=b[0], max1=b[1], ctl2=row["2h"]["p1 = p2 = 0"][0], theta2=a[2], meets=bool(meets), control_worse=bool(worse))
                else:
                    extra = " | "
                print(f"| {tag} ({ntr} fit, {nte} predicted) | {name} | {a[0]:.4f} ({a[1]:.4f}) | {b[0]:.4f} ({b[1]:.4f}) | {extra} |")
    print(f"\nACCEPTANCE (both hold-outs at most {LIMIT} for sigma_1 and sigma_2 with two harmonics, and the p1 = p2 = 0 control worse): {'MET' if allok else 'NOT MET'}")
    json.dump(rec, open("results_601.json", "w"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("cmd", choices=["planted", "summarize", "data"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--scenario", default="P1")
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--out", default=None)
    ap.add_argument("--verdict", default=None)
    a = ap.parse_args()
    pp = load_pp(a.raw)
    if a.cmd == "planted":
        cmd_planted(pp, a.scenario, a.seeds, a.out or f"planted_601_{a.scenario}.json")
    elif a.cmd == "summarize":
        sys.exit(0 if cmd_summarize(a.files) else 1)
    else:
        if not a.verdict:
            sys.exit("data needs --verdict=<the planted summary file>")
        cmd_data(pp, a.verdict)
