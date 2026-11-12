#!/usr/bin/env python3
"""#602: where ln sigma_1's H2 hold-out miss of #601 comes from: the trend's degree against the waveform. Analysis only.
usage: python trend_degree_602.py --raw=<raw worktree with I533-win2, ...> planted --scenario=T0|T1 [--seeds=N] [--out=FILE]
       python trend_degree_602.py --raw=... summarize FILE...        (the planted verdict; needs T0 and T1)
       python trend_degree_602.py --raw=... data --verdict=FILE      (the real series; refuses unless FILE's VERDICT line says PASS)
Needs holdout2_601.py in this folder (a copy of I601-win's: its 2-harmonic fit with a global trend degree DEG, which is set here).
Variants for each trend degree d in 2, 3, 4, with the two-harmonic waveform of #601 (six linear parameters at d = 3), the hold-outs of #601 (H1 fit D <= 232.7, predict 233.13..237.13;
H2 fit D >= 214, predict 210.13..213.63):
  (a) the whole fit extrapolated (trend and oscillation from the training states);
  (b) the oscillation alone extrapolated from the training fit, with the trend (degree d) refitted to all 51 states of (y - oscillation) afterwards (it leaks the trend: how much of the miss is the trend's).
Diagnostic R: the residual rms of the 2-harmonic cubic fit to all 51 states over D < 214 divided by that over D >= 214 (a low-D excess the model does not carry).
Planted truth (the same code, the whole pipeline, the D of the data, 100 seeds per scenario, noise 0.003, a1 = 0.11, rho = 0.065, theta 0, phi from P0 2.62, p1 +0.0165, p2 +0.0003, trend
0.3 - 1.1 u + 0.15 u^2 - 0.09 u^3, u = (D - 228) / 10): T0 the trend alone (no structure); T1 the trend plus g(D) = 0.05 exp(-(D - 210) / 3), structure at the low-D end
(0.050 at D 210, 0.016 at D 213.6, 0.013 at D 214, 0.0002 at D 228, not a polynomial); the amplitude 0.05 was chosen on planted data only (8 seeds at 0.03, 0.06, 0.10, 0.15) so that the cubic
variant (a) misses H2 by about #601's observed 0.0146 (0.03 gave a median 0.0092, 0.06 gave 0.0169).
Rules (fixed on the issue before the real series was read):
  T0 (control, no structure): C1 (a) cubic and (b) cubic meet 0.014 in at least 80% of seeds in H1 and in H2.
  T1 (structure at the low-D end): S1 the median H2 rms of (a) cubic lies in [0.012, 0.017] (the structure makes a miss of the observed size); S2 (a) cubic H2 exceeds 0.014 in at least
      35% of seeds; S3 the median H2 rms of (b) cubic is at least 30% below (a) cubic's; S4 at least 40% of the seeds have R above the 90th percentile of T0's R; S5 the median rho_hat of
      the full-51 cubic 2-harmonic fit lies in [0.049, 0.081].
Real data (ln sigma_1; ln sigma_2 as information): the table of (a) and (b) for d = 2, 3, 4 in H1 and H2 and E, then the statement: the variants for which H2 <= 0.014 with H1 <= 0.014
(separately for (a) and (b)), or that none does; (b) cubic at most 0.014 in H2 with (a) cubic above it is read as the trend's extrapolation being the cause.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

import holdout2_601 as h

SEED0 = {"T0": 21000, "T1": 22000}
NOISE, LIMIT, DEGS = 0.003, 0.014, (2, 3, 4)


def g_low(D):
    return 0.05 * np.exp(-(D - 210.0) / 3.0)


def planted_y(pp, D, scen, rng):
    y = h.planted_y(pp, D, 0.0, 0.0, rng)  # trend + two harmonics, no noise (noise 0)
    if scen == "T1":
        y = y + g_low(D)
    return y + rng.normal(0, NOISE, len(D))


def variants(pp, D, y):
    out = {}
    for d in DEGS:
        h.DEG = d
        u = (D - pp.D0) / 10.0
        V = np.column_stack([u ** j for j in range(d + 1)])
        for tag, trf, tef in h.HOLD:
            tr, te = trf(D), tef(D)
            Dtr, ytr = D[tr], y[tr]
            F = pp.Fitter(Dtr, d)
            b1, f01 = F.fit_free(ytr)
            fit = h.fit2(pp, Dtr, ytr, [b1["theta"], f01["theta"]])
            th = fit["theta"]
            beta, _ = h.lin2(pp, Dtr, ytr, th)
            Xall = h.cols2(pp, D, pp.phase(D, *th))
            pred_a = Xall[te] @ beta
            osc = Xall[:, d + 1:] @ beta[d + 1:]
            c = np.linalg.lstsq(V, y - osc, rcond=None)[0]
            pred_b = (V @ c)[te] + osc[te]
            ea, eb = y[te] - pred_a, y[te] - pred_b
            out[(d, tag)] = dict(a=math.sqrt(float(np.mean(ea ** 2))), b=math.sqrt(float(np.mean(eb ** 2))), amax=float(np.max(np.abs(ea))), bmax=float(np.max(np.abs(eb))),
                                 theta=[float(v) for v in th])
    h.DEG = 3
    return out


def diagnostic(pp, D, y):
    h.DEG = 3
    F = pp.Fitter(D, 3)
    b1, f01 = F.fit_free(y)
    fit = h.fit2(pp, D, y, [b1["theta"], f01["theta"]])
    beta, ss = h.lin2(pp, D, y, fit["theta"])
    X = h.cols2(pp, D, pp.phase(D, *fit["theta"]))
    res = y - X @ beta
    rho, th = h.harmonics(beta)
    lo = D < 214.0
    return dict(E=float(np.mean(res[D < 213.0])), R=float(np.sqrt(np.mean(res[lo] ** 2)) / np.sqrt(np.mean(res[~lo] ** 2))), rho=rho, theta=th, rms=math.sqrt(ss / len(D)),
                P=[float(v) for v in fit["theta"]])


def cmd_planted(pp, scen, nseeds, out):
    D, _ = pp.collect51()
    recs, t0 = [], time.time()
    for s in range(nseeds):
        rng = np.random.default_rng(SEED0[scen] + s)
        y = planted_y(pp, D, scen, rng)
        v = variants(pp, D, y)
        dg = diagnostic(pp, D, y)
        recs.append(dict(seed=SEED0[scen] + s, diag=dg, v={f"{d}_{t}": {k: x for k, x in r.items() if k in ("a", "b", "amax", "bmax")} for (d, t), r in v.items()}))
        if (s + 1) % 10 == 0 or s == 0:
            print(f"{scen}: {s + 1}/{nseeds} seeds, {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(scenario=scen, recs=recs), open(out, "w"))
    print(f"{scen}: wrote {out} ({nseeds} seeds, {time.time() - t0:.0f} s)")


def cmd_summarize(files):
    R = {}
    for f in files:
        d = json.load(open(f))
        R[d["scenario"]] = d
    if not {"T0", "T1"} <= set(R):
        sys.exit("needs T0 and T1")
    ok = True
    print(f"seeds per scenario {[(k, len(R[k]['recs'])) for k in sorted(R)]}; planted noise {NOISE}, limit {LIMIT}")
    print("\nShare of seeds with the rms at most 0.014, and median rms, per variant:")
    print("| scenario | degree | (a) H1 share (median) | (a) H2 share (median) | (b) H1 share (median) | (b) H2 share (median) |\n|---|---|---|---|---|---|")
    for k in ("T0", "T1"):
        rc = R[k]["recs"]
        for d in DEGS:
            cells = []
            for var in ("a", "b"):
                for H in ("H1", "H2"):
                    x = np.array([r["v"][f"{d}_{H}"][var] for r in rc])
                    cells.append(f"{100 * np.mean(x <= LIMIT):.0f}% ({np.median(x):.4f})")
            print(f"| {k} | {d} | " + " | ".join(cells) + " |")
    s = lambda k, d, H, var: np.array([r["v"][f"{d}_{H}"][var] for r in R[k]["recs"]])
    Rr = lambda k: np.array([r["diag"]["R"] for r in R[k]["recs"]])
    r90 = float(np.percentile(Rr("T0"), 90))
    print("\nRules:")
    c1 = all(np.mean(s("T0", 3, H, v) <= LIMIT) >= 0.80 for H in ("H1", "H2") for v in ("a", "b"))
    med_a = float(np.median(s("T1", 3, "H2", "a")))
    s1 = 0.012 <= med_a <= 0.017
    s2v = float(np.mean(s("T1", 3, "H2", "a") > LIMIT))
    s2 = s2v >= 0.35
    red = 1 - np.median(s("T1", 3, "H2", "b")) / med_a
    s3 = red >= 0.30
    s4v = float(np.mean(Rr("T1") > r90))
    s4 = s4v >= 0.40
    rh = float(np.median([r["diag"]["rho"] for r in R["T1"]["recs"]]))
    s5 = 0.049 <= rh <= 0.081
    for name, val, text in (
        ("C1 (T0) (a), (b) cubic meet 0.014 in >= 80% of seeds, H1 and H2", c1, f"(a) H1 {100 * np.mean(s('T0', 3, 'H1', 'a') <= LIMIT):.0f}%, H2 {100 * np.mean(s('T0', 3, 'H2', 'a') <= LIMIT):.0f}%; (b) H1 {100 * np.mean(s('T0', 3, 'H1', 'b') <= LIMIT):.0f}%, H2 {100 * np.mean(s('T0', 3, 'H2', 'b') <= LIMIT):.0f}%"),
        ("S1 (T1) median (a) cubic H2 rms in [0.012, 0.017]", s1, f"{med_a:.4f}"),
        ("S2 (T1) (a) cubic H2 exceeds 0.014 in >= 35% of seeds", s2, f"{100 * s2v:.0f}%"),
        ("S3 (T1) (b) cubic median H2 rms >= 30% below (a)'s", s3, f"{100 * red:.0f}% below ({np.median(s('T1', 3, 'H2', 'b')):.4f} against {med_a:.4f})"),
        ("S4 (T1) >= 40% of seeds with R above T0's 90th percentile", s4, f"{100 * s4v:.0f}% (R90 of T0 {r90:.2f}; medians T0 {np.median(Rr('T0')):.2f}, T1 {np.median(Rr('T1')):.2f})"),
        ("S5 (T1) median rho_hat in [0.049, 0.081]", s5, f"{rh:.3f}")):
        ok = ok and val
        print(f"- {name}: {'pass' if val else 'FAIL'} {text}")
    print(f"\nVERDICT: {'PASS' if ok else 'FAIL'}; T0 R90 {r90:.3f}")
    return ok


def cmd_data(pp, verdict):
    vline = [ln for ln in open(verdict).read().splitlines() if ln.startswith("VERDICT:")]
    if not vline or not vline[0].startswith("VERDICT: PASS"):
        sys.exit(f"{verdict} does not say VERDICT: PASS; the real series is not read")
    import re
    r90 = float(re.search(r"T0 R90 ([\d.]+)", vline[0]).group(1))
    D, Y = pp.collect51()
    print(f"{len(D)} states D {D[0]:.2f} to {D[-1]:.2f}; planted verdict file {verdict}; limit {LIMIT}")
    rec = {}
    for i in (1, 2):
        y = Y[:, i - 1]
        dg = diagnostic(pp, D, y)
        print(f"\n=== ln sigma_{i}{' (the series asked)' if i == 1 else ' (information, not asked)'}: 2-harmonic cubic fit over all 51 states: P0 {dg['P'][0]:.3f}, p1 {dg['P'][1]:+.4f}, p2 {dg['P'][2]:+.5f}, rho {dg['rho']:.3f}, rms {dg['rms']:.4f}; diagnostic R (residual rms over D < 214 / over D >= 214) {dg['R']:.2f} against T0's 90th percentile {r90:.2f}: {'low-D excess flagged' if dg['R'] > r90 else 'no low-D excess flagged'} (E, mean residual over D < 213: {dg['E']:+.4f})")
        v = variants(pp, D, y)
        print("| trend degree | (a) H1 rms (max) | (a) H2 rms (max) | (a) both <= 0.014 | (b) H1 rms (max) | (b) H2 rms (max) | (b) both <= 0.014 |\n|---|---|---|---|---|---|---|")
        meets = {"a": [], "b": []}
        for d in DEGS:
            c = {H: v[(d, H)] for H in ("H1", "H2")}
            oka = c["H1"]["a"] <= LIMIT and c["H2"]["a"] <= LIMIT
            okb = c["H1"]["b"] <= LIMIT and c["H2"]["b"] <= LIMIT
            if oka:
                meets["a"].append(d)
            if okb:
                meets["b"].append(d)
            print(f"| {d} | {c['H1']['a']:.4f} ({c['H1']['amax']:.4f}) | {c['H2']['a']:.4f} ({c['H2']['amax']:.4f}) | {'yes' if oka else 'no'} | {c['H1']['b']:.4f} ({c['H1']['bmax']:.4f}) | {c['H2']['b']:.4f} ({c['H2']['bmax']:.4f}) | {'yes' if okb else 'no'} |")
            rec[f"sigma_{i}_deg{d}"] = {H: dict(a=c[H]["a"], b=c[H]["b"], amax=c[H]["amax"], bmax=c[H]["bmax"]) for H in ("H1", "H2")}
        rec[f"sigma_{i}_diag"] = dg
        print(f"variants with H1 and H2 both at most 0.014: (a) {meets['a'] or 'none'}; (b) {meets['b'] or 'none'}")
        if i == 1:
            cause = v[(3, "H2")]["b"] <= LIMIT < v[(3, "H2")]["a"]
            print("statement: " + ("(b) cubic meets H2 while (a) cubic does not: the trend's extrapolation is the cause" if cause else
                                    "(b) cubic does not separate from (a) cubic at the bound (not read as the trend's extrapolation alone)"))
    json.dump(rec, open("results_602.json", "w"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("cmd", choices=["planted", "summarize", "data"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--scenario", default="T0")
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--out", default=None)
    ap.add_argument("--verdict", default=None)
    a = ap.parse_args()
    pp = h.load_pp(a.raw)
    if a.cmd == "planted":
        cmd_planted(pp, a.scenario, a.seeds, a.out or f"planted_602_{a.scenario}.json")
    elif a.cmd == "summarize":
        sys.exit(0 if cmd_summarize(a.files) else 1)
    else:
        if not a.verdict:
            sys.exit("data needs --verdict=<the planted summary file>")
        cmd_data(pp, a.verdict)
