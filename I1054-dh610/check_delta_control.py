#!/usr/bin/env python3
"""check_delta_control.py A.npz B.npz LOG [--mutate]: control of exact_recip_check.py delta before job 5's real deltas. 'delta A A' must print Delta(b) - Delta(a) = 0 and
'delta A B' must give Delta(B) - Delta(A) equal, to 1e-30, to the difference of the two 'Delta of the saved state, its eight parts summed exactly' lines of LOG (anm_run.py's
own sum of the saved parts, mpmath at 600 bits here). Exit 0 when both hold, 1 when not, 2 on an unreadable input. --mutate: the log's second value moved by 1e-20, which must exit 1."""
import json
import re
import subprocess
import sys
import mpmath as mp

mp.mp.prec = 600
a, b, log = sys.argv[1:4]
mutate = "--mutate" in sys.argv
vals = re.findall(r"Delta of the saved state, its eight parts summed exactly: (\S+)", open(log).read())
if len(vals) < 2:
    print("fewer than two 'Delta of the saved state' lines in", log)
    sys.exit(2)
want = mp.mpf(vals[1]) - mp.mpf(vals[0]) + (mp.mpf("1e-20") if mutate else 0)


def delta(x, y, out):
    r = subprocess.run([sys.executable, "exact_recip_check.py", "delta", x, y, "--out", out], capture_output=True, text=True)
    if r.returncode not in (0, 1):
        print(r.stdout, r.stderr)
        sys.exit(2)
    j = json.load(open(out))
    return mp.mpf(j["Delta_b"]) - mp.mpf(j["Delta_a"]), j


d0, j0 = delta(a, a, out=log + ".aa.json")
d1, j1 = delta(a, b, out=log + ".ab.json")
ok0 = d0 == 0
ok1 = abs(d1 - want) <= mp.mpf("1e-30")
print(f"delta A A: Delta(b) - Delta(a) = {mp.nstr(d0, 6)} (must be 0): {'ok' if ok0 else 'FAIL'}")
print(f"delta A B: {mp.nstr(d1, 20)} against the log's sums {mp.nstr(want, 20)}{' (--mutate, moved by 1e-20)' if mutate else ''}: difference {mp.nstr(d1 - want, 3)} (bound 1e-30): {'ok' if ok1 else 'FAIL'}")
sys.exit(0 if ok0 and ok1 else 1)
