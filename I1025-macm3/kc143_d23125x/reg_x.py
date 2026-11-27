#!/usr/bin/env python3
"""reg_x.py [--mutate=ref] > reg_x_output.txt : the arithmetic behind the registration of README.md (written before the regrid of this folder), from the files (arithmetic only, not a result).
Reference = my k_c 143 state at D 23.125 regridded from k_c 135 (kc143_d23125/): record, root and bracket. Source = my k_c 127 state there (in/l1kc127Lmacm3.jsonl).
Prints t5's bars (comment 7213649039) as intervals around the reference root, what the scan window (-0.030, -0.020) can see, the sensitivity of the root to Delta implied by #1101's two numbers
(root scatter 1.75e-4, Delta scatter 4.2e-7 between two solves of one state; t5's figures, an order of magnitude only), and the chained shifts of Delta at D 23.0625 and D 23.125.
--mutate=ref moves the reference root up by 0.004 (a control: every interval and the window verdict must move)."""
import json, re, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()][-1]
ref = rd(R + "kc143_d23125/in/l1kc143macm3d23125.jsonl"); r135 = rd(R + "kc143_d23125/in/l1kc135macm3d23125.jsonl"); src = rd(R + "kc143_d23125x/in/l1kc127Lmacm3.jsonl")
t = open(R + "kc143_d23125/point_summary.txt").read(); m = re.search(r"secant root bracket \[(\S+), (\S+)\], width (\S+), signs.*det-linear root (\S+);", t)
lo, hi, w, root = float(m.group(1).rstrip(",")), float(m.group(2).rstrip(",")), float(m.group(3).rstrip(",")), float(m.group(4))
if "--mutate=ref" in sys.argv: root += 0.004; lo += 0.004; hi += 0.004
print("reference (k_c 143 at D 23.125 via k_c 135): Delta %.12f, lam_gauge %.12f, |F| %.4e, steps %d, constraint %.4e, F_start %.3e, %s s; root %+.8f, robust bracket [%.8f, %.8f]" % (ref["Delta"], ref["lam_gauge"], ref["F"], ref["steps"], ref["constraint"], ref["F_start"], ref["seconds"], root, lo, hi))
print("k_c 135 (the chain's middle): Delta %.12f, lam_gauge %.12f, |F| %.4e, steps %d, constraint %.4e, %s s" % (r135["Delta"], r135["lam_gauge"], r135["F"], r135["steps"], r135["constraint"], r135["seconds"]))
print("source (k_c 127 at D 23.125): Delta %.12f, lam_gauge %.12f, |F| %.4e, steps %d, constraint %.4e, F_start %.3e, %s s" % (src["Delta"], src["lam_gauge"], src["F"], src["steps"], src["constraint"], src["F_start"], src["seconds"]))
print("Delta shifts at D 23.125: 127 -> 135 %+.4e, 135 -> 143 %+.4e, 127 -> 143 by the chain %+.4e; lam_gauge: 127 -> 135 %+.3e, 135 -> 143 %+.3e, 127 -> 143 by the chain %+.3e" % (
    r135["Delta"] - src["Delta"], ref["Delta"] - r135["Delta"], ref["Delta"] - src["Delta"], r135["lam_gauge"] - src["lam_gauge"], ref["lam_gauge"] - r135["lam_gauge"], ref["lam_gauge"] - src["lam_gauge"]))
print("steps ratio to the source by the chain: %.4f; constraint ratio: %.4f" % (ref["steps"] / src["steps"], ref["constraint"] / src["constraint"]))
print("t5's bars as intervals of the new root: reproduced (within 1e-3) (%+.6f, %+.6f); between (1e-3 to 3e-3) (%+.6f, %+.6f) and (%+.6f, %+.6f); path-dependent (3e-3 or more) below %+.6f or above %+.6f" % (
    root - 1e-3, root + 1e-3, root - 3e-3, root - 1e-3, root + 1e-3, root + 3e-3, root - 3e-3, root + 3e-3))
print("the scan's window (-0.030, -0.020): root below -0.030 reads as no robust change (%.4f below the reference root); above -0.020 as none too; the reference root is %.4f from the lower end and %.4f from the upper end" % (
    -0.030 - root, root + 0.030, -0.020 - root))
sens = 1.75e-4 / 4.2e-7
print("sensitivity of the root to Delta from #1101's two figures (root scatter 1.75e-4, Delta scatter 4.2e-7): %.0f per unit Delta (order of magnitude only); a Delta difference of 1e-6 would move the root by %.1e, of 4e-7 by %.1e; a root move of 3e-3 needs a Delta difference of %.1e" % (
    sens, 1e-6 * sens, 4e-7 * sens, 3e-3 / sens))
print("t5's Delta bar: a difference above 1e-6 from %.12f means a different state (Delta outside (%.12f, %.12f))" % (ref["Delta"], ref["Delta"] - 1e-6, ref["Delta"] + 1e-6))
print("wall references: k_c 127 -> 135 regrid at D 23.125 3574 s (F_start 5.416e-06), k_c 135 -> 143 5856 s (F_start %.3e); k_c 127 source: %s s (F_start %.3e)" % (ref["F_start"], src["seconds"], src["F_start"]))
