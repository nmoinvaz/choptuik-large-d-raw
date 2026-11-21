#!/usr/bin/env python3
"""repeat_check_b.py B1.jsonl B2.jsonl [INPUTS] | --selftest [--break]: the repeat check of the split B windows of #1025 d185map (the coordinator's hc of 2026-11-21 ~19:32 UTC): the first points of both B processes,
lambda 1.55, are repeats of xfkappa's point at D 18.5 (inputs/d185_scan_1025.jsonl: sign -1, ln|det| -1899.8809001371699), "which must agree", by repeat_check.py's rule (the same sign, ln|det| within 1e-2, noise-robust).
Exit 0 both agree, 1 a disagreement, 2 a first point is not there yet. --selftest is repeat_check.py's (the same verdict function), --break likewise."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repeat_check as rc  # noqa: E402

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(rc.selftest("--break" in sys.argv))
    inp = sys.argv[3] if len(sys.argv) > 3 else "D:/choptuik-i935-raw/I1025-win2/d185map/inputs"
    status = 0
    for name, path in (("B1", sys.argv[1]), ("B2", sys.argv[2])):
        r = rc.first(path, 1.55)
        if r is None:
            print("window %s: the lambda 1.55 point is not there yet" % name)
            status = max(status, 2) if status != 1 else 1
            continue
        x = rc.ref_row(inp, "d185_scan_1025.jsonl", 1.55)
        ok, same, d = rc.verdict(r, x)
        print("window %s lambda 1.55: win2 sign %+d ln|det| %.12f (noise robust %s); xfkappa %+d %.12f; same sign %s, ln difference %+.3e (bar 1e-2): %s" % (
            name, r["sign"], r["ln"], r["noise_robust"], x["sign"], x["ln"], same, d, "agree" if ok else "DISAGREE"))
        if not ok:
            status = 1
    print("REPEATS: %s" % {0: "both agree", 1: "a repeated point DISAGREES", 2: "waiting for the first points"}[status])
    sys.exit(status)
