#!/usr/bin/env python3
"""#1025 kc79_d19low (dh610) control_check.py LOG ROW.jsonl REF.jsonl LAM | selftest [--mutate]: the k_c 79 control at D 19.0, lambda 1.54 on this machine's build against winb's row
(I1025-win/kc79_d19/scan_kc79_D19_1025.jsonl, a Windows build, copied as in/ref_winb_scan_kc79_D19_1025.jsonl, blob 321fb621). Passes (exit 0) only if the log prints 'the record system' (not 'NOT the record system'),
the hybrid sign equals winb's (any sign) and ln|det| equals winb's to 1e-6 relative. Exit 1 otherwise.
selftest: a planted agreeing row must pass, for a + and a - reference; a not-the-record-system log, a sign flip (both ways) and a ln|det| shift of 1e-5 relative must each fail. --mutate raises the ln bar to 1e-3, which the shifted case must then fail to catch (exit 1)."""
import sys, json

BAR = 1e-6


def check(log, row, ref, bar=BAR):
    ok_sys = "the record system" in log and "NOT the record system" not in log
    d = abs(row["ln"] - ref["ln"]) / abs(ref["ln"])
    ok = ok_sys and row["sign"] == ref["sign"] and d <= bar
    return ok, f"record system {ok_sys}, sign {row['sign']:+.0f} (winb {ref['sign']:+.0f}), ln|det| {row['ln']:.10f} (winb {ref['ln']:.10f}), relative difference {d:.3e} (bar {bar:g}), noise_robust {row.get('noise_robust')}, float64 ln {row.get('f64_ln')} (winb {ref.get('f64_ln')})"


def selftest(mutate):
    bar = 1e-3 if mutate else BAR
    ref = dict(sign=-1.0, ln=-2547.786620251229, f64_ln=-2544.7945061324563)
    refm = dict(ref, sign=1.0)
    good = dict(ref, noise_robust=True)
    cases = [("agreeing, - reference", "D 19.0: the record system", good, ref, True),
             ("agreeing, + reference", "D 19.0: the record system", dict(good, sign=1.0), refm, True),
             ("not the record system", "D 19.0: NOT the record system", good, ref, False),
             ("a sign flip (- reference)", "D 19.0: the record system", dict(good, sign=1.0), ref, False),
             ("a sign flip (+ reference)", "D 19.0: the record system", good, refm, False),
             ("ln shift 1e-5 relative", "D 19.0: the record system", dict(good, ln=ref["ln"] * (1 + 1e-5)), ref, False)]
    bad = 0
    for name, log, row, rf, want in cases:
        got, msg = check(log, row, rf, bar)
        ok = got == want
        bad += not ok
        print(f"  {name}: {'pass' if got else 'fail'} (expected {'pass' if want else 'fail'}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    log, rowf, reff, lam = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
    pick = lambda f: [json.loads(l) for l in open(f) if l.strip() and json.loads(l)["lam"] == lam][-1]
    ok, msg = check(open(log).read(), pick(rowf), pick(reff))
    print(("PASS: " if ok else "FAIL: ") + msg)
    sys.exit(0 if ok else 1)
