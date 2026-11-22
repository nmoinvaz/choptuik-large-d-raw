#!/usr/bin/env python3
"""#1075 repeat_bits.py SCAN.jsonl | selftest [--mutate]: every lambda that occurs more than once in a scan file must repeat bit for bit: sign, ln|det|, both noise
signs, noise_robust, float64 sign and float64 ln|det| equal (==, no tolerance). Exit 0 agree, 1 disagree, 2 no repeat.
selftest: a planted agreeing set passes; a ln|det| shift of one ulp, a noise sign flip and a float64 ln|det| shift of one ulp each fail. --mutate compares with a
tolerance of 1e-6 on the two ln fields, so the one-ulp cases pass and the selftest must exit 1."""
import collections
import json
import math
import sys

FIELDS = ("sign", "ln", "noise", "noise_robust", "f64_sign", "f64_ln")


def same(a, b, tol):
    for k in FIELDS:
        x, y = a.get(k), b.get(k)
        if k in ("ln", "f64_ln") and tol:
            if abs(x - y) > tol:
                return False
        elif x != y:
            return False
    return True


def check(rows, tol=0.0):
    g = collections.defaultdict(list)
    for r in rows:
        g[r["lam"]].append(r)
    rep = {k: v for k, v in g.items() if len(v) > 1}
    if not rep:
        return 2, "no repeated lambda"
    bad = [k for k, v in rep.items() if any(not same(v[0], x, tol) for x in v[1:])]
    return (1, f"DISAGREE at {bad}") if bad else (0, f"lambda {sorted(rep)}: {[len(v) for k, v in sorted(rep.items())]} evaluations each, bit for bit equal")


def selftest(mutate):
    tol = 1e-6 if mutate else 0.0
    mk = lambda lam, s, ln, f=-5.0: dict(lam=lam, sign=s, ln=ln, noise=[s, s], noise_robust=True, f64_sign=s, f64_ln=f)
    base = [mk(1.27, -1.0, -2500.123456789), mk(1.22, 1.0, -2501.0)]
    cases = [("agreeing", base + [mk(1.27, -1.0, -2500.123456789)], 0),
             ("ln one ulp", base + [mk(1.27, -1.0, math.nextafter(-2500.123456789, 0))], 1),
             ("noise sign flip", base + [dict(mk(1.27, -1.0, -2500.123456789), noise=[-1.0, 1.0])], 1),
             ("float64 ln one ulp", base + [mk(1.27, -1.0, -2500.123456789, math.nextafter(-5.0, 0))], 1),
             ("no repeat", base, 2)]
    bad = 0
    for name, rows, want in cases:
        got = check(rows, tol)[0]
        ok = got == want
        bad += not ok
        print(f"  {name}: exit {got} (expected {want}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    c, msg = check([json.loads(l) for l in open(sys.argv[1]) if l.strip()])
    print(("AGREE: " if c == 0 else "FAIL: ") + msg)
    sys.exit(c)
