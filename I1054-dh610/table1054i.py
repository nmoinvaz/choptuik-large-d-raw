#!/usr/bin/env python3
"""table1054i.py: job 6's report from job6_r0.log and job6_r1.log: each log's first polish lines, its attempt lines read by refusal.py with, for each, the octo-double
Newton line before it (its max|F| and 'converged', reading (c): converged iff that line says so with max|F| at or below --tol_od, 1e-60; the printed figure on the attempt line is the
double-double |F| of the first two parts, and its 'stall accepted' label is printed whenever the step was accepted and that figure is above tol, so it is not read), and, at each D both
runs saved (job6_r<R>/anm_pin3_D<D>.npz), the change Delta(on) - Delta(off) of delta_job6_<D>.json with its share of the nearest quoted error and its ratio
to +3.290002e-13 (the change at D 241.96, delta241.json; 3.5 flags with --qd_it 12, no strong chord)."""
import glob
import json
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, H)
from refusal import attempts, first_refusal  # noqa: E402

REF = 3.290002e-13
TOL_OD = 1e-60
OD = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| (\S+?), (converged|not converged);")
ATT = re.compile(r"^    a [0-9.]+ -> D ([0-9.]+): ")


def od_word(o):
    """reading (c): converged iff the line says so with max|F| at or below tol_od"""
    return "converged (at or below tol_od 1e-60)" if o[2] and o[1] <= TOL_OD else ("says converged, max|F| above tol_od" if o[2] else "not converged")


def od_before(text):
    """{D string: (steps, max|F|, the line says converged)} from the octo-double line last seen before each attempt line"""
    last, out = None, {}
    for ln in text.splitlines():
        m = OD.search(ln)
        if m:
            last = (int(m.group(1)), float(m.group(2)), m.group(3) == "converged")
        m = ATT.match(ln)
        if m and last:
            out[m.group(1)[:7]] = last
    return out
for R in (0, 1):
    t = open(H + f"job6_r{R}.log").read() if os.path.exists(H + f"job6_r{R}.log") else ""
    print(f"flag {'on' if R else 'off'} (job6_r{R}.log):")
    for ln in t.splitlines():
        if re.search(r"octo-double Newton|base polish", ln):
            print("  first polish line: " + ln.strip()[:200])
            break
    od = od_before(t)
    for n, (a, D, k, fc, tol, acc) in enumerate(attempts(t), 1):
        o = od.get(D[:7])
        ods = f"octo-double {o[0]} steps, max|F| {o[1]:.1e}, {od_word(o)}" if o else "no octo-double line"
        print(f"  attempt {n}: a {a} -> D {D}: {ods}; double-double |F| of its first two parts {fc:.2e}; {'accepted' if acc else 'REFUSED'}")
    r = first_refusal(t)
    print("  " + (r or "no refusal") + ("; ends with 'done'" if re.search(r"^done$", t, re.M) else "; no 'done' line"))
print()
print("| D | flag off (octo-double steps, max\\|F\\|) | flag on (octo-double steps, max\\|F\\|) | change (on - off) | nearest row, quoted error | share | change / (+3.290002e-13 at D 241.96) |")
print("|---|---|---|---|---|---|---|")
t0 = open(H + "job6_r0.log").read() if os.path.exists(H + "job6_r0.log") else ""
t1 = open(H + "job6_r1.log").read() if os.path.exists(H + "job6_r1.log") else ""
a0, a1 = attempts(t0), attempts(t1)
for p in sorted(glob.glob(H + "job6_r0/anm_pin3_D*.npz")):
    Ds = os.path.basename(p)[len("anm_pin3_D"):-4]
    jp = H + f"delta_job6_{Ds}.json"
    if not os.path.exists(H + f"job6_r1/anm_pin3_D{Ds}.npz") or not os.path.exists(jp):
        print(f"| {Ds} | saved by the flag-off run | no flag-on state or delta | none | none | none | none |")
        continue
    j = json.load(open(jp))
    e = (j.get("csv_rows") or [None])[0]
    row = f"D {float(e['D']):.4f}, {float(e['err']):.1e} ({e['err_kind']})" if e else "none"
    share = f"{abs(j['change']) / float(e['err']):.2e}" if e else "none"
    m0 = [x for x in a0 if x[1][:7] == Ds[:7] and x[5]]
    m1 = [x for x in a1 if x[1][:7] == Ds[:7] and x[5]]
    o0, o1 = od_before(t0).get(Ds[:7]), od_before(t1).get(Ds[:7])
    c = lambda m, o: (f"{o[0]} steps, {o[1]:.1e}, {od_word(o)}" if o else "?")
    print(f"| {Ds} | {c(m0, o0)} | {c(m1, o1)} | {j['change']:+.6e} | {row} | {share} | {j['change'] / REF:.3g} |")
