"""Delta minus Track C for every step line of a lastnode.log, from the log's own digits (mpmath, 50 digits).
    python3 diff_trackc.py lastnode.log 1.64441243858130260
"""
import re
import sys

import mpmath as mp

mp.mp.dps = 50
log, tc = sys.argv[1], mp.mpf(sys.argv[2])
for line in open(log):
    m = re.search(r"^\s+it (\d+)( \(chord\))?: .*Delta (1\.\d+)$", line.rstrip("\n"))
    if m:
        print(f"it {m.group(1)}{m.group(2) or ''}: Delta {m.group(3)[:24]}  - Track C = {mp.nstr(mp.mpf(m.group(3)) - tc, 5)}")
