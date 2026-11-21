#!/usr/bin/env python3
"""#1025 winb, the low-lambda scans: the coordinator's readings (comment 7067116072, fixed before the run) applied to the two window readings of xfkappa's d18f_read.py.
usage: read_scanlow_1025.py READ_D18.0625.log READ_D18.log
The logs are `d18f_read.py window D 1.00 1.55 FILES` outputs (a robust change prints its bracket, orientation, det-linear estimate and the four-estimator range, which is
information, not a bound). Readings, fixed now:
 - a robust change in (1.20, 1.30) at D 18.0625 and one in (1.00, 1.20) at D 18 mean the root ROSE through 1.20; its rate is read from the two positions;
 - a robust change in (1.20, 1.55) at D 18 and none in that range at D 18.0625 mean it FELL through 1.20;
 - any other pattern is reported as found, with no reading.
The rate is then compared with the 1.3885 root at D 18.25 (xfkappa's (ii): range [1.388522, 1.388581]): can one track join them at a rate between the two bases, or are they
two roots? Only the numbers are printed for that. A 'robust change' is one the reader counts (both grid points noise-robust); a STOP-level reader message (a repeated point that
disagrees) is flagged and the pattern is then reported without a reading."""
import re, sys
D0, D1, D2 = 18.0, 18.0625, 18.25
P25, P25LO, P25HI = 1.3885, 1.388522, 1.388581
def parse(fn):
    t = open(fn).read()
    ch = [dict(br=(float(a), float(b)), ori=f"{o1} to {o2}", lin=float(l), lo=float(lo), hi=float(hi))
          for a, b, o1, o2, l, lo, hi in re.findall(r"change in \(([\d.]+), ([\d.]+)\), ([+-]) to ([+-]) in this state: det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", t)]
    non = re.search(r"touching a non-robust point \(not counted\): (.*)", t)
    mins = re.search(r"ln\|det\| local minima without a sign change in the window: (.*)", t)
    rd = re.search(r"^reading: (.*)$", t, re.M) or re.search(r"^no reading: (.*)$", t, re.M)
    f64 = re.search(r"float64 in the window: (.*)", t)
    sig = re.search(r"^signs: (.*)$", t, re.M)
    return dict(ch=ch, non=non.group(1).strip() if non else "?", mins=mins.group(1).strip() if mins else "?", reading=rd.group(0)[:200] if rd else "?",
                stop="STOP-level" in t, f64=f64.group(1).strip() if f64 else "?", signs=sig.group(1).strip() if sig else "?")
a, b = parse(sys.argv[1]), parse(sys.argv[2])
for D, r in ((D1, a), (D0, b)):
    print(f"D {D:g}: signs {r['signs']}")
    for c in r["ch"]:
        print(f"   robust change in ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {c['ori']} in this state: det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    if not r["ch"]:
        print("   no robust change in the window")
    print(f"   touching a non-robust point (not counted): {r['non']}; ln|det| minima without a sign change: {r['mins']}")
    print(f"   reader: {r['reading']}; float64 in the window: {r['f64']}")
inr = lambda r, lo, hi: [c for c in r["ch"] if c["br"][0] >= lo - 1e-9 and c["br"][1] <= hi + 1e-9]
stop = a["stop"] or b["stop"]
rose = len(inr(a, 1.20, 1.30)) == 1 and len(inr(b, 1.00, 1.20)) == 1 and len(a["ch"]) == 1 and len(b["ch"]) == 1
fell = len(inr(b, 1.20, 1.55)) >= 1 and len(a["ch"]) == 0
if stop:
    print("STOP-LEVEL: a reader flagged a repeated point that disagrees; the pattern above is reported as found, no reading")
elif rose:
    ca, cb = a["ch"][0], b["ch"][0]
    r = (ca["lin"] - cb["lin"]) / (D1 - D0); rlo = (ca["lo"] - cb["hi"]) / (D1 - D0); rhi = (ca["hi"] - cb["lo"]) / (D1 - D0)
    print(f"READING: the root ROSE through 1.20: from {cb['lin']:.6f} at D 18 (range [{cb['lo']:.6f}, {cb['hi']:.6f}]) to {ca['lin']:.6f} at D 18.0625 (range [{ca['lo']:.6f}, {ca['hi']:.6f}]); "
          f"rate {r:+.4f} per unit D (extremes of the ranges {rlo:+.4f} to {rhi:+.4f})")
    r2 = (P25 - ca["lin"]) / (D2 - D1); r3 = (P25 - cb["lin"]) / (D2 - D0)
    print(f"comparison with D 18.25's root at {P25} (range [{P25LO}, {P25HI}]): from D 18.0625 to D 18.25 a track would need {r2:+.4f} per unit D; from D 18 to D 18.25 {r3:+.4f}; "
          f"the rate between D 18 and D 18.0625 is {r:+.4f}")
elif fell:
    cb = inr(b, 1.20, 1.55)[0]
    print(f"READING: the root FELL through 1.20: a robust change at D 18 in ({cb['br'][0]:.2f}, {cb['br'][1]:.2f}) (det-linear {cb['lin']:.6f}, range [{cb['lo']:.6f}, {cb['hi']:.6f}]) and none in "
          f"1.00-1.55 at D 18.0625; it must have moved at least {(cb['lin'] - 1.20) / (D1 - D0):.4f} per unit D down to cross 1.20 by D 18.0625")
    print(f"comparison with D 18.25's root at {P25}: from D 18 a rise to it would need {(P25 - cb['lin']) / (D2 - D0):+.4f} per unit D (the fall and the rise are opposite)")
else:
    print("NO READING: any other pattern is reported as found (above); the coordinator rules")
