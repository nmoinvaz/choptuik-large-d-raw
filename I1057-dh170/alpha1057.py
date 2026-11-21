#!/usr/bin/env python3
"""#1057: the Delta direction's angle alpha in the plane of the two lowest near_null vectors, and its forecast. Model-independent summary of the Delta shares.

    alpha1057.py [--mutate]        table over the states D 260.2515 to the latest (c3b_ks293 records of this folder), and the registered forecast
    alpha1057.py --selftest [--mutate]   planted: shares built from a known alpha (and a Delta weight w of the plane) must give alpha back to 1e-12 degrees

Definition: with s1, s2 the Delta shares of vectors 1 and 2 (sorted by sigma), w = s1 + s2 (0.9922 at D 260.8483 and D 260.9271), alpha = atan(sqrt(s2 / s1)):
s1 = w cos^2 alpha, s2 = w sin^2 alpha. alpha is 0 when the Delta mode is wholly in the lowest vector and 90 degrees when it is wholly in the upper one. Item (e) of #1057
(classified Delta share >= 0.9) needs s2 >= 0.9, i.e. alpha >= asin(sqrt(0.9 / w)) = 72.2 degrees for w 0.9922.
Forecast (a registered extrapolation, not a fit): alpha(D) = alpha_last + r (D - D_last) with the rate r between 0 (rotation stops) and the last step's rate, in degrees per unit D;
s2 = w sin^2 alpha."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = False


def alpha_of(s1, s2):
    return math.degrees(math.atan(math.sqrt(s2 / s1))) if not MUTATE else math.degrees(math.atan(math.sqrt(s1 / s2)))


def shares_of(alpha, w):
    a = math.radians(alpha)
    return w * math.cos(a) ** 2, w * math.sin(a) ** 2


def selftest():
    ok = True
    for alpha, w in ((4.0, 0.99), (27.5, 0.9922), (45.0, 1.0), (48.5, 0.9922), (80.0, 0.95)):
        s1, s2 = shares_of(alpha, w)
        got = alpha_of(s1, s2)
        good = abs(got - alpha) < 1e-12
        ok &= good
        print(f"selftest: alpha {alpha}, w {w}: shares {s1:.6f}, {s2:.6f} -> alpha {got:.12f}: {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if MUTATE else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    names = ["260.2515", "260.4708", "260.6706", "260.8483", "260.9271"] + [a for a in sys.argv[1:] if a[:1].isdigit()]
    rows = []
    for n in names:
        p = os.path.join(HERE, f"c3b_ks293_D{n}.json")
        if not os.path.exists(p):
            continue
        r = json.load(open(p))
        v = r["vectors"]
        s1, s2 = v[0]["delta"], v[1]["delta"]
        rows.append((r["D"], s1, s2, alpha_of(s1, s2), s1 + s2))
    print(f"{'D':>9} {'share v1':>9} {'share v2':>9} {'w':>7} {'alpha deg':>10} {'rate deg/D':>11}")
    for i, (D, s1, s2, a, w) in enumerate(rows):
        rate = "" if i == 0 else f"{(a - rows[i - 1][3]) / (D - rows[i - 1][0]):.1f}"
        print(f"{D:9.4f} {s1:9.4f} {s2:9.4f} {w:7.4f} {a:10.2f} {rate:>11}")
    D, s1, s2, a, w = rows[-1]
    rl = (a - rows[-2][3]) / (D - rows[-2][0])
    a90 = math.degrees(math.asin(math.sqrt(0.9 / w)))
    print(f"item (e): share of v2 >= 0.9 needs alpha >= {a90:.1f} degrees (w {w:.4f}); last step's rate {rl:.1f} deg/D reaches it {(a90 - a) / rl:.2f} of D past D {D:.4f} (a lower bound on the distance if the rate keeps falling)")
    print(f"forecast, registered {sys.argv[0]}: share of v2 = w sin^2(alpha), alpha = {a:.2f} + r (D - {D:.4f}), r between 0 and {rl:.1f} deg/D")
    print(f"{'D':>9} {'v2 share, r=0':>14} {'v2 share, r=last/2':>19} {'v2 share, r=last':>17}")
    for dn in (261.0, 261.05, 261.1, 261.2, 261.4, 261.6):
        f = [shares_of(a + r * (dn - D), w)[1] for r in (0.0, rl / 2, rl)]
        print(f"{dn:9.4f} {f[0]:14.3f} {f[1]:19.3f} {f[2]:17.3f}")


if __name__ == "__main__":
    MUTATE = "--mutate" in sys.argv
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    main()
