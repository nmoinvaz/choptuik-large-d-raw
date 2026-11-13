#!/usr/bin/env python3
"""#597: the smoothness table, old build against new, from smooth/{old,new}_<case>.log, with #609 / #612's counts
(macm3, the old crate built from 742bb879's source) beside them. Asserts that each case's two logs are byte for byte
equal when --same is given (exit 1 otherwise).

    python3 table597.py [--same] [--mutate]

--mutate, the control of --same: the control case's old log is replaced by smooth/new_mutate_lo_D30_M32_phys.log, so
--same must exit 1.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# #609 / #612 (I609-macm3, I612-macm3): count of non-linear entries
MACM3 = {"ctrl_D30_M32_phys": 1, "D30_M40_phys": 830, "D30_M48_phys": 3921, "D30_M64_phys": 57,
         "D30_M80_phys": 20539, "D61_M64_s3": 55821, "D30_M64_pos1": 4979, "D30_M80_pos1": 46073}


def read(path):
    t = open(path).read()
    ch = int(re.search(r"entries changed by one ulp (\d+)", t).group(1))
    nl = int(re.search(r"entries with \|d2 - 2 d1\| > \|d1\|/2: (\d+)", t).group(1))
    rows = re.search(r"their rows by block of 4M: \[([^\]]*)\]", t)
    blocks = [int(x) for x in rows.group(1).split()] if rows else []
    big = re.search(r"largest: row (\d+), col (\d+): \|A\| ([^,]+), \|d1\| ([^,]+),", t)
    return ch, nl, blocks, big, t


bad = 0
print("| case | changed | old (here) | new | share | first / last block (new) | largest abs(d1)/abs(A) (new) | "
      "#609/#612 (macm3) | logs old = new |")
print("|---|---|---|---|---|---|---|---|---|")
for case, ref in MACM3.items():
    o, n = (os.path.join(HERE, "smooth", f"{b}_{case}.log") for b in ("old", "new"))
    if "--mutate" in sys.argv and case == "ctrl_D30_M32_phys":
        o = os.path.join(HERE, "smooth", "new_mutate_lo_D30_M32_phys.log")
    ch, nl, blocks, big, tn = read(n)
    cho, nlo, _, _, to = read(o)
    same = tn == to
    bad += not same
    rel = float(big.group(4)) / float(big.group(3)) if big else 0.0
    print(f"| {case} | {ch} | {nlo} | {nl} | {100 * nl / ch:.3g}% | {blocks[0] if blocks else 0} / "
          f"{blocks[-1] if len(blocks) > 1 else 0} | {rel:.1e} | {ref} | {'yes' if same else 'NO'} |")
if "--same" in sys.argv and bad:
    sys.exit(f"{bad} cases whose old and new logs differ")
