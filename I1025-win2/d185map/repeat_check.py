#!/usr/bin/env python3
"""repeat_check.py A.jsonl B.jsonl [RAWQ] | --selftest [--break]: the repeat check of #1025 d185map (the coordinator's hc of 2026-11-21 ~19:20 UTC): the first points of the two windows, lambda 2.40 (A) and 1.55 (B), are
repeats of xfkappa's points at D 18.5 (copies in inputs/ of I1025-mac/d18/d185_scanup_1025.jsonl and d185_scan_1025.jsonl), "which must agree". Agree (fixed before the run): the same sign, ln|det| within 1e-2 (the cross-machine bar of the
control, where win2 and the Mac differed by 8.9e-4; the reader's same-machine repeat bar of 1e-6 does not apply across machines), and both points noise-robust. Exit 0 both agree, 1 a disagreement, 2 a first point is
not there yet. --selftest runs planted rows through the same function with expected verdicts (identical agrees; a flipped sign, ln off by 0.05 and a non-robust point do not; off by 5e-3 does), exit 0 when all are as expected;
--break flips one expectation and must exit 1."""
import json
import os
import sys

TOL = 1e-2


def verdict(r, ref):
    same = float(r["sign"]) == float(ref["sign"])
    d = float(r["ln"]) - float(ref["ln"])
    return same and abs(d) <= TOL and bool(r.get("noise_robust", True)) and bool(ref.get("noise_robust", True)), same, d


def first(path, lam):
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.strip():
            r = json.loads(line)
            if abs(r["lam"] - lam) < 1e-9:
                return r
    return None


def ref_row(rawq, fname, lam):
    for line in open(os.path.join(rawq, fname)):
        r = json.loads(line)
        if r["D"] == 18.5 and abs(r["lam"] - lam) < 1e-9:
            return r
    raise SystemExit("no reference row for lambda %s in %s" % (lam, fname))


def selftest(brk):
    ref = dict(sign=1.0, ln=-1887.2954204507596, noise_robust=True)
    cases = [("identical", dict(ref), True), ("sign flipped", dict(ref, sign=-1.0), False), ("ln off by 0.05", dict(ref, ln=ref["ln"] + 0.05), False),
             ("ln off by 5e-3, same sign", dict(ref, ln=ref["ln"] + 5e-3), True), ("not noise-robust", dict(ref, noise_robust=False), False)]
    allok = True
    for name, r, want in cases:
        if brk and name == "identical":
            want = not want
        got = verdict(r, ref)[0]
        print("planted: %s: verdict %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        allok = allok and got == want
    print("selftest: %s%s" % ("PASS" if allok else "FAIL", " [break]" if brk else ""))
    return 0 if allok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    A, B = sys.argv[1], sys.argv[2]
    rawq = sys.argv[3] if len(sys.argv) > 3 else "D:/choptuik-i935-raw/I1025-win2/d185map/inputs"
    pairs = [("A", A, 2.4, "d185_scanup_1025.jsonl"), ("B", B, 1.55, "d185_scan_1025.jsonl")]
    status = 0
    for name, path, lam, ref in pairs:
        r = first(path, lam)
        if r is None:
            print("window %s: the lambda %.2f point is not there yet" % (name, lam))
            status = max(status, 2) if status != 1 else 1
            continue
        x = ref_row(rawq, ref, lam)
        ok, same, d = verdict(r, x)
        print("window %s lambda %.2f: win2 sign %+d ln|det| %.12f (noise robust %s); xfkappa %+d %.12f (%s); same sign %s, ln difference %+.3e (bar %.0e): %s" % (
            name, lam, r["sign"], r["ln"], r["noise_robust"], x["sign"], x["ln"], ref, same, d, TOL, "agree" if ok else "DISAGREE"))
        if not ok:
            status = 1
    print("REPEATS: %s" % {0: "both agree", 1: "a repeated point DISAGREES", 2: "waiting for the first points"}[status])
    sys.exit(status)
