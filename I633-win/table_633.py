#!/usr/bin/env python3
"""#633: Delta at eta = 5, 6, 7, 8.5, 10 (and 14, 20, inf) for k_c 23 and 39, the bracket of the minimum, and the parabola's eta_min and Delta_min (rules in README.md).
usage: python table_633.py [--selftest] [--shift ETA X]       (from this folder; needs data/sigdss_i633{a,b}.jsonl and data/sigdss_refine_i633_kc{23,39}_eta{6,8.5}.jsonl here, and ../I623-win, ../I630-win, ../I631-win)
Bracket: eta ordered 5, 6, 7, 8.5, 10, 14, 20, inf; s_i = Delta(next) - Delta(eta_i); s is RESOLVED when its sign is the same at k_c 23 and 39 and its magnitude at both exceeds c = |s_39 - s_23|, else OPEN;
the minimum is BRACKETED between eta_{i-1} and eta_{i+1} when s_{i-1} < 0 and s_i > 0 are both resolved.
Parabola: at each k_c the three adjacent grid points of eta = 5, 6, 7, 8.5, 10 around the smallest Delta (the three smallest must be neighbours, else it says so), Delta = a + b x + c x^2 in x = eta
(primary), ln eta and 1/eta (sensitivity), vertex x* = -b/(2c), flagged when outside the span of the three points. --selftest: planted tables and parabolas. --shift ETA X: adds X to Delta(ETA) at k_c 39."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D623, D630, D631 = (os.path.join(HERE, "..", d) for d in ("I623-win", "I630-win", "I631-win"))
ETAS = ("5", "6", "7", "8.5", "10", "14", "20", "inf")
FIVE = ("5", "6", "7", "8.5", "10")
VAL = {"5": 5.0, "6": 6.0, "7": 7.0, "8.5": 8.5, "10": 10.0, "14": 14.0, "20": 20.0}
VARS = {"eta": (lambda e: e, lambda x: x), "ln eta": (math.log, math.exp), "eps = 1/eta": (lambda e: 1.0 / e, lambda x: 1.0 / x)}


def resolved(a, b):
    c = abs(b - a)
    if (a > 0) != (b > 0):
        return False, c
    return (abs(a) > c and abs(b) > c), c


def analyse(D23, D39, etas=ETAS):
    rows = []
    for i in range(len(etas) - 1):
        a, b = etas[i], etas[i + 1]
        s23, s39 = D23[b] - D23[a], D39[b] - D39[a]
        ok, c = resolved(s23, s39)
        rows.append(((a, b), s23, s39, ok, c))
    brackets = []
    for i in range(1, len(etas) - 1):
        lo, hi = rows[i - 1], rows[i]
        if lo[3] and hi[3] and lo[1] < 0 and lo[2] < 0 and hi[1] > 0 and hi[2] > 0:
            brackets.append((etas[i - 1], etas[i], etas[i + 1]))
    return rows, brackets


def vertex(xs, ys):
    """Vertex (x*, y*) of the parabola through three points, with the middle point as origin (no cancellation of the 0.46)."""
    (x1, x2, x3), (y1, y2, y3) = xs, ys
    u1, u3, v1, v3 = x1 - x2, x3 - x2, y1 - y2, y3 - y2
    det = u1 * u3 * (u3 - u1)
    b = (v1 * u3 * u3 - v3 * u1 * u1) / det
    c = (v3 * u1 - v1 * u3) / det
    xs_ = -b / (2 * c)
    return x2 + xs_, y2 - b * b / (4 * c), c


def parabola(D, label="eta"):
    """(three etas used, adjacent?, eta_min, Delta_min, inside span?, curvature>0?) for the five-point table D, in the variable named."""
    order = sorted(FIVE, key=lambda e: D[e])
    pos = sorted(FIVE.index(e) for e in order[:3])
    adjacent = pos[2] - pos[0] == 2
    if not adjacent:
        i = FIVE.index(order[0])
        i = min(max(i, 1), len(FIVE) - 2)
        pos = [i - 1, i, i + 1]
    used = [FIVE[p] for p in pos]
    f, finv = VARS[label]
    xs = [f(VAL[e]) for e in used]
    ys = [D[e] for e in used]
    xv, yv, c = vertex(xs, ys)
    lo, hi = min(xs), max(xs)
    return used, adjacent, finv(xv), yv, lo <= xv <= hi, c > 0


def selftest():
    u = 1e-4
    quad = {"5": 10.0, "6": 9.0, "7": 8.0, "8.5": 8.5, "10": 9.5, "14": 11.0, "20": 12.0, "inf": 13.0}
    bad = 0
    # a clear minimum at 7: bracket (6, 7, 8.5); k_c 39 moved by 1e-2 u
    d23 = {e: v * u for e, v in quad.items()}
    d39 = {e: (v + 0.01) * u for e, v in quad.items()}
    got = analyse(d23, d39)[1]
    ok = got == [("6", "7", "8.5")]
    print(f"  planted clear minimum at 7: brackets {got} {'ok' if ok else 'WRONG'}")
    bad += not ok
    # the sign of s(7, 8.5) flips between the resolutions: open at 7, so no bracket there
    flip = dict(d23, **{"8.5": 7.5 * u})
    got = analyse(d23, flip)[1]
    ok = ("6", "7", "8.5") not in got
    print(f"  planted sign flip of s(7,8.5): brackets {got} {'ok' if ok else 'WRONG'}")
    bad += not ok
    # exact parabolas in eta: vertex 7.3, Delta 0.46; recovered to 1e-10 in eta, and the three points are neighbours
    D = {e: 0.46 + 1e-6 * (VAL[e] - 7.3) ** 2 for e in FIVE}
    used, adj, em, dm, inside, conv = parabola(D, "eta")
    ok = adj and used == ["6", "7", "8.5"] and abs(em - 7.3) < 1e-9 and abs(dm - 0.46) < 1e-12 and inside and conv
    print(f"  planted parabola in eta (vertex 7.3, 0.46): used {used}, eta_min {em:.10f}, Delta_min {dm:.12f}, inside {inside} {'ok' if ok else 'WRONG'}")
    bad += not ok
    # exact parabola in ln eta, vertex at ln 7.3: the eta parabola is off by more than the ln eta one
    D2 = {e: 0.46 + 1e-6 * (math.log(VAL[e]) - math.log(7.3)) ** 2 for e in FIVE}
    r_eta, r_ln = parabola(D2, "eta"), parabola(D2, "ln eta")
    ok = abs(r_ln[2] - 7.3) < 1e-9 and abs(r_eta[2] - 7.3) > 1e-4
    print(f"  planted parabola in ln eta: ln-eta fit {r_ln[2]:.10f}, eta fit {r_eta[2]:.6f} (the variable matters) {'ok' if ok else 'WRONG'}")
    bad += not ok
    # a vertex outside the span: a parabola with its minimum at eta = 3 gives smallest points 5, 6, 7 and the vertex 3 is flagged
    D3 = {e: 0.46 + 1e-6 * (VAL[e] - 3.0) ** 2 for e in FIVE}
    used, adj, em, dm, inside, conv = parabola(D3, "eta")
    ok = used == ["5", "6", "7"] and abs(em - 3.0) < 1e-9 and not inside
    print(f"  planted vertex outside the span (3.0): used {used}, eta_min {em:.6f}, inside {inside} {'ok' if ok else 'WRONG'}")
    bad += not ok
    # three smallest not neighbours: Delta small at 5 and 10 and large between: reported as not adjacent
    D4 = {"5": 0.46, "6": 0.47, "7": 0.48, "8.5": 0.47, "10": 0.4601}
    used, adj, *_ = parabola(D4, "eta")
    ok = not adj
    print(f"  planted non-adjacent smallest: adjacent {adj}, used {used} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def last(path):
    if not os.path.exists(path):
        return None
    return [json.loads(ln) for ln in open(path) if ln.strip()][-1]


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    k15 = json.load(open(os.path.join(D623, "kc15_values.json")))
    R = {15: {}, 23: {}, 39: {}}
    for e, L in (("5", "5.0000"), ("10", "10.0000"), ("inf", "inf")):
        R[15][e] = dict(Delta=k15[L]["Delta"], F=k15[L]["F"], constraint=k15[L]["constraint"], N=k15[L]["N"])
        for kc in (23, 39):
            R[kc][e] = last(os.path.join(D623, "data", f"sigdss_refine_i623_kc{kc}_eta{L}.jsonl"))
    R[15]["20"] = last(os.path.join(D630, "data", "sigdss_i630.jsonl"))
    R[15]["7"], R[15]["14"] = (last(os.path.join(D631, "data", f"sigdss_i631{x}.jsonl")) for x in "ab")
    R[15]["6"], R[15]["8.5"] = (last(os.path.join(HERE, "data", f"sigdss_i633{x}.jsonl")) for x in "ab")
    for kc in (23, 39):
        R[kc]["20"] = last(os.path.join(D630, "data", f"sigdss_refine_i630_kc{kc}_eta20.jsonl"))
        for e in ("7", "14"):
            R[kc][e] = last(os.path.join(D631, "data", f"sigdss_refine_i631_kc{kc}_eta{e}.jsonl"))
        for e in ("6", "8.5"):
            R[kc][e] = last(os.path.join(HERE, "data", f"sigdss_refine_i633_kc{kc}_eta{e}.jsonl"))
    if "--shift" in sys.argv:
        i = sys.argv.index("--shift")
        e, x = sys.argv[i + 1], float(sys.argv[i + 2])
        R[39][e] = dict(R[39][e], Delta=R[39][e]["Delta"] + x)
        print(f"MUTATION: Delta({e}) at k_c 39 shifted by {x:+.1e}\n")
    fmt = lambda v, f: "n/a" if v is None else f % v
    print("| eta | k_c | N | Delta | F | constraint |\n|---|---|---|---|---|---|")
    for e in ETAS:
        for kc in (15, 23, 39):
            r = R[kc][e]
            print(f"| {e} | {kc} | " + ("| not yet | | |" if r is None else f"{r.get('N') or ''} | {r['Delta']:.10f} | {fmt(r.get('F'), '%.2e')} | {fmt(r.get('constraint'), '%.4e')} |"))
    new = [R[kc][e] for kc in (23, 39) for e in ("6", "8.5")]
    conts = [R[15][e] for e in ("6", "8.5")]
    print(f"\ncontinuations present: {sum(c is not None for c in conts)} of 2 (target landed: {[bool(c and c.get('target')) for c in conts]}, F {[fmt(c and c.get('F'), '%.2e') for c in conts]}); "
          f"new refines present and converged (F < 1e-10): {all(r is not None and r['F'] < 1e-10 for r in new) if all(new) else 'n/a until all 4 are present'}")
    if not all(R[kc][e] for kc in (23, 39) for e in ETAS):
        return
    D = {kc: {e: R[kc][e]["Delta"] for e in ETAS} for kc in (23, 39)}
    rows, brackets = analyse(D[23], D[39])
    print("\n| neighbouring pair s = Delta(next) - Delta(first) | s at k_c 23 | s at k_c 39 | change c | status |\n|---|---|---|---|---|")
    for (a, b), s23, s39, ok, c in rows:
        print(f"| ({a}, {b}) | {s23:+.3e} | {s39:+.3e} | {c:.3e} | {'RESOLVED ' + ('rise' if s23 > 0 else 'fall') if ok else 'OPEN'} |")
    print("\neta of the smallest Delta: " + ", ".join(f"k_c {kc} {min(ETAS, key=lambda e: D[kc][e])}" for kc in (23, 39)))
    if brackets:
        for lo, m, hi in brackets:
            print(f"BRACKET: the minimum lies between eta = {lo} and eta = {hi} (Delta falls into eta = {m} and rises out of it, both resolved)")
    else:
        print(f"NO BRACKET by the rule; open differences: {[f'({a},{b})' for (a, b), _, _, ok, _ in rows if not ok] or 'none'}")
    for kc in (23, 39):
        print(f"order of Delta at k_c {kc} (low to high): " + " < ".join(f"Delta({e})" for e in sorted(ETAS, key=lambda e: D[kc][e])))
    print("\nparabola through the three smallest of eta = 5, 6, 7, 8.5, 10 (primary variable eta):\n| variable | k_c | points used | adjacent | eta_min | Delta_min | vertex inside span |\n|---|---|---|---|---|---|---|")
    res = {}
    for label in VARS:
        for kc in (23, 39):
            used, adj, em, dm, inside, conv = parabola(D[kc], label)
            res[(label, kc)] = (em, dm)
            print(f"| {label} | {kc} | {','.join(used)} | {adj} | {em:.4f} | {dm:.10f} | {inside}{'' if conv else ' (CONCAVE)'} |")
    em23, dm23 = res[("eta", 23)]
    em39, dm39 = res[("eta", 39)]
    print(f"\nprimary (eta): eta_min {em23:.4f} (k_c 23), {em39:.4f} (k_c 39), change {em39 - em23:+.4f}; Delta_min {dm23:.10f}, {dm39:.10f}, change {dm39 - dm23:+.3e}")
    for kc in (23, 39):
        v = [res[(label, kc)][0] for label in VARS]
        print(f"spread of eta_min over the three variables at k_c {kc}: {min(v):.4f} to {max(v):.4f} (width {max(v) - min(v):.4f})")


if __name__ == "__main__":
    main()
