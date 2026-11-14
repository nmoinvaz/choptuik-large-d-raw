#!/usr/bin/env python3
"""#796: the table of the order-132 climb from w = 1/2 to 1 at D 245.1366 (#783's table, the rungs changed).
    python -I table_796.py FOLDER       (FOLDER: I796-win2; its parent is the raw clone)
    python -I table_796.py --selftest
Per rung (w25 from I744-win2, then w3125, w375, w4375, w5b where run): Newton steps, final max|F| and converged, from
the log's last "octo-double Newton" line; Delta - Delta(w25), Delta the exact sum of the saved base's eight parts
(mpmath, 600 bits); the failed projections from the log's last "elim projections" line. A rung without a base is listed
as not run or not saved."""
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 600
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
RUNGS = [("w625", 0.625), ("w75", 0.75), ("w875", 0.875), ("w1", 1.0), ("cold1", 1.0)]


def delta(path):
    d = np.load(path, allow_pickle=False)
    return mp.fsum(mp.mpf(float(d[k][-1])) for k in KEYS if k in d.files)


def base(folder):
    names = [f for f in os.listdir(folder) if f.startswith("base_pin3_D") and f.endswith(".npz")] if os.path.isdir(folder) else []
    return os.path.join(folder, sorted(names)[0]) if names else None


def newton_line(line):
    m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan), (not converged|converged)", line)
    return (int(m.group(1)), m.group(2), m.group(3) == "converged") if m else None


def last(log, pat):
    if not os.path.exists(log):
        return None
    hits = [s.strip() for s in open(log, encoding="utf-8", errors="replace") if re.search(pat, s)]
    return hits[-1] if hits else None


def main(folder):
    raw = os.path.dirname(os.path.abspath(folder))
    b25 = base(os.path.join(raw, "I744-win2", "w25"))
    d25 = delta(b25)
    d0 = delta(base(os.path.join(raw, "I744-win2", "w0")))
    d5 = delta(base(os.path.join(raw, "I783-win2", "w5b")))
    print(f"Delta(w25) - Delta(w0) {mp.nstr(d25 - d0, 4)}; Delta(w5b) - Delta(w0) {mp.nstr(d5 - d0, 4)}\n")
    print("| rung | w | Newton steps | final max\\|F\\| | converged | Delta - Delta(w25) | elim projections |")
    print("|---|---|---|---|---|---|---|")
    print(f"| w25 (#744) | 0.25 | | | yes | 0 | |")
    for tag, w in RUNGS:
        log = os.path.join(folder, f"{tag}.log")
        nl = last(log, r"octo-double Newton: \d+ steps")
        nw = newton_line(nl) if nl else None
        if nw is None:
            continue
        b = base(os.path.join(folder, tag))
        dd = (f"{mp.nstr(delta(b) - d25, 4)} (from w0 {mp.nstr(delta(b) - d0, 4)})") if b and nw[2] else "no converged base"
        ep = last(log, r"elim projections") or ""
        ep = ep.split("elim projections", 1)[1].strip(" :") if ep else ""
        print(f"| {tag} | {w} | {nw[0]} | {nw[1]} | {'yes' if nw[2] else 'NO'} | {dd} | {ep} |")
    return 0


def selftest():
    ln = "  octo-double Newton: 5 steps, max|F| 8.2e-76, converged; double-double |F| of its first two parts 1.0e+06"
    cases = [(newton_line(ln), (5, "8.2e-76", True)),
             (newton_line(ln.replace(", converged", ", not converged"))[2], False),
             (newton_line("no such line"), None)]
    bad = sum(got != want for got, want in cases)
    print("selftest", "passed" if not bad else f"FAILED ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
