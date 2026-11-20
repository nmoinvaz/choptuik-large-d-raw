#!/usr/bin/env python3
"""#1057 amended stop rule (coordinator, issue comment 7047123609, 2026-11-20 18:13 UTC), checked after each new ks_chain3b state from track949.csv, track949.log and the
state records (run track949.py first).

    stopcheck1057.py                 prints each condition, the pushes of leg 11 not yet read, and 'STOP CONDITION (x): ...' lines, or 'no stop condition'
    stopcheck1057.py --selftest [--mutate]   planted series, ratios, fold lines, pushes and times (exit 1 on failure; --mutate counts the excess one-sidedly (no lower bound),
                                             takes sigma_2/sigma_Delta <= 1.05 as below, and ignores pushed leg 11 states: each planted case must then fail)
(a) the latest five-state fold window of ks_chain3b reads TTTT and valid: report at once on #1057 and #966;
(b) sigma_2/sigma_Delta below 1.05 at a state past D 259.7352: report at once (a near crossing: the two-mode fit is rerun with D-linear slopes);
(c) |excess| <= 0.05 at the last 5 states in a row, all of them states past D 259.7352;
(d) 2026-11-21 12:00 UTC has passed.
The pushes of leg 11 (ks 315, a new order: flag it in each row) are listed from the raw repository's origin/main, as the autoqueue fetches it."""
import calendar
import csv
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BAND, RUN, RATIO = 0.05, 5, 1.05
D_FIRST_NEW = 259.9                                     # states past D 259.7352 are the new ones
DEADLINE = calendar.timegm((2026, 11, 21, 12, 0, 0))
PUSH_REPO = os.path.expanduser("~/Source/choptuik-large-d-raw-push")
ONE_SIDED = False                                       # --mutate: no lower bound on the band
RATIO_LE = False                                        # --mutate: <= instead of <
IGNORE_LEG11 = False                                    # --mutate: pushed leg 11 states are not listed


def inside(x):
    return x is not None and (x <= BAND if ONE_SIDED else abs(x) <= BAND)


def below(r):
    return r is not None and (r <= RATIO if RATIO_LE else r < RATIO)


def evaluate(rows, fold_lines, now):
    """rows: dicts with D, ks, excess (float or None), ratio (sigma_2/sigma_Delta or None), ordered by D; fold_lines: track949.log's '(chain 3b)' lines; now: epoch seconds"""
    out = {}
    last = fold_lines[-1] if fold_lines else ""
    m = re.search(r"conditions (\S+) (not valid|valid)", last)
    out["a"] = bool(m and m.group(1) == "TTTT" and m.group(2) == "valid")
    out["fold_line"] = last.strip()
    new = [r for r in rows if r["D"] > D_FIRST_NEW]
    out["b"] = any(below(r["ratio"]) for r in new)
    out["b_at"] = [r["D"] for r in new if below(r["ratio"])]
    tail = new[-RUN:]
    out["c"] = len(tail) == RUN and all(inside(r["excess"]) for r in tail)
    run_new = 0
    for r in reversed(new):
        if not inside(r["excess"]):
            break
        run_new += 1
    out["run_new"] = run_new
    out["d"] = now >= DEADLINE
    out["new"] = len(new)
    out["ratio_last"] = new[-1]["ratio"] if new else None
    return out


def pushed_unread(paths, have):
    """paths: anm_pin3 files of ks_chain3b in the raw repository; have: names with a record here. Returns (unread names, those with a ks other than 293)"""
    unread, other = [], []
    for p in sorted(paths):
        m, d = re.search(r"[_/]ks(\d+)/", p), re.search(r"anm_pin3_D(\d+\.\d+)\.npz$", p)
        if not (m and d) or float(d.group(1)) <= D_FIRST_NEW:
            continue
        if IGNORE_LEG11 and "/leg11_" in p:
            continue
        name = f"c3b_ks{m.group(1)}_D{d.group(1)}"
        if name not in have:
            unread.append(name)
            if m.group(1) != "293":
                other.append(name)
    return unread, other


