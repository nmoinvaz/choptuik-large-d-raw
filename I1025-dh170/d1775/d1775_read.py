#!/usr/bin/env python3
"""#1025 D 17.75 (coordinator's hc, 21 Nov): the reading of the hybrid sign scan, as the coordinator fixed it: count the robust sign changes and bracket each; two changes mean the second eigenvalue is present at D 17.75 too.

    d1775_read.py SCAN.jsonl            the sign sequence (lam, sign, noise test, float64 sign), the robust changes with their brackets and orientation, the points whose sign is not noise-robust,
                                        the points where the float64 sign differs from the hybrid's, and the reading
    d1775_read.py --selftest [--mutate] planted scans: -,-,-,+,+,+,-,- all robust -> 2 changes with the right brackets and orientations; the same with a non-robust point at one change -> that change is
                                        not counted (1); one change only -> 1; no change -> 0; --mutate counts a non-robust neighbour as robust and must fail

A sign change counts when the two neighbouring grid points both have noise_robust true (p4_hybrid's 1e-15 noise test, 2 seeds, leaves the hybrid sign unchanged). Records are d18_hybsign.py's jsonl lines."""
import json
import sys

ROBUST_ONLY = True                                   # --mutate: a change counts whether or not its neighbours are noise-robust


def analyse(recs):
    L = sorted(recs, key=lambda r: r["lam"])
    ch, uncounted = [], []
    for a, b in zip(L, L[1:]):
        if a["sign"] != b["sign"]:
            (ch if (not ROBUST_ONLY) or (a["noise_robust"] and b["noise_robust"]) else uncounted).append(
                (a["lam"], b["lam"], "+ to -" if a["sign"] > 0 else "- to +"))
    nonrob = [r["lam"] for r in L if not r["noise_robust"]]
    f64 = [(r["lam"], r["sign"], r["f64_sign"]) for r in L if r["f64_sign"] != r["sign"]]
    return L, ch, uncounted, nonrob, f64


def reading(n):
    return {0: "no robust sign change in the scanned range", 1: "one robust sign change: only one eigenvalue crosses in the range"}.get(
        n, f"{n} robust sign changes: the second eigenvalue is present at D 17.75 too" if n == 2 else f"{n} robust sign changes (more than two: reported as they are)")


def report(recs):
    L, ch, uncounted, nonrob, f64 = analyse(recs)
    print("lam    hybrid sign  noise-robust  float64 sign  ln|det|")
    for r in L:
        print(f"{r['lam']:.2f}   {r['sign']:+.0f}          {str(r['noise_robust']):5s}         {r['f64_sign']:+.0f}            {r['ln']:.6f}")
    print("signs:", " ".join(f"{r['lam']:.2f}{'+' if r['sign'] > 0 else '-'}" for r in L))
    print("robust sign changes:", len(ch), [(round(a, 2), round(b, 2), o) for a, b, o in ch])
    print("sign changes not counted (a non-robust neighbour):", [(round(a, 2), round(b, 2), o) for a, b, o in uncounted] or "none")
    print("points not noise-robust:", [round(x, 2) for x in nonrob] or "none")
    print("points where the float64 sign differs from the hybrid's:", [(round(a, 2), int(s), int(f)) for a, s, f in f64] or "none")
    print("READING:", reading(len(ch)))
    return len(ch)


def selftest(mutate):
    global ROBUST_ONLY
    ROBUST_ONLY = not mutate
    lam = [1.70 + 0.01 * i for i in range(8)]

    def mk(signs, nonrob=()):
        return [dict(lam=l, sign=float(s), ln=-1900.0, noise_robust=(i not in nonrob), f64_sign=float(s)) for i, (l, s) in enumerate(zip(lam, signs))]
    ok = True
    cases = [("two changes, all robust", mk([-1, -1, -1, 1, 1, 1, -1, -1]), 2, [(1.72, 1.73, "- to +"), (1.75, 1.76, "+ to -")]),
             ("two changes, a non-robust point at the second", mk([-1, -1, -1, 1, 1, 1, -1, -1], nonrob=(6,)), 1, [(1.72, 1.73, "- to +")]),
             ("one change", mk([1, 1, 1, 1, -1, -1, -1, -1]), 1, [(1.73, 1.74, "+ to -")]),
             ("no change", mk([1] * 8), 0, [])]
    for label, recs, want_n, want_b in cases:
        L, ch, un, nr, f = analyse(recs)
        got_b = [(round(a, 2), round(b, 2), o) for a, b, o in ch]
        good = len(ch) == want_n and got_b == want_b
        ok &= good
        print(f"selftest: {label}: {len(ch)} change(s) {got_b} (want {want_n} {want_b}): {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    report(recs)
