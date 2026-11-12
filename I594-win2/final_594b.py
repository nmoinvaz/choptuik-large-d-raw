#!/usr/bin/env python3
"""#594(b): the state of the R 0.2 circle at the 20:06 UTC cap, from the cache of ball determinants (data/modecount_D61.0264_M64_kf23_ball320_evals.jsonl).
Sorts the points on the circle (centre 0.032 + 3.086i, R 0.2) by angle, takes the arg steps between neighbours (wrapped to (-pi, pi]) and the angular gaps, and reports the steps above pi/4, the
sum of the step sizes (a lower bound of the total variation of arg: steps near pi hide more), the points that bound needs at pi/4 a step, and the step size by gap. A smooth arg gives steps
proportional to the gap; steps that stay of order 1 whatever the gap look like noise. No winding is read from steps that are not resolved.
usage: python final_594b.py CACHE.jsonl"""
import cmath, json, math, statistics, sys
import numpy as np
c = complex(0.032, 3.086)
L = [json.loads(l) for l in open(sys.argv[1])]
on = [x for x in L if abs(abs(complex(x["re"], x["im"])) - 0) >= 0 and abs(abs(complex(x["re"], x["im"]) - c) - 0.2) < 1e-9]
pts = sorted(on, key=lambda x: cmath.phase(complex(x["re"], x["im"]) - c))
ar = np.array([x["arg"] for x in pts]); la = np.array([x["lnabs"] for x in pts])
th = np.array([cmath.phase(complex(x["re"], x["im"]) - c) for x in pts])
d = np.diff(np.append(ar, ar[0])); d = (d + np.pi) % (2 * np.pi) - np.pi
dl = np.diff(np.append(la, la[0]))
gap = np.diff(np.append(th, th[0] + 2 * np.pi))
sec = [x["sec"] for x in L]
print(f"determinants {len(L)} ({len(on)} on the circle, {len(L) - len(on)} elsewhere), median {statistics.median(sec):.1f} s, total {sum(sec) / 3600:.2f} h")
print(f"steps above pi/4: {(abs(d) > math.pi / 4).sum()} of {len(d)} (pi/4..pi/2 {((abs(d) >= math.pi / 4) & (abs(d) < math.pi / 2)).sum()}, pi/2..pi {(abs(d) >= math.pi / 2).sum()}), largest {abs(d).max():.3f} rad, largest gap {gap.max():.4f} rad")
tv = abs(d).sum()
print(f"sum of the step sizes {tv:.1f} rad -> at least {tv / (math.pi / 4):.0f} points at pi/4 a step")
print("step by gap (gap rounded to 3 digits): n, median |d arg|, fraction above pi/4, median |d ln|det||")
for g in sorted({round(x, 3) for x in gap}):
    m = np.abs(gap - g) < 0.0006
    if m.sum() >= 3:
        print(f"  gap {g:.3f}: n {m.sum():3d}, median |d arg| {np.median(abs(d[m])):.2f}, above pi/4 {np.mean(abs(d[m]) > math.pi / 4):.2f}, median |d ln| {np.median(abs(dl[m])):.2f}")
# where: the steps by quadrant of the angle, and the full list of points and steps in steps_at_cap.csv beside the cache
import csv, os
q = ((th + 2 * np.pi) % (2 * np.pi) // (np.pi / 2)).astype(int)
print("steps above pi/4 by quadrant of the angle (0 to pi/2, pi/2 to pi, pi to 3pi/2, 3pi/2 to 2pi): " + ", ".join(f"{int(((abs(d) > math.pi / 4) & (q == k)).sum())} of {int((q == k).sum())}" for k in range(4)))
with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "steps_at_cap.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["angle_rad", "re", "im", "lnabs", "arg", "step_arg_to_next", "step_lnabs_to_next", "gap_to_next_rad", "above_pi_over_4"])
    for i, x in enumerate(pts):
        w.writerow([f"{th[i]:.6f}", x["re"], x["im"], x["lnabs"], x["arg"], f"{d[i]:.6f}", f"{dl[i]:.6f}", f"{gap[i]:.6f}", int(abs(d[i]) > math.pi / 4)])
print("(a smooth arg would halve its median step with the gap; a median near pi/2 = 1.57 at every gap is what uniform random phases give)")
