#!/usr/bin/env python3
"""#1025 win2b, the D 18.0625 scan above the first window (lambda 1.95 to 2.35 at 0.01, 41 points, two processes with 1.95 first in both): merge A and B, check the repeated point.
usage: merge_up.py SCAN_A.jsonl SCAN_B.jsonl MERGED.jsonl PRIOR_SCAN.jsonl
The same bar and the same logic as winb's merge_d18mid_1025.py (raw I1025-win/d18mid, blob b8b47a44), with the window as here. REPEAT CHECK (the gate): the two records at lambda 1.95
have the same hybrid sign and |ln|det| difference| <= 1e-6. The merged file (each lambda once, ascending, the repeated point from A) is written only if that check passes, every record
is at D 18.0625, and every lambda from 1.95 to 2.35 is present. PRIOR SCAN (information, not a gate): the record at 1.95 of the first window's merged scan, compared with A's at the same bar."""
import json, os, sys
D, LO, N, REP, BAR = 18.0625, 1.95, 41, 1.95, 1e-6
load = lambda f: [json.loads(l) for l in open(f) if l.strip()] if os.path.exists(f) else []
A, B, prior = load(sys.argv[1]), load(sys.argv[2]), load(sys.argv[4])
key = lambda r: round(r["lam"], 2)
a = {key(r): r for r in A}; b = {key(r): r for r in B}
print(f"A: {len(A)} records, B: {len(B)} records")
wrongD = [r["lam"] for r in A + B if abs(r["D"] - D) > 1e-9]
if wrongD:
    print(f"records at a D other than {D}: lambda {wrongD} -> no merged scan")
rep = sorted(set(a) & set(b))
ok = bool(rep) and rep == [REP] and not wrongD
for k in rep:
    x, y = a[k], b[k]
    d = abs(x["ln"] - y["ln"])
    good = x["sign"] == y["sign"] and d <= BAR
    ok = ok and good
    print(f"REPEAT CHECK at lambda {k}: sign A {x['sign']:+.0f} B {y['sign']:+.0f}; ln|det| A {x['ln']!r} B {y['ln']!r}, difference {d:.3e} (bar 1e-6); noise robust A {x['noise_robust']} B {y['noise_robust']}; "
          f"float64 sign A {x['f64_sign']:+.0f} B {y['f64_sign']:+.0f}; {x['sec']} s and {y['sec']} s -> {'PASS' if good else 'FAIL'}")
if not rep:
    print("REPEAT CHECK: no repeated point in both files -> FAIL")
elif rep != [REP]:
    print(f"REPEAT CHECK: the points in both files are {rep}, not [{REP}] -> FAIL")
pr = [r for r in prior if key(r) == REP]
if pr and REP in a:
    p, x = pr[-1], a[REP]
    d = abs(p["ln"] - x["ln"])
    print(f"PRIOR SCAN at lambda {REP} (the first window's merged scan, D {p['D']}): sign {p['sign']:+.0f} against A's {x['sign']:+.0f}; ln|det| {p['ln']!r} against {x['ln']!r}, difference {d:.3e} "
          f"(bar 1e-6) -> {'AGREES' if p['sign'] == x['sign'] and d <= BAR else 'DIFFERS'} (information, not a gate)")
else:
    print(f"PRIOR SCAN at lambda {REP}: not available in one of the files (information)")
want = [round(LO + 0.01 * i, 2) for i in range(N)]
miss = [w for w in want if w not in a and w not in b]
if miss:
    print(f"missing lambda: {miss} -> no merged scan")
elif ok:
    M = sorted(({**b, **a}).values(), key=lambda r: r["lam"])
    open(sys.argv[3], "w", newline="\n").write("".join(json.dumps(r) + "\n" for r in M))
    print(f"merged {len(M)} points ({LO:.2f} to {want[-1]:.2f}) into {sys.argv[3]}")
else:
    print("the repeat check failed: no merged scan")
