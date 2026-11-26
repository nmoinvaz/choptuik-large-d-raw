#!/usr/bin/env python3
"""checks_gate.py DIR | --selftest [--mutate]   (I1088-win2/L8000; the gate of the form-S selftests, registered in
I1025-win2/hp_form_s_build/README.md before they ran)

Reads DIR = I1025-win2/hp_form_s_build: checks_exits.txt and checks/*.log, and exits 0 only when all five read as registered:
  floor_stop           exit 0 and 'PASS' in the log
  floor_stop_stale     exit 0 and 'PASS'
  floor_stop_nofloor   exit non-zero and 'FAIL' (the control fires)
  form_s_check         'converged' (not 'NOT converged') and |Delta_S - Delta_A| <= 1e-20
  form_s_check_flux    'NOT converged', or |Delta_S - Delta_A| >= 1e-12 (the control moves Delta)
--selftest: planted logs (all as registered; each of the five broken once) must read as written; --mutate makes the gate
accept everything, which the planted broken cases must catch (exit 1)."""
import os
import re
import sys

MUT = "--mutate" in sys.argv


def diff_of(text):
    m = re.search(r"Delta_S - Delta_A\s+(-?[0-9.]+(?:e[-+]?[0-9]+)?)", text)
    return abs(float(m.group(1))) if m else None


def read(name, exit_code, text):
    """(ok, why) for one check"""
    if MUT:
        return True, "mutated: accepts"
    if name in ("floor_stop", "floor_stop_stale"):
        ok = exit_code == 0 and "PASS" in text
        return ok, "exit %s, PASS %s" % (exit_code, "PASS" in text)
    if name == "floor_stop_nofloor":
        ok = exit_code != 0 and "FAIL" in text
        return ok, "exit %s, FAIL %s" % (exit_code, "FAIL" in text)
    d = diff_of(text)
    conv = ("converged" in text) and ("NOT converged" not in text)
    if name == "form_s_check":
        ok = conv and d is not None and d <= 1e-20
        return ok, "converged %s, |diff| %s" % (conv, d)
    if name == "form_s_check_flux":
        ok = ("NOT converged" in text) or (d is not None and d >= 1e-12)
        return ok, "converged %s, |diff| %s" % (conv, d)
    return False, "unknown check"


NAMES = ("floor_stop", "floor_stop_stale", "floor_stop_nofloor", "form_s_check", "form_s_check_flux")


def gate(exits, logs):
    """exits: {name: int}; logs: {name: text}"""
    allok, lines = True, []
    for n in NAMES:
        if n not in exits or n not in logs:
            allok = False
            lines.append("%s: missing" % n)
            continue
        ok, why = read(n, exits[n], logs[n])
        allok = allok and ok
        lines.append("%s: %s (%s)" % (n, "OK" if ok else "NOT as registered", why))
    return allok, lines


def selftest():
    good_logs = {
        "floor_stop": "... PASS (mutate none)", "floor_stop_stale": "... PASS (stale J, mutate none)", "floor_stop_nofloor": "... FAIL (mutate nofloor)",
        "form_s_check": "  converged in 3 steps: Delta_S 1.2, Delta_S - Delta_A 3.4e-29",
        "form_s_check_flux": "  NOT converged in 12 steps: Delta_S 1.2, Delta_S - Delta_A 5e-5",
    }
    good_exits = {"floor_stop": 0, "floor_stop_stale": 0, "floor_stop_nofloor": 1, "form_s_check": 0, "form_s_check_flux": 0}
    bad = []
    ok, _ = gate(good_exits, good_logs)
    if not ok:
        bad.append("the registered readings were refused")
    breaks = [
        ("floor_stop fails", dict(good_exits, floor_stop=1), dict(good_logs, floor_stop="... FAIL")),
        ("stale fails", good_exits, dict(good_logs, floor_stop_stale="... FAIL")),
        ("nofloor control does not fire", dict(good_exits, floor_stop_nofloor=0), dict(good_logs, floor_stop_nofloor="... PASS")),
        ("check does not converge", good_exits, dict(good_logs, form_s_check="  NOT converged in 12 steps: Delta_S - Delta_A 1e-30")),
        ("check diff too large", good_exits, dict(good_logs, form_s_check="  converged in 3 steps: Delta_S - Delta_A 2e-18")),
        ("flux control does not move Delta", good_exits, dict(good_logs, form_s_check_flux="  converged in 3 steps: Delta_S - Delta_A 1e-25")),
        ("a log is missing", good_exits, {k: v for k, v in good_logs.items() if k != "form_s_check"}),
    ]
    for name, e, l in breaks:
        ok, _ = gate(e, l)
        if ok:
            bad.append("accepted: " + name)
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    d = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    exits = {}
    p = os.path.join(d, "checks_exits.txt")
    for line in open(p) if os.path.exists(p) else []:
        m = re.search(r"check (\w+): exit (\d+) ", line)
        if m:
            exits[m.group(1)] = int(m.group(2))
    logs = {}
    for n in NAMES:
        f = os.path.join(d, "checks", n + ".log")
        if os.path.exists(f):
            logs[n] = open(f, errors="replace").read()
    ok, lines = gate(exits, logs)
    print("\n".join(lines))
    print("GATE: %s" % ("the selftests read as registered" if ok else "NOT as registered"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
