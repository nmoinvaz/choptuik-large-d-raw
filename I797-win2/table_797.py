#!/usr/bin/env python3
"""#797: the order-132 climb's rungs 13/32 and 15/32 at D 245.1366 beside #783's (#783's table).
    python -I table_797.py FOLDER       (FOLDER: I797-win2; its parent is the raw clone)
    python -I table_797.py --selftest
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
RUNGS = [("w375", 0.375), ("w40625", 0.40625), ("w4375", 0.4375), ("w46875", 0.46875), ("w5b", 0.5)]
OLD = {"w375", "w4375", "w5b"}   # #783's rungs, read from I783-win2


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
    print("| rung | w | Newton steps | final max\\|F\\| | converged | Delta - Delta(w25) | elim projections |")
    print("|---|---|---|---|---|---|---|")
    print(f"| w25 (#744) | 0.25 | | | yes | 0 | |")
    for tag, w in RUNGS:
        here = os.path.join(raw, "I783-win2") if tag in OLD else folder
        log = os.path.join(here, f"{tag}.log")
        nl = last(log, r"octo-double Newton: \d+ steps")
        nw = newton_line(nl) if nl else None
        if nw is None:
            continue
        b = base(os.path.join(here, tag))
        dd = mp.nstr(delta(b) - d25, 4) if b and nw[2] else "no converged base"
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
