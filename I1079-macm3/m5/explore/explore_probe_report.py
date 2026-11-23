#!/usr/bin/env python3
"""explore_probe_report.py: the four probe logs (logs/start_x1_xi{0.2,0.17}_{fm,v3}.log) as one table, with the level-3 trial lines of the verbose-3 logs and the
harmonics of the last level-3 iterate of the floor_max logs."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import explore_report as E  # noqa: E402

print("| probe | xi1 | \\|r1\\| | \\|r3\\| | \\|r5\\| | \\|F5\\|/\\|F3\\| |")
print("|---|---|---|---|---|---|")
for xi in ("0.2", "0.17"):
    for tag, lab in (("_fm", "--floor_max=1e-3 (verbose 2)"), ("_v3", "--verbose=3")):
        r = E.parse(open(os.path.join(HERE, "logs", f"start_x1_xi{xi}{tag}.log")).read())
        print(f"| {lab} | {xi} | {r['r1']:.1e} | {r['r3']:.1e} | {r['r5']:.1e} | {r['F5'] / r['F3']:.4f} |")
print()
for xi in ("0.2", "0.17"):
    t = open(os.path.join(HERE, "logs", f"start_x1_xi{xi}_v3.log")).read()
    print(f"xi1 {xi}, verbose 3, level 3 trials:")
    for l in re.findall(r"^\s+level 3 \(top\) it .*$", t, re.M):
        print("   ", l.strip())
    x = re.findall(r"^level 3 it \d+: .* x \[([^\]]*)\]", open(os.path.join(HERE, "logs", f"start_x1_xi{xi}_fm.log")).read(), re.M)
    v = [float(s) for s in x[-1].split(",")]
    print(f"xi1 {xi}, floor_max, last level-3 iterate (B3, C3, B5, C5): ({v[2]:.9f}, {v[3]:.9f}, {v[4]:.9f}, {v[5]:.9f}); start (B3, C3) was (0.8054175864, 0.0117800438)")
