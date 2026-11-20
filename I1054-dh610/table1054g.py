#!/usr/bin/env python3
"""table1054g.py: job 4's report from cont241_r0.log and cont241_r1.log: each log's first polish lines, its attempt lines read by refusal.py, and, at each D both
runs saved (cont241_r<R>/anm_pin3_D<D>.npz), the change Delta(on) - Delta(off) of delta_cont<D>.json with its share of the nearest quoted error and its ratio
to +3.290002e-13 (the change at D 241.96, delta241.json)."""
import glob
import json
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, H)
from refusal import attempts, first_refusal  # noqa: E402

REF = 3.290002e-13
for R in (0, 1):
    t = open(H + f"cont241_r{R}.log").read() if os.path.exists(H + f"cont241_r{R}.log") else ""
    print(f"flag {'on' if R else 'off'} (cont241_r{R}.log):")
    for ln in t.splitlines():
        if re.search(r"octo-double Newton|base polish", ln):
            print("  first polish line: " + ln.strip()[:200])
            break
    for n, (a, D, k, fc, tol, acc) in enumerate(attempts(t), 1):
        print(f"  attempt {n}: a {a} -> D {D}, {k} steps -> {fc:.2e} (tol {tol:.0e}), {('accepted' + (', above its tol (stall accepted)' if fc > tol else ', at or below its tol')) if acc else 'REFUSED'}")
    r = first_refusal(t)
    print("  " + (r or "no refusal") + ("; ends with 'done'" if re.search(r"^done$", t, re.M) else "; no 'done' line"))
print()
print("| D | flag off (steps -> max\\|F\\|) | flag on (steps -> max\\|F\\|) | change (on - off) | nearest row, quoted error | share | change / (+3.290002e-13 at D 241.96) |")
print("|---|---|---|---|---|---|---|")
t0 = open(H + "cont241_r0.log").read() if os.path.exists(H + "cont241_r0.log") else ""
t1 = open(H + "cont241_r1.log").read() if os.path.exists(H + "cont241_r1.log") else ""
a0, a1 = attempts(t0), attempts(t1)
for p in sorted(glob.glob(H + "cont241_r0/anm_pin3_D*.npz")):
    Ds = os.path.basename(p)[len("anm_pin3_D"):-4]
    jp = H + f"delta_cont{Ds}.json"
    if not os.path.exists(H + f"cont241_r1/anm_pin3_D{Ds}.npz") or not os.path.exists(jp):
        print(f"| {Ds} | saved by the flag-off run | no flag-on state or delta | none | none | none | none |")
        continue
    j = json.load(open(jp))
    e = (j.get("csv_rows") or [None])[0]
    row = f"D {float(e['D']):.4f}, {float(e['err']):.1e} ({e['err_kind']})" if e else "none"
    share = f"{abs(j['change']) / float(e['err']):.2e}" if e else "none"
    m0 = [x for x in a0 if x[1][:7] == Ds[:7] and x[5]]
    m1 = [x for x in a1 if x[1][:7] == Ds[:7] and x[5]]
    c = lambda m: (f"{m[-1][2]} -> {m[-1][3]:.1e}" + (" (stall accepted)" if m[-1][3] > m[-1][4] else "") if m else "?")
    print(f"| {Ds} | {c(m0)} | {c(m1)} | {j['change']:+.6e} | {row} | {share} | {j['change'] / REF:.3g} |")
