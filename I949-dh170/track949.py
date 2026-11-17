#!/usr/bin/env python3
"""#949: the running table of the Delta mode's sigma along the order-tied chain, with the local slope of ln sigma_Delta and the fold fit.

    track949.py [FOLDER]            read the state JSONs of near_null.py in FOLDER (default: this folder): ksNNN_DDDD.json (one per
                                    state, run949.sh), ctl_planted.json (D 229.0509 re-read, with the planted check) and from941/
                                    (the five states of #941, I941-dh370 9da736f7), write FOLDER/track949.csv and
                                    FOLDER/intervals949.csv and print the tables
    track949.py --selftest [--mutate]   planted series with known slopes and a planted fold; --mutate uses a forward difference
                                    for the slope, which the checks must catch (exit 1)

Classification of a state's six vectors is #941's analyze941.py (copied): the Delta mode is the vector with the largest Delta share
(it must exceed 0.5), sigma_pair is the geometric mean of the two vectors, not the Delta mode, whose two largest (block, harmonic)
components are (p1, 3) and (m_h, 3) (in either order, one of them among the first two and the other among the printed five); exactly
two must qualify. A state that does not classify is printed with its vectors and left out of the slope and the fit.

A row's local slope is -ln(sigma_{i+1} / sigma_{i-1}) / (D_{i+1} - D_{i-1}) over its two neighbours, and an interval's slope is
-ln(sigma_{i+1} / sigma_i) / (D_{i+1} - D_i) (the quantity #941 quotes). They are used for the triggers and the fit only when every
state involved has the same ks (the chain changes its horizon order at each leg, and sigma_Delta jumps there). The literal
trigger of the issue is three consecutive such rows with slope above 0.10; the excess trigger, three with slope - 0.405 above
0.10 (0.405 is #941's constant slope at order 240). The fold fit (fold949.py: model B, c, D* and s free) is run on the last five
states of each ks, with model A (the literal linear fit) and model C (s fixed at 0.405) beside it."""
import csv
import glob
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fold949  # noqa: E402

BASE = 0.405                        # #941's log slope at order 240
QUOTED_941 = [0.412, 0.410, 0.407, 0.405]   # the intervals over D 229.0509, 229.9822, 230.9281, 231.7466, 232.0 (#941's closing)


def is_pair_member(top):
    names = {(b, k) for b, k, _ in top}
    first2 = {(b, k) for b, k, _ in top[:2]}
    return ("p1", 3) in names and ("m_h", 3) in names and bool(first2 & {("p1", 3), ("m_h", 3)})


