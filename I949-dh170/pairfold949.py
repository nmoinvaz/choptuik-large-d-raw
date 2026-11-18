#!/usr/bin/env python3
"""#949: sigma_pair along the order-tied chain, its interval slope, and the fold law's D* over the last 4 and 5 states with the window shift, state by state.

    python pairfold949.py [FOLDER]          the last states' table (also written to FOLDER/pairfold949.csv), the reading and the alert
    python pairfold949.py --selftest [--mutate]    planted series with known answers (exit 1 on failure; --mutate breaks the stability test, must fail)

The series is every classified state of ks >= 291 (ks_chain2, dh370's ks_chain3b and ks_chain3), in D order, one state per D (equal D to 1e-6 keeps
the first of ks_chain2, ks_chain3b, ks_chain3): the pair does not move with ks above 291 (sigma_pair equal to 3e-9 at D 237.7132 for ks 291, 295, 299,
#949), so the series runs across the chains; a window can span two chains and the interval slope across a chain boundary is a reading too.

The fold law (fold949.fit_B): sigma_pair^2 = c (D* - D) exp(-2 s (D - D_last)), c, D* and s free. For the state n as the latest:
  D4, D5   D* of the window of the last 4 and of the last 5 states (None without an interior minimum);
  shift4, shift5   D* of the same window moved back by one state, minus D4 and D5.
The coordinator's reading rule (hc 2026-11-18 about 22:50 UTC, fixed before more states came): a state satisfies the rule when |D4 - D5| <= 0.1 and
|shift4| <= 0.1 and |shift5| <= 0.1; a candidate zero of sigma_pair at D* is called only when two states in a row satisfy it. Until then the
reading is 'falling, no stable D*' (or 'not falling' where the slope is not positive). Alert: a state whose D lies within 0.3 of the previous
state's D* estimate (the mean of D4 and D5) is reported at once."""
import csv
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fold949  # noqa: E402

AGREE, SHIFT, ALERT = 0.1, 0.1, 0.3
CHAIN_ORDER = {2: 0, 4: 1, 3: 2}      # which chain's state is kept where two have the same D


def series(folder, kmin=291):
    rows = [r for r in csv.DictReader(open(os.path.join(folder, "track949.csv")))
            if int(r["ks"]) >= kmin and int(r["chain"]) in CHAIN_ORDER and int(r["classified"]) == 1]
    rows.sort(key=lambda r: (float(r["D"]), CHAIN_ORDER[int(r["chain"])]))
    out = []
    for r in rows:
        d = float(r["D"])
        if out and abs(d - out[-1]["D"]) < 1e-6:
            continue
        out.append(dict(D=d, sp=float(r["sigma_pair"]), sd=float(r["sigma_delta"]), chain=int(r["chain"]), ks=int(r["ks"])))
    return out


def dstar(win):
    D = np.array([w["D"] for w in win])
    s2 = np.array([w["sp"] ** 2 for w in win])
    b = fold949.fit_B(D, s2)
    return (b["Dstar"] if b["interior"] else None), b


def evaluate(ser, n):
    """the row of state n (index into ser) as the latest state"""
    out = dict(D=ser[n]["D"], sp=ser[n]["sp"], ks=ser[n]["ks"], chain=ser[n]["chain"])
    out["slope"] = -math.log(ser[n]["sp"] / ser[n - 1]["sp"]) / (ser[n]["D"] - ser[n - 1]["D"]) if n >= 1 else None
    for k in (4, 5):
        if n - k < 0:
            out.update({f"D{k}": None, f"shift{k}": None})
            continue
        d, _ = dstar(ser[n - k + 1:n + 1])
        ds, _ = dstar(ser[n - k:n]) if d is not None else (None, None)
        out[f"D{k}"] = d
        out[f"shift{k}"] = None if d is None or ds is None else ds - d
    ok = all(out[x] is not None for x in ("D4", "D5", "shift4", "shift5"))
    out["rule"] = bool(ok and abs(out["D4"] - out["D5"]) <= AGREE and abs(out["shift4"]) <= SHIFT and abs(out["shift5"]) <= SHIFT)
    return out


def reading(rows):
    """the reading at the last row: candidate zero (two in a row), or falling without a stable D*, or not falling"""
    last = rows[-1]
    if len(rows) >= 2 and last["rule"] and rows[-2]["rule"]:
        return f"CANDIDATE ZERO of sigma_pair at D* {(last['D4'] + last['D5']) / 2:.3f} (rule met at the last two states)"
    if last["slope"] is None or last["slope"] <= 0:
        return "not falling"
    return "falling, no stable D*"


def alerts(rows):
    """states within ALERT of the D* estimate (the mean of D4 and D5) of the state before them"""
    out = []
    for prev, cur in zip(rows, rows[1:]):
        if prev["D4"] is not None and prev["D5"] is not None:
            est = (prev["D4"] + prev["D5"]) / 2
            if cur["D"] >= est - ALERT:
                out.append(f"ALERT: the state at D {cur['D']:.4f} lies {est - cur['D']:+.3f} from the D* estimate {est:.3f} of the state at D {prev['D']:.4f}")
    return out


def fmt(x, w=8, signed=False):
    return " " * (w - 1) + "-" if x is None else f"{x:{'+' if signed else ''}{w}.3f}"


