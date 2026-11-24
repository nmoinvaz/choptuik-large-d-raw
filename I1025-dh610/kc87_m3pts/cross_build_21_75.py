#!/usr/bin/env python3
"""#1025 kc87_m3pts (dh610) cross_build_21_75.py [selftest [--mutate]]: macm3's macOS scan rows of the k_c 87 state at D 21.75 (21.75/macm3_scan_D21.75_1025.jsonl, a copy of I1025-macm3/kc87_leg_lambda/21.75/scan/scan_D21.75_1025.jsonl)
beside this lane's Linux rows (21.75/scan/scan_D21.75_all.jsonl): ln|det| per lambda, the hybrid and float64 signs, and the det-linear root of the sign change from each side to 10 digits (linear interpolation of the signed
determinants between the two grid points, with |det| ratios from the ln values: root = l1 + (l2 - l1) a / (a + b), a = |det(l1)|, b = |det(l2)|). Run from this folder: python3 -I cross_build_21_75.py > 21.75/cross_build_21_75.txt
selftest: planted ln values with the root known (a = b gives the midpoint); --mutate swaps the weights, the selftest exits 1."""
import json, math, sys


def root(l1, l2, ln1, ln2, mutate=False):
    r = math.exp(ln1 - ln2)  # a / b
    w = r / (1 + r)
    if mutate:
        w = 1 - w
    return l1 + (l2 - l1) * w


def selftest(mutate):
    ok = abs(root(0.645, 0.650, -10.0, -10.0, mutate) - 0.6475) < 1e-12 and abs(root(0.0, 1.0, -1.0, -1.0 - math.log(3), mutate) - 0.75) < 1e-12
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def rows(path):
    d = {}
    for l in open(path):
        if l.strip():
            r = json.loads(l)
            d.setdefault(round(r["lam"], 3), r)
    return d


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    m, L = rows("21.75/macm3_scan_D21.75_1025.jsonl"), rows("21.75/scan/scan_D21.75_all.jsonl")
    lams = sorted(set(m) & set(L))
    print("| lambda | ln abs det, macm3 (macOS) | ln abs det, Linux | Linux - macm3 | hybrid sign m / L | float64 sign m / L |")
    print("|---|---|---|---|---|---|")
    for lam in lams:
        a, b = m[lam], L[lam]
        print(f"| {lam:.3f} | {a['ln']!r} | {b['ln']!r} | {b['ln'] - a['ln']:+.3e} | {a['sign']:+.0f} / {b['sign']:+.0f} | {a['f64_sign']:+.0f} / {b['f64_sign']:+.0f} |")
    ch = [(x, y) for x, y in zip(lams, lams[1:]) if m[x]["sign"] != m[y]["sign"]]
    chL = [(x, y) for x, y in zip(lams, lams[1:]) if L[x]["sign"] != L[y]["sign"]]
    print(f"\nhybrid sign changes: macm3 {ch}, Linux {chL}; same: {ch == chL}")
    for (x, y) in ch:
        rm, rl = root(x, y, m[x]["ln"], m[y]["ln"]), root(x, y, L[x]["ln"], L[y]["ln"])
        print(f"det-linear root in ({x}, {y}): macm3 {rm:.10f}, Linux {rl:.10f}, Linux - macm3 {rl - rm:+.3e}")
