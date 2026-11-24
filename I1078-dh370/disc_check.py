"""#1078: the discriminator for the quad-double pair (t5's order): are two more qd determinants on the line through a simple zero lying between the pair?

    python3 disc_check.py modeqd_pair.jsonl modeqd_disc.jsonl [--bar=0.1]      |      python3 disc_check.py selftest [--mutate=sign|shift]

Reading (a): |det M| is linear in |lam - lam*| near a simple zero lam* between lam1 < lam2 (the pair, opposite signs): ln|f2| - ln|f1| = ln((lam2... d2 / d1)) with d1 = lam* - lam1, d2 = lam2 - lam*, d1 + d2 = lam2 - lam1,
so d1 = (lam2 - lam1) / (1 + exp(ln2 - ln1)). A third point lam on the side of lam1 (lam < lam*) has the sign of the first and ln = ln1 + ln((lam* - lam) / d1); one on the side of lam2 (lam > lam*) has the sign of the second
and ln = ln2 + ln((lam - lam*) / d2). Pass: the sign as predicted and |ln - predicted| <= bar (default 0.1) at both points. (b) (the entries' noise) predicts neither. Exit 0 iff both points pass."""
import json
import math
import sys


def predict(pair, lam):
    (l1, s1, f1), (l2, s2, f2) = pair
    d1 = (l2 - l1) / (1 + math.exp(f2 - f1))
    d2 = (l2 - l1) - d1
    zero = l1 + d1
    if lam < zero:
        return s1, f1 + math.log((zero - lam) / d1), zero
    return s2, f2 + math.log((lam - zero) / d2), zero


def check(pair_rows, new_rows, bar=0.1, verbose=True):
    pair = sorted((r["lam"], r["sign"], r["ln"]) for r in pair_rows)
    ok = True
    for r in new_rows:
        s, f, zero = predict(pair, r["lam"])
        good = r["sign"] == s and abs(r["ln"] - f) <= bar
        ok &= good
        if verbose:
            print(f"lam {r['lam']!r}: measured ({r['sign']:+.0f}, {r['ln']:.6f}); predicted under (a) ({s:+.0f}, {f:.6f}) with the zero at lam1 + {zero - pair[0][0]:.4e}: "
                  f"sign {'ok' if r['sign'] == s else 'WRONG'}, ln difference {r['ln'] - f:+.4f} (bar {bar}): {'ON THE LINE' if good else 'OFF THE LINE'}")
    return 0 if ok else 1


def selftest():
    l1, l2 = 5.140819788786, 5.1408197887863025
    zero = l1 + 2.9e-13
    k = 1.0
    def f(lam):                                           # a planted function with a simple zero at `zero`: |f| = k |lam - zero| e^(3604), sign + below, - above
        return (1.0 if lam < zero else -1.0), 3604.0 + math.log(abs(lam - zero) * 1e13)
    pair = [dict(lam=l, sign=f(l)[0], ln=f(l)[1]) for l in (l1, l2)]
    la, lb = 5.1408197887857, 5.1408197887866
    good = [dict(lam=l, sign=f(l)[0], ln=f(l)[1]) for l in (la, lb)]
    ok1 = check(pair, good, verbose=False) == 0
    bad_sign = [dict(g, sign=-g["sign"]) for g in good]
    bad_shift = [dict(g, ln=g["ln"] + 3.0) for g in good]
    ok2 = check(pair, bad_sign, verbose=False) == 1
    ok3 = check(pair, bad_shift, verbose=False) == 1
    print(f"selftest: planted simple zero: the two points on the line pass {'PASS' if ok1 else 'FAIL'}; with the signs flipped it fails {'PASS' if ok2 else 'FAIL'}; with ln shifted by 3 it fails {'PASS' if ok3 else 'FAIL'}")
    return 0 if ok1 and ok2 and ok3 else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    bar = float(next((x.split("=")[1] for x in sys.argv if x.startswith("--bar=")), 0.1))
    rc = check([json.loads(l) for l in open(a[0])], [json.loads(l) for l in open(a[1])], bar)
    print("ALL ON THE LINE" if rc == 0 else "OFF THE LINE")
    sys.exit(rc)