def classify(rec):
    """-> (index of the Delta mode, [two pair indices]) or raises ValueError"""
    v = rec["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    if v[d]["delta"] <= 0.5:
        raise ValueError(f"no vector has a Delta share above 0.5 (largest {v[d]['delta']:.3f})")
    pair = [i for i in range(len(v)) if i != d and is_pair_member(v[i]["top"])]
    if len(pair) != 2:
        raise ValueError(f"{len(pair)} vectors look like the harmonic-3 pair (need 2): {pair}")
    return d, pair


def row_of(rec, src):
    ks = int(re.search(r"_ks(\d+)/", rec["state"]).group(1))
    r = dict(D=float(rec["D"]), ks=ks, src=src, state=rec["state"], ok=True, note="")
    v = rec["vectors"]
    try:
        d, pair = classify(rec)
    except ValueError as e:
        r.update(ok=False, note=str(e), sd=float("nan"), sp=float("nan"), share=float("nan"), conv=float("nan"), dvec=0, pvec="")
        d = int(np.argmin([x["sigma"] for x in v]))
        r.update(sd=v[d]["sigma"], share=v[d]["delta"], conv=v[d]["conv"])
        return r
    second = sorted((x["delta"] for i, x in enumerate(v) if i != d), reverse=True)[0]
    r.update(sd=v[d]["sigma"], sp=math.sqrt(v[pair[0]]["sigma"] * v[pair[1]]["sigma"]), share=v[d]["delta"], conv=v[d]["conv"],
             dvec=d + 1, pvec=f"{pair[0] + 1}+{pair[1] + 1}", s5=v[4]["sigma"], share2=second)
    return r


def load(folder):
    rows = {}
    for p in sorted(glob.glob(os.path.join(folder, "from941", "o*_D*.json"))):
        r = row_of(json.load(open(p)), "I941-dh370")
        rows[(r["ks"], round(r["D"], 6))] = r
    own = {}
    for p in sorted(glob.glob(os.path.join(folder, "ks*_D*.json")) + glob.glob(os.path.join(folder, "ctl_planted.json"))):
        r = row_of(json.load(open(p)), os.path.basename(p)[:-5])
        key = (r["ks"], round(r["D"], 6))
        if key in rows:                        # a re-read of a #941 state: kept apart for the comparison
            own[key] = r
        else:
            rows[key] = r
    return sorted(rows.values(), key=lambda r: r["D"]), own


def slopes(rows, central=True):
    """per row: local slope over the two neighbours (None at the ends or where a neighbour is not classified), and whether its three
    states share a ks"""
    out = []
    for i, r in enumerate(rows):
        s, same = None, True
        if 0 < i < len(rows) - 1:
            a, b = rows[i - 1], rows[i + 1]
            if a["ok"] and b["ok"] and r["ok"]:
                if central:
                    s = -math.log(b["sd"] / a["sd"]) / (b["D"] - a["D"])
                else:                          # --mutate: a forward difference
                    s = -math.log(b["sd"] / r["sd"]) / (b["D"] - r["D"])
                same = a["ks"] == r["ks"] == b["ks"]
        out.append((s, same))
    return out


def intervals(rows):
    out = []
    for a, b in zip(rows, rows[1:]):
        if a["ok"] and b["ok"]:
            out.append(dict(D0=a["D"], D1=b["D"], ks0=a["ks"], ks1=b["ks"], slope=-math.log(b["sd"] / a["sd"]) / (b["D"] - a["D"]),
                            cross=a["ks"] != b["ks"]))
    return out


def run_trigger(rows, sl, key):
    """the index of the third consecutive row (same ks run, same-ks neighbours) whose key(slope) exceeds 0.10, or None"""
    n = 0
    for i, (r, (s, same)) in enumerate(zip(rows, sl)):
        if s is not None and same and key(s) > 0.10 and (n == 0 or rows[i - 1]["ks"] == r["ks"]):
            n += 1
            if n >= 3:
                return i
        else:
            n = 0
    return None


def fits(rows):
    """the fold fit on the last five states of each ks that has five: [(ks, D list, A, B, C)]"""
    out = []
    for ks in sorted({r["ks"] for r in rows}):
        g = [r for r in rows if r["ks"] == ks and r["ok"]][-5:]
        if len(g) < 5:
            continue
        D = np.array([r["D"] for r in g])
        s2 = np.array([r["sd"] ** 2 for r in g])
        out.append((ks, D, fold949.fit_A(D, s2), fold949.fit_B(D, s2), fold949.fit_C(D, s2, BASE)))
    return out


def tables(folder, central=True, quiet=False):
    rows, own = load(folder)
    sl = slopes(rows, central)
    iv = intervals(rows)
    with open(os.path.join(folder, "track949.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["D", "ks", "sigma_delta", "sigma_pair", "delta_share", "delta_share_2nd", "delta_vec", "pair_vecs", "conv_delta", "slope", "excess_over_0.405",
                    "slope_same_ks", "classified", "source"])
        for r, (s, same) in zip(rows, sl):
            w.writerow([f"{r['D']:.6f}", r["ks"], f"{r['sd']:.6e}", f"{r.get('sp', float('nan')):.6e}", f"{r['share']:.4f}", f"{r.get('share2', float('nan')):.4f}", r.get("dvec", ""),
                        r.get("pvec", ""), f"{r['conv']:.1e}", "" if s is None else f"{s:.4f}", "" if s is None else f"{s - BASE:+.4f}",
                        "" if s is None else int(same), int(r["ok"]), r["src"]])
    with open(os.path.join(folder, "intervals949.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["D0", "D1", "ks0", "ks1", "slope", "crosses_ks"])
        for x in iv:
            w.writerow([f"{x['D0']:.6f}", f"{x['D1']:.6f}", x["ks0"], x["ks1"], f"{x['slope']:.4f}", int(x["cross"])])
    ok = True
    if not quiet:
        print(f"{'D':>9} {'ks':>4} {'sigma_Delta':>12} {'sigma_pair':>12} {'Dshare':>7} {'2nd':>6} {'conv':>8} {'slope':>7} {'excess':>7}  note")
        for r, (s, same) in zip(rows, sl):
            conv = "" if r["conv"] < 1e-3 else "  NOT CONVERGED (rerun --its=32)"
            note = ("" if r["ok"] else "  NOT CLASSIFIED: " + r["note"]) + conv + ("" if same else "  (spans a ks change)")
            print(f"{r['D']:9.4f} {r['ks']:4d} {r['sd']:12.4e} {r.get('sp', float('nan')):12.4e} {r['share']:7.3f} {r.get('share2', float('nan')):6.3f} {r['conv']:8.1e} "
                  f"{'' if s is None else format(s, '7.4f'):>7} {'' if s is None else format(s - BASE, '+7.4f'):>7}  "
                  f"v{r.get('dvec', '?')}/{r.get('pvec', '?')}{note}")
        print("\nintervals (slope -d ln sigma_Delta / dD per consecutive pair):")
        for x in iv:
            print(f"  {x['D0']:9.4f} -> {x['D1']:9.4f}  ks {x['ks0']}->{x['ks1']}  {x['slope']:.4f}{'  (crosses a ks change)' if x['cross'] else ''}")
        bad = [r for r in rows if not r["ok"] or r["conv"] >= 1e-3]
        print(f"\nstates {len(rows)}, not classified or not converged: {len(bad)}" + "".join(f"\n  D {r['D']:.4f}: {r['note'] or 'conv ' + format(r['conv'], '.1e')}" for r in bad))
        # criterion 5: #941's four intervals
        w941 = [x for x in iv if 229.0 < x["D0"] and x["D1"] <= 232.0001 and x["ks0"] == x["ks1"] == 240][-4:]
        if len(w941) == 4:
            d = [abs(x["slope"] - q) for x, q in zip(w941, QUOTED_941)]
            print(f"\ncriterion 5, intervals D 229.05 to 232.0: {', '.join(format(x['slope'], '.4f') for x in w941)} against #941's "
                  f"{', '.join(map(str, QUOTED_941))}: largest difference {max(d):.4f}: {'pass' if max(d) <= 0.01 else 'FAIL'}")
            ok &= max(d) <= 0.01
        for key, r in own.items():
            ref = next(x for x in rows if (x["ks"], round(x["D"], 6)) == key)
            print(f"re-read of #941's state D {key[1]:.4f}: sigma_Delta {r['sd']:.10e} here ({r['src']}) against {ref['sd']:.10e} (relative "
                  f"difference {abs(r['sd'] / ref['sd'] - 1):.1e}); Delta share {r['share']:.4f} against {ref['share']:.4f}")
        it = run_trigger(rows, sl, lambda s: s)
        ie = run_trigger(rows, sl, lambda s: s - BASE)
        print(f"\nliteral trigger (slope > 0.10, three in a row, same ks): {'at D ' + format(rows[it]['D'], '.4f') if it is not None else 'not reached'}")
        print(f"excess trigger (slope - 0.405 > 0.10, three in a row, same ks): {'at D ' + format(rows[ie]['D'], '.4f') + ' (fold candidate)' if ie is not None else 'not reached'}")
        print("\nfold fit on the last five states of each ks (valid: every relative residual of sigma^2 within 0.10, D* past the last state):")
        for ks, D, A, B, C in fits(rows):
            vb = fold949.valid(B, D)
            res = "n/a" if not B["interior"] else f"{np.abs(B['res']).max():.1e}"
            print(f"  ks {ks}, D {D[0]:.4f} to {D[-1]:.4f}: B D* {B['Dstar']:.1f} (c {B['c']:.3g}, s {B['s']:.4f}, max |res| {res}, "
                  f"{'valid' if vb else 'not valid'}{'' if B['interior'] else ', no interior minimum'}); "
                  f"A D* {A['Dstar']:.1f} max|res| {np.abs(A['res']).max():.2f}; C (s 0.405) D* {C['Dstar']:.1f} max|res| {np.abs(C['res']).max():.2f}")
    return ok, rows, sl


def selftest(mutate):
    """planted series: a pure exponential (slope 0.40, uneven D), a fold with the exponential (D* 260), and a record that must not
    classify; every check must be able to fail, and the forward-difference mutation must fail the fold series' central slope"""
    ok = True
    D = [200.0, 202.0, 203.5, 206.0, 208.0, 210.0, 213.0]
    rows = [dict(D=d, ks=211, sd=1e-14 * math.exp(-0.40 * (d - 200)), ok=True) for d in D]
    sl = slopes(rows, not mutate)
    e1 = max(abs(s - 0.40) for s, _ in sl if s is not None)
    ok &= e1 < 1e-12
    print(f"selftest: pure exponential, central slope error {e1:.1e}: {'pass' if e1 < 1e-12 else 'FAIL'}")
    D = [233.0, 234.0, 235.0, 236.0, 237.0, 238.0]
    s2 = [0.3 * (260 - d) * math.exp(-2 * 0.405 * (d - 232)) for d in D]
    rows = [dict(D=d, ks=250, sd=math.sqrt(v), ok=True) for d, v in zip(D, s2)]
    sl = slopes(rows, not mutate)
    # central slope of the planted fold series: exact secant -ln(sd_{i+1}/sd_{i-1})/(D_{i+1}-D_{i-1}) = 0.405 + ln((260-D_{i-1})/(260-D_{i+1}))/(2 dD)
    want = [0.405 + 0.5 * math.log((260 - D[i - 1]) / (260 - D[i + 1])) / (D[i + 1] - D[i - 1]) for i in range(1, 5)]
    e2 = max(abs(sl[i][0] - want[i - 1]) for i in range(1, 5))
    ok &= e2 < 1e-12
    print(f"selftest: planted fold + exponential, central slope error {e2:.1e}: {'pass' if e2 < 1e-12 else 'FAIL'}")
    it = run_trigger(rows, sl, lambda s: s)
    ie = run_trigger(rows, sl, lambda s: s - BASE)
    ok &= it == 3 and ie is None            # literal trigger fires at the third slope, the excess (about 0.02) never does
    print(f"selftest: planted fold 28 units off: literal trigger row {it} (want 3), excess trigger {ie} (want None): "
          f"{'pass' if it == 3 and ie is None else 'FAIL'}")
    D = [255.0, 255.5, 256.0, 256.5, 257.0, 257.5]
    rows = [dict(D=d, ks=250, sd=math.sqrt(0.3 * (260 - d) * math.exp(-2 * 0.405 * (d - 232))), ok=True) for d in D]
    sl = slopes(rows, not mutate)
    ie = run_trigger(rows, sl, lambda s: s - BASE)
    ok &= ie is not None
    print(f"selftest: planted fold 3 to 5 units off: excess trigger row {ie} (want not None): {'pass' if ie is not None else 'FAIL'}")
    sl2 = slopes([dict(D=1.0, ks=1, sd=1.0, ok=True), dict(D=2.0, ks=2, sd=0.5, ok=True), dict(D=3.0, ks=2, sd=0.25, ok=True)])
    ok &= sl2[1][1] is False
    print(f"selftest: a ks change among the three states is flagged: {'pass' if sl2[1][1] is False else 'FAIL'}")
    rec = dict(vectors=[dict(sigma=1e-9 * (i + 1), delta=0.1, top=[["p1", 1, 0.5]]) for i in range(6)], state="x_ks1/y.npz", D=1.0)
    try:
        classify(rec)
        ok = False
        print("selftest: a record with no Delta mode must not classify: FAIL")
    except ValueError:
        print("selftest: a record with no Delta mode does not classify: pass")
    print(f"selftest{' --mutate' if mutate else ''}: {'pass' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(0 if tables(args[0] if args else os.path.dirname(os.path.abspath(__file__)))[0] else 1)