def table(folder, last=10):
    ser = series(folder)
    rows = [evaluate(ser, n) for n in range(len(ser))]
    with open(os.path.join(folder, "pairfold949.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["D", "ks", "chain", "sigma_pair", "interval_slope", "Dstar_last4", "shift4", "Dstar_last5", "shift5", "rule_met"])
        for r in rows:
            w.writerow([f"{r['D']:.6f}", r["ks"], r["chain"], f"{r['sp']:.6e}", "" if r["slope"] is None else f"{r['slope']:+.4f}",
                        "" if r["D4"] is None else f"{r['D4']:.3f}", "" if r["shift4"] is None else f"{r['shift4']:+.3f}",
                        "" if r["D5"] is None else f"{r['D5']:.3f}", "" if r["shift5"] is None else f"{r['shift5']:+.3f}", int(r["rule"])])
    print("sigma_pair, ks >= 291 (the pair does not move with ks above 291), the fold law's D* over the last 4 and 5 states and the window shift:")
    print(f"{'D':>9} {'ks':>4} {'ch':>2} {'sigma_pair':>11} {'slope':>7} {'D*(4)':>8} {'shift4':>7} {'D*(5)':>8} {'shift5':>7}  rule (|D4-D5|, shifts <= 0.1)")
    for r in rows[-last:]:
        print(f"{r['D']:9.4f} {r['ks']:4d} {r['chain']:2d} {r['sp']:11.4e} {'' if r['slope'] is None else format(r['slope'], '+7.3f'):>7} {fmt(r['D4'])} "
              f"{fmt(r['shift4'], 7, True)} {fmt(r['D5'])} {fmt(r['shift5'], 7, True)}  {'met' if r['rule'] else 'not met'}")
    print("reading:", reading(rows))
    for a in alerts(rows):
        print(a)
    return rows


def planted(Dstar, D0, n, h, law=1.0):
    return [dict(D=D0 + h * i, sp=math.sqrt(0.3 * (Dstar - (D0 + h * i)) ** law), sd=1.0, chain=2, ks=291) for i in range(n)]


def selftest(mutate):
    global SHIFT, AGREE
    ok = True
    saved = (SHIFT, AGREE)
    if mutate:
        SHIFT, AGREE = 1e9, 1e9      # the stability test off: the drifting law below would then be accepted
    # (a) the fold law itself, sigma^2 = 0.3 (260 - D), states 0.4 apart: D4 = D5 = 260, shifts 0, rule met twice, candidate called
    ser = planted(260.0, 256.0, 9, 0.4)
    rows = [evaluate(ser, n) for n in range(len(ser))]
    r = rows[-1]
    good = r["rule"] and rows[-2]["rule"] and abs(r["D4"] - 260) < 1e-6 and abs(r["D5"] - 260) < 1e-6 and abs(r["shift4"]) < 1e-6 and reading(rows).startswith("CANDIDATE")
    ok &= good
    print(f"selftest: planted fold 260: D4 {r['D4']:.6f}, D5 {r['D5']:.6f}, shifts {r['shift4']:+.1e} {r['shift5']:+.1e}, {reading(rows)[:28]}: {'pass' if good else 'FAIL'}")
    # (b) another law, sigma^2 = 0.3 (260 - D)^2.5: the fit's D* moves with the window, the rule is not met and no zero is called
    ser = planted(260.0, 255.0, 9, 0.5, law=2.5)
    rows = [evaluate(ser, n) for n in range(len(ser))]
    good = (not rows[-1]["rule"]) and reading(rows) == "falling, no stable D*"
    ok &= good
    print(f"selftest: planted (260 - D)^2.5 law, D4 {rows[-1]['D4']:.3f} D5 {rows[-1]['D5']:.3f} shifts {rows[-1]['shift4']:+.3f} {rows[-1]['shift5']:+.3f}, {reading(rows)}: {'pass' if good else 'FAIL'}")
    # (c) the rule needs two states in a row: one met state after a not-met one is no candidate
    rows2 = [dict(rows[-1], rule=False), dict(rows[-1], rule=True, slope=0.3)]
    good = reading(rows2) == "falling, no stable D*"
    ok &= good
    print(f"selftest: one met state after a not-met one is no candidate: {'pass' if good else 'FAIL'}")
    # (d) a rising pair is 'not falling'
    ser = [dict(D=230 + 0.4 * i, sp=1e-10 * (1 + 0.01 * i), sd=1.0, chain=2, ks=291) for i in range(9)]
    rows3 = [evaluate(ser, n) for n in range(len(ser))]
    good = reading(rows3) == "not falling"
    ok &= good
    print(f"selftest: a rising pair reads 'not falling': {'pass' if good else 'FAIL'}")
    # (e) the alert: states within 0.3 of the previous state's D* estimate
    ser = planted(260.0, 258.0, 7, 0.3)
    rows4 = [evaluate(ser, n) for n in range(len(ser))]
    al = alerts(rows4)
    good = len(al) >= 1
    ok &= good
    print(f"selftest: states within 0.3 of the previous D* estimate raise the alert ({len(al)}): {'pass' if good else 'FAIL'}")
    SHIFT, AGREE = saved
    print(f"selftest{' --mutate' if mutate else ''}: {'pass' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    table(args[0] if args else HERE)
