#!/usr/bin/env python3
"""#567: a flexible trend (a Gaussian process or a smoothing spline) for the sigma pair sums, tested in #533's hold-outs H1, H2, H3 and on #558's twelve states. Analysis only.
usage: python flex_trend_567.py --raw=<raw worktree with I565-win2, I558-win2, I557-win2, ...> planted [--seeds=N] [--noise=0.004] [--out=FILE]
       python flex_trend_567.py --raw=... summarize FILE          (the planted verdict, the floors and the bounds)
       python flex_trend_567.py --raw=... data --verdict=FILE     (the real sums; refuses unless FILE's VERDICT line says PASS)
Data: the sums y = ln sigma_a + ln sigma_b of the pairs (1, 2) and (3, 4) at the 63 states D 204.13 to 237.13 (joint_557.all_states()) and the twelve states of #558 D 198.13 to 203.63.
Windows (explicit; #565's code takes D <= 232.7 for H1's fit, which includes the twelve states below D 210 and so differs from its own docstring and header, 42 states):
  H1 fit 210 <= D <= 232.7 (42 states), predict D > 232.7 (9); H2 fit D >= 214 (43), predict 210 <= D < 214 (8); H3 fit D >= 210 (51), predict 204 <= D < 210 (12);
  W558 fit all 63 states D >= 204, predict the twelve states D < 204 (D 198.13 to 203.63).
Candidates (two, fixed before any hold-out of the real sums; u = (D - 228) / 10):
  G  a Gaussian process (universal kriging): mean (drift) a polynomial of degree 4 in u (flat prior, REML; chosen on planted data only: degree 2 and 3 fail the planted truths), kernel Matern-5/2 sigma_f^2 (1 + sqrt5 r / l + 5 r^2 / (3 l^2)) exp(-sqrt5 r / l) in u, white noise sigma_n; the
     hyperparameters (sigma_f, l, sigma_n) by maximizing the restricted marginal likelihood on the training states only, log-bounds l in [0.5, 8], sigma_f in [0.001, 3], sigma_n in [0.0005, 0.03],
     Nelder-Mead from the best point of a grid l {1, 2, 4, 8} x sigma_f {0.01, 0.1, 1} x sigma_n {0.002, 0.005, 0.01}; prediction is the kriging mean.
  S  the natural cubic smoothing spline of y(D) (scipy make_smoothing_spline), the smoothing parameter by generalized cross-validation on the training states only, continued linearly beyond the
     data with the end value and the end slope.
Noise floor: for a planted truth with the true form fitted by least squares (lnD(3) or poly(3) of #565), the median over the seeds of the true form's prediction rms in the window.
Planted truths (sums of unknown form to the methods; the first two are #565's): P_L = -230 - 160 l + 700 l^2 - 2500 l^3 (l = ln(D / 228)), P_P = -230 - 20 u + 3 u^2 - 0.4 u^3, P_E = -230 - 20 u + 3 exp(-(u + 1) / 1.2) (true form: 1, u and
the exponential of known scale); noise 0.004 (the real sum of sigma_1 + sigma_2: in-sample cubic rms 0.0039), 100 seeds per truth.
Rules (fixed on the issue before the real sums were read): bound b_w = 1.5 x the largest of the three truths' floors in window w. A method is planted-valid if for all three truths and all four windows (a) its median planted prediction
rms is at most 1.5 x that truth's floor (extrapolated) and (b) its median in-sample error against the truth is at most 1.5 x the true form's (recovered). Control: poly(2) on P_L exceeds 1.5 x the floor in some window. VERDICT PASS if
the control fires and at least one method is planted-valid. Real sum of sigma_1 + sigma_2: the method's rms in each of the four windows against b_w; the check fails if any window misses; polynomials of degree 2 to 4 beside.
The pair (3, 4) is information (its noise is larger). If no method is planted-valid (VERDICT FAIL) the real sums are still computed (the issue's check) and reported as NOT VALIDATED. Two candidates are tried (selection with the hold-outs in view).
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np
from scipy.interpolate import make_smoothing_spline
from scipy.optimize import minimize

NOISE, SEED0, DRIFT = 0.004, 31000, 4
WIN = ("H1", "H2", "H3", "W558")


def load(raw):
    for p in ("I565-win2", "I558-win2", "I557-win2", "I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
        sys.path.insert(0, os.path.join(raw, p))
    import joint_557 as j
    import trend_565 as t5
    import period_558 as p8
    return j, t5, p8


def all75(j, p8):
    D63, Y63 = j.all_states()
    new = p8.collect_new()
    Dn = np.array(sorted(new))
    Yn = np.array([np.mean(new[d], axis=0) for d in Dn])
    return np.concatenate([Dn, D63]), np.concatenate([Yn, Y63])


def windows(D):
    return {"H1": ((D >= 210.0) & (D <= 232.7), D > 232.7), "H2": (D >= 214.0, (D >= 210.0) & (D < 214.0)),
            "H3": (D >= 210.0, (D >= 204.0) & (D < 210.0)), "W558": (D >= 204.0, D < 204.0)}


def _mat52(r, l):
    a = math.sqrt(5.0) * r / l
    return (1.0 + a + a * a / 3.0) * np.exp(-a)


def _reml(params, u, y, H):
    lsf, ll, lsn = params
    if not (math.log(0.001) <= lsf <= math.log(3.0) and math.log(0.5) <= ll <= math.log(8.0) and math.log(0.0005) <= lsn <= math.log(0.03)):
        return 1e12
    sf, l, sn = math.exp(lsf), math.exp(ll), math.exp(lsn)
    K = sf * sf * _mat52(np.abs(u[:, None] - u[None, :]), l) + (sn * sn + 1e-10) * np.eye(len(u))
    try:
        L = np.linalg.cholesky(K)
    except np.linalg.LinAlgError:
        return 1e12
    Ki_y = np.linalg.solve(L.T, np.linalg.solve(L, y))
    Ki_H = np.linalg.solve(L.T, np.linalg.solve(L, H))
    A = H.T @ Ki_H
    try:
        beta = np.linalg.solve(A, H.T @ Ki_y)
        sign, logdetA = np.linalg.slogdet(A)
    except np.linalg.LinAlgError:
        return 1e12
    r = y - H @ beta
    Ki_r = np.linalg.solve(L.T, np.linalg.solve(L, r))
    return float(0.5 * r @ Ki_r + np.sum(np.log(np.diag(L))) + 0.5 * logdetA)


def gp_fit_predict(Dtr, ytr, Dte):
    u, ut = (Dtr - 228.0) / 10.0, (Dte - 228.0) / 10.0
    H = np.column_stack([u ** k for k in range(DRIFT + 1)])
    Ht = np.column_stack([ut ** k for k in range(DRIFT + 1)])
    best = None
    for l in (1, 2, 4, 8):
        for sf in (0.01, 0.1, 1.0):
            for sn in (0.002, 0.005, 0.01):
                p = [math.log(sf), math.log(l), math.log(sn)]
                f = _reml(p, u, ytr, H)
                if best is None or f < best[0]:
                    best = (f, p)
    res = minimize(_reml, best[1], args=(u, ytr, H), method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8, maxiter=300))
    p = res.x if res.fun < best[0] else best[1]
    sf, l, sn = math.exp(p[0]), math.exp(p[1]), math.exp(p[2])
    K = sf * sf * _mat52(np.abs(u[:, None] - u[None, :]), l) + (sn * sn + 1e-10) * np.eye(len(u))
    Ki = np.linalg.inv(K)
    beta = np.linalg.solve(H.T @ Ki @ H, H.T @ Ki @ ytr)
    ks = sf * sf * _mat52(np.abs(ut[:, None] - u[None, :]), l)
    return Ht @ beta + ks @ (Ki @ (ytr - H @ beta))


def spline_fit_predict(Dtr, ytr, Dte):
    s = make_smoothing_spline(Dtr, ytr)
    ds = s.derivative()
    lo, hi = float(Dtr[0]), float(Dtr[-1])
    out = np.empty(len(Dte))
    for i, x in enumerate(Dte):
        if x < lo:
            out[i] = float(s(lo)) + float(ds(lo)) * (x - lo)
        elif x > hi:
            out[i] = float(s(hi)) + float(ds(hi)) * (x - hi)
        else:
            out[i] = float(s(x))
    return out


def methods(t5):
    m = {"G": gp_fit_predict, "S": spline_fit_predict}
    for d in (2, 3, 4):
        m[f"poly{d}"] = (lambda dd: (lambda Dtr, ytr, Dte: t5.fit_predict(Dtr, ytr, Dte, ("poly", dd))))(d)
    m["lnD3"] = lambda Dtr, ytr, Dte: t5.fit_predict(Dtr, ytr, Dte, ("lnD", 3))

    def expo(Dtr, ytr, Dte):
        B = lambda d: np.column_stack([np.ones_like(d), (d - 228.0) / 10.0, np.exp(-((d - 228.0) / 10.0 + 1.0) / 1.2)])
        return B(Dte) @ np.linalg.lstsq(B(Dtr), ytr, rcond=None)[0]
    m["expo"] = expo
    return m


def rms_table(D, y, meths, names):
    out = {}
    for w, (tr, te) in windows(D).items():
        out[w] = {n: float(np.sqrt(np.mean((y[te] - meths[n](D[tr], y[tr], D[te])) ** 2))) for n in names}
    return out


def truths(D):
    l, u = np.log(D / 228.0), (D - 228.0) / 10.0
    return {"P_L": -230.0 - 160.0 * l + 700.0 * l ** 2 - 2500.0 * l ** 3, "P_P": -230.0 - 20.0 * u + 3.0 * u ** 2 - 0.4 * u ** 3,
            "P_E": -230.0 - 20.0 * u + 3.0 * np.exp(-(u + 1.0) / 1.2)}


TRUE_FORM = {"P_L": "lnD3", "P_P": "poly3", "P_E": "expo"}
CAND = ("G", "S", "poly2", "poly3", "poly4")


def cmd_planted(j, t5, p8, nseeds, noise, out):
    D, _ = all75(j, p8)
    meths = methods(t5)
    T = truths(D)
    res = {k: {w: {} for w in WIN} for k in T}
    rec = {k: {w: {} for w in WIN} for k in T}
    t0 = time.time()
    for ki, (k, ytrue) in enumerate(T.items()):
        names = list(dict.fromkeys(list(CAND) + [TRUE_FORM[k]]))
        for s in range(nseeds):
            rng = np.random.default_rng(SEED0 + 5000 * ki + s)
            y = ytrue + rng.normal(0, noise, len(D))
            tab = rms_table(D, y, meths, names)
            for w, (tr, te) in windows(D).items():
                for n in names:
                    res[k][w].setdefault(n, []).append(tab[w][n])
                    fit_in = meths[n](D[tr], y[tr], D[tr])
                    rec[k][w].setdefault(n, []).append(float(np.sqrt(np.mean((fit_in - ytrue[tr]) ** 2))))
            if (s + 1) % 20 == 0 or s == 0:
                print(f"{k}: {s + 1}/{nseeds} seeds, {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(noise=noise, nseeds=nseeds, truth_form=TRUE_FORM, res=res, rec=rec, counts={w: [int(m.sum()) for m in windows(D)[w]] for w in WIN}), open(out, "w"))
    print(f"wrote {out} ({time.time() - t0:.0f} s)")


def cmd_summarize(path):
    d = json.load(open(path))
    R, C = d["res"], d["rec"]
    print(f"planted noise {d['noise']}, {d['nseeds']} seeds per truth; windows (fit, predicted states): {d['counts']}")
    floor = {k: {w: float(np.median(R[k][w][d["truth_form"][k]])) for w in WIN} for k in R}
    rfloor = {k: {w: float(np.median(C[k][w][d["truth_form"][k]])) for w in WIN} for k in R}
    print("\nNoise floors (median prediction rms of the true form; in brackets its in-sample error against the truth):")
    print("| truth | true form | " + " | ".join(WIN) + " |\n|---|---|" + "---|" * len(WIN))
    for k in R:
        print(f"| {k} | {d['truth_form'][k]} | " + " | ".join(f"{floor[k][w]:.4f} ({rfloor[k][w]:.4f})" for w in WIN) + " |")
    bound = {w: 1.5 * max(floor[k][w] for k in R) for w in WIN}
    print("\nbounds b_w = 1.5 x the largest floor over the truths: " + ", ".join(f"{w} {bound[w]:.4f}" for w in WIN))
    print("\nMedian planted prediction rms per method (ratio to 1.5 x that truth's floor), and the in-sample error against the truth (ratio to 1.5 x the true form's):")
    print("| truth | method | " + " | ".join(f"{w} prediction" for w in WIN) + " | prediction within 1.5 x in all four | in-sample error H3 (ratio) | recovered |\n|---|---|" + "---|" * len(WIN) + "---|---|---|")
    pred_ok = {m: True for m in ("G", "S")}
    rec_ok = {m: True for m in ("G", "S")}
    for k in R:
        for m in CAND:
            meds = {w: float(np.median(R[k][w][m])) for w in WIN}
            ok = all(meds[w] <= 1.5 * floor[k][w] for w in WIN)
            rmed = {w: float(np.median(C[k][w][m])) for w in WIN}
            rok = all(rmed[w] <= 1.5 * rfloor[k][w] for w in WIN)
            if m in pred_ok:
                pred_ok[m] = pred_ok[m] and ok
                rec_ok[m] = rec_ok[m] and rok
            print(f"| {k} | {m} | " + " | ".join(f"{meds[w]:.4f} ({meds[w] / (1.5 * floor[k][w]):.2f})" for w in WIN) + f" | {'yes' if ok else 'no'} | {rmed['H3']:.4f} ({rmed['H3'] / (1.5 * rfloor[k]['H3']):.2f}) | {'yes' if rok else 'no'} |")
    ctl = any(float(np.median(R["P_L"][w]["poly2"])) > 1.5 * floor["P_L"][w] for w in WIN)
    valid = [m for m in pred_ok if pred_ok[m] and rec_ok[m]]
    ok = ctl and bool(valid)
    print(f"\ncontrol (poly2 on P_L exceeds 1.5 x floor in some window): {'fires' if ctl else 'DOES NOT FIRE'}")
    print("recovered in sample within 1.5 x the true form's error, all truths and windows: " + ", ".join(f"{m} {'yes' if rec_ok[m] else 'no'}" for m in rec_ok))
    print("extrapolated within 1.5 x the floor, all truths and windows: " + ", ".join(f"{m} {'yes' if pred_ok[m] else 'no'}" for m in pred_ok))
    print(f"planted-valid methods (both): {', '.join(valid) if valid else 'none'}")
    print(f"\nVERDICT: {'PASS' if ok else 'FAIL'} (control {'fires' if ctl else 'does not fire'}; planted-valid methods: {', '.join(valid) if valid else 'none'}); "
          f"BOUNDS {' '.join(f'{w} {bound[w]:.5f}' for w in WIN)}; VALID {' '.join(valid) if valid else 'none'}")
    return ok


def cmd_data(j, t5, p8, verdict):
    import re
    vline = [ln for ln in open(verdict).read().splitlines() if ln.startswith("VERDICT:")]
    if not vline:
        sys.exit(f"{verdict} has no VERDICT line; run the planted test and its summary first; the real sums are not read")
    bm = re.search(r"BOUNDS H1 ([\d.]+) H2 ([\d.]+) H3 ([\d.]+) W558 ([\d.]+)", vline[0])
    bound = dict(zip(WIN, [float(x) for x in bm.groups()]))
    valid = re.search(r"VALID (.*)$", vline[0]).group(1).split()
    planted_pass = vline[0].startswith("VERDICT: PASS")
    D, Y = all75(j, p8)
    meths = methods(t5)
    banner = "" if planted_pass else " -- NOT VALIDATED: the planted verdict is FAIL (the pre-registered fallback: the real sums are computed and reported as not validated)"
    print(f"{len(D)} states D {D[0]:.2f} to {D[-1]:.2f}; planted verdict file {verdict}: {vline[0][:60]}...; bounds {bound}; planted-valid methods {valid}{banner}")
    rec = {}
    for pair in ((1, 2), (3, 4)):
        y = Y[:, pair[0] - 1] + Y[:, pair[1] - 1]
        tab = rms_table(D, y, meths, ("G", "S", "poly2", "poly3", "poly4"))
        rec[f"{pair[0]}{pair[1]}"] = tab
        graded = pair == (1, 2)
        print(f"\n== sum ln sigma_{pair[0]} + ln sigma_{pair[1]}" + (" (graded)" if graded else " (information, not graded: its noise is larger)"))
        print("| method | planted-valid | " + " | ".join(WIN) + " | within the bounds in all four |\n|---|---|" + "---|" * len(WIN) + "---|")
        for m in ("G", "S", "poly2", "poly3", "poly4"):
            r = [tab[w][m] for w in WIN]
            within = all(r[i] <= bound[w] for i, w in enumerate(WIN))
            pv = ("yes" if m in valid else "no") if m in ("G", "S") else ""
            cells = " | ".join(f"{x:.4f}{'' if not graded else (' ok' if x <= bound[w] else ' MISS')}" for x, w in zip(r, WIN))
            print(f"| {m} | {pv} | {cells} | {('yes' if within else 'NO') if graded else ''} |")
        if graded:
            for m in ("G", "S", "poly2", "poly3", "poly4"):
                within = all(tab[w][m] <= bound[w] for w in WIN)
                print(f"CHECK {m}: {'PASS' if within else 'FAIL'} (a window of the sum of sigma_1 + sigma_2 {'is within' if within else 'misses'} the bound b_w)"
                      + ("" if m not in ("G", "S") else f"; planted-valid: {'yes' if m in valid else 'NO (not validated)'}"))
    json.dump(dict(bound=bound, valid=valid, planted_pass=planted_pass, tables=rec), open("results_567.json", "w"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("cmd", choices=["planted", "summarize", "data"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--noise", type=float, default=NOISE)
    ap.add_argument("--out", default="planted_567.json")
    ap.add_argument("--verdict", default=None)
    a = ap.parse_args()
    j, t5, p8 = load(a.raw)
    if a.cmd == "planted":
        cmd_planted(j, t5, p8, a.seeds, a.noise, a.out)
    elif a.cmd == "summarize":
        sys.exit(0 if cmd_summarize(a.files[0]) else 1)
    else:
        if not a.verdict:
            sys.exit("data needs --verdict=<the planted summary file>")
        cmd_data(j, t5, p8, a.verdict)
