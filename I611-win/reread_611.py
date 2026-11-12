#!/usr/bin/env python3
"""#611: #404's RT ladders read against hp's quad-double Delta of the uncut problem (and of the kf 13 cut).
usage: python reread_611.py D50|D54|D60 [SHIFT]      (from this folder; needs qd_<kf13|kfm1>_<D>.jsonl here and ../I404-win/roots)
SHIFT is the mutation control: it adds SHIFT to both references (the verdict must change for a shift of 1e-14 at D50; reread_D50_shift.txt).
Delta_qd = the sum of the four parts Delta_q of the last record of a polish (exact, in arb at 400 bits). Delta_RT = the 30-digit Delta_str of the records of a101_32xN.jsonl and b121_32xN.jsonl at that D.
Per N: root a - uncut, root b - uncut, E_uncut(N) = the larger of the two, the same against the kf 13 value, the spread a - b. Verdict (#404's rule on the uncut reference): the ladder FALLS to below 1e-14 when some N* has
both roots within 1e-14 of the reference and a spread below 1e-14 with E_uncut strictly falling up to N* (or N* is the first rung); otherwise it STOPS FALLING at N_s, the first rung whose E is not below the previous rung's."""
import json
import os
import sys

import flint

flint.ctx.prec = 400
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = os.path.join(HERE, "..", "I404-win", "roots")
DVAL = {"D50": 50.007491, "D54": 54.996085, "D60": 60.001952}
LADDER = (99, 103, 107, 111, 115, 119, 123)
TOL = 1e-14


def delta_qd(tag):
    last = None
    for ln in open(os.path.join(HERE, f"qd_{tag}.jsonl")):
        r = json.loads(ln)
        if r.get("ok"):          # each jsonl holds the converged own-D record of its start (and the converged continuation steps, none of which exist here)
            last = r
    if last is None:
        return None, None
    s = arb(0)
    for p in last["Delta_q"]:
        s += arb(p)
    return s, last


def rt_delta(t, N, D):
    p = os.path.join(ROOTS, f"{t}_32x{N}.jsonl")
    out = None
    for ln in open(p):
        r = json.loads(ln)
        if r.get("solver") == "mp" and r.get("ok") and abs(r["D"] - D) < 1e-5:
            out = arb(r["Delta_str"])
    return out


def f(x):
    return float(x.mid())


