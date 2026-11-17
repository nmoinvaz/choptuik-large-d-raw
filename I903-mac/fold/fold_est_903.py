#!/usr/bin/env python3
"""D* of the fold from one base's Taylor series of Delta in D (#903), by #829's two approximant families
(hp/fold_mirror.py: M1 the differential approximant Q1 f' + Q0 f + R = 0, M2 the quadratic Pade P f^2 + Q f + R = 0,
each matched at one base, degrees DA_DEG1 and QP_DEG1), with the branch point searched within WIN of 259.9033
instead of fold_mirror's 0.02, so that a moved fold is found.

    PYTHONPATH=<worktree>/hp python3 fold_est_903.py planted [--bases=B1,..] [--win=0.5] [--noise=1e-30] [--json=OUT]
    PYTHONPATH=<worktree>/hp python3 fold_est_903.py real JETDIR [--Dmin=..] [--win=0.5] [--json=OUT]

Per approximant: M1, the real zero h* of Q1 nearest D* - D_b within WIN, polished, with the local exponent
mu = -Q0(h*)/Q1'(h*), counted only when |mu - 1/2| <= MU_TOL; M2, the real zero of the discriminant Q^2 - 4 P R
nearest D* - D_b within WIN, polished, counted only when the discriminant is positive at the base. A method's value at
a base is the median over its counted approximants, its spread their half range. The base's D* is the mean of M1 and
M2, its error the larger of their spreads and half their difference: a spread over approximants and methods, not a
bound.

planted: the series of fold_mirror's plant (R + S sqrt(D* - D) + C at the chain's sizes, #782's near singularities at
260.17 and 259.47 +- 1.17i, relative noise NOISE) with D* moved by each of SHIFTS, at each base. A base is usable when
both methods give a value for every shift and |D*_est - D*_planted| <= TOL_B for every shift. Pass: at least NUSE
usable bases, and at each usable base the verdict bands (|D*_est - 259.9033| > 0.05 the truncation's, < 0.01 not,
between reported) classify every shift as its planted value does. Control (--win=0.02, fold_mirror's window): the
moved plants find no zero, so no base is usable, and it must fail. Exit 0 when the verdict is the expected one.
"""
import glob
import json
import os
import statistics
import sys

import mpmath as mp
import numpy as np

import fold_mirror as fm

args = dict(a.lstrip("-").split("=", 1) if "=" in a else (a.lstrip("-"), "1") for a in sys.argv[2:] if a.startswith("--"))
pos = [a for a in sys.argv[2:] if not a.startswith("--")]
WIN = float(args.get("win", 0.5))
MU_TOL = 0.1
SHIFTS = [0.0, 0.03, -0.03, 0.06, -0.06]
TOL_B, NUSE = 0.005, 2
BASES = [254.13125, 255.13125, 256.13125, 257.13125, 258.13125, 258.9, 259.4, 259.7]


def band(d):
    return "T" if abs(d) > 0.05 else ("N" if abs(d) < 0.01 else "B")


def real_zero(p, hs):
    """the real zero of p nearest hs within WIN, polished, or None"""
    zs = [z for z in fm.proots(p) if abs(z.imag) < 1e-6 and abs(z.real - hs) < WIN]
    if not zs:
        return None
    return mp.re(fm.polish(p, min(zs, key=lambda z: abs(z.real - hs)).real))


def estimate(Db, c):
    hs = float(fm.DSTAR - Db)
    out = {}
    v, mus, why = [], [], []
    for deg in fm.DA_DEG1:
        try:
            (Q1, Q0, R), _ = fm.forms([(Db, c)], deg, "DA")
        except (ZeroDivisionError, ValueError) as ex:
            why.append(str(ex))
            continue
        h = real_zero(Q1, hs)
        if h is None:
            why.append("no real zero of Q1 in the window")
            continue
        dQ1 = [k * Q1[k] for k in range(1, len(Q1))]
        mu = -fm.peval(Q0, h) / fm.peval(dQ1, h)
        if abs(mu - mp.mpf(1) / 2) > MU_TOL:
            why.append("mu %.3g" % float(mu))
            continue
        v.append(Db + h)
        mus.append(mu)
    out["M1"] = dict(n=len(v), vals=[float(x) for x in v], mu=float(statistics.median(mus)) if mus else None,
                     why=sorted(set(why)))
    v, why = [], []
    for deg in fm.QP_DEG1:
        try:
            (P, Q, R), _ = fm.forms([(Db, c)], deg, "QP")
        except (ZeroDivisionError, ValueError) as ex:
            why.append(str(ex))
            continue
        PR, QQ = fm.smul(P, R), fm.smul(Q, Q)
        L = max(len(PR), len(QQ))
        disc = [(QQ[k] if k < len(QQ) else 0) - 4 * (PR[k] if k < len(PR) else 0) for k in range(L)]
        if fm.peval(disc, 0) <= 0:
            why.append("discriminant <= 0 at the base")
            continue
        h = real_zero(disc, hs)
        if h is None:
            why.append("no real zero of the discriminant in the window")
            continue
        v.append(Db + h)
    out["M2"] = dict(n=len(v), vals=[float(x) for x in v], why=sorted(set(why)))
    for m in ("M1", "M2"):
        vals = out[m]["vals"]
        out[m]["med"] = statistics.median(vals) if vals else None
        out[m]["half"] = (max(vals) - min(vals)) / 2 if vals else None
    if out["M1"]["med"] is not None and out["M2"]["med"] is not None:
        a, b = out["M1"]["med"], out["M2"]["med"]
        out["Dstar"] = (a + b) / 2
        out["err"] = max(out["M1"]["half"], out["M2"]["half"], abs(a - b) / 2)
    else:
        out["Dstar"] = out["err"] = None
    return out


