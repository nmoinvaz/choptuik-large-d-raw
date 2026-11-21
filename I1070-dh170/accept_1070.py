#!/usr/bin/env python3
"""accept_1070.py RECORD.jsonl | --selftest [--mutate]: the issue's acceptance (#1070) for one run's record: exactly one sign change in the bracket (n_signchanges 1) and F after the polish below 1e-27.
Prints PASS or FAIL with the numbers; exit 0 on PASS. --selftest: planted records (the passing one and four broken ones: no sign change, two sign changes, F 1e-26, F missing) must give the verdicts written here;
--mutate loosens the F bar to 1e-20 and the selftest must then fail."""
import json
import sys

FBAR = 1e-27


def verdict(rec, fbar=FBAR):
    n, F = rec.get("n_signchanges"), rec.get("F")
    ok = (n == 1) and F is not None and F < fbar
    return ok, f"n_signchanges {n}, F after the polish {F}, lam {rec.get('lam')}, gamma {rec.get('gamma')}"


def selftest(mutate):
    fbar = 1e-20 if mutate else FBAR
    cases = [(dict(n_signchanges=1, F=1.1e-28, lam=4.4, gamma=0.227), True), (dict(n_signchanges=0, F=1.1e-28, lam=None, gamma=None), False), (dict(n_signchanges=2, F=1.1e-28, lam=4.4, gamma=0.227), False),
             (dict(n_signchanges=1, F=1e-26, lam=4.4, gamma=0.227), False), (dict(n_signchanges=1, F=None, lam=4.4, gamma=0.227), False)]
    ok = True
    for rec, want in cases:
        got, msg = verdict(rec, fbar)
        print(f"selftest: {'pass' if got == want else 'FAIL'}: want {want}, got {got}: {msg}")
        ok &= (got == want)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    if not recs:
        print("FAIL: no record")
        sys.exit(1)
    ok, msg = verdict(recs[-1])
    print(("PASS: " if ok else "FAIL: ") + msg)
    sys.exit(0 if ok else 1)
