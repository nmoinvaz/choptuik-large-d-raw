#!/usr/bin/env python3
"""#949: the running table of the Delta mode's sigma along the order-tied chain, the frozen baseline, the trigger and the fold rule.

    track949.py [FOLDER]            read the state JSONs of near_null.py in FOLDER (default: this folder): ksNNN_DDDD.json (one per
                                    state, run949.sh), ctl_planted.json (D 229.0509 re-read, with the planted check) and from941/
                                    (the five states of #941, I941-dh370 9da736f7), write FOLDER/track949.csv and
                                    FOLDER/intervals949.csv and print the tables, the null control and the fold rule
    track949.py --freeze [FOLDER]   fit the baseline s(ks) on the backfill's legs (ks 211 to 240) and write baseline949.json; refuses
                                    when a state of a higher ks has been read, when a leg has fewer than five states or an unconverged
                                    or unclassified one, or when baseline949.json exists
    track949.py --selftest [--mutate]   planted records and series with known answers; --mutate uses a forward difference for the
                                    central slope and the checks must catch it (exit 1)

Classification of a state's six vectors is #941's analyze941.py (copied): the Delta mode is the vector with the largest Delta share
(it must exceed 0.5), sigma_pair is the geometric mean of the two vectors, not the Delta mode, whose two largest (block, harmonic)
components are (p1, 3) and (m_h, 3) (in either order, one of them among the first two and the other among the printed five); exactly
two must qualify. A state that does not classify is printed with its vectors and left out of every slope and fit.

The rule (coordinator, issue #949, 2026-11-17 23:18 UTC, fixed before leg 8's first read):
  baseline   s(ks) = a + b / ks, a least-squares line in 1/ks through each backfill leg's slope of ln sigma_Delta against D (the leg's
             states, ks 211, 220, 230, 240; the least-squares slope over the leg), frozen in baseline949.json before any state of
             ks >= 250 is read. For ks >= 250 it is extrapolated, and the spread against a line in ks is reported.
  trigger    the interval slope -ln(sigma_i / sigma_{i-1}) / (D_i - D_{i-1}) minus s(ks) exceeds 0.10 at three consecutive states of one
             leg (an interval belongs to its later state, and both states must have the same ks).
  fold       fold949.rule on the five latest states of one ks: residuals within 10%, D* past the last state by no more than 3, the
             window moved back by one state within 0.3, and the planted series with the frozen slope and a scatter of 0.03 returns D*
             within 0.3. A fold is claimed only from a valid fit with the trigger fired.
  null       the rule applied to every five-state window of every backfill leg must return no valid fold, and the ks 211 window's D*
             of 212.8 must fail by condition 2 (a window that passes stops the work)."""
import csv
import glob
import json
import math
import os
import re
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fold949  # noqa: E402

TRIGGER = 0.10
QUOTED_941 = [0.412, 0.410, 0.407, 0.405]   # the intervals over D 229.0509, 229.9822, 230.9281, 231.7466, 232.0 (#941's closing)
BACKFILL_KS = (211, 220, 230, 240)
EXTRAP_KS = (250, 260, 270, 300, 400)


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
        d = int(np.argmin([x["sigma"] for x in v]))
        r.update(ok=False, note=str(e), sd=v[d]["sigma"], sp=float("nan"), share=v[d]["delta"], share2=float("nan"), conv=v[d]["conv"],
                 dvec=0, pvec="")
        return r
    second = sorted((x["delta"] for i, x in enumerate(v) if i != d), reverse=True)[0]
    r.update(sd=v[d]["sigma"], sp=math.sqrt(v[pair[0]]["sigma"] * v[pair[1]]["sigma"]), share=v[d]["delta"], share2=second,
             conv=v[d]["conv"], dvec=d + 1, pvec=f"{pair[0] + 1}+{pair[1] + 1}")
    return r


def load(folder):
    rows, own = {}, {}
    for p in sorted(glob.glob(os.path.join(folder, "from941", "o*_D*.json"))):
        r = row_of(json.load(open(p)), "I941-dh370")
        rows[(r["ks"], round(r["D"], 6))] = r
    for p in sorted(glob.glob(os.path.join(folder, "ks*_D*.json")) + glob.glob(os.path.join(folder, "ctl_planted.json"))):
        r = row_of(json.load(open(p)), os.path.basename(p)[:-5])
        key = (r["ks"], round(r["D"], 6))
        if key in rows:                        # a re-read of a #941 state: kept apart for the comparison
            own[key] = r
        else:
            rows[key] = r
    return sorted(rows.values(), key=lambda r: r["D"]), own


