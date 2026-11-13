#!/usr/bin/env python3
"""#642: the planted control of release_held.py, #640's: the perturbed release must equal the unperturbed one, the no-release run must not.
usage: python compare_control.py [--selftest]          (from this folder; reads control_p0/release.jsonl, control_p1e-10/release.jsonl, control_p1e-10_it0/release.jsonl, last record of each)
Pass: |Delta_full(p) - Delta_full(0)| <= 1e-25 and max |coeffs_end(p) - coeffs_end(0)| <= 1e-20 for the perturbed release; and the no-release run (it_max 0) FAILS the same two tests (its coefficients stay at the
perturbation, 1e-10 off). Delta_full is the 40-digit string of the record, compared in mpmath at 80 digits; the coefficients are the floats of p1's harmonics 5, 7, 9, 11, 13 (cos, sin).
--selftest: planted records of known answer (an equal pair, a pair off by 1e-12 in Delta, a pair off by 1e-10 in one coefficient) through the same comparison."""
import json
import os
import sys

import mpmath as mp

mp.mp.dps = 80
HERE = os.path.dirname(os.path.abspath(__file__))
TOL_D, TOL_C = mp.mpf("1e-25"), 1e-20


def last(path):
    return [json.loads(ln) for ln in open(path) if ln.strip()][-1]


def compare(a, b):
    """(|dDelta|, max |dcoeff|) between the ends of two records."""
    dd = abs(mp.mpf(a["Delta_full"]) - mp.mpf(b["Delta_full"]))
    dc = max(abs(x - y) for ca, cb in zip(a["coeffs_end"], b["coeffs_end"]) for x, y in zip(ca, cb))
    return dd, dc


def passes(dd, dc):
    return dd <= TOL_D and dc <= TOL_C


def selftest():
    base = dict(Delta_full="1.8" + "0" * 38, coeffs_end=[[1e-3, 2e-3], [3e-4, 4e-4]])
    equal = dict(base)
    off_d = dict(base, Delta_full="1.8" + "0" * 10 + "1" + "0" * 27)         # 1e-12 away in Delta (the 12th decimal)
    off_c = dict(base, coeffs_end=[[1e-3 + 1e-10, 2e-3], [3e-4, 4e-4]])       # 1e-10 away in one coefficient
    bad = 0
    for name, other, want in (("equal", equal, True), ("Delta off by 1e-12", off_d, False), ("one coefficient off by 1e-10", off_c, False)):
        dd, dc = compare(other, base)
        got = passes(dd, dc)
        print(f"  planted '{name}': |dDelta| {mp.nstr(dd, 3)}, max|dcoeff| {dc:.2e} -> {'pass' if got else 'fail'} (expected {'pass' if want else 'fail'}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    r0, r1, r2 = (last(os.path.join(HERE, d, "release.jsonl")) for d in ("control_p0", "control_p1e-10", "control_p1e-10_it0"))
    print(f"unperturbed release: Delta_full {r0['Delta_full']}, |F| {r0['F']:.2e} after {r0['steps']} steps, ok {r0['ok']}, Delta change {r0['diff']:+.3e}")
    print(f"perturbed release (1e-10): Delta_full {r1['Delta_full']}, |F| {r1['F']:.2e} after {r1['steps']} steps, ok {r1['ok']}, Delta change {r1['diff']:+.3e}")
    print(f"no release (it_max 0): Delta_full {r2['Delta_full']}, |F| {r2['F']:.2e}, steps {r2['steps']}")
    d1, c1 = compare(r1, r0)
    d2, c2 = compare(r2, r0)
    p1, p2 = passes(d1, c1), passes(d2, c2)
    print(f"perturbed release against unperturbed: |dDelta| {mp.nstr(d1, 3)} (<= 1e-25), max|dcoeff| {c1:.2e} (<= 1e-20) -> {'pass' if p1 else 'FAIL'}")
    print(f"no release against unperturbed:        |dDelta| {mp.nstr(d2, 3)}, max|dcoeff| {c2:.2e} -> {'passes the tests (the control is blind)' if p2 else 'fails them, as it must'}")
    ok = p1 and not p2
    print(f"CONTROL {'PASSED' if ok else 'FAILED'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
