#!/usr/bin/env python3
"""#775: |Delta(M 64) - Delta(M 48)| at each lowD-M48-unresolved row against the err delta_all.csv gives it (#764's dM
neighbours rule), with #766's D 7.0 and 8.2 read from I766-win. Delta is the double-double sum of a state's last entries.
    python -I compare_775.py RAW DELTA_ALL.csv     exit 0 when every err covers its difference, 1 otherwise
    python -I compare_775.py --selftest            the match of a state's D to a row's D, and the within test
A row whose err does not cover its difference is a result (the rule underestimates there), not a failure of the run."""
import csv
import glob
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 120


def delta(p):
    d = np.load(p, allow_pickle=False)
    return mp.mpf(float(d["zh"][-1])) + mp.mpf(float(d["zl"][-1]))


def row_for(D, rows):
    """the delta_all row whose D matches the state's 4-decimal D to 5e-5"""
    m = [r for r in rows if abs(float(r["D"]) - D) < 5e-5]
    return m[0] if len(m) == 1 else None


def main(raw, csvp):
    rows = [r for r in csv.DictReader(open(csvp)) if r["source"].endswith("lowD-M48-unresolved")]
    ok, n, under = True, 0, 0
    print("| D | Delta(64) - Delta(48) | err (kind) | within | ratio |\n|---|---|---|---|---|")
    for p in sorted(glob.glob(os.path.join(raw, "I775-win", "m64_D*.npz")) + glob.glob(os.path.join(raw, "I766-win", "m64_D*.npz"))):
        tag = re.search(r"m64_D([0-9.]+)\.npz$", p).group(1)
        r = row_for(float(tag), rows)
        if r is None:
            print(f"| {tag} | no unique row | | | |")
            ok = False
            continue
        d = float(delta(p) - delta(os.path.join(raw, "T79-win", f"down_D{tag}.npz")))
        err = float(r["err"])
        w = abs(d) <= err
        n += 1
        under += not w
        ok &= w
        print(f"| {r['D']} | {d:+.3e} | {err:.1e} ({r['err_kind']}) | {'yes' if w else 'NO'} | {abs(d) / err:.2g} |")
    print(f"\n{n} rows; the err understates the difference at {under}")
    return 0 if ok else 1


def selftest():
    rows = [{"D": "7.559265"}, {"D": "7.87793"}, {"D": "8.2"}]
    cases = [(row_for(7.5593, rows) is rows[0], True), (row_for(7.8779, rows) is rows[1], True),
             (row_for(8.2000, rows) is rows[2], True), (row_for(7.6, rows) is None, True)]
    bad = sum(got != want for got, want in cases)
    print("selftest", "passed" if not bad else f"FAILED ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else __doc__)