def central(rows, forward=False):
    """per row: the slope over the two neighbours -ln(sigma_{i+1} / sigma_{i-1}) / (D_{i+1} - D_{i-1}), or None; forward=True (the
    --mutate control) takes the forward difference instead"""
    out = []
    for i, r in enumerate(rows):
        s = None
        if 0 < i < len(rows) - 1:
            a, b = rows[i - 1], rows[i + 1]
            if a["ok"] and b["ok"] and r["ok"] and a["ks"] == r["ks"] == b["ks"]:
                lo = r if forward else a
                s = -math.log(b["sd"] / lo["sd"]) / (b["D"] - lo["D"])
        out.append(s)
    return out


def interval_slopes(rows):
    """per row: the slope of the interval from the previous row, or None unless both are classified and share a ks"""
    out = [None]
    for a, b in zip(rows, rows[1:]):
        out.append(-math.log(b["sd"] / a["sd"]) / (b["D"] - a["D"]) if a["ok"] and b["ok"] and a["ks"] == b["ks"] else None)
    return out


def leg_slope(g):
    """least-squares slope of -ln sigma_Delta against D over a leg's states"""
    D = np.array([r["D"] for r in g])
    y = -np.log([r["sd"] for r in g])
    return float(np.polyfit(D, y, 1)[0])


def make_baseline(rows):
    """the backfill's baseline: per leg slope, a + b/ks and a + b' ks through them, and their extrapolations"""
    legs = {}
    for ks in BACKFILL_KS:
        g = [r for r in rows if r["ks"] == ks]
        if len(g) < 5 or not all(r["ok"] and r["conv"] < 1e-3 for r in g):
            raise ValueError(f"ks {ks}: {len(g)} states, or one is unclassified or unconverged")
        legs[ks] = dict(n=len(g), D0=g[0]["D"], D1=g[-1]["D"], slope=leg_slope(g))
    ks = np.array(sorted(legs), float)
    sl = np.array([legs[int(k)]["slope"] for k in ks])
    b, a = np.polyfit(1 / ks, sl, 1)
    b2, a2 = np.polyfit(ks, sl, 1)
    for k, y in zip(ks, a + b / ks):
        legs[int(k)]["fit_inv_ks"] = float(y)
    return dict(inv_ks=[float(a), float(b)], lin_ks=[float(a2), float(b2)], legs=legs,
                extrapolation={str(k): dict(inv_ks=float(a + b / k), lin_ks=float(a2 + b2 * k)) for k in EXTRAP_KS},
                states=[r["state"] for r in rows if r["ks"] in BACKFILL_KS])


def s_of(base, ks):
    return base["inv_ks"][0] + base["inv_ks"][1] / ks


def trigger(rows, iv, base):
    """the index of the third consecutive row of one leg whose interval slope exceeds s(ks) by more than TRIGGER, or None"""
    n = 0
    for i, r in enumerate(rows):
        if iv[i] is not None and iv[i] - s_of(base, r["ks"]) > TRIGGER and (n == 0 or rows[i - 1]["ks"] == r["ks"]):
            n += 1
            if n >= 3:
                return i
        else:
            n = 0
    return None


def windows(rows, base):
    """the fold rule on the window ending at each state that has at least five states of its leg up to it:
    [(ks, window rows, rule result)]"""
    out = []
    for ks in sorted({r["ks"] for r in rows}):
        g = [r for r in rows if r["ks"] == ks and r["ok"]]
        for i in range(5, len(g) + 1):
            D = [r["D"] for r in g[:i]]
            s2 = [r["sd"] ** 2 for r in g[:i]]
            out.append((ks, g[i - 5:i], fold949.rule(D, s2, s_of(base, ks))))
    return out


def fmt_conds(c):
    return "".join({True: "T", False: "F", None: "-"}[x] for x in c)


