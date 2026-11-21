#!/usr/bin/env python3
"""ctl_check.py FILE.jsonl | --selftest [--break]: the cross-machine control of #1025 (the coordinator's hc of 2026-11-21 ~16:15 UTC). The hybrid determinant of the Mac's D 18 point at lambda 1.8
(k_c 63, state sol_l1kc63W1025_D18.000000.npy 45e72c6a, stub d18_stub_l1kc63W1025.jsonl 2cfdb833, lane_d18b.sh's call), run on win2: the Mac read sign +1 and ln|det| -1925.018228986828
(I1025-mac/d18/d18_hybsign_1025.jsonl). Reading (fixed before the run): the same sign with ln|det| within 1e-2 (the hybrid's float64 noise) means win2's environment and the Mac's agree, so a sign pattern across D belongs to the
states; a different sign means an environment difference, and then every cross-machine orientation is void. Exit 0 agree, 1 not. The float64 sign and ln|det| beside are information (the Mac: +1, -1920.991037082774).
--selftest runs planted records through the same function, each with its expected verdict (the Mac's own values agree; the sign flipped does not; ln off by 0.05 does not; off by 5e-3 does), exit 0 when all are as expected;
--break flips one expectation and must exit 1."""
import json
import sys

MAC = dict(sign=1.0, ln=-1925.018228986828, f64_sign=1.0, f64_ln=-1920.991037082774)
TOL = 1e-2


def verdict(r):
    same_sign = float(r["sign"]) == MAC["sign"]
    d = float(r["ln"]) - MAC["ln"]
    ok = same_sign and abs(d) <= TOL and bool(r.get("noise_robust", True))
    return ok, same_sign, d


def selftest(brk):
    base = dict(sign=1.0, ln=MAC["ln"], noise_robust=True)
    cases = [
        ("the Mac's own values", dict(base), True),
        ("the sign flipped", dict(base, sign=-1.0), False),
        ("ln|det| off by 0.05", dict(base, ln=MAC["ln"] + 0.05), False),
        ("ln|det| off by 5e-3, same sign", dict(base, ln=MAC["ln"] + 5e-3), True),
        ("same values, not noise-robust", dict(base, noise_robust=False), False),
    ]
    allok = True
    for name, r, want in cases:
        if brk and name == "the Mac's own values":
            want = not want
        got = verdict(r)[0]
        print("planted: %s: verdict %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        allok = allok and got == want
    print("selftest: %s%s" % ("PASS" if allok else "FAIL", " [break]" if brk else ""))
    return 0 if allok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    rows = [json.loads(x) for x in open(sys.argv[1]) if x.strip()]
    rows = [r for r in rows if r.get("D") == 18.0 and abs(r["lam"] - 1.8) < 1e-12]
    if not rows:
        print("no record for D 18, lambda 1.8")
        sys.exit(1)
    r = rows[-1]
    ok, same, d = verdict(r)
    print("win2: sign %+d, ln|det| %.12f, noise %s (robust %s); the Mac: sign %+d, ln|det| %.12f" % (r["sign"], r["ln"], r["noise"], r["noise_robust"], MAC["sign"], MAC["ln"]))
    print("same sign: %s; ln difference %+.3e (bar %.0e); information: float64 sign %+d ln %.10f (the Mac %+d %.10f), %s s" % (
        same, d, TOL, r["f64_sign"], r["f64_ln"], MAC["f64_sign"], MAC["f64_ln"], r.get("sec")))
    print("CONTROL: %s" % ("agree: win2's environment and the Mac's give the same sign and ln|det| within 1e-2" if ok else
                           "DISAGREE: an environment difference; every cross-machine orientation is void"))
    sys.exit(0 if ok else 1)
