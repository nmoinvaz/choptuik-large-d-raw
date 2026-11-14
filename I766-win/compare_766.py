#!/usr/bin/env python3
"""#766: |Delta(M 64) - Delta(M 48)| at D 7.0 and 8.2 against the errs delta_all.csv gives those rows (#764's dM
neighbours rule). Delta is the double-double sum of a state's last entries (zh + zl), mpmath at 120 bits.
    python -I compare_766.py RAW          exit 0 when both differences lie within their errs, 1 otherwise
    python -I compare_766.py --selftest   the test on planted differences; exit 0
A difference above its err means the rule underestimates there, which is a result to report, not a failure of the run."""
import os
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 120
ERR = {"7.0000": 3.0e-14, "8.2000": 9.5e-21}


def delta(p):
    d = np.load(p, allow_pickle=False)
    return mp.mpf(float(d["zh"][-1])) + mp.mpf(float(d["zl"][-1]))


def within(diff, err):
    return abs(diff) <= err


def main(raw):
    ok = True
    print("| D | Delta(48) | Delta(64) - Delta(48) | err | within |\n|---|---|---|---|---|")
    for D, err in ERR.items():
        a, b = os.path.join(raw, "T79-win", f"down_D{D}.npz"), os.path.join(raw, "I766-win", f"m64_D{D}.npz")
        if not os.path.exists(b):
            print(f"| {D} | | not run | {err:.1e} | |")
            ok = False
            continue
        d48, d64 = delta(a), delta(b)
        w = within(float(d64 - d48), err)
        ok &= w
        print(f"| {D} | {mp.nstr(d48, 18)} | {mp.nstr(d64 - d48, 4)} | {err:.1e} | {'yes' if w else 'NO'} |")
    return 0 if ok else 1


def selftest():
    cases = [(2.9e-14, 3.0e-14, True), (3.1e-14, 3.0e-14, False), (-1e-20, 9.5e-21, False), (5e-21, 9.5e-21, True)]
    bad = sum(within(d, e) != w for d, e, w in cases)
    print("selftest", "passed" if not bad else f"FAILED ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1]) if len(sys.argv) == 2 else __doc__)