def main():
    dt = sys.argv[1]
    D = DVAL[dt]
    refs = {}
    for k in ("kf13", "kfm1"):
        tags = [f"{k}_{dt}"] if dt != "D54" else [f"{k}_D54a", f"{k}_D54b"]
        for tg in tags:
            try:
                v, rec = delta_qd(tg)
            except FileNotFoundError:        # a polish that did not converge writes no record (only its attempts file)
                continue
            if v is not None:
                refs[tg] = (v, rec)
    print(f"== D {D}: hp quad-double Delta (the last converged record of each polish)")
    for tg, (v, rec) in refs.items():
        print(f"  {tg}: Delta {v.mid().str(32, radius=False)}  max|F| {rec['F']:.1e}, {rec['steps']} Newton steps, {rec['seconds']:.0f} s")
    estimated = False
    if dt == "D54":
        # no polish exists at D 54.996085 (no state of that D is kept and scan_qd.py's continuation fails here): the references are ESTIMATED from the two own-D polishes
        # at D 54.041398 (b) and D 55.035148 (a), linearly in D: the quad-double kf 13 Delta as the dd row of delta_all.csv at 54.996085 plus the interpolated (qd - row) offset,
        # the uncut one as that plus the interpolated cut effect (no cut - kf 13)
        rows = {}
        for ln in open(os.path.join(HERE, "..", "..", "choptuik-i611", "hp", "data", "delta_all.csv")):
            c = ln.split(",")
            try:
                rows[round(float(c[0]), 6)] = arb(c[1]) + arb(c[2])
            except (ValueError, IndexError):
                pass
        Db, Da, Dt = 54.041398, 55.035148, 54.996085
        qb, qa = refs["kf13_D54b"][0], refs["kf13_D54a"][0]
        ub, ua = refs["kfm1_D54b"][0], refs["kfm1_D54a"][0]
        w = arb((Dt - Db) / (Da - Db))
        off = (qb - rows[Db]) * (1 - w) + (qa - rows[Da]) * w
        eff = (ub - qb) * (1 - w) + (ua - qa) * w
        cut = rows[Dt] + off
        uncut = cut + eff
        estimated = True
        print(f"  qd - dd row: {f(qb - rows[Db]):+.2e} at {Db}, {f(qa - rows[Da]):+.2e} at {Da}; interpolated to {Dt}: {f(off):+.2e}")
        print(f"  the cut's effect (no cut - kf 13): {f(ub - qb):+.4e} at {Db}, {f(ua - qa):+.4e} at {Da}; interpolated to {Dt}: {f(eff):+.4e} (the two differ by {f((ua - qa) - (ub - qb)):+.1e})")
        print(f"  ESTIMATED Delta at D {Dt}: kf 13 {cut.mid().str(30, radius=False)}, no cut {uncut.mid().str(30, radius=False)} (error of the estimate about 5e-17: the offset qd - dd row is +4.8e-17, -1.7e-18, +1.3e-17, -6.9e-17 at D 50, 54.04, 55.04, 60)")
    elif dt == "D60":
        cut = refs.get("kf13_D60", (None,))[0]
        uncut = None
        print("  the no-cut polish did not converge (see the README): the table below is against the kf 13 quad-double Delta; the uncut column is n/a")
    else:
        uncut = refs.get(f"kfm1_{dt}", (None,))[0]
        cut = refs.get(f"kf13_{dt}", (None,))[0]
    if cut is None or (uncut is None and dt != "D60"):
        print("missing polishes")
        return
    if uncut is not None and not estimated:
        print(f"  the cut's effect (no cut - kf 13): {f(uncut - cut):+.4e}")
    if uncut is None:
        uncut = cut
    if len(sys.argv) > 2:                  # mutation control: the references are moved by SHIFT
        uncut, cut = uncut + arb(float(sys.argv[2])), cut + arb(float(sys.argv[2]))
        print(f"  MUTATION: both references shifted by {float(sys.argv[2]):+.1e}")
    print("\n| N | root a - uncut | root b - uncut | E_uncut(N) | root a - kf 13 | root b - kf 13 | E_cut(N) | spread a - b | passes 1e-14 (uncut) |\n|---|---|---|---|---|---|---|---|---|")
    rows = []
    for N in LADDER:
        a, b = rt_delta("a101", N, D), rt_delta("b121", N, D)
        if a is None or b is None:
            continue
        ea, eb, ca, cb, sp = f(a - uncut), f(b - uncut), f(a - cut), f(b - cut), f(a - b)
        Eu, Ec = max(abs(ea), abs(eb)), max(abs(ca), abs(cb))
        ok = abs(ea) < TOL and abs(eb) < TOL and abs(sp) < TOL
        rows.append((N, Eu, ok, ea, eb, sp))
        print(f"| {N} | {ea:+.2e} | {eb:+.2e} | {Eu:.2e} | {ca:+.2e} | {cb:+.2e} | {Ec:.2e} | {sp:+.2e} | {'yes' if ok else 'no'} |")
    ok_i = [i for i, r in enumerate(rows) if r[2]]
    verdict = None
    if ok_i:
        k = ok_i[0]
        if all(rows[i][1] > rows[i + 1][1] for i in range(k)):
            verdict = f"the ladder FALLS to below 1e-14 at N* = {rows[k][0]} (E_uncut = {rows[k][1]:.2e}, spread {abs(rows[k][5]):.2e})" + ("" if k else " (the first rung)")
    if verdict is None:
        ns = next((i for i in range(len(rows) - 1) if rows[i + 1][1] >= rows[i][1]), None)
        if ns is None:
            ns = min(range(len(rows)), key=lambda i: rows[i][1])
        r = rows[ns]
        verdict = f"the ladder STOPS FALLING at N_s = {r[0]}: E_uncut = {r[1]:.2e}, spread {abs(r[5]):.2e}" + ("" if not ok_i else f"; a grid passes (N = {rows[ok_i[0]][0]}) but E_uncut does not fall strictly up to it")
    best = min(rows, key=lambda r: r[1])
    print(f"\nVERDICT {dt} against the uncut Delta: {verdict}; the best N is {best[0]} with E_uncut = {best[1]:.2e}; passing grids: {[r[0] for r in rows if r[2]] or 'none'}")


if __name__ == "__main__":
    main()
