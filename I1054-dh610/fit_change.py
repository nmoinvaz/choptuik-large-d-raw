#!/usr/bin/env python3
"""fit_change.py JSON [JSON ...] [--at D] [--err E] [--mutate]: the changes Delta(exact 1/k) - Delta(recip_int) of exact_recip_check.py delta files
(delta<D>.json), against D and against the quoted errors of their nearest delta_all.csv rows, and the least-squares line of log10|change| in D evaluated at --at
(251.878219928, the D 251.88 state) and set against --err (4.7e-7, the quoted error of the row at D 251.886). The line is an extrapolation, not a measurement.
fit_change.py --selftest: the line through planted points y = a + b D must give the planted value at D* (control; --selftest --mutate moves one planted point by one decade
and must fail, exit 1)."""
import json
import math
import sys


def line(pts):
    """least squares y = a + b x through (x, y) points; returns a, b"""
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    b = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
    return my - b * mx, b


def selftest(mutate):
    a, b, Dstar = -144.84, 0.55, 251.878219928
    Ds = [241.9602371, 246.439946659, 249.466404961]
    ys = [a + b * D for D in Ds]
    if mutate:
        ys[1] += 1.0
    aa, bb = line(list(zip(Ds, ys)))
    got, want = aa + bb * Dstar, a + b * Dstar
    ok = abs(got - want) < 1e-9
    print(f"selftest{' --mutate' if mutate else ''}: planted log10 value at D* {want:.9f}, fitted {got:.9f}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    mutate = "--mutate" in args
    if "--selftest" in args:
        return selftest(mutate)
    opt = {"--at": 251.878219928, "--err": 4.7e-7}
    for k in opt:
        if k in args:
            i = args.index(k)
            opt[k] = float(args[i + 1])
            del args[i:i + 2]
    files = [a for a in args if not a.startswith("--")]
    pts = []
    for f in files:
        r = json.load(open(f))
        D = float(r["D_a"])
        ch = r["change"] * (10.0 if mutate and not pts else 1.0)
        pts.append((D, ch, r.get("csv_rows", []), f))
        print(f"D {D:.6f}: Delta(on) - Delta(off) = {ch:+.6e}  ({f.split('/')[-1]})")
        for row in r.get("csv_rows", []):
            print(f"    row D {float(row['D']):.4f} ({row['kind']}, {row['err_kind']}): quoted error {float(row['err']):.2e}, |change| / error {abs(ch) / float(row['err']):.2e}")
    if len(pts) < 2:
        print("need at least two points for the line")
        return 1
    a, b = line([(p[0], math.log10(abs(p[1]))) for p in pts])
    res = [math.log10(abs(p[1])) - (a + b * p[0]) for p in pts]
    pred = 10 ** (a + b * opt["--at"])
    print(f"least-squares line of log10|change| in D through {len(pts)} points: log10|change| = {a:.4f} + {b:.5f} D (a factor {10 ** b:.3f} per unit D), residuals {', '.join(f'{x:+.3f}' for x in res)} decades")
    if len(pts) == 2:
        print("the line goes through two points and has no spread (no residual to read)")
    print(f"EXTRAPOLATION (not a measurement) to D {opt['--at']}: |change| about {pred:.2e}, against the row's quoted error {opt['--err']:.1e}: {pred / opt['--err']:.2e} of it; the last point is {opt['--at'] - max(p[0] for p in pts):.2f} below")
    return 0


sys.exit(main())
