#!/usr/bin/env python3
"""#1025 winb, the k_c 55 test at D 18: the coordinator's reading (hc 2026-11-21 about 22:0x UTC, fixed before the run) applied to the `d18f_read.py window 18.0 1.70 1.85` output.
usage: read_kc55_1025.py READ_kc55_D18.log
Compare with k_c 63 at D 18 (roots 1.7750 and 1.8074; signs minus, plus, minus over 1.70 to 1.85): the same two changes within 0.01 means the D 18 pair is k_c-stable;
any other pattern means it depends on k_c.
How it is applied (mine, to make that exact): 'the same two changes' = exactly two robust changes (both grid points noise-robust; none touching a non-robust point), the lower
minus-to-plus and the upper plus-to-minus as for k_c 63 in this window, each with its det-linear position within 0.01 of 1.7750 and of 1.8074. Anything else is 'depends on
k_c' as found, with the details. The one case the order does not name, two changes in the right places with the orientation reversed (plus-to-minus then minus-to-plus), is
printed as that and left to the coordinator, because the hybrid's overall sign is not comparable across states."""
import re, sys
R1, R2, TOL = 1.7750, 1.8074, 0.01
t = open(sys.argv[1]).read()
ch = [dict(br=(float(a), float(b)), o1=o1, o2=o2, lin=float(l), lo=float(lo), hi=float(hi))
      for a, b, o1, o2, l, lo, hi in re.findall(r"change in \(([\d.]+), ([\d.]+)\), ([+-]) to ([+-]) in this state: det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", t)]
non = re.search(r"touching a non-robust point \(not counted\): (.*)", t)
nonrob = re.search(r"not noise-robust: (.*)", t)
mins = re.search(r"ln\|det\| local minima without a sign change in the window: (.*)", t)
sig = re.search(r"^signs: (.*)$", t, re.M)
f64 = re.search(r"float64 in the window: (.*)", t)
print(f"k_c 55, D 18, window 1.70-1.85: signs {sig.group(1) if sig else '?'}")
for c in ch:
    print(f"   robust change in ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {c['o1']} to {c['o2']} in this state: det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
if not ch:
    print("   no robust change in the window")
print(f"   points not noise-robust: {nonrob.group(1) if nonrob else '?'}; changes touching a non-robust point (not counted): {non.group(1).strip() if non else '?'}; "
      f"ln|det| minima without a sign change: {mins.group(1).strip() if mins else '?'}; float64: {f64.group(1) if f64 else '?'}")
print(f"k_c 63 at D 18 (the same window, same reader): 1.775263 [1.774793, 1.775263] minus to plus and 1.806298 [1.806298, 1.807635] plus to minus; the coordinator's roots {R1} and {R2}")
clean = (nonrob is None or nonrob.group(1).strip() == "none") and (non is None or non.group(1).strip() == "none")
if len(ch) == 2 and clean:
    lo_c, up_c = sorted(ch, key=lambda c: c["lin"])
    d1, d2 = lo_c["lin"] - R1, up_c["lin"] - R2
    ori_same = (lo_c["o1"], lo_c["o2"], up_c["o1"], up_c["o2"]) == ("-", "+", "+", "-")
    ori_rev = (lo_c["o1"], lo_c["o2"], up_c["o1"], up_c["o2"]) == ("+", "-", "-", "+")
    pos_ok = abs(d1) <= TOL + 1e-9 and abs(d2) <= TOL + 1e-9
    print(f"two robust changes: lower at {lo_c['lin']:.6f} ({d1:+.4f} from {R1}), upper at {up_c['lin']:.6f} ({d2:+.4f} from {R2}); orientation {'as k_c 63 (minus-to-plus, plus-to-minus)' if ori_same else ('REVERSED (plus-to-minus, minus-to-plus)' if ori_rev else 'other')}")
    if pos_ok and ori_same:
        print("READING: the same two changes within 0.01: the D 18 pair is k_c-STABLE")
    elif pos_ok and ori_rev:
        print("READING: the two changes are within 0.01 of k_c 63's, with the orientation reversed: not covered by the order's wording; the coordinator rules")
    else:
        print("READING: any other pattern: the D 18 pair DEPENDS on k_c (the two changes are not both within 0.01 of 1.7750 and 1.8074 with k_c 63's orientation)")
else:
    print(f"READING: any other pattern: the D 18 pair DEPENDS on k_c ({len(ch)} robust change(s) in the window"
          + ("" if clean else ", a point or a change is not noise-robust") + ")")
