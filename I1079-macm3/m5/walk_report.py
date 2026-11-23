#!/usr/bin/env python3
"""walk_report.py table FILE.jsonl | end FILE.jsonl | shift FILE.jsonl NAME | selftest: #1080's extended-precision walk (zero_mp.py --M=5), its rows.
table   one line per iteration: A, w/w_inf, |R_1|, |R_1|/sigma, the Newton step (dA, dw), orientation, valued flags, the slowest point's seconds
end     the last row's A, w/w_inf and solved v (the harmonics at the centre point), one per line: the arguments of `value_mp.py pointv ... --v=` after a located end
shift   the M = 3 -> 5 shift from NAME's box centre (inputs/) to the last row's (A, w/w_inf), its Euclidean norm, against the M = 1 -> 3 shift (0.140 for x1, 0.210 for x2,
        report1080.py partners), and |F5|/|F3| from the last row's v
selftest  synthetic rows: the table's |R| and ratio, `end` returning the last row, and a swapped-pair v changing |F5|/|F3|"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import report1080 as R1080  # noqa: E402

M1TO3 = dict(x1=0.14035, x2=0.20993)


def rows_of(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def table(rows):
    print("| it | A | w/w_inf | \\|R_1\\| | \\|R_1\\|/sigma | step dA | step dw | orient. | valued | slowest point s |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['it']} | {r['A']:.15f} | {r['wf']:.15f} | {math.hypot(r['re'], r['im']):.3e} | {r['R_over_sig']:.2e} | {r['dA']:+.2e} | {r['dwf']:+.2e} | "
              f"{r['orientation']:+d} | {sum(r['valued'])}/{len(r['valued'])} | {max(r['sec']):.0f} |")


def fratio(v):
    f3, f5 = math.hypot(float(v[0]), float(v[1])), math.hypot(float(v[2]), float(v[3]))
    return f5 / f3


def selftest():
    rows = [dict(it=0, A=3.4, wf=0.3, re=3.0, im=4.0, sig=1e-17, R_over_sig=5e17, valued=[True] * 5, orientation=1, dA=1e-3, dwf=-2e-3, sec=[10] * 5, F3=["3", "4", "6", "8"])]
    ok = abs(math.hypot(rows[0]["re"], rows[0]["im"]) - 5.0) < 1e-12 and abs(fratio(rows[0]["F3"]) - 2.0) < 1e-12
    ok &= abs(fratio(["6", "8", "3", "4"]) - 0.5) < 1e-12 and fratio(["6", "8", "3", "4"]) != fratio(rows[0]["F3"])
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(a):
    if a[:1] == ["selftest"]:
        return selftest()
    rows = rows_of(a[1])
    if a[0] == "table":
        table(rows)
    elif a[0] == "end":
        r = rows[-1]
        print(repr(r["A"]))
        print(repr(r["wf"]))
        print(",".join(r["F3"]))
    elif a[0] == "shift":
        c = R1080.box_centre(a[2], os.path.join(HERE, "inputs"))
        r = rows[-1]
        s53 = math.hypot(r["A"] - c[0], r["wf"] - c[1])
        print(f"{a[2]}: M3 -> 5 shift ({r['A'] - c[0]:+.6f}, {r['wf'] - c[1]:+.6f}), norm {s53:.6f}, against M1 -> 3 {M1TO3[a[2]]}: {'smaller' if s53 < M1TO3[a[2]] else 'NOT smaller'}; "
              f"|F5|/|F3| {fratio(r['F3']):.4f} (last row's v)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
