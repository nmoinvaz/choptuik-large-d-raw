#!/usr/bin/env python3
"""cmddiff1035.py NAME (--log LOG | --actual "CMD") [--ref FILE] | --selftest [--break]: the diff of the command line a run uses against the coordinator's (ref/commands_hc_1035.txt, verbatim from the message and notes/FACTORED_HORIZON.md 5.3),
asked for on 21 Nov after three slips: run it before each launch and keep its output (empty or not) in the run's log or README. Both commands are reduced to the tokens of the factored_raise.py invocation (the `timeout`, `nice`, redirection,
comment and `echo` parts dropped), $RAW, $OUT, $P0 and $PR replaced by the values, and the token lists diffed (unified diff, one token a line). NAME is the output folder name (planted, planted_order, planted_old, planted_linear). Prints the diff
(nothing when empty) and a line 'cmddiff NAME: EMPTY' or 'cmddiff NAME: DIFFERS'; exit 0 when empty. --log reads the command from the log's first line ('# <time> UTC factored_raise.py <args>', which factored_raise.py writes); --actual takes the command
string (the harness passes it before the launch). --selftest plants the slips: the same command (empty), the order run without --mutate=order (must differ), a wrong --ks, a wrong bar, a wrong state path; --break expects the omission to be empty and must exit 1."""
import difflib
import os
import re
import shlex
import sys

RAW = "/home/nathan/Source/choptuik-large-d-raw"
VALUES = {"$RAW": RAW, "$P0": "I1064-dh610/ho2_D237.7132/ks307/base_pin3_D237.7132.npz", "$PR": "I1064-dh170/p315/ks315/base_pin3_D237.7132.npz"}
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = f"{RAW}/I1035-dh610/stage2_planted"


def tokens(cmd, out=OUT):
    """the factored_raise.py invocation's tokens: from 'factored_raise.py' to the redirection or the first ';' / '#', variables substituted"""
    cmd = cmd.replace("$OUT", out)
    for k, v in VALUES.items():
        cmd = cmd.replace(k, v)
    m = re.search(r"factored_raise\.py(.*)$", cmd)
    if not m:
        return None
    rest = re.split(r"\s>\s|\s2>&1|;|\s#", m.group(1))[0]
    return ["factored_raise.py"] + shlex.split(rest)


def reference(name, ref):
    for line in open(ref):
        if line.startswith("#"):
            continue
        t = tokens(line)
        if t and f"{OUT}/{name}" in t:
            return t
    return None


def diff(name, actual_cmd, ref):
    a = reference(name, ref)
    b = tokens(actual_cmd)
    if a is None:
        return None, f"no reference line for {name}"
    if b is None:
        return None, "no factored_raise.py invocation in the actual command"
    d = list(difflib.unified_diff(a, b, "coordinator", "actual", lineterm="", n=1))
    return d, None


def selftest(brk):
    ref = os.path.join(HERE, "ref", "commands_hc_1035.txt")
    base = (f"timeout -s TERM 7200 nice -n 10 python3 -u factored_raise.py {RAW} {OUT}/planted_order --state {VALUES['$P0']} --ks 315 --threads 10 --ref {VALUES['$PR']} --bar 1e-60 --mutate=order")
    cases = [("the same command", base, True), ("the order run without --mutate=order (the slip of 21 Nov)", base.replace(" --mutate=order", ""), False),
             ("a wrong --ks", base.replace("--ks 315", "--ks 314"), False), ("a wrong bar", base.replace("--bar 1e-60", "--bar 1e-55"), False),
             ("a wrong state path", base.replace("ks307", "ks308"), False), ("a changed thread count", base.replace("--threads 10", "--threads 6"), False)]
    if brk:
        cases[1] = (cases[1][0], cases[1][1], True)
    bad = 0
    for name, cmd, want_empty in cases:
        d, err = diff("planted_order", cmd, ref)
        ok = err is None and (len(d) == 0) == want_empty
        print(f"  {name}: {'empty' if d == [] else ('differs' if d else err)} (expected {'empty' if want_empty else 'differs'}): {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    name = sys.argv[1]
    ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else os.path.join(HERE, "ref", "commands_hc_1035.txt")
    if "--log" in sys.argv:
        first = open(sys.argv[sys.argv.index("--log") + 1], errors="replace").readline()
        actual = first
    else:
        actual = sys.argv[sys.argv.index("--actual") + 1]
    d, err = diff(name, actual, ref)
    if d is None:
        print(f"cmddiff {name}: ERROR {err}")
        sys.exit(2)
    for l in d:
        print(l)
    print(f"cmddiff {name}: {'EMPTY' if not d else 'DIFFERS'}")
    sys.exit(0 if not d else 1)
