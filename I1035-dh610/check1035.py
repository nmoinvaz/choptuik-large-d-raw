#!/usr/bin/env python3
"""check1035.py KIND LOG EXIT | --selftest [--mutate]: reads a factored_raise.py log of the #1035 stage 2 planted run by the coordinator's lines.
KIND selftest-log: the selftest log (must end 'selftest: 19 of 19 pass' with exit 0); nopred: the --mutate=nopred selftest (must contain 'FAIL: model factored (--mutate=nopred)', exit 1);
planted: PASS = exit 0 plus 'raise converged (converged) after N line(s), last max|F| ... written raise_pin3_D237.7132.npz' and 'against I1064-dh170/p315/ks315/base_pin3_D237.7132.npz (ks 315, plan the same): largest entry
difference ...: PASS (bar 1e-60)'; a line saying the plans DIFFER is a setup failure, not a raise failure; order: the state line 'ks 307 -> 314 (--mutate=order: ks - 1)' and an end of 'FAIL (bar 1e-60)' or 'NOT converged', exit 1.
Prints the verdict, the header line ('hpkernel <path> (<isa>; ...) ...') and any 'notice:' lines. Exit 0 when the kind's rule is met, 1 otherwise. --selftest runs planted logs through the same function (each broken case must fail;
--mutate loosens each rule and the selftest must then fail, exit 1)."""
import re
import sys

PASS_RAISE = re.compile(r"raise converged \(converged\) after (\d+) line\(s\), last max\|F\|[^\n]*written raise_pin3_D237\.7132\.npz")
PASS_CMP = re.compile(r"against I1064-dh170/p315/ks315/base_pin3_D237\.7132\.npz \(ks 315, plan the same\): largest entry difference[^\n]*: PASS \(bar 1e-60\)")
PLANS_DIFFER = re.compile(r"plan[^\n]*\bDIFFER\b")
STATE_ORDER = re.compile(r"ks 307 -> 314 \(--mutate=order: ks - 1\)")
FAIL_BAR = re.compile(r"FAIL \(bar 1e-60\)")
NOT_CONV = re.compile(r"NOT converged")


def verdict(kind, text, rc, mutate=False):
    """(ok, text of the verdict)"""
    if kind == "selftest-log":
        ok = rc == 0 and re.search(r"selftest: 19 of 19 pass\s*$", text.strip().splitlines()[-1] if text.strip() else "") is not None
        return (ok or (mutate and rc == 0), f"exit {rc}, last line {text.strip().splitlines()[-1] if text.strip() else ''!r}")
    if kind == "nopred":
        ok = rc == 1 and "FAIL: model factored (--mutate=nopred)" in text
        return (ok or (mutate and rc == 1), f"exit {rc}, the nopred FAIL line {'present' if 'FAIL: model factored (--mutate=nopred)' in text else 'missing'}")
    if kind == "planted":
        if PLANS_DIFFER.search(text):
            return False, "SETUP FAILURE: the plans differ"
        a, b = PASS_RAISE.search(text), PASS_CMP.search(text)
        ok = rc == 0 and a is not None and b is not None
        if mutate:
            ok = rc == 0 or (a is not None or b is not None)
        return ok, f"exit {rc}, raise line {'found (' + a.group(1) + ' line(s))' if a else 'missing'}, comparison PASS line {'found' if b else 'missing'}"
    if kind == "order":
        s = STATE_ORDER.search(text) is not None
        end = "FAIL (bar 1e-60)" if FAIL_BAR.search(text) else ("NOT converged" if NOT_CONV.search(text) else "neither")
        ok = rc == 1 and s and end != "neither"
        if mutate:
            ok = (rc == 1 or s) and (s or end != "neither")
        return ok, f"exit {rc}, state line {'present' if s else 'missing'}, ends {end}"
    raise SystemExit(f"unknown kind {kind}")


def header(text):
    h = [l for l in text.splitlines() if l.startswith("hpkernel ")]
    n = [l for l in text.splitlines() if l.startswith("notice:")]
    return (h[0] if h else "no hpkernel header line"), n


def selftest(mutate):
    pass_log = ("hpkernel /x/hpkernel (avx2; multidouble 5.1.0); built from main at HEAD 276aa1cd; this script at bae00edf\n"
                "raise converged (converged) after 6 line(s), last max|F| <=1e-80 (2.1e-86), written raise_pin3_D237.7132.npz\n"
                "against I1064-dh170/p315/ks315/base_pin3_D237.7132.npz (ks 315, plan the same): largest entry difference 3.0e-86: PASS (bar 1e-60)\n")
    cases = [
        ("selftest-log", "x\nselftest: 19 of 19 pass\n", 0, True), ("selftest-log", "x\nselftest: 18 of 19 pass\n", 1, False), ("selftest-log", "x\nselftest: 19 of 19 pass\n", 1, False),
        ("nopred", "FAIL: model factored (--mutate=nopred)\n", 1, True), ("nopred", "selftest: 19 of 19 pass\n", 0, False), ("nopred", "FAIL: model factored (--mutate=nopred)\n", 0, False),
        ("planted", pass_log, 0, True), ("planted", pass_log, 1, False),
        ("planted", pass_log.replace("PASS (bar 1e-60)", "FAIL (bar 1e-60)"), 0, False),
        ("planted", pass_log.replace("plan the same", "plans DIFFER"), 0, False),
        ("planted", pass_log.split("\n")[0] + "\n" + pass_log.split("\n")[2] + "\n", 0, False),
        ("order", "ks 307 -> 314 (--mutate=order: ks - 1)\nagainst ...: FAIL (bar 1e-60)\n", 1, True), ("order", "ks 307 -> 314 (--mutate=order: ks - 1)\nNOT converged\n", 1, True),
        ("order", "ks 307 -> 314 (--mutate=order: ks - 1)\nagainst ...: FAIL (bar 1e-60)\n", 0, False), ("order", "ks 307 -> 315\nNOT converged\n", 1, False),
    ]
    bad = 0
    for kind, text, rc, want in cases:
        ok, _ = verdict(kind, text, rc, mutate)
        good = ok == want
        print(f"  {kind} exit {rc}: {'ok' if ok else 'not ok'} (expected {'ok' if want else 'not ok'}): {'ok' if good else 'WRONG'}")
        bad += not good
    h, n = header(pass_log + "notice: a\n")
    g = h.startswith("hpkernel /x/hpkernel (avx2;") and n == ["notice: a"]
    print(f"  header and notice lines read: {'ok' if g else 'WRONG'}")
    bad += not g
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    kind, log, rc = sys.argv[1], sys.argv[2], int(sys.argv[3])
    text = open(log, errors="replace").read()
    ok, msg = verdict(kind, text, rc)
    h, n = header(text)
    print(f"{kind}: {'RULE MET' if ok else 'RULE NOT MET'}: {msg}")
    print(h[:300])
    for l in n:
        print(l[:300])
    sys.exit(0 if ok else 1)
