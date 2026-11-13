#!/usr/bin/env python3
"""#623: the table of Delta, F and the constraint at each (eta, k_c) and the verdict of the issue's rule.
usage: python table_623.py [--selftest] [--shift X]       (from this folder; needs kc15_values.json and data/sigdss_refine_i623_kc{23,39}_eta*.jsonl here)
Rule (written in README.md before the data): d_kc = Delta_kc(5) - Delta_kc(inf); c = |d_39 - d_23|; the question is ANSWERED when every run converged (F < 1e-10),
sign(d_23) = sign(d_39), |d_23| > c and |d_39| > c; otherwise it stays OPEN. The same d and c are printed for eta = 10 and 2 (outside the rule).
--selftest runs the verdict on planted (d_23, d_39) pairs with known answers, including the ones that must fail. --shift X adds X to Delta(5) at k_c 39 (a mutation: the verdict must be able to change)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ETAS = ("inf", "10.0000", "5.0000", "2.0000")
MAC_KC23_INF = 0.4598654552          # data/sigdss_log_d4eta_kc23_aborted.txt (the Mac)


def verdict(d23, d39):
    """(answered, why) for the planted or measured differences."""
    c = abs(d39 - d23)
    if (d23 > 0) != (d39 > 0):
        return False, f"signs differ (d_23 {d23:+.3e}, d_39 {d39:+.3e})"
    if not (abs(d23) > c and abs(d39) > c):
        return False, f"a difference does not exceed c = {c:.3e} (|d_23| {abs(d23):.3e}, |d_39| {abs(d39):.3e})"
    return True, f"same sign {'+' if d23 > 0 else '-'}, |d_23| {abs(d23):.3e} and |d_39| {abs(d39):.3e} both exceed c = {c:.3e}"


def selftest():
    cases = [((-6e-5, -7e-5), True), ((6e-5, -7e-5), False), ((-6e-5, -1.5e-4), False), ((-1e-4, -1e-4 - 2e-4), False), ((3e-5, 3.2e-5), True), ((0.0, 1e-9), False)]
    bad = 0
    for (a, b), want in cases:
        got = verdict(a, b)[0]
        print(f"  planted d_23 {a:+.1e}, d_39 {b:+.1e}: {'answered' if got else 'open'} (expected {'answered' if want else 'open'}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def rec(kc, e):
    p = os.path.join(HERE, "data", f"sigdss_refine_i623_kc{kc}_eta{e}.jsonl")
    if not os.path.exists(p):
        return None
    return [json.loads(ln) for ln in open(p) if ln.strip()][-1]


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    shift = float(sys.argv[sys.argv.index("--shift") + 1]) if "--shift" in sys.argv else 0.0
    k15 = json.load(open(os.path.join(HERE, "kc15_values.json")))
    R = {15: {e: dict(Delta=k15[e]["Delta"], F=k15[e]["F"], constraint=k15[e]["constraint"], N=k15[e]["N"], solve_seconds=None) for e in ETAS}}
    for kc in (23, 39):
        R[kc] = {e: rec(kc, e) for e in ETAS}
    if shift and R[39]["5.0000"]:
        R[39]["5.0000"] = dict(R[39]["5.0000"], Delta=R[39]["5.0000"]["Delta"] + shift)
        print(f"MUTATION: Delta(5) at k_c 39 shifted by {shift:+.1e}")
    print("| eta | k_c | N | Delta | F | constraint | solve s |\n|---|---|---|---|---|---|---|")
    for e in ETAS:
        for kc in (15, 23, 39):
            r = R[kc][e]
            if r is None:
                print(f"| {e} | {kc} | | not yet | | | |")
                continue
            print(f"| {e} | {kc} | {r['N']} | {r['Delta']:.10f} | {r['F']:.2e} | {r['constraint']:.4e} | {r['solve_seconds'] if r['solve_seconds'] is not None else '(seed)'} |")
    allr = [R[kc][e] for kc in (23, 39) for e in ETAS]
    done = all(r is not None for r in allr)
    conv = done and all(r["F"] < 1e-10 for r in allr)
    print(f"\nruns present: {sum(r is not None for r in allr)} of 8; every run converged (F < 1e-10): {conv if done else 'n/a until all 8 are present'}")
    if R[23]["inf"]:
        print(f"eta = inf at k_c 23: Delta {R[23]['inf']['Delta']:.10f} against the Mac's {MAC_KC23_INF:.10f}: difference {R[23]['inf']['Delta'] - MAC_KC23_INF:+.2e}")
    print("\n| eta | Delta - Delta(inf) at k_c 15 | at k_c 23 | at k_c 39 | c = abs(d_39 - d_23) |\n|---|---|---|---|---|")
    d = {}
    for e in ETAS[1:]:
        row = []
        for kc in (15, 23, 39):
            a, b = R[kc][e], R[kc]["inf"]
            row.append(None if a is None or b is None else a["Delta"] - b["Delta"])
        d[e] = row
        c = abs(row[2] - row[1]) if row[1] is not None and row[2] is not None else None
        print(f"| {e} | " + " | ".join("n/a" if v is None else f"{v:+.3e}" for v in row) + f" | {'n/a' if c is None else f'{c:.3e}'} |")
    print("\nchange of each Delta between resolutions:\n| eta | Delta_23 - Delta_15 | Delta_39 - Delta_23 |\n|---|---|---|")
    for e in ETAS:
        a15, a23, a39 = R[15][e], R[23][e], R[39][e]
        print(f"| {e} | {a23['Delta'] - a15['Delta']:+.3e} | " + ("n/a" if a39 is None or a23 is None else f"{a39['Delta'] - a23['Delta']:+.3e}") + " |")
    if d["5.0000"][1] is not None and d["5.0000"][2] is not None:
        ok, why = verdict(d["5.0000"][1], d["5.0000"][2])
        print(f"\nVERDICT (rule on eta = 5): {'ANSWERED' if ok and conv else ('OPEN' if not ok else 'OPEN (not every run converged)')}: {why}")
        print(f"sign of Delta(5) - Delta(inf): k_c 23 {'+' if d['5.0000'][1] > 0 else '-'}, k_c 39 {'+' if d['5.0000'][2] > 0 else '-'}")
    o = [None if R[kc]["5.0000"] is None or R[kc]["10.0000"] is None else R[kc]["5.0000"]["Delta"] - R[kc]["10.0000"]["Delta"] for kc in (15, 23, 39)]
    print("(outside the rule) Delta(5) - Delta(10) at k_c 15, 23, 39: " + ", ".join("n/a" if v is None else f"{v:+.3e}" for v in o))
    for e in ("10.0000", "2.0000"):
        if d[e][1] is not None and d[e][2] is not None:
            print(f"(outside the rule) eta = {e}: {verdict(d[e][1], d[e][2])[1]}")


if __name__ == "__main__":
    main()
