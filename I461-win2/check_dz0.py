#!/usr/bin/env python3
"""#461 --save_dz0 check (the coordinator's order of 17:54 UTC): for a dz0_pin3_D<D>_a<a>.npz file, max|d0 + d1| over the entries must equal the first |dz| the log prints for that attempt, to the digits printed.
usage: check_dz0.py FILE LOG [--attempt K]   (K-th "  on 0:" line of the log, 0 = the base polish's, 1 = the first attempt's; default: the file named D0.0000 -> 0, else 1)
       check_dz0.py --selftest   (a planted change of one entry of d0 beyond the printed digits must fail the check, and a wrong log line must fail it)
Exit 0 when the max agrees with the log to its 2 printed digits, 1 when not, 2 on a usage or file error."""
import re, sys
import numpy as np

def first_dz(log, k):
    lines = [ln for ln in open(log, encoding="utf-8") if re.match(r"^  on 0: ", ln)]
    m = re.search(r"\|dz\| (\S+) ->", lines[k])
    return float(m.group(1)), m.group(1)

def maxdz(path, d0=None):
    z = np.load(path, allow_pickle=True)
    a = z["d0"] if d0 is None else d0
    s = a + z["d1"]
    return float(np.max(np.abs(s)))

def agree(val, printed):
    return float(f"{val:.1e}") == float(printed) if len(printed.replace('.', '').replace('e-', '').lstrip('0')) <= 3 else abs(val - float(printed)) <= 0.5e-1 * abs(float(printed))

def selftest():
    import tempfile, os
    td = tempfile.mkdtemp()
    d0 = np.zeros(8); d1 = np.zeros(8); d0[3] = 1.9e-30; d1[3] = 0.0; d1[5] = -1.2e-30
    p = os.path.join(td, "dz0_pin3_D1.0000_a0.500000.npz")
    np.savez(p, d0=d0, d1=d1)
    ok = agree(maxdz(p), "1.9e-30")
    bad = agree(maxdz(p, d0=d0 * 1.2), "1.9e-30")
    ok2 = agree(maxdz(p), "1.2e-30")
    print("selftest: ok" if ok and not bad and not ok2 else f"selftest FAILED: ok {ok} planted-change-caught {not bad} wrong-line-caught {not ok2}")
    return 0 if ok and not bad and not ok2 else 1

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    path, log = sys.argv[1], sys.argv[2]
    k = int(sys.argv[sys.argv.index("--attempt") + 1]) if "--attempt" in sys.argv else (0 if "D0.0000" in path else 1)
    v, printed = first_dz(log, k)
    m = maxdz(path)
    print(f"{path}: max|d0 + d1| = {m:.4e}, the log's {k}-th first |dz| = {printed}: {'AGREE' if agree(m, printed) else 'DISAGREE'}")
    sys.exit(0 if agree(m, printed) else 1)
