#!/usr/bin/env python3
"""report_mp.py report [--dir logs] | selftest: the per-run table of #1080's extended-precision M = 5 values (exploratory).
Each logs/pointv_NAME.log holds the JSON line value_mp.py pointv prints. r_rest = (Re r_3, Im r_3, Re r_5, Im r_5) (inner_mp.residual_demixed returns
[Re r_1, Im r_1, Re r_3, Im r_3, ...] and value_mp keeps r[2:]), so |r3| = hypot(r_rest[0:2]) and |r5| = hypot(r_rest[2:4]). Also R_1 = re + i im, sig,
R_1/sig, valued, ymax, calls (the two precisions), seconds, and the solved v (strings). selftest: a synthetic line gives the |r3|, |r5| computed by hand, and
the same line with r_rest's pairs swapped must give the other values."""
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def line_of(path):
    for l in reversed(open(path).read().splitlines()):
        if l.startswith("{"):
            return json.loads(l)
    return None


def norms(d):
    r = d["r_rest"]
    return math.hypot(r[0], r[1]), math.hypot(r[2], r[3])


def report(d):
    for p in sorted(glob.glob(os.path.join(d, "pointv_*.log"))):
        name = os.path.basename(p)[len("pointv_"):-4]
        r = line_of(p)
        if r is None:
            print(f"{name}: no JSON line yet (log {os.path.basename(p)})")
            continue
        r3, r5 = norms(r)
        print(f"{name}: |r3| {r3:.3e} |r5| {r5:.3e}; R_1 = {r['re']:.6e} {r['im']:+.6e}i, sig {r['sig']:.3e}, |R_1|/sig {r['R_over_sig']:.3e}, valued {r['valued']}, "
              f"ymax {r['ymax']:.4g}, calls {r['calls']}, {r['seconds']} s, info {r['info']:.2e}, dR {r['dR']:.2e}, dr1 {r['dr1']:.2e}")
        print(f"    solved v (B3, C3, B5, C5) at dps {r['mp_dps'][1]}: {', '.join(r['v'])}")


def selftest():
    d = dict(r_rest=[3e-20, 4e-20, 6e-18, 8e-18])
    a = norms(d)
    sw = norms(dict(r_rest=[6e-18, 8e-18, 3e-20, 4e-20]))
    ok = abs(a[0] - 5e-20) < 1e-30 and abs(a[1] - 1e-17) < 1e-27 and abs(sw[0] - 1e-17) < 1e-27 and abs(sw[1] - 5e-20) < 1e-30 and a != sw
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest())
    if a[:1] == ["report"]:
        report(a[a.index("--dir") + 1] if "--dir" in a else os.path.join(HERE, "logs"))
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
