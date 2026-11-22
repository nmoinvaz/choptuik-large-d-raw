#!/usr/bin/env python3
"""cmddiff997.py ACTUAL_COMMAND | --selftest [--break]: the diff of the anm_lowd.py command a launch uses against the coordinator's (ref/commands_hc_997.txt, verbatim from his #997 comment of 2026-11-22), before the launch.
Both reduced to the tokens after 'anm_lowd.py' (nice, python, '-u' dropped; RAW replaced by the raw clone), the empty --checks argument kept; unified diff, one token a line; 'cmddiff997: EMPTY' (exit 0) or 'DIFFERS' (exit 1).
--selftest plants slips (--N 9, --target 3.0432, --threads 6, a wrong state, a dropped --checks '') which must each differ and the same command, which must be empty; --break expects a slip to be empty and must exit 1."""
import difflib
import os
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "/home/nathan/Source/choptuik-large-d-raw"


def toks(cmd):
    t = shlex.split(cmd.replace("RAW/", RAW + "/").replace("RAW ", RAW + " "))
    return t[t.index("anm_lowd.py") + 1:]


def ref():
    for line in open(os.path.join(HERE, "ref", "commands_hc_997.txt")):
        if line.startswith("anm_lowd.py"):
            return toks(line.strip())
    raise SystemExit("no anm_lowd.py line in the reference")


def diff(cmd):
    return list(difflib.unified_diff(ref(), toks(cmd), "coordinator", "actual", lineterm="", n=1))


def selftest(brk):
    good = "nice -n 10 python3 -u anm_lowd.py " + " ".join(f"'{x}'" if x == "" else x for x in ref())
    good = good.replace(RAW + "/", "RAW/").replace(RAW + " ", "RAW ")
    cases = [("the same command", good, True), ("--N 9", good.replace("--N 8", "--N 9"), False), ("--target 3.0432", good.replace("3.0431", "3.0432"), False),
             ("--threads 6", good.replace("--threads 10", "--threads 6"), False), ("a wrong state", good.replace("D3.043150", "D3.043100"), False),
             ("a dropped --checks ''", good.replace("--checks '' ", ""), False)]
    if brk:
        cases[1] = (cases[1][0], cases[1][1], True)
    bad = 0
    for name, c, want in cases:
        d = diff(c)
        ok = (not d) == want
        print(f"  {name}: {'empty' if not d else 'differs'} (expected {'empty' if want else 'differs'}): {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    d = diff(sys.argv[1])
    for l in d:
        print(l)
    print("cmddiff997: " + ("EMPTY" if not d else "DIFFERS"))
    sys.exit(0 if not d else 1)
