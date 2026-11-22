#!/usr/bin/env python3
"""pair_check2.py DIR D | --selftest [--break]: the repeat gate of one D of #1025 kc71_leap: the first points of the pairs (P1, P2) and (P3, P4), at the check lambdas of checks_D<D>.json, must agree (same machine, same code:
the same sign, ln|det| within 1e-6, noise-robust). Exit 0 both pairs agree, 1 a disagreement, 2 a first point is not there yet. --selftest and --break are pair_check.py's (the same verdict function)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "D:/choptuik-i935-raw/I1025-win2/kc71_d185")
import pair_check as pc  # noqa: E402

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(pc.selftest("--break" in sys.argv))
    H = sys.argv[1].replace("\\", "/").rstrip("/") + "/"
    tag = "%g" % float(sys.argv[2])
    ch = json.load(open(H + "checks_D%s.json" % tag))
    status = 0
    for x, y, lam in ((1, 2, ch["c12"]), (3, 4, ch["c34"])):
        ra, rb = pc.first(H + "scan_D%s_P%d.jsonl" % (tag, x), lam), pc.first(H + "scan_D%s_P%d.jsonl" % (tag, y), lam)
        if ra is None or rb is None:
            print("pair (P%d, P%d) lambda %.2f: first points not there yet (P%d %s, P%d %s)" % (x, y, lam, x, ra is not None, y, rb is not None))
            status = max(status, 2) if status != 1 else 1
            continue
        ok = pc.agree(ra, rb)
        print("pair (P%d, P%d) lambda %.2f: %+d %.10f and %+d %.10f, difference %+.2e (bar 1e-6): %s" % (x, y, lam, ra["sign"], ra["ln"], rb["sign"], rb["ln"], rb["ln"] - ra["ln"], "agree" if ok else "DISAGREE"))
        if not ok:
            status = 1
    print("PAIRS: %s" % {0: "both agree", 1: "a repeated point DISAGREES", 2: "waiting for the first points"}[status])
    sys.exit(status)
