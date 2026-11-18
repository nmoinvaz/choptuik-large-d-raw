#!/usr/bin/env python3
"""#949 (coordinator's request, hc 2026-11-18 about 22:30 UTC): the fold fit of #949 (sigma^2 = c (D* - D) exp(-2 s (D - D_last)), c, D*, s free; fold949.fit_B)
applied to sigma_pair over the last 4 and the last 5 states, with D*, c, s, the residuals and the window shifted back by one state. A reading, outside the
pre-set trigger, never a claim.
    python pairfold949.py [FOLDER]
The series is ks 291's: the ks_chain2 states and dh370's ks_chain3b states (same ks, and ks_chain3b restarts from ks_chain2's D 237.7132 state), taken in D
order, so a window can span both chains (said in the output). The noise of sigma_pair (the relative change over the last two iterations of near_null's
subspace iteration, `conv` of the two pair vectors in each state's JSON) is used for a Monte Carlo spread of D*: sigma_pair times 1 + N(0, conv) 400 times.
The coordinator's arithmetic: if ln sigma_pair follows a fold, its slope is 1/(2 (D* - D)) at the interval's midpoint."""
import csv
import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fold949  # noqa: E402


def series(folder, ks=291):
    rows = [r for r in csv.DictReader(open(os.path.join(folder, "track949.csv"))) if int(r["ks"]) == ks and int(r["classified"]) == 1]
    out = []
    for r in sorted(rows, key=lambda r: float(r["D"])):
        pv = r["pair_vecs"].split("+")
        conv = 0.0
        for p in glob.glob(os.path.join(folder, f"*{ks}_D*.json")):
            j = json.load(open(p))
            if abs(float(j["D"]) - float(r["D"])) < 1e-5 and j["state"].find(f"_ks{ks}/") >= 0:
                conv = max(float(j["vectors"][int(i) - 1]["conv"]) for i in pv)
                break
        out.append(dict(D=float(r["D"]), sp=float(r["sigma_pair"]), chain=int(r["chain"]), conv=conv))
    return out


def fit(win):
    D = np.array([w["D"] for w in win])
    s2 = np.array([w["sp"] ** 2 for w in win])
    return D, s2, fold949.fit_B(D, s2), fold949.fit_A(D, s2)


def show(label, win, mc=400):
    D, s2, B, A = fit(win)
    chains = sorted({w["chain"] for w in win})
    print(f"{label}: D {D[0]:.4f} to {D[-1]:.4f} ({len(D)} states, chains {chains}{', spans two chains' if len(chains) > 1 else ''}), "
          f"conv up to {max(w['conv'] for w in win):.1e}")
    if B["interior"]:
        print(f"   model B: D* {B['Dstar']:.3f} ({B['Dstar'] - D[-1]:.3f} past the last state), c {B['c']:.4g}, s {B['s']:+.4f}, relative residuals of sigma^2 "
              + ", ".join(f"{x:+.1e}" for x in B["res"]))
    else:
        print(f"   model B: no interior minimum (the series is a pure exponential to the fit), s {B['s']:+.4f}")
    print(f"   model A (s = 0, the plain fold law sigma^2 = c (D* - D)): D* {A['Dstar']:.3f}, relative residuals " + ", ".join(f"{x:+.1e}" for x in A["res"]))
    if B["interior"] and mc:
        rng = np.random.default_rng(949)
        noise = max(max(w["conv"] for w in win), 1e-6)
        got = []
        for _ in range(mc):
            y = s2 * (1 + 2 * noise * rng.standard_normal(len(D)))
            b = fold949.fit_B(D, y)
            got.append(b["Dstar"] if b["interior"] else math.inf)
        q = np.percentile(got, [16, 50, 84])
        print(f"   Monte Carlo at sigma_pair noise {noise:.1e}: D* 16/50/84 percent {q[0]:.2f} {q[1]:.2f} {q[2]:.2f} ({sum(not math.isfinite(g) for g in got)} of {mc} without an interior minimum)")
    return B


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else HERE
    ser = series(folder)
    print("sigma_pair at ks 291, last states:", "; ".join(f"{w['D']:.4f}: {w['sp']:.4e} (chain {w['chain']})" for w in ser[-8:]))
    # the coordinator's arithmetic from the interval slopes
    print("coordinator's arithmetic, D* = midpoint + 1 / (2 slope) of each interval of the last 5:")
    for a, b in zip(ser[-5:], ser[-4:]):
        sl = -math.log(b["sp"] / a["sp"]) / (b["D"] - a["D"])
        mid = (a["D"] + b["D"]) / 2
        print(f"   {a['D']:.4f} -> {b['D']:.4f}: slope {sl:+.3f}" + (f", D* {mid + 1 / (2 * sl):.2f}" if sl > 0 else ", rising: no D*"))
    Bs = {}
    for n in (4, 5):
        if len(ser) >= n:
            Bs[n] = show(f"last {n}", ser[-n:])
            if len(ser) >= n + 1:
                bs = show(f"last {n} shifted back by one state", ser[-n - 1:-1], mc=0)
                if Bs[n]["interior"] and bs["interior"]:
                    print(f"   window shift: D* moves by {bs['Dstar'] - Bs[n]['Dstar']:+.3f}")


main()
