#!/usr/bin/env python3
"""#603's control: at D 235.13125 the chain's Delta (the last entry of the eight parts of its saved state, summed exactly in mpmath) must lie 3.5313e-12 below the table's crawlI row
(hp/data/delta_all.csv, Delta_q0..q3 summed), within 1e-14. #595 measured that shift from the double-double projector's rows to the exact ones.
usage: python control_603.py STATE.npz DELTA_ALL.csv [--D 235.13125] [--shift -3.5313e-12] [--tol 1e-14]
       python control_603.py --selftest STATE_AT_D225.npz DELTA_ALL.csv     the start state against the table's D 225.13125 row with the D 235 shift: it must FAIL (the shift there is -7.8e-16)
exit 0 when the control passes, 1 when it fails."""
import csv, json, sys
import numpy as np
from mpmath import mp, mpf
mp.dps = 60


def delta(path):
    z = np.load(path)
    parts = [k for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in z.files]
    return sum((mpf(float(z[k][-1])) for k in parts), mpf(0)), json.loads(str(z["meta"]))["D"]


def table(csvp, D):
    row = [r for r in csv.DictReader(open(csvp)) if abs(float(r["D"]) - D) < 1e-9][0]
    return sum((mpf(float(row[k])) for k in ("Delta_q0", "Delta_q1", "Delta_q2", "Delta_q3") if row[k] != ""), mpf(0)), row


def arg(name, default):
    return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


args = [a for a in sys.argv[1:] if not a.startswith("--") and a.replace(".", "").replace("-", "").replace("e", "").replace("+", "").isdigit() is False]
selftest = "--selftest" in sys.argv
files = [a for a in sys.argv[1:] if a.endswith(".npz") or a.endswith(".csv")]
state, csvp = files[0], files[1]
shift, tol = arg("--shift", -3.5313e-12), arg("--tol", 1e-14)
d, D = delta(state)
D_tab = D if selftest else arg("--D", 235.13125)
t, row = table(csvp, D_tab)
diff = d - t
err = diff - mpf(shift)
print(f"state D {D}: Delta {mp.nstr(d, 30)}")
print(f"table D {D_tab} ({row['kind']}, source {row['source']}): Delta {mp.nstr(t, 30)}")
print(f"chain - table = {mp.nstr(diff, 8)}; expected {shift:+.4e} +- {tol:.0e}; deviation from the expected shift {mp.nstr(err, 4)}")
ok = abs(err) <= tol
print("CONTROL " + ("PASSES" if ok else "FAILS"))
if selftest:
    print("selftest: the control is expected to FAIL here" + (" and does" if not ok else " but PASSES (the control cannot fail)"))
    sys.exit(0 if not ok else 1)
sys.exit(0 if ok else 1)
