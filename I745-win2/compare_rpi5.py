#!/usr/bin/env python3
"""#745: this run (win2, x86, Windows) against rpi5's run (aarch64, Linux, I745-rpi5/logs/main_1000.log) on the same state and command, starts present in both
(rpi5 printed 0 to 7), in printed digits and products, with #681's bound and products (250 cap) and #720's (starts 0 to 2) as references.

usage: python compare_rpi5.py [WIN2_LOG] [RPI5_LOG]     (defaults logs/main_1000.log and ../I745-rpi5/logs/main_1000.log)
       python compare_rpi5.py --selftest                 a planted change of one printed bound and one product count must be counted as a difference
Columns: printed bound (four significant digits of the log line) for each machine and whether equal as printed, the relative difference of the printed values, products on each machine,
max|x| equal as printed, and the printed final residual max|J x - v| of each (these differ in the last digits, #720 found the same across stacks)."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINE = re.compile(r"^\s+start (\d+): max\|x\| ([0-9.e+-]+), bound on the smallest gain ([0-9.e+-]+), max\|J x - v\| ([0-9.e+-]+), (\d+) products")


def parse(path):
    out = {}
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8", errors="replace"):
            m = LINE.match(ln)
            if m:
                out[int(m.group(1))] = dict(x=m.group(2), bound=m.group(3), res=m.group(4), prods=int(m.group(5)))
    return out


def rows(a, b, r681, r720):
    out = []
    for i in sorted(set(a) & set(b)):
        d = abs(float(a[i]["bound"]) - float(b[i]["bound"])) / float(b[i]["bound"])
        out.append(dict(i=i, a=a[i], b=b[i], eq=a[i]["bound"] == b[i]["bound"], d=d, xeq=a[i]["x"] == b[i]["x"], peq=a[i]["prods"] == b[i]["prods"],
                        r681=r681.get(i), r720=r720.get(i)))
    return out


def report(a, b, r681, r720):
    rs = rows(a, b, r681, r720)
    print("| start | win2 bound | rpi5 bound | equal as printed | relative diff | win2 products | rpi5 products | win2 - rpi5 | #681 bound, products | #720 bound, products | max\\|x\\| equal | win2 max\\|J x - v\\| | rpi5 max\\|J x - v\\| |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rs:
        r6 = f"{r['r681']['bound']}, {r['r681']['prods']}" if r["r681"] else "-"
        r7 = f"{r['r720']['bound']}, {r['r720']['prods']}" if r["r720"] else "-"
        print(f"| {r['i']} | {r['a']['bound']} | {r['b']['bound']} | {'yes' if r['eq'] else '**no**'} | {r['d']:.1e} | {r['a']['prods']} | {r['b']['prods']} | {r['a']['prods'] - r['b']['prods']:+d} | {r6} | {r7} | "
              f"{'yes' if r['xeq'] else '**no**'} | {r['a']['res']} | {r['b']['res']} |")
    n = len(rs)
    print(f"\n  starts in both: {n} ({', '.join(str(r['i']) for r in rs)}); bounds equal as printed: {sum(r['eq'] for r in rs)} of {n}; max|x| equal as printed: {sum(r['xeq'] for r in rs)} of {n}; "
          f"products equal: {sum(r['peq'] for r in rs)} of {n}")
    if n:
        print(f"  largest relative difference of the printed bounds {max(r['d'] for r in rs):.1e}; products win2 / rpi5 range {min(r['a']['prods'] / r['b']['prods'] for r in rs):.2f} to {max(r['a']['prods'] / r['b']['prods'] for r in rs):.2f}")
    return rs


def selftest():
    b = {0: dict(x="1.0e+33", bound="1.257e-34", res="1e-14", prods=606), 1: dict(x="2.0e+33", bound="9.921e-34", res="1e-14", prods=276)}
    a = {i: dict(v) for i, v in b.items()}
    ok1 = all(r["eq"] and r["peq"] for r in rows(a, b, {}, {}))
    a[1]["bound"] = "9.920e-34"
    a[0]["prods"] = 607
    rs = rows(a, b, {}, {})
    ok2 = [r["i"] for r in rs if not r["eq"]] == [1] and [r["i"] for r in rs if not r["peq"]] == [0]
    print(f"  identical -> equal: {'ok' if ok1 else 'WRONG'}; start 1's printed bound changed in the 4th digit and start 0's products by 1 -> counted: {'ok' if ok2 else 'WRONG'}")
    print("selftest", "passed" if ok1 and ok2 else "FAILED")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    wlog = args[0] if args else os.path.join(HERE, "logs", "main_1000.log")
    rlog = args[1] if len(args) > 1 else os.path.join(HERE, "..", "I745-rpi5", "logs", "main_1000.log")
    r681 = parse(os.path.join(HERE, "..", "I681-win", "logs", "K7_D40_rough.log"))
    r720 = parse(os.path.join(HERE, "..", "I720-win2", "logs", "main_1000.log"))
    report(parse(wlog), parse(rlog), r681, r720)