def freeze(folder):
    path = os.path.join(folder, "baseline949.json")
    if os.path.exists(path):
        sys.exit("baseline949.json exists: the baseline is frozen")
    late = [p for p in glob.glob(os.path.join(folder, "ks*_D*.json")) if int(re.match(r"ks(\d+)_", os.path.basename(p)).group(1)) > 240]
    if late:
        sys.exit(f"a state of ks > 240 has been read ({os.path.basename(late[0])}): the baseline cannot be frozen before leg 8's first read")
    rows, _ = load(folder)
    base = make_baseline(rows)
    base["frozen_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    json.dump(base, open(path, "w"), indent=1)
    print(f"frozen {base['frozen_utc']} UTC: s(ks) = {base['inv_ks'][0]:.5f} + {base['inv_ks'][1]:.3f} / ks")
    for ks, l in base["legs"].items():
        print(f"  ks {ks}: {l['n']} states D {l['D0']:.4f} to {l['D1']:.4f}, leg slope {l['slope']:.4f}, fit {l['fit_inv_ks']:.4f} "
              f"(residual {l['slope'] - l['fit_inv_ks']:+.4f})")
    for k, e in base["extrapolation"].items():
        print(f"  ks {k}: 1/ks {e['inv_ks']:.4f}, linear in ks {e['lin_ks']:.4f}, spread {abs(e['inv_ks'] - e['lin_ks']):.4f}")


def tables(folder, forward=False):
    rows, own = load(folder)
    bpath = os.path.join(folder, "baseline949.json")
    base = json.load(open(bpath)) if os.path.exists(bpath) else None
    cen, iv = central(rows, forward), interval_slopes(rows)
    ok = True
    with open(os.path.join(folder, "track949.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["D", "ks", "sigma_delta", "sigma_pair", "delta_share", "delta_share_2nd", "delta_vec", "pair_vecs", "conv_delta",
                    "local_slope", "interval_slope", "s_baseline", "excess", "classified", "source"])
        for r, c, v in zip(rows, cen, iv):
            sb = None if base is None else s_of(base, r["ks"])
            w.writerow([f"{r['D']:.6f}", r["ks"], f"{r['sd']:.6e}", f"{r['sp']:.6e}", f"{r['share']:.4f}", f"{r['share2']:.4f}", r["dvec"],
                        r["pvec"], f"{r['conv']:.1e}", "" if c is None else f"{c:.4f}", "" if v is None else f"{v:.4f}",
                        "" if sb is None else f"{sb:.4f}", "" if v is None or sb is None else f"{v - sb:+.4f}", int(r["ok"]), r["src"]])
    with open(os.path.join(folder, "intervals949.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["D0", "D1", "ks0", "ks1", "slope", "crosses_ks"])
        for a, b in zip(rows, rows[1:]):
            if a["ok"] and b["ok"]:
                w.writerow([f"{a['D']:.6f}", f"{b['D']:.6f}", a["ks"], b["ks"], f"{-math.log(b['sd'] / a['sd']) / (b['D'] - a['D']):.4f}",
                            int(a["ks"] != b["ks"])])
    print(f"{'D':>9} {'ks':>4} {'sigma_Delta':>12} {'sigma_pair':>12} {'Dshare':>7} {'2nd':>6} {'conv':>8} {'local':>7} {'interval':>8} {'excess':>7}  note")
    for r, c, v in zip(rows, cen, iv):
        conv = "" if r["conv"] < 1e-3 else "  NOT CONVERGED (rerun --its=32)"
        note = ("" if r["ok"] else "  NOT CLASSIFIED: " + r["note"]) + conv
        ex = "" if v is None or base is None else format(v - s_of(base, r["ks"]), "+7.4f")
        print(f"{r['D']:9.4f} {r['ks']:4d} {r['sd']:12.4e} {r['sp']:12.4e} {r['share']:7.3f} {r['share2']:6.3f} {r['conv']:8.1e} "
              f"{'' if c is None else format(c, '7.4f'):>7} {'' if v is None else format(v, '8.4f'):>8} {ex:>7}  v{r['dvec']}/{r['pvec']}{note}")
    bad = [r for r in rows if not r["ok"] or r["conv"] >= 1e-3]
    print(f"\nstates {len(rows)}, not classified or not converged: {len(bad)}"
          + "".join(f"\n  D {r['D']:.4f}: {r['note'] or 'conv ' + format(r['conv'], '.1e')}" for r in bad))
    # criterion 5: #941's four intervals, and the re-reads
    w941 = [(r, v) for r, v in zip(rows, iv) if r["ks"] == 240 and 229.5 < r["D"] <= 232.0001 and v is not None][-4:]
    if len(w941) == 4:
        d = [abs(v - q) for (_, v), q in zip(w941, QUOTED_941)]
        print(f"\ncriterion 5, intervals D 229.05 to 232.0: {', '.join(format(v, '.4f') for _, v in w941)} against #941's "
              f"{', '.join(map(str, QUOTED_941))}: largest difference {max(d):.4f}: {'pass' if max(d) <= 0.01 else 'FAIL'}")
        ok &= max(d) <= 0.01
    for key, r in own.items():
        ref = next(x for x in rows if (x["ks"], round(x["D"], 6)) == key)
        print(f"re-read of #941's state D {key[1]:.4f}: sigma_Delta {r['sd']:.10e} here ({r['src']}) against {ref['sd']:.10e} (relative "
              f"difference {abs(r['sd'] / ref['sd'] - 1):.1e}); Delta share {r['share']:.4f} against {ref['share']:.4f}")
    if base is None:
        print("\nbaseline: not frozen (track949.py --freeze, once the backfill is read and before any state of ks >= 250)")
        try:
            b = make_baseline(rows)
            print(f"  the backfill so far would give s(ks) = {b['inv_ks'][0]:.5f} + {b['inv_ks'][1]:.3f} / ks; legs "
                  + ", ".join(f"{k}: {l['slope']:.4f} (fit {l['fit_inv_ks']:.4f})" for k, l in b["legs"].items()))
        except ValueError as e:
            print("  not yet possible:", e)
        return ok, rows
    print(f"\nbaseline frozen {base['frozen_utc']} UTC: s(ks) = {base['inv_ks'][0]:.5f} + {base['inv_ks'][1]:.3f} / ks; legs "
          + ", ".join(f"{k}: {l['slope']:.4f} (fit {l['fit_inv_ks']:.4f})" for k, l in base["legs"].items()))
    print("  extrapolation to " + ", ".join(f"ks {k}: {e['inv_ks']:.4f} / {e['lin_ks']:.4f} (1/ks, linear in ks)" for k, e in base["extrapolation"].items()))
    it = trigger(rows, iv, base)
    print(f"\ntrigger (interval slope - s(ks) > {TRIGGER}, three consecutive states of one leg): "
          f"{'FIRED at D ' + format(rows[it]['D'], '.4f') if it is not None else 'not reached'}")
    mx = max(((v - s_of(base, r["ks"]), r["D"]) for r, v in zip(rows, iv) if v is not None), default=None)
    if mx:
        print(f"  largest excess so far {mx[0]:+.4f} at D {mx[1]:.4f}")
    wins = windows(rows, base)
    print("\nfold rule on every five-state window (conditions: 1 residuals, 2 D* within 3 past, 3 shifted window, 4 planted scatter; "
          "T true, F false, - not evaluated):")
    null_fail = []
    for ks, g, res in wins:
        B = res["B"]
        back = ks in BACKFILL_KS
        if back and res["valid"]:
            null_fail.append((ks, g[-1]["D"]))
        print(f"  ks {ks} D {g[0]['D']:.4f} to {g[-1]['D']:.4f}: D* {B['Dstar']:.2f} (s {B['s']:.3f}) conditions {fmt_conds(res['conds'])} "
              f"{'VALID' if res['valid'] else 'not valid'}{'  [backfill: null control]' if back else ''}")
    w211 = [res for ks, g, res in wins if ks == 211]
    if w211:
        c2 = w211[0]["conds"][1] is False
        print(f"null control: {'no backfill window is valid' if not null_fail else 'WINDOWS VALID ' + str(null_fail) + ': STOP, find the cause'}; "
              f"ks 211's window D* {w211[0]['B']['Dstar']:.1f}: {'fails by condition 2' if c2 else 'DOES NOT FAIL BY CONDITION 2'}")
        ok &= not null_fail and c2
    late = [(ks, g, res) for ks, g, res in wins if ks not in BACKFILL_KS and res["valid"]]
    if late:
        ks, g, res = late[-1]
        print(f"\nVALID FOLD FIT at ks {ks}, window ending D {g[-1]['D']:.4f}: D* {res['B']['Dstar']:.2f}; trigger "
              f"{'fired' if it is not None else 'NOT fired (no claim)'}")
    return ok, rows


def selftest(mutate):
    """planted records and series; every check must be able to fail, and --mutate (forward difference for the central slope) must fail"""
    ok = True
    D = [200.0, 202.0, 203.5, 206.0, 208.0, 210.0, 213.0]
    rows = [dict(D=d, ks=211, sd=1e-14 * math.exp(-0.40 * (d - 200)), ok=True) for d in D]
    e1 = max(abs(s - 0.40) for s in central(rows, mutate) if s is not None)
    ok &= e1 < 1e-12
    print(f"selftest: pure exponential, central slope error {e1:.1e}: {'pass' if e1 < 1e-12 else 'FAIL'}")
    D = [233.0, 234.0, 235.0, 236.0, 237.0, 238.0]
    rows = [dict(D=d, ks=250, sd=math.sqrt(0.3 * (260 - d) * math.exp(-2 * 0.405 * (d - 232))), ok=True) for d in D]
    cen = central(rows, mutate)
    want = [0.405 + 0.5 * math.log((260 - D[i - 1]) / (260 - D[i + 1])) / (D[i + 1] - D[i - 1]) for i in range(1, 5)]
    e2 = max(abs(cen[i] - want[i - 1]) for i in range(1, 5))
    ok &= e2 < 1e-12
    print(f"selftest: planted fold + exponential, central slope error {e2:.1e}: {'pass' if e2 < 1e-12 else 'FAIL'}")
    # trigger: baseline s(ks) = 0.40 + 20 / ks, so 0.48 at ks 250; intervals 0.55 are 0.07 over (no), 0.60 are 0.12 over (yes)
    base = dict(inv_ks=[0.40, 20.0])
    s250 = s_of(base, 250)
    rows = [dict(D=float(i), ks=250, sd=1.0, ok=True) for i in range(8)]
    for i in range(1, 8):
        rows[i]["sd"] = rows[i - 1]["sd"] * math.exp(-(0.55 if i < 4 else 0.60))
    iv = interval_slopes(rows)
    t = trigger(rows, iv, base)
    t_early = trigger(rows[:6], iv[:6], base)
    ok &= abs(s250 - 0.48) < 1e-12 and t == 6 and t_early is None
    print(f"selftest: baseline {s250:.3f} at ks 250; intervals 0.07 over (x3), then 0.12 over (x4): trigger at the third 0.12 "
          f"(row {t}, want 6), not on the first six rows ({t_early}): {'pass' if t == 6 and t_early is None else 'FAIL'}")
    rows2 = [dict(r) for r in rows]
    for i in (5, 6, 7):
        rows2[i]["ks"] = 260
    t2 = trigger(rows2, interval_slopes(rows2), base)
    ok &= t2 is None
    print(f"selftest: the same series with a ks change at row 5: trigger {t2} (want None): {'pass' if t2 is None else 'FAIL'}")
    rec = dict(vectors=[dict(sigma=1e-9 * (i + 1), delta=0.1, top=[["p1", 1, 0.5]]) for i in range(6)], state="x_ks1/y.npz", D=1.0)
    try:
        classify(rec)
        ok = False
        print("selftest: a record with no Delta mode must not classify: FAIL")
    except ValueError:
        print("selftest: a record with no Delta mode does not classify: pass")
    # baseline fit: planted legs on s = 0.40 + 20/ks exactly must come back with a, b to 1e-9, and the two extrapolations differ
    rows = []
    for ks in BACKFILL_KS:
        s = 0.40 + 20.0 / ks
        for j in range(6):
            rows.append(dict(D=float(ks) + j, ks=ks, sd=math.exp(-s * j), ok=True, conv=0.0, state=f"x_ks{ks}/y"))
    b = make_baseline(rows)
    eb = max(abs(b["inv_ks"][0] - 0.40), abs(b["inv_ks"][1] - 20.0))
    good = eb < 1e-9 and abs(b["extrapolation"]["250"]["inv_ks"] - 0.48) < 1e-9 and abs(b["extrapolation"]["250"]["lin_ks"] - 0.48) > 1e-4
    ok &= good
    print(f"selftest: baseline fit of planted legs, a and b error {eb:.1e}, 1/ks extrapolation to ks 250 "
          f"{b['extrapolation']['250']['inv_ks']:.6f} (want 0.48), linear in ks {b['extrapolation']['250']['lin_ks']:.4f} (differs): "
          f"{'pass' if good else 'FAIL'}")
    print(f"selftest{' --mutate' if mutate else ''}: {'pass' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    folder = args[0] if args else HERE
    if "--freeze" in sys.argv:
        freeze(folder)
        sys.exit(0)
    sys.exit(0 if tables(folder)[0] else 1)
