#!/usr/bin/env python3
"""pair79.py A.jsonl B.jsonl | --selftest [--break]: the repeat gate of the k_c 79 D 20 scan (#1025 kc79_d20). The first record of each file is the same lambda (1.26) evaluated in two processes; they must agree in
hybrid sign, noise-test signs, float64 sign and ln|det| within 1e-6 (read_lower.py's repeat rule). Exit 0 agree, 1 disagree, 2 a first record is not there yet. --selftest runs planted records; --break makes the
ln|det| bar 1 so that the planted disagreement passes, and the selftest must then exit 1."""
import json, sys, os
BAR = 1.0 if "--break" in sys.argv else 1e-6


def verdict(a, b):
    why = []
    if abs(a["lam"] - b["lam"]) > 1e-9: why.append("different lambda %r %r" % (a["lam"], b["lam"]))
    if a["sign"] != b["sign"]: why.append("hybrid sign %s vs %s" % (a["sign"], b["sign"]))
    if a.get("noise") != b.get("noise"): why.append("noise signs differ")
    if a.get("f64_sign") != b.get("f64_sign"): why.append("float64 sign differs")
    if abs(a["ln"] - b["ln"]) > BAR: why.append("ln|det| differs by %.3e (bar %g)" % (abs(a["ln"] - b["ln"]), BAR))
    return not why, why


def first(p):
    if not os.path.exists(p): return None
    for l in open(p):
        if l.strip(): return json.loads(l)
    return None


if "--selftest" in sys.argv:
    r = dict(lam=1.26, sign=1.0, noise=[1.0, 1.0], f64_sign=1.0, ln=-2000.123456)
    cases = [("equal", r, dict(r), True), ("ln|det| 1e-5 apart", r, dict(r, ln=r["ln"] + 1e-5), False), ("ln|det| 5e-7 apart", r, dict(r, ln=r["ln"] + 5e-7), True),
             ("opposite sign", r, dict(r, sign=-1.0), False), ("noise differs", r, dict(r, noise=[1.0, -1.0]), False), ("float64 sign differs", r, dict(r, f64_sign=-1.0), False),
             ("different lambda", r, dict(r, lam=1.27), False)]
    ok = True
    for n, a, b, want in cases:
        got = verdict(a, b)[0]; print("planted: %s: %s, expected %s: %s" % (n, got, want, "PASS" if got == want else "FAIL")); ok = ok and got == want
    print("selftest: %s" % ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
a, b = first(sys.argv[1]), first(sys.argv[2])
if a is None or b is None: sys.exit(2)
ok, why = verdict(a, b)
print("repeat %.2f: %s %.10f | %s %.10f: %s" % (a["lam"], a["sign"], a["ln"], b["sign"], b["ln"], "agree" if ok else "DISAGREE " + "; ".join(why)))
sys.exit(0 if ok else 1)
