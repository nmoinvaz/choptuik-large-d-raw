#!/usr/bin/env python3
"""explore_report.py args NAME | report [--dir logs] | selftest: #1080's EXPLORATORY start solves (not a reading, no walks).
args NAME   print "A w B3 C3" of x1, x2 or control as walk1026.py's first solve formats them (A, w to 12 decimals, B3, C3 to 10).
report      one table from logs/start_*.log: the FIXED-A line (r_1), F_3/F_1 with r_3, F_5/F_1 with r_5 (the regular expressions of walk1026.py's solve),
            |F5|/|F3|, and max|Y| when a line prints it (hier_nb.py does not at --verbose 1 or 2). A log with no FIXED-A line is listed as such.
selftest    parses the main run's logs (../logs/fix_*_01.log) and must reproduce the walk JSONs' first points to the digits printed; a log with its
            FIXED-A line removed must be read as no result."""
import glob
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
M5 = os.path.dirname(HERE)
sys.path.insert(0, M5)
import report1080 as R1080  # noqa: E402

CTRL = (2.726475885672135, 1.0156030949093042, 0.1444194785, 0.0110874259)


def args(name):
    if name == "control":
        A, w, b, c = CTRL
        return f"{A:.12f} {w:.12f} {b:.10f} {c:.10f}"
    A, w, b, c = R1080.box_centre(name, os.path.join(M5, "inputs"))
    return f"{A:.12f} {w:.12f} {b:.10f} {c:.10f}"


def parse(txt):
    m = re.findall(r"FIXED-A M (\d+): A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", txt)
    f3 = re.findall(r"F_3/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_3 ([0-9.]+e[+-]\d+)", txt)
    f5 = re.findall(r"F_5/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_5 ([0-9.]+e[+-]\d+)", txt)
    if not (m and f3 and f5):
        return None
    y = re.findall(r"max\s*\|Y\|\s*[=:]?\s*([0-9.]+(?:e[+-]?\d+)?)", txt)
    r1 = (float(m[-1][3]), float(m[-1][4]))
    F3, F5 = (float(f3[-1][0]), float(f3[-1][1])), (float(f5[-1][0]), float(f5[-1][1]))
    return dict(A=float(m[-1][1]), w=float(m[-1][2]), r1=math.hypot(*r1), r3=float(f3[-1][2]), r5=float(f5[-1][2]),
                F3=math.hypot(*F3), F5=math.hypot(*F5), maxY=(max(float(v) for v in y) if y else None))


def report(d):
    print("| start | xi1 | \\|r1\\| | \\|r3\\| | \\|r5\\| | \\|F3\\| | \\|F5\\| | \\|F5\\|/\\|F3\\| | max\\|Y\\| |")
    print("|---|---|---|---|---|---|---|---|---|")
    for p in sorted(glob.glob(os.path.join(d, "start_*.log"))):
        base = os.path.basename(p)[len("start_"):-4]
        name, rest = base.split("_xi", 1)
        r = parse(open(p).read())
        if r is None:
            print(f"| {name} | {rest} | no FIXED-A line (see {os.path.basename(p)}) | | | | | | |")
            continue
        print(f"| {name} | {rest} | {r['r1']:.2e} | {r['r3']:.1e} | {r['r5']:.1e} | {r['F3']:.4f} | {r['F5']:.4f} | {r['F5'] / r['F3']:.4f} | "
              f"{'not printed' if r['maxY'] is None else format(r['maxY'], '.3g')} |")


def selftest():
    ok = True
    for name in ("x1", "x2", "control"):
        for xi in ("0.2", "0.25"):
            wj = os.path.join(M5, "walks", f"walk_{name}_xi{xi}.json")
            lg = os.path.join(M5, "logs", f"fix_{name}_xi{xi}_01.log")
            if not (os.path.exists(wj) and os.path.exists(lg)):
                continue
            q = json.load(open(wj))["points"][0]
            txt = open(lg).read()
            r = parse(txt)
            good = r is not None and abs(r["r1"] - math.hypot(*q["r1"])) <= 1e-3 * r["r1"] and f"{r['r3']:.1e}" == f"{q['r3']:.1e}" and f"{r['r5']:.1e}" == f"{q['r5']:.1e}"
            mut = parse("\n".join(l for l in txt.splitlines() if not l.startswith("FIXED-A")))
            good &= mut is None
            ok &= good
            print(f"selftest: {name} xi1 {xi}: parse {'ok' if good else 'FAIL'} (log read against the walk JSON; the log without its FIXED-A line reads as no result)")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["args"]:
        print(args(a[1]))
    elif a[:1] == ["report"]:
        report(a[a.index("--dir") + 1] if "--dir" in a else os.path.join(HERE, "logs"))
    elif a[:1] == ["selftest"]:
        sys.exit(selftest())
    else:
        print(__doc__)
        sys.exit(2)
