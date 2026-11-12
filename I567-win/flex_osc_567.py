#!/usr/bin/env python3
"""#567 part 2: ln sigma_1 alone, the two-harmonic chirp of #601/#602 with a flexible (GP) trend, in the windows of part 1. Analysis only.
usage: python flex_osc_567.py --raw=<raw worktree> planted [--seeds=N] [--out=FILE]
       python flex_osc_567.py --raw=<raw worktree> summarize FILE
       python flex_osc_567.py --raw=<raw worktree> data --verdict=FILE      (needs the VERDICT line of the summary; FAIL is reported as NOT VALIDATED)
Needs flex_trend_567.py (part 1: the GP 'G' with a quartic drift, REML, and the windows H1, H2, H3, W558) and holdout2_601.py (a copy of I601-win's: the two-harmonic chirp fit with a polynomial trend) in this folder.
Methods on ln sigma_1 (y), trained on the training states of a window only:
  Gb  backfitting: start from #601's cubic-trend two-harmonic chirp fit (theta = P0, p1, p2 and the four harmonic coefficients); then four times: the GP trend f from the residual y - oscillation (hyperparameters
      re-optimized by part 1's rule), then (theta, harmonic coefficients) by least squares and Nelder-Mead on y - f with a harmonics-only design; the prediction is f (extrapolated by the GP) + the oscillation at the
      test states; a final GP pass on the last residual.
  P3, P4  #601/#602's polynomial trends of degree 3 and 4 with the same two-harmonic chirp (variant (a) of #602).
Planted truth (the same code, the whole pipeline, the 75 D of the data, noise 0.003, 50 seeds): y = Q + 0.11 cos(phi + 0.7) + 0.065 x 0.11 cos(2 phi + 1.4), phi from P0 2.62, p1 +0.0165, p2 +0.0003, trend
Q = -115 - 10 u + 1.5 u^2 - 0.2 u^3 (half of part 1's P_P), u = (D - 228) / 10. The floor in a window is the median over the seeds of P3's prediction rms (the true form); the bound b_w is 1.5 x the floor.
Rules (fixed on the issue before the real ln sigma_1 was read): Gb is planted-valid if its median planted rms is at most 1.5 x the floor in all four windows; control: P4 or Gb with the drift/degree wrong is not used; the control
is a polynomial trend of degree 2 (P2) which must exceed 1.5 x the floor in some window. Real ln sigma_1: the rms of Gb, P3, P4 in H1, H2, H3, W558 against b_w.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

import flex_trend_567 as ft
import holdout2_601 as h

NOISE2, SEED0, WIN = 0.003, 41000, ft.WIN
Q = lambda D: -115.0 - 10.0 * ((D - 228.0) / 10.0) + 1.5 * ((D - 228.0) / 10.0) ** 2 - 0.2 * ((D - 228.0) / 10.0) ** 3


def hdesign(pp, D, th):
    ph = pp.phase(D, th[0], th[1], th[2])
    if ph is None:
        return None
    return np.column_stack([np.cos(ph), np.sin(ph), np.cos(2 * ph), np.sin(2 * ph)])


def fit_osc(pp, D, r, th0):
    def ss(th):
        X = hdesign(pp, D, th)
        if X is None:
            return 1e9
        e = r - X @ np.linalg.lstsq(X, r, rcond=None)[0]
        return float(e @ e)
    x, f = pp.nm(ss, list(th0), [0.03, 0.004, 0.0004])
    th = np.array(x)
    X = hdesign(pp, D, th)
    return th, np.linalg.lstsq(X, r, rcond=None)[0]


def poly_pred(pp, Dtr, ytr, Dte, deg):
    h.DEG = deg
    F = pp.Fitter(Dtr, deg)
    b1, f01 = F.fit_free(ytr)
    fit = h.fit2(pp, Dtr, ytr, [b1["theta"], f01["theta"]])
    return h.predict2(pp, Dte, Dtr, ytr, fit["theta"]), fit["theta"]


def backfit_pred(pp, Dtr, ytr, Dte):
    h.DEG = 3
    F = pp.Fitter(Dtr, 3)
    b1, f01 = F.fit_free(ytr)
    fit = h.fit2(pp, Dtr, ytr, [b1["theta"], f01["theta"]])
    th = fit["theta"]
    beta, _ = h.lin2(pp, Dtr, ytr, th)
    bh = beta[4:]
    n = len(Dtr)
    Dcat = np.concatenate([Dtr, Dte])
    for _ in range(4):
        osc_tr = hdesign(pp, Dtr, th) @ bh
        f_tr = ft.gp_fit_predict(Dtr, ytr - osc_tr, Dtr)
        th, bh = fit_osc(pp, Dtr, ytr - f_tr, th)
    osc_tr = hdesign(pp, Dtr, th) @ bh
    f_all = ft.gp_fit_predict(Dtr, ytr - osc_tr, Dcat)
    return f_all[n:] + hdesign(pp, Dte, th) @ bh


def rms_all(pp, D, y):
    out = {}
    for w, (tr, te) in ft.windows(D).items():
        Dtr, ytr, Dte = D[tr], y[tr], D[te]
        e = {}
        e["Gb"] = y[te] - backfit_pred(pp, Dtr, ytr, Dte)
        e["P3"] = y[te] - poly_pred(pp, Dtr, ytr, Dte, 3)[0]
        e["P4"] = y[te] - poly_pred(pp, Dtr, ytr, Dte, 4)[0]
        e["P2"] = y[te] - poly_pred(pp, Dtr, ytr, Dte, 2)[0]
        out[w] = {k: float(np.sqrt(np.mean(v ** 2))) for k, v in e.items()}
    h.DEG = 3
    return out


def cmd_planted(pp, j, p8, nseeds, out):
    D, _ = ft.all75(j, p8)
    ph = pp.phase(D, 2.62, 0.0165, 0.0003)
    clean = Q(D) + 0.11 * np.cos(ph + 0.7) + 0.065 * 0.11 * np.cos(2 * ph + 1.4)
    res = {w: {m: [] for m in ("Gb", "P3", "P4", "P2")} for w in WIN}
    t0 = time.time()
    for s in range(nseeds):
        y = clean + np.random.default_rng(SEED0 + s).normal(0, NOISE2, len(D))
        tab = rms_all(pp, D, y)
        for w in WIN:
            for m in tab[w]:
                res[w][m].append(tab[w][m])
        if (s + 1) % 5 == 0 or s == 0:
            print(f"planted {s + 1}/{nseeds} seeds, {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(noise=NOISE2, nseeds=nseeds, res=res), open(out, "w"))
    print(f"wrote {out} ({time.time() - t0:.0f} s)")


def cmd_summarize(path):
    d = json.load(open(path))
    R = d["res"]
    floor = {w: float(np.median(R[w]["P3"])) for w in WIN}
    bound = {w: 1.5 * floor[w] for w in WIN}
    print(f"planted noise {d['noise']}, {d['nseeds']} seeds; floor = the median rms of P3 (the true form): " + ", ".join(f"{w} {floor[w]:.4f}" for w in WIN))
    print("bounds b_w = 1.5 x floor: " + ", ".join(f"{w} {bound[w]:.4f}" for w in WIN))
    print("\n| method | " + " | ".join(f"{w} median rms (ratio to b_w)" for w in WIN) + " | within b_w in all four |\n|---|" + "---|" * (len(WIN) + 1))
    ok = {}
    for m in ("Gb", "P3", "P4", "P2"):
        meds = {w: float(np.median(R[w][m])) for w in WIN}
        ok[m] = all(meds[w] <= bound[w] for w in WIN)
        print(f"| {m} | " + " | ".join(f"{meds[w]:.4f} ({meds[w] / bound[w]:.2f})" for w in WIN) + f" | {'yes' if ok[m] else 'no'} |")
    ctl = not ok["P2"]
    valid = ok["Gb"]
    print(f"\ncontrol (P2 exceeds b_w in some window): {'fires' if ctl else 'DOES NOT FIRE'}; Gb planted-valid: {'yes' if valid else 'no'}")
    print(f"\nVERDICT: {'PASS' if (ctl and valid) else 'FAIL'} (control {'fires' if ctl else 'does not fire'}; Gb {'valid' if valid else 'not valid'}); BOUNDS {' '.join(f'{w} {bound[w]:.5f}' for w in WIN)}; VALID {'Gb' if valid else 'none'}")
    return ctl and valid


def cmd_data(pp, j, p8, verdict):
    import re
    vline = [ln for ln in open(verdict).read().splitlines() if ln.startswith("VERDICT:")]
    if not vline:
        sys.exit(f"{verdict} has no VERDICT line; run the planted test and its summary first; the real series is not read")
    bm = re.search(r"BOUNDS H1 ([\d.]+) H2 ([\d.]+) H3 ([\d.]+) W558 ([\d.]+)", vline[0])
    bound = dict(zip(WIN, [float(x) for x in bm.groups()]))
    passed = vline[0].startswith("VERDICT: PASS")
    D, Y = ft.all75(j, p8)
    y = Y[:, 0]
    print(f"{len(D)} states; planted verdict: {vline[0][:70]}...; bounds {bound}" + ("" if passed else " -- NOT VALIDATED (planted verdict FAIL)"))
    tab = rms_all(pp, D, y)
    print("\n== ln sigma_1, two harmonics + trend (prediction rms; bound b_w)")
    print("| method | " + " | ".join(f"{w} (b {bound[w]:.4f})" for w in WIN) + " | within b_w in all four |\n|---|" + "---|" * (len(WIN) + 1))
    for m in ("Gb", "P3", "P4", "P2"):
        r = [tab[w][m] for w in WIN]
        within = all(r[i] <= bound[w] for i, w in enumerate(WIN))
        print(f"| {m} | " + " | ".join(f"{x:.4f}{' ok' if x <= bound[w] else ' MISS'}" for x, w in zip(r, WIN)) + f" | {'yes' if within else 'NO'} |")
    json.dump(dict(bound=bound, planted_pass=passed, table=tab), open("results_567_part2.json", "w"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("cmd", choices=["planted", "summarize", "data"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--seeds", type=int, default=50)
    ap.add_argument("--out", default="planted_567_part2.json")
    ap.add_argument("--verdict", default=None)
    a = ap.parse_args()
    j, t5, p8 = ft.load(a.raw)
    pp = h.load_pp(a.raw)
    if a.cmd == "planted":
        cmd_planted(pp, j, p8, a.seeds, a.out)
    elif a.cmd == "summarize":
        sys.exit(0 if cmd_summarize(a.files[0]) else 1)
    else:
        if not a.verdict:
            sys.exit("data needs --verdict=<the planted summary file>")
        cmd_data(pp, j, p8, a.verdict)
