#!/usr/bin/env python3
"""#966 A/B reading (b): Delta of an accepted state against the linear prediction from the two previous accepted states (coordinator hc 2026-11-20).
usage: python3 -I pred966.py                 predicts from leg 10's last two states (D 260.6706 and 260.8483) at the D and Delta of the newest accepted state of the newest leg
       python3 -I pred966.py selftest        predicts leg 10's step 17 from steps 15 and 16 and step 16 from steps 14 and 15 (the typical miss), exit 0
Delta and D are read from the logs' 'a ... -> D <D>' and 'Delta of the saved state, its eight parts summed exactly: <40 digits>' lines, as decimals."""
import glob, re, sys
from decimal import Decimal, getcontext
getcontext().prec = 60
def states(log):
    out, D = [], None
    for l in open(log):
        m = re.search(r"-> D (\d+\.\d+): predicted", l)
        if m: D = Decimal(m.group(1)); continue
        m = re.search(r"Delta of the saved state, its eight parts summed exactly: (\d\.\d+)", l)
        if m and D is not None: out.append((D, Decimal(m.group(1)))); D = None
    return out
def predict(p1, p2, Dn):
    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return p2[1] + slope * (Dn - p2[0]), slope
leg10 = states(sorted(glob.glob("ks_chain3b/leg10_*/anm_run.log"))[0])
if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    for i in (-1, -2):
        a, b, c = leg10[i - 2], leg10[i - 1], leg10[i]
        pr, sl = predict(a, b, c[0])
        print(f"predict D {c[0]} from D {a[0]}, {b[0]}: slope {float(sl):.6e}, predicted {pr}, actual {c[1]}, miss {float(c[1] - pr):+.3e}")
    sys.exit(0)
p1, p2 = leg10[-2], leg10[-1]
print(f"leg 10's last two: D {p1[0]} Delta {p1[1]}; D {p2[0]} Delta {p2[1]}; slope {float((p2[1]-p1[1])/(p2[0]-p1[0])):.6e} per unit D")
legs = [g for g in sorted(glob.glob("ks_chain3b/leg*/anm_run.log")) if g.split("/")[-2] > "leg10_zzz"]
new = states(legs[-1]) if legs else []
if not new: print("no accepted state in the newest leg yet"); sys.exit(0)
Dn, dn = new[0]
pr, sl = predict(p1, p2, Dn)
print(f"newest leg {legs[-1].split('/')[-2]}: first accepted D {Dn} Delta {dn}; predicted {pr}; difference {float(dn - pr):+.3e}; reading (b) (within 1e-6): {'PASS' if abs(dn - pr) <= Decimal('1e-6') else 'FAIL'}")