def cmd_planted():
    mp.mp.dps = fm.DPS
    noise = float(args.get("noise", 1e-30))
    bases = [float(x) for x in args["bases"].split(",")] if "bases" in args else BASES
    print("planted: shifts %s, window %.3g, noise %.0e, usable at |error| <= %.3g for every shift" % (
        SHIFTS, WIN, noise, TOL_B))
    rows, usable = [], []
    for i, b in enumerate(bases):
        Db = mp.mpf(repr(b))
        line = dict(D=b, shifts={})
        ok = True
        for j, s in enumerate(SHIFTS):
            c = fm.Plant(s, 0.3, noise).series(Db, 903 + 10 * i + j)
            e = estimate(Db, c)
            d_true = float(fm.DSTAR) + s
            err = e["Dstar"] - d_true if e["Dstar"] is not None else None
            good = err is not None and abs(err) <= TOL_B and band(e["Dstar"] - float(fm.DSTAR)) == band(s)
            ok &= good
            line["shifts"][str(s)] = dict(est=e, err=err, good=good)
            print("  D_b %.5f shift %+.2f: M1 %d/7 %s (mu %s), M2 %d/7 %s -> D* %s, error %s %s" % (
                b, s, e["M1"]["n"], "%.6f" % e["M1"]["med"] if e["M1"]["med"] is not None else "-",
                "%.4f" % e["M1"]["mu"] if e["M1"]["mu"] is not None else "-", e["M2"]["n"],
                "%.6f" % e["M2"]["med"] if e["M2"]["med"] is not None else "-",
                "%.6f +- %.1e" % (e["Dstar"], e["err"]) if e["Dstar"] is not None else "none",
                "%+.2e" % err if err is not None else "-", "" if good else "(miss)"), flush=True)
        line["usable"] = ok
        rows.append(line)
        if ok:
            usable.append(b)
    verdict = len(usable) >= NUSE
    print("planted: %d usable bases (%s): %s" % (len(usable), ", ".join("%.5f" % b for b in usable),
                                                 "PASS" if verdict else "FAIL"))
    if "json" in args:
        json.dump(dict(win=WIN, noise=noise, shifts=SHIFTS, tol=TOL_B, rows=rows, usable=usable, ok=verdict),
                  open(args["json"], "w"), indent=1, default=float)
    expect = WIN > 0.1
    return 0 if verdict == expect else 1


def cmd_real():
    mp.mp.dps = fm.DPS
    jd = pos[0]
    dmin = float(args.get("Dmin", 0))
    fs = sorted(glob.glob(os.path.join(jd, "jet_pin3_D*.npz")), key=lambda f: float(f.rsplit("_D", 1)[1][:-4]))
    rows = []
    print("real: %s, window %.3g" % (jd, WIN))
    print("  D_b          M1 n  M1 median    half     mu      M2 n  M2 median    half     D*           error    "
          "D* - 259.9033")
    for f in fs:
        Db, c = fm.delta_series(f)
        if float(Db) < dmin:
            continue
        if len(c) != fm.N + 1:
            print("  %s: %d orders, not %d; skipped" % (os.path.basename(f), len(c), fm.N + 1))
            continue
        e = estimate(Db, c)
        e["D"] = float(Db)
        e["file"] = os.path.basename(f)
        rows.append(e)
        g = lambda x, f="%.6f": f % x if x is not None else "-"   # noqa: E731
        print("  %-12.6f %d/7  %-11s  %-7s  %-6s  %d/7  %-11s  %-7s  %-11s  %-7s  %s" % (
            float(Db), e["M1"]["n"], g(e["M1"]["med"]), g(e["M1"]["half"], "%.1e"), g(e["M1"]["mu"], "%.4f"),
            e["M2"]["n"], g(e["M2"]["med"]), g(e["M2"]["half"], "%.1e"), g(e["Dstar"]), g(e["err"], "%.1e"),
            g(e["Dstar"] - float(fm.DSTAR) if e["Dstar"] is not None else None, "%+.6f")), flush=True)
    if "json" in args:
        json.dump(dict(jets=jd, win=WIN, rows=rows), open(args["json"], "w"), indent=1, default=float)
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "planted":
        sys.exit(cmd_planted())
    if cmd == "real":
        sys.exit(cmd_real())
    raise SystemExit(__doc__)
