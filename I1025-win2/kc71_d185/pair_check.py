#!/usr/bin/env python3
"""pair_check.py DIR | --selftest [--break]: the repeat gate of #1025 kc71_d185: the first points of the pairs (P1, P2) at lambda 1.77 and (P3, P4) at 2.25 must agree (same machine, same code: the same sign, ln|det| within 1e-6, noise-robust).
Exit 0 both pairs agree, 1 a disagreement, 2 a first point is not there yet. --selftest runs planted rows (identical agrees; a flipped sign, ln off by 1e-3 and a non-robust point do not), --break flips one expectation and must exit 1."""
import json
import os
import sys


def agree(a, b):
    return a["sign"] == b["sign"] and abs(a["ln"] - b["ln"]) <= 1e-6 and bool(a.get("noise_robust", True)) and bool(b.get("noise_robust", True))


def first(path, lam):
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.strip():
            r = json.loads(line)
            if abs(r["lam"] - lam) < 1e-9:
                return r
    return None


def selftest(brk):
    a = dict(sign=1.0, ln=-1900.0, noise_robust=True)
    cases = [("identical", dict(a), True), ("sign flipped", dict(a, sign=-1.0), False), ("ln off by 1e-3", dict(a, ln=a["ln"] + 1e-3), False), ("ln off by 5e-7", dict(a, ln=a["ln"] + 5e-7), True), ("not noise-robust", dict(a, noise_robust=False), False)]
    ok = True
    for name, b, want in cases:
        if brk and name == "identical":
            want = not want
        got = agree(a, b)
        print("planted: %s: verdict %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        ok = ok and got == want
    print("selftest: %s%s" % ("PASS" if ok else "FAIL", " [break]" if brk else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    H = sys.argv[1].replace("\\", "/").rstrip("/") + "/"
    status = 0
    for x, y, lam in ((1, 2, 1.77), (3, 4, 2.25)):
        ra, rb = first(H + "scan_P%d.jsonl" % x, lam), first(H + "scan_P%d.jsonl" % y, lam)
        if ra is None or rb is None:
            print("pair (P%d, P%d) lambda %.2f: first points not there yet (P%d %s, P%d %s)" % (x, y, lam, x, ra is not None, y, rb is not None))
            status = max(status, 2) if status != 1 else 1
            continue
        ok = agree(ra, rb)
        print("pair (P%d, P%d) lambda %.2f: %+d %.10f and %+d %.10f, difference %+.2e (bar 1e-6): %s" % (x, y, lam, ra["sign"], ra["ln"], rb["sign"], rb["ln"], rb["ln"] - ra["ln"], "agree" if ok else "DISAGREE"))
        if not ok:
            status = 1
    print("PAIRS: %s" % {0: "both agree", 1: "a repeated point DISAGREES", 2: "waiting for the first points"}[status])
    sys.exit(status)
