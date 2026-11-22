#!/usr/bin/env python3
"""kcl_ext.py SUBCMD ...: helpers of kcl_ext.sh (#1025 kc71_leap), kept in Python so that the shell script has no nested here-documents.
  kcl_ext.py edge DIR D SIDE        -> prints the edge lambda of the window so far (the lowest or highest lambda of scan_D<D>_P*.jsonl and scan_D<D>_X*.jsonl)
  kcl_ext.py lists EDGE SIDE        -> prints the two lambda lists, one per line: X1 = edge and 5 new points, X2 = edge and 5 further new points (e -/+ 0.01 i, i = 1 to 10)
  kcl_ext.py gate DIR D K EDGE      -> exit 0 the edge points of X<K>1 and X<K>2 agree (same sign, ln|det| within 1e-6, noise-robust), 1 they disagree, 2 not there yet
  kcl_ext.py selftest [--break]     -> planted lists and gate cases"""
import glob
import json
import os
import sys

sys.path.insert(0, "D:/choptuik-i935-raw/I1025-win2/kc71_d185")
import pair_check as pc  # noqa: E402


def lists(edge, side):
    s = -1 if side == "low" else 1
    pts = [round(edge + s * 0.01 * i, 2) for i in range(0, 11)]
    return pts[0:6], [pts[0]] + pts[6:11]


def selftest(brk):
    a, b = lists(1.22, "low")
    ok1 = a == [1.22, 1.21, 1.20, 1.19, 1.18, 1.17] and b == [1.22, 1.16, 1.15, 1.14, 1.13, 1.12]
    c, d = lists(1.62, "high")
    ok2 = c == [1.62, 1.63, 1.64, 1.65, 1.66, 1.67] and d == [1.62, 1.68, 1.69, 1.70, 1.71, 1.72]
    if brk:
        ok1 = not ok1
    print("planted: low-side lists %s %s: %s" % (a, b, "PASS" if ok1 else "FAIL"))
    print("planted: high-side lists %s %s: %s" % (c, d, "PASS" if ok2 else "FAIL"))
    print("selftest: %s%s" % ("PASS" if ok1 and ok2 else "FAIL", " [break]" if brk else ""))
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selftest":
        sys.exit(selftest("--break" in sys.argv))
    if cmd == "edge":
        H, ds, side = sys.argv[2].replace("\\", "/").rstrip("/"), sys.argv[3], sys.argv[4]
        lams = []
        for f in glob.glob("%s/scan_D%s_P*.jsonl" % (H, ds)) + glob.glob("%s/scan_D%s_X*.jsonl" % (H, ds)):
            lams += [json.loads(x)["lam"] for x in open(f) if x.strip()]
        print("%.2f" % (min(lams) if side == "low" else max(lams)))
    elif cmd == "lists":
        a, b = lists(float(sys.argv[2]), sys.argv[3])
        print(",".join("%.2f" % x for x in a))
        print(",".join("%.2f" % x for x in b))
    elif cmd == "gate":
        H, ds, k, e = sys.argv[2].replace("\\", "/").rstrip("/"), sys.argv[3], sys.argv[4], float(sys.argv[5])
        a, b = pc.first("%s/scan_D%s_X%s1.jsonl" % (H, ds, k), e), pc.first("%s/scan_D%s_X%s2.jsonl" % (H, ds, k), e)
        if a is None or b is None:
            print("edge point %.2f: not there yet" % e)
            sys.exit(2)
        ok = pc.agree(a, b)
        print("edge point %.2f (X%s1, X%s2): %+d %.10f and %+d %.10f, difference %+.2e (bar 1e-6): %s" % (e, k, k, a["sign"], a["ln"], b["sign"], b["ln"], b["ln"] - a["ln"], "agree" if ok else "DISAGREE"))
        sys.exit(0 if ok else 1)
