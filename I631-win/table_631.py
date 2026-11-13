#!/usr/bin/env python3
"""#631: Delta at eta = 5, 7, 10, 14, 20, inf for k_c 23 and 39, and the bracket of the minimum by the pre-registered rule (README.md).
usage: python table_631.py [--selftest] [--shift ETA X]       (from this folder; needs data/sigdss_i631{a,b}.jsonl, data/sigdss_refine_i631_kc{23,39}_eta{7,14}.jsonl here, and ../I623-win, ../I630-win)
Rule: eta increasing 5, 7, 10, 14, 20, inf; s_i = Delta(eta_{i+1}) - Delta(eta_i) for each neighbouring pair at k_c 23 and 39. s is RESOLVED when its sign is the same at both k_c and its magnitude at both
exceeds its change c = |s_39 - s_23|; else OPEN. The minimum is BRACKETED between eta_{i-1} and eta_{i+1} when s_{i-1} < 0 and s_i > 0 are both resolved. --selftest: planted tables with a known bracket.
--shift ETA X adds X to Delta(ETA) at k_c 39 (a mutation: the bracket must be able to change)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
I623, I630 = os.path.join(HERE, "..", "I623-win"), os.path.join(HERE, "..", "I630-win")
ETAS = ("5", "7", "10", "14", "20", "inf")
LABEL = {"5": "5.0000", "10": "10.0000", "inf": "inf", "20": "20.0000", "7": "7.0000", "14": "14.0000"}


def resolved(a, b):
    c = abs(b - a)
    if (a > 0) != (b > 0):
        return False, c
    return (abs(a) > c and abs(b) > c), c


def analyse(D23, D39):
    """D23, D39: dict eta -> Delta. Returns (list of (pair, s23, s39, resolved, c), brackets, argmins)."""
    rows = []
    for i in range(len(ETAS) - 1):
        a, b = ETAS[i], ETAS[i + 1]
        s23, s39 = D23[b] - D23[a], D39[b] - D39[a]
        ok, c = resolved(s23, s39)
        rows.append(((a, b), s23, s39, ok, c))
    brackets = []
    for i in range(1, len(ETAS) - 1):
        lo, hi = rows[i - 1], rows[i]
        if lo[3] and hi[3] and lo[1] < 0 and lo[2] < 0 and hi[1] > 0 and hi[2] > 0:
            brackets.append((ETAS[i - 1], ETAS[i], ETAS[i + 1]))
    argmin = tuple(min(ETAS, key=lambda e: D[e]) for D in (D23, D39))
    return rows, brackets, argmin


def selftest():
    u = 1e-4
    quad = {"5": 10.0, "7": 9.0, "10": 8.0, "14": 9.0, "20": 10.0, "inf": 11.0}
    cases = []
    # a clear minimum at eta = 10, the k_c 39 table moved by 1e-2 u: bracket (7, 10, 14)
    cases.append(("clear minimum at 10", {e: v * u for e, v in quad.items()}, {e: (v + 0.01) * u for e, v in quad.items()}, [("7", "10", "14")]))
    # eta = 7 and 10 within 0.01 u of each other while k_c 39 moves them by 0.05 u: s(7,10) is open, no bracket
    near = dict(quad, **{"7": 8.005, "10": 8.0})
    near39 = dict(quad, **{"7": 8.0, "10": 8.045})
    cases.append(("7 and 10 not separated", {e: v * u for e, v in near.items()}, {e: v * u for e, v in near39.items()}, []))
    # the sign of s(10, 14) flips between the resolutions: open, no bracket
    flip23 = dict(quad, **{"14": 8.5})
    flip39 = dict(quad, **{"14": 7.5})
    cases.append(("sign flip of s(10,14)", {e: v * u for e, v in flip23.items()}, {e: v * u for e, v in flip39.items()}, []))
    # minimum at the edge, eta = 5: no interior bracket
    mono = {"5": 8.0, "7": 9.0, "10": 10.0, "14": 11.0, "20": 12.0, "inf": 13.0}
    cases.append(("monotone rise from 5", {e: v * u for e, v in mono.items()}, {e: (v + 0.01) * u for e, v in mono.items()}, []))
    bad = 0
    for name, d23, d39, want in cases:
        got = analyse(d23, d39)[1]
        print(f"  planted '{name}': brackets {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def last(path):
    if not os.path.exists(path):
        return None
    return [json.loads(ln) for ln in open(path) if ln.strip()][-1]


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    k15 = json.load(open(os.path.join(I623, "kc15_values.json")))
    R = {15: {}, 23: {}, 39: {}}
    for e in ("5", "10", "inf"):
        L = LABEL[e]
        R[15][e] = dict(Delta=k15[L]["Delta"], F=k15[L]["F"], constraint=k15[L]["constraint"], N=k15[L]["N"])
        for kc in (23, 39):
            R[kc][e] = last(os.path.join(I623, "data", f"sigdss_refine_i623_kc{kc}_eta{L}.jsonl"))
    R[15]["20"] = last(os.path.join(I630, "data", "sigdss_i630.jsonl"))
    for kc in (23, 39):
        R[kc]["20"] = last(os.path.join(I630, "data", f"sigdss_refine_i630_kc{kc}_eta20.jsonl"))
    for e, letter in (("7", "a"), ("14", "b")):
        R[15][e] = last(os.path.join(HERE, "data", f"sigdss_i631{letter}.jsonl"))
        for kc in (23, 39):
            R[kc][e] = last(os.path.join(HERE, "data", f"sigdss_refine_i631_kc{kc}_eta{e}.jsonl"))
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
            print(f"| {e} | {kc} | " + (f"| not yet | | |" if r is None else f"{r.get('N') or ''} | {r['Delta']:.10f} | {fmt(r.get('F'), '%.2e')} | {fmt(r.get('constraint'), '%.4e')} |"))
    new = [R[kc][e] for kc in (23, 39) for e in ("7", "14")]
    conts = [R[15][e] for e in ("7", "14")]
    print(f"\ncontinuations present: {sum(c is not None for c in conts)} of 2 (target landed: {[bool(c and c.get('target')) for c in conts]}, F {[fmt(c and c.get('F'), '%.2e') for c in conts]}); "
          f"new refines present and converged (F < 1e-10): {all(r is not None and r['F'] < 1e-10 for r in new) if all(new) else 'n/a until all 4 are present'}")
    if not all(R[kc][e] for kc in (23, 39) for e in ETAS):
        return
    D23 = {e: R[23][e]["Delta"] for e in ETAS}
    D39 = {e: R[39][e]["Delta"] for e in ETAS}
    rows, brackets, argmin = analyse(D23, D39)
    print("\n| neighbouring pair s = Delta(next) - Delta(first) | s at k_c 23 | s at k_c 39 | change c | status |\n|---|---|---|---|---|")
    for (a, b), s23, s39, ok, c in rows:
        print(f"| ({a}, {b}) | {s23:+.3e} | {s39:+.3e} | {c:.3e} | {'RESOLVED ' + ('rise' if s23 > 0 else 'fall') if ok else 'OPEN'} |")
    print(f"\neta of the smallest Delta: k_c 23 {argmin[0]}, k_c 39 {argmin[1]}")
    if brackets:
        for lo, m, hi in brackets:
            print(f"BRACKET: the minimum lies between eta = {lo} and eta = {hi} (Delta falls into eta = {m} and rises out of it, both resolved)")
    else:
        opn = [f"({a},{b})" for (a, b), _, _, ok, _ in rows if not ok]
        print(f"NO BRACKET by the rule; open differences: {opn or 'none'}")
    for kc, D in ((23, D23), (39, D39)):
        print(f"order of Delta at k_c {kc} (low to high): " + " < ".join(f"Delta({e})" for e in sorted(ETAS, key=lambda e: D[e])))


if __name__ == "__main__":
    main()
