"""Delta's change per accepted outer step and per harmonic from rls.log's own digits (mpmath, 50 digits).
    python3 diff_delta.py rls.log
"""
import re
import sys

import mpmath as mp

mp.mp.dps = 50
prev = start = None
rel = {}
for line in open(sys.argv[1]):
    m = re.match(r"release_ls from .*Delta (1\.\d+),", line)
    if m:
        prev = start = mp.mpf(m.group(1))
        print(f"start Delta {m.group(1)[:30]}")
    m = re.match(r"  h(\d+) outer (\d+): target .*Delta (1\.\d+) \(", line)
    if m and prev is not None:
        k, d = int(m.group(1)), mp.mpf(m.group(3))
        print(f"h{k} outer {m.group(2)}: change {mp.nstr(d - prev, 5)}   (cumulative {mp.nstr(d - start, 5)})")
        prev = d
