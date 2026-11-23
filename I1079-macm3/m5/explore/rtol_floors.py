#!/usr/bin/env python3
"""rtol_floors.py [LOGS]: x1's start at xi1 0.2 with --floor_max=1e-3 at three integrator tolerances (rtol 1e-13, 1e-12 = the default's earlier run, 1e-11). Per run: the
sensitivity table K (max |d r_l / d x_nu| over nu = 3, 5), the residuals at which the level-5 top solves stopped (min, median, max) and the level-3 stall, their ratios to K,
the stop reasons, and the final |r_1|, |r_3|, |r_5|, |F5|/|F3|. Then the reading fixed before the run (README): level 5 'unchanged' when the 1e-13 and 1e-11 stall ranges both
overlap the default's range, 'scales' when the 1e-11 range lies wholly above the default's and the 1e-13 range wholly below it; level 3 'unchanged' when both are within 3x of
the default's stall, 'scales' when it falls by 3x or more at 1e-13 and rises by 3x or more at 1e-11; otherwise 'mixed'.
selftest: the reading's function on synthetic ranges (an unchanged, a scaling and a mixed case must give those words)."""
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import explore_report as E  # noqa: E402

RUNS = [("1e-13", "start_x1_xi0.2_fm_rtol1e-13.log"), ("1e-12 (default)", "start_x1_xi0.2_fm.log"), ("1e-11", "start_x1_xi0.2_fm_rtol1e-11.log")]


def stalls(txt, lev):
    return [float(v) for v, _ in re.findall(rf"level {lev} \(top\): stop at \|r_{lev}\| ([0-9.e+-]+): (.*)", txt)]


def K(txt):
    return {int(m[0]): max(float(m[1]), float(m[2])) for m in re.findall(r"^\s+l (\d): [0-9.e+]+\s+([0-9.e+]+)\s+([0-9.e+]+)", txt, re.M)}


def read5(lo, mid, hi):
    """lo, mid, hi: (min, max) stall ranges of level 5 at rtol 1e-13, 1e-12, 1e-11."""
    ov = lambda a, b: a[0] <= b[1] and b[0] <= a[1]
    if ov(lo, mid) and ov(hi, mid):
        return "unchanged"
    if hi[0] > mid[1] and lo[1] < mid[0]:
        return "scales"
    return "mixed"


def read3(lo, mid, hi):
    near = lambda v: mid / 3 <= v <= mid * 3
    if near(lo) and near(hi):
        return "unchanged"
    if lo <= mid / 3 and hi >= mid * 3:
        return "scales"
    return "mixed"


def selftest():
    ok = read5((1e-6, 4e-6), (1e-6, 4e-6), (1.5e-6, 5e-6)) == "unchanged" and read5((1e-7, 4e-7), (1e-6, 4e-6), (1e-5, 4e-5)) == "scales" and read5((1e-7, 4e-7), (1e-6, 4e-6), (2e-6, 5e-6)) == "mixed"
    ok &= read3(4e-4, 4.6e-4, 5e-4) == "unchanged" and read3(4e-5, 4.6e-4, 4e-3) == "scales" and read3(4e-5, 4.6e-4, 5e-4) == "mixed"
    ok &= read3(6.0, 4.6e-4, 7.5e-5) == "mixed" and read3(4e-4, 4.6e-4, 7.5e-6) == "mixed"   # a stall far above the default's, or far below, is not "unchanged"
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    if "selftest" in sys.argv[1:]:
        return selftest()
    rng5, st3 = [], []
    for rt, name in RUNS:
        p = os.path.join(HERE, "logs", name)
        if not os.path.exists(p):
            print(f"rtol {rt}: {name} missing")
            return 1
        t = open(p).read()
        k, s5, s3 = K(t), stalls(t, 5), stalls(t, 3)
        r = E.parse(t)
        reasons5 = sorted(set(x for _, x in re.findall(r"level 5 \(top\): stop at \|r_5\| ([0-9.e+-]+): (.*)", t)))
        print(f"rtol {rt}: K_5 {k[5]:.2e} K_3 {k[3]:.2e} K_1 {k[1]:.2e}")
        print(f"  level 5: {len(s5)} top solves, stop |r_5| min {min(s5):.2e} median {statistics.median(s5):.2e} max {max(s5):.2e}; stop/K_5 {min(s5) / k[5]:.1e} to {max(s5) / k[5]:.1e}; {'; '.join(reasons5)}")
        print(f"  level 3: stop |r_3| {s3[-1]:.2e} ({len(s3)} top solve); stop/K_3 {s3[-1] / k[3]:.1e}")
        print(f"  final: |r_1| {r['r1']:.2e} |r_3| {r['r3']:.1e} |r_5| {r['r5']:.1e} |F5|/|F3| {r['F5'] / r['F3']:.4f}")
        rng5.append((min(s5), max(s5)))
        st3.append(s3[-1])
    print(f"reading: level 5 {read5(*rng5)}; level 3 {read3(*st3)}")
    return 0


sys.exit(main())
