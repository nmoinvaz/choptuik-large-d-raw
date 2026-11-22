#!/usr/bin/env python3
"""#1025 kc79_d19125low (dh170) control_check_k79.py LOG ROW.jsonl REF.jsonl LAM | selftest [--mutate]: the k_c 79 control at D 19.125, lambda 1.50, this run against dh370's row
(I1025-dh370/kc79_d19125/scan/scan_D19.125_p0.jsonl at raw 9cd09b8a: hybrid -1, ln|det| -2537.823195774449; a Linux build on 1 thread; here a Linux build on 4 threads). Derived from dh610's control_check.py
(blob c8ef82e5, bar 1e-6) with the bar 1e-9 the order asks for. Passes (exit 0) only if the log prints 'the record system' (not 'NOT the record system'), the hybrid sign equals dh370's,
the point is noise-robust and ln|det| equals dh370's to 1e-9 relative. Exit 1 otherwise.
selftest: a planted agreeing row (a + and a - reference, and a ln shift of 5e-10 relative) must pass; a not-the-record-system log, a sign flip (both ways), a non-robust row and ln shifts of 1e-8 and 1e-5 relative
must each fail. --mutate raises the bar to 1e-6, so the 1e-8 shift passes and the selftest must exit 1."""
import sys, json

BAR = 1e-9


def check(log, row, ref, bar=BAR):
    ok_sys = "the record system" in log and "NOT the record system" not in log
    d = abs(row["ln"] - ref["ln"]) / abs(ref["ln"])
    ok = ok_sys and row["sign"] == ref["sign"] and row.get("noise_robust", False) and d <= bar
    return ok, (f"record system {ok_sys}, sign {row['sign']:+.0f} (dh370 {ref['sign']:+.0f}), ln|det| {row['ln']:.10f} (dh370 {ref['ln']:.10f}), "
                f"relative difference {d:.3e} (bar {bar:g}), noise_robust {row.get('noise_robust')}, float64 ln {row.get('f64_ln')} (dh370 {ref.get('f64_ln')})")


def selftest(mutate):
    bar = 1e-6 if mutate else BAR
    ref = dict(sign=-1.0, ln=-2537.823195774449, f64_ln=-2536.0)
    refp = dict(ref, sign=1.0)
    good = dict(ref, noise_robust=True)
    ok_log, bad_log = "D 19.125: the record system", "D 19.125: NOT the record system"
    cases = [("agreeing, - reference", ok_log, good, ref, True),
             ("agreeing, + reference", ok_log, dict(good, sign=1.0), refp, True),
             ("ln shift 5e-10 relative", ok_log, dict(good, ln=ref["ln"] * (1 + 5e-10)), ref, True),
             ("not the record system", bad_log, good, ref, False),
             ("a sign flip (- reference)", ok_log, dict(good, sign=1.0), ref, False),
             ("a sign flip (+ reference)", ok_log, good, refp, False),
             ("not noise-robust", ok_log, dict(good, noise_robust=False), ref, False),
             ("ln shift 1e-8 relative", ok_log, dict(good, ln=ref["ln"] * (1 + 1e-8)), ref, False),
             ("ln shift 1e-5 relative", ok_log, dict(good, ln=ref["ln"] * (1 + 1e-5)), ref, False)]
    bad = 0
    for name, log, row, rf, want in cases:
        got, _ = check(log, row, rf, bar)
        ok = got == want
        bad += not ok
        print(f"  {name}: {'pass' if got else 'fail'} (expected {'pass' if want else 'fail'}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    log, rowf, reff, lam = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
    pick = lambda f: [json.loads(l) for l in open(f) if l.strip() and abs(json.loads(l)["lam"] - lam) < 1e-9][-1]
    ok, msg = check(open(log).read(), pick(rowf), pick(reff))
    print(("PASS: " if ok else "FAIL: ") + msg)
    sys.exit(0 if ok else 1)
