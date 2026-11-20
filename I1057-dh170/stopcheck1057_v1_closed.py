#!/usr/bin/env python3
"""#1057 stop rule (issue body, fixed before the first read), checked after each new ks_chain3b state from track949.csv and track949.log (run track949.py first).

    stopcheck1057.py                 prints each condition and 'STOP CONDITION (x): ...' lines, or 'no stop condition'
    stopcheck1057.py --selftest [--mutate]   planted excess series, fold lines, states and times (exit 1 on failure; --mutate counts the excess one-sidedly, x <= 0.05
                                             with no lower bound, and a planted -0.08 must then be wrongly inside the band: the check must fail)
(a) the latest five-state fold window of ks_chain3b reads TTTT and valid;
(b) |excess| <= 0.05 at the last 5 states in a row, all of them states past D 259.7352 (the run counting D 259.7352 is also printed);
(c) a ks_chain3b state with D >= 266.18 (dh370's leg boundary) or ks >= 315 (a leg 11 restart) has been read;
(d) 2026-11-21 12:00 UTC has passed."""
import calendar
import csv
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BAND, RUN, D_LEG, KS_NEXT = 0.05, 5, 266.18, 315
D_FIRST_NEW = 259.9                                     # states past D 259.7352 are the new ones
DEADLINE = calendar.timegm((2026, 11, 21, 12, 0, 0))
ONE_SIDED = False                                       # --mutate: no lower bound on the band


def inside(x):
    return x is not None and (x <= BAND if ONE_SIDED else abs(x) <= BAND)


def evaluate(rows, fold_lines, now):
    """rows: dicts with D, ks, excess (float or None), ordered by D; fold_lines: track949.log's '(chain 3b)' lines; now: epoch seconds"""
    out = {}
    last = fold_lines[-1] if fold_lines else ""
    m = re.search(r"conditions (\S+) (not valid|valid)", last)
    out["a"] = bool(m and m.group(1) == "TTTT" and m.group(2) == "valid")
    out["fold_line"] = last.strip()
    new = [r for r in rows if r["D"] > D_FIRST_NEW]
    tail = new[-RUN:]
    out["b"] = len(tail) == RUN and all(inside(r["excess"]) for r in tail)
    run_new = 0
    for r in reversed(new):
        if not inside(r["excess"]):
            break
        run_new += 1
    run_all = 0
    for r in reversed(rows):
        if not inside(r["excess"]):
            break
        run_all += 1
    out["run_new"], out["run_all"] = run_new, run_all
    out["c"] = any(r["D"] >= D_LEG or r["ks"] >= KS_NEXT for r in rows)
    out["d"] = now >= DEADLINE
    out["new"] = len(new)
    return out


def selftest(mutate):
    global ONE_SIDED
    ONE_SIDED = mutate
    ok = True

    def mk(ex, D0=259.7352, ks=293):
        return [dict(D=D0 + 0.27 * i, ks=ks, excess=x) for i, x in enumerate(ex)]
    t0 = DEADLINE - 3600
    cases = [
        ("five inside the band (0.05 counts)", mk([0.027, 0.02, 0.01, -0.03, 0.04, 0.05]), "TTTF not valid", t0, "b", True),
        ("four inside then outside", mk([0.027, 0.02, 0.01, -0.03, 0.06, 0.04]), "TTTF not valid", t0, "b", False),
        ("0.0501 is outside", mk([0.027, 0.02, 0.01, 0.0501, 0.04, 0.03]), "TTTF not valid", t0, "b", False),
        ("a planted -0.08 breaks the run", mk([0.027, 0.02, -0.08, 0.01, 0.03, 0.04]), "FFF- not valid", t0, "b", False),
        ("the old state D 259.7352 does not count towards five new ones", mk([0.02, 0.01, 0.03, 0.04]), "FFF- not valid", t0, "b", False),
        ("TTTT valid", mk([0.2]), "TTTT valid", t0, "a", True),
        ("TTTF not valid", mk([0.2]), "TTTF not valid", t0, "a", False),
        ("TTTT not valid is not a pass", mk([0.2]), "TTTT not valid", t0, "a", False),
        ("D 266.18 is the leg boundary", [dict(D=266.18, ks=293, excess=0.1)], "FFF- not valid", t0, "c", True),
        ("D 266.1799 is not", [dict(D=266.1799, ks=293, excess=0.1)], "FFF- not valid", t0, "c", False),
        ("ks 315 is a restart", [dict(D=262.0, ks=315, excess=0.1)], "FFF- not valid", t0, "c", True),
        ("before the deadline", mk([0.2]), "FFF- not valid", DEADLINE - 1, "d", False),
        ("at the deadline", mk([0.2]), "FFF- not valid", DEADLINE, "d", True),
    ]
    for name, rows, fold, now, key, want in cases:
        got = evaluate(rows, [f"  ks 293 (chain 3b) D 1 to 2: D* inf (s 0.4) conditions {fold}"], now)[key]
        good = got == want
        ok &= good
        print(f"selftest: {name}: {key} = {got} (want {want}): {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    rows = []
    for r in csv.DictReader(open(os.path.join(HERE, "track949.csv"))):
        if r["chain"] == "4" and r["classified"] == "1":
            rows.append(dict(D=float(r["D"]), ks=int(float(r["ks"])), excess=float(r["trigger_excess"]) if r["trigger_excess"] else None))
    rows.sort(key=lambda r: r["D"])
    fold = [l for l in open(os.path.join(HERE, "track949.log")).read().splitlines() if "(chain 3b)" in l]
    res = evaluate(rows, fold, time.time())
    ex = [f"{r['excess']:+.4f}" for r in rows[-6:]]
    print(f"#1057 states past D 259.7352 read: {res['new']}; last excess: {', '.join(ex)} (D {rows[-1]['D']:.4f}); run within +-{BAND} counting only new states: {res['run_new']} of {RUN}, counting D 259.7352 too: {res['run_all']}")
    print(f"latest fold window: {res['fold_line']}")
    msg = {"a": "a TTTT fold window (report at once on #966 and #1057)", "b": f"the excess within +-{BAND} at {RUN} new states in a row",
           "c": f"dh370's leg boundary D {D_LEG} or a leg 11 restart (ks {KS_NEXT}) has been read", "d": "2026-11-21 12:00 UTC has passed"}
    hit = [k for k in "abcd" if res[k]]
    for k in hit:
        print(f"STOP CONDITION ({k}): {msg[k]}")
    if not hit:
        print("no stop condition")


if __name__ == "__main__":
    main()
