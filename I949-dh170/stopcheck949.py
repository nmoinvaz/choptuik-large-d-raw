#!/usr/bin/env python3
"""#949 (coordinator's stop rule of 2026-11-20 03:1x UTC): the early-stop conditions after each new ks_chain3b state, read from track949.csv and track949.log
(run track949.py first). The fits' code and pass criteria are not touched.

    stopcheck949.py                 prints the excess run above 0.10, the run below 0.10, the latest ks_chain3b fold window's conditions, and 'STOP CONDITION: ...' or 'no stop condition'
    stopcheck949.py --selftest [--mutate]   planted excess series and fold lines (exit 1 on failure; --mutate uses <= 0.10 for 'below' and ignores condition 4, both must fail)
Stop early, with a closing row, when (a) the latest five-state fold window of ks_chain3b passes all four conditions (TTTT and valid), or (b) the trigger's excess is
below 0.10 for two states in a row."""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRIGGER = 0.10


def runs(ex, mutate=False):
    above = below = 0
    for x in reversed(ex):
        if x is not None and x > TRIGGER:
            above += 1
        else:
            break
    for x in reversed(ex):
        if x is not None and (x <= TRIGGER if mutate else x < TRIGGER):
            below += 1
        else:
            break
    return above, below


def fold_conditions(lines, mutate=False):
    """(conditions string, valid) of the last window line of ks_chain3b"""
    last = [l for l in lines if "(chain 3b)" in l and "conditions" in l]
    if not last:
        return None, False
    m = re.search(r"conditions (\S+) (not valid|valid)", last[-1])
    if not m:
        return None, False
    cond, v = m.group(1), m.group(2) == "valid"
    ok = v and (set(cond) == {"T"} or (mutate and cond[:3] == "TTT"))
    return cond, ok


def decide(ex, lines, mutate=False):
    above, below = runs(ex, mutate)
    cond, fold = fold_conditions(lines, mutate)
    msgs = []
    if fold:
        msgs.append(f"the fold fit passes all four conditions ({cond})")
    if below >= 2:
        msgs.append(f"the excess has been below {TRIGGER} for {below} states in a row")
    return above, below, cond, msgs


def selftest(mutate):
    L = "  ks 293 (chain 3b) D 252.4034 to 254.1769: D* 257.04 (s 0.326) conditions %s %s\n"
    cases = [
        ([0.1035, 0.1233, 0.1408], L % ("TTTF", "not valid"), False),          # the state at 03:14 UTC: no stop
        ([0.12, 0.14, 0.15], L % ("TTTT", "valid"), True),                      # the fold fit passes: stop
        ([0.12, 0.099, 0.098], L % ("TTTF", "not valid"), True),                # below 0.10 twice: stop
        ([0.12, 0.14, 0.099], L % ("TTTF", "not valid"), False),                # below once: no stop
        ([0.12, 0.14, 0.10], L % ("TTTF", "not valid"), False),                 # exactly 0.10 is not below
        ([0.12, 0.14, 0.15], L % ("TTTF", "not valid"), False),                 # condition 4 false: no stop
        ([0.12, 0.099, 0.10], L % ("TTTF", "not valid"), False),                # 0.099 then exactly 0.10: one below only
    ]
    ok = True
    for ex, line, want in cases:
        _, _, _, msgs = decide(ex, [line], mutate)
        got = bool(msgs)
        good = got == want
        ok &= good
        print(f"selftest: excess {ex}, {line.split('conditions')[1].strip()} -> stop {got} (want {want}): {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "track949.csv"))) if r["chain"] == "4" and r["classified"] == "1"]
    rows.sort(key=lambda r: float(r["D"]))
    ex = [float(r["trigger_excess"]) if r["trigger_excess"] else None for r in rows]
    lines = open(os.path.join(HERE, "track949.log")).read().splitlines()
    above, below, cond, msgs = decide(ex, lines)
    print(f"last states' excess: {', '.join(f'{x:+.4f}' for x in ex[-5:])} (D {rows[-1]['D'][:8]}); run above {TRIGGER}: {above}; run below {TRIGGER}: {below}; latest ks_chain3b fold window conditions: {cond}")
    print("STOP CONDITION: " + "; ".join(msgs) if msgs else "no stop condition")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    main()