def unclassified(all_rows):
    """chain 4 states past D 259.7352 that track949.py leaves out because no vector has a Delta share above 0.5 (the two lowest vectors share the Delta mode: a crossing)"""
    return [r for r in all_rows if r["classified"] == "0" and float(r["D"]) > D_FIRST_NEW and not IGNORE_LEG11]


def selftest(mutate):
    global ONE_SIDED, RATIO_LE, IGNORE_LEG11
    ONE_SIDED = RATIO_LE = IGNORE_LEG11 = mutate
    ok = True

    def mk(ex, rat=None, D0=259.7352, ks=293):
        rat = rat or [1.5] * len(ex)
        return [dict(D=D0 + 0.27 * i, ks=ks, excess=x, ratio=r) for i, (x, r) in enumerate(zip(ex, rat))]
    t0 = DEADLINE - 3600
    F = "TTTF not valid"
    cases = [
        ("five inside the band (0.05 counts)", mk([0.027, 0.02, 0.01, -0.03, 0.04, 0.05]), F, t0, "c", True),
        ("four inside then outside", mk([0.027, 0.02, 0.01, -0.03, 0.06, 0.04]), F, t0, "c", False),
        ("0.0501 is outside", mk([0.027, 0.02, 0.01, 0.0501, 0.04, 0.03]), F, t0, "c", False),
        ("a planted -0.08 breaks the run", mk([0.027, 0.02, -0.08, 0.01, 0.03, 0.04]), F, t0, "c", False),
        ("the old state D 259.7352 does not count towards five new ones", mk([0.02, 0.01, 0.03, 0.04]), F, t0, "c", False),
        ("the excess +0.0804 of D 260.4708 breaks a run of two", mk([0.0146, 0.0294, 0.0804, 0.02, 0.03]), F, t0, "c", False),
        ("TTTT valid", mk([0.2]), "TTTT valid", t0, "a", True),
        ("TTTF not valid", mk([0.2]), F, t0, "a", False),
        ("TTTT not valid is not a pass", mk([0.2]), "TTTT not valid", t0, "a", False),
        ("sigma_2/sigma_Delta 1.0499 at a new state", mk([0.1] * 3, [1.2, 1.1, 1.0499]), F, t0, "b", True),
        ("sigma_2/sigma_Delta exactly 1.05 is not below", mk([0.1] * 3, [1.2, 1.1, 1.05]), F, t0, "b", False),
        ("the old state D 259.7352 at 1.0 does not count", mk([0.1] * 3, [1.0, 1.2, 1.2]), F, t0, "b", False),
        ("a ratio of None is not below", mk([0.1] * 2, [None, 1.2]), F, t0, "b", False),
        ("before the deadline", mk([0.2]), F, DEADLINE - 1, "d", False),
        ("at the deadline", mk([0.2]), F, DEADLINE, "d", True),
    ]
    for name, rows, fold, now, key, want in cases:
        got = evaluate(rows, [f"  ks 293 (chain 3b) D 1 to 2: D* inf (s 0.4) conditions {fold}"], now)[key]
        good = got == want
        ok &= good
        print(f"selftest: {name}: {key} = {got} (want {want}): {'pass' if good else 'FAIL'}")
    allr = [dict(D="260.6706", classified="1"), dict(D="260.8483", classified="0"), dict(D="250.0", classified="0")]
    u = [r["D"] for r in unclassified(allr)]
    good = u == ["260.8483"]
    ok &= good
    print(f"selftest: unclassified states past D 259.7352: {u} (want ['260.8483']; the classified one and the old one are not listed): {'pass' if good else 'FAIL'}")
    base = "I966-dh370/ks_chain3b/"
    paths = [base + "leg10_D256.1776_ks293/anm_pin3_D260.4708.npz", base + "leg10_D256.1776_ks293/anm_pin3_D260.6706.npz", base + "leg10_D256.1776_ks293/pred_pin3_D260.6706.npz",
             base + "leg11_D260.8483_ks315/anm_pin3_D261.0123.npz", base + "leg10_D256.1776_ks293/anm_pin3_D259.7352.npz"]
    have = {"c3b_ks293_D260.4708"}
    u, o = pushed_unread(paths, have)
    want_u = ["c3b_ks293_D260.6706", "c3b_ks315_D261.0123"]
    good = u == want_u and o == ["c3b_ks315_D261.0123"]
    ok &= good
    print(f"selftest: pushes: unread {u} (want {want_u}), other order {o} (want ['c3b_ks315_D261.0123']), the read state, the predictor file and D 259.7352 are not listed: {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def ratios(rows):
    from row949 import picks
    for r in rows:
        p = os.path.join(HERE, f"c3b_ks{r['ks']}_D{r['D']:.4f}.json")
        r["ratio"] = None
        if os.path.exists(p):
            rec = json.load(open(p))
            d, k2 = picks(rec)
            r["ratio"] = rec["vectors"][k2]["sigma"] / rec["vectors"][d]["sigma"]


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    rows = []
    allr = [r for r in csv.DictReader(open(os.path.join(HERE, "track949.csv"))) if r["chain"] == "4"]
    for r in allr:
        if r["classified"] == "1":
            rows.append(dict(D=float(r["D"]), ks=int(float(r["ks"])), excess=float(r["trigger_excess"]) if r["trigger_excess"] else None))
    rows.sort(key=lambda r: r["D"])
    ratios(rows)
    fold = [l for l in open(os.path.join(HERE, "track949.log")).read().splitlines() if "(chain 3b)" in l]
    res = evaluate(rows, fold, time.time())
    ex = [f"{r['excess']:+.4f}" for r in rows[-6:]]
    print(f"#1057 states past D 259.7352 read: {res['new']} (latest ks {rows[-1]['ks']}); last excess: {', '.join(ex)} (D {rows[-1]['D']:.4f}); "
          f"sigma_2/sigma_Delta {res['ratio_last']:.3f}; run of |excess| <= {BAND} at the end counting only new states: {res['run_new']} of {RUN}")
    print(f"latest fold window: {res['fold_line']}")
    uc = unclassified(allr)
    print("UNCLASSIFIED states past D 259.7352 (no vector with a Delta share above 0.5, left out of every series and fit): " + (", ".join(f"D {float(r['D']):.4f} (largest share {float(r['delta_share']):.3f})" for r in uc) if uc else "none"))
    try:
        have = {os.path.basename(p)[:-5] for p in os.listdir(HERE) if p.startswith("c3b_ks") and p.endswith(".json")}
        paths = subprocess.run(["git", "-C", PUSH_REPO, "ls-tree", "-r", "--name-only", "origin/main", "I966-dh370/ks_chain3b/"], capture_output=True, text=True, check=True).stdout.split()
        unread, other = pushed_unread(paths, have)
        print(f"pushed and not yet read (raw origin/main as last fetched): {', '.join(unread) or 'none'}" + (f"; ORDER CHANGE (ks != 293): {', '.join(other)}" if other else ""))
    except Exception as e:                              # the push listing is a convenience, not a stop condition
        print(f"push listing failed: {e}")
    msg = {"a": "a TTTT fold window (report at once on #1057 and #966)", "b": "sigma_2/sigma_Delta below 1.05 (report at once: a near crossing, rerun the two-mode fit with D-linear slopes)",
           "c": f"the excess within +-{BAND} at {RUN} new states in a row", "d": "2026-11-21 12:00 UTC has passed"}
    hit = [k for k in "abcd" if res[k]]
    for k in hit:
        print(f"STOP CONDITION ({k}): {msg[k]}" + (f" at D {', '.join(f'{d:.4f}' for d in res['b_at'])}" if k == "b" else ""))
    if not hit:
        print("no stop condition")


if __name__ == "__main__":
    main()
