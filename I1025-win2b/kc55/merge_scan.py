#!/usr/bin/env python3
"""#1025 win2b, the D 18.5 scan at k_c 55 in two processes with one point repeated as the check: merge A and B, check the repeated point. The same logic and bar as merge_up.py of
I1025-win2b/d18mid (and winb's merge_d18mid_1025.py, raw I1025-win/d18mid, blob b8b47a44), with the window as arguments.
usage: merge_scan.py LO N REP D SCAN_A.jsonl SCAN_B.jsonl MERGED.jsonl     (lambda LO + 0.01 i for i < N; REP is the point first in both files; D the record's D)
REPEAT CHECK (the gate): the two records at REP have the same hybrid sign and |ln|det| difference| <= 1e-6. The merged file (each lambda once, ascending, the repeated point from A) is written
only if that check passes, the two files share exactly the one point REP, every record is at D and every lambda of the window is present."""
import json, os, sys
LO, N, REP, D = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
BAR = 1e-6
load = lambda f: [json.loads(l) for l in open(f) if l.strip()] if os.path.exists(f) else []
A, B = load(sys.argv[5]), load(sys.argv[6])
key = lambda r: round(r["lam"], 2)
a = {key(r): r for r in A}; b = {key(r): r for r in B}
print(f"A: {len(A)} records, B: {len(B)} records")
wrongD = [r["lam"] for r in A + B if abs(r["D"] - D) > 1e-9]
if wrongD:
    print(f"records at a D other than {D}: lambda {wrongD} -> no merged scan")
rep = sorted(set(a) & set(b))
ok = rep == [round(REP, 2)] and not wrongD
for k in rep:
    x, y = a[k], b[k]
    d = abs(x["ln"] - y["ln"])
    good = x["sign"] == y["sign"] and d <= BAR
    ok = ok and good
    print(f"REPEAT CHECK at lambda {k}: sign A {x['sign']:+.0f} B {y['sign']:+.0f}; ln|det| A {x['ln']!r} B {y['ln']!r}, difference {d:.3e} (bar 1e-6); noise robust A {x['noise_robust']} B {y['noise_robust']}; "
          f"float64 sign A {x['f64_sign']:+.0f} B {y['f64_sign']:+.0f}; {x['sec']} s and {y['sec']} s -> {'PASS' if good else 'FAIL'}")
if not rep:
    print("REPEAT CHECK: no repeated point in both files -> FAIL")
elif rep != [round(REP, 2)]:
    print(f"REPEAT CHECK: the points in both files are {rep}, not [{round(REP, 2)}] -> FAIL")
want = [round(LO + 0.01 * i, 2) for i in range(N)]
miss = [w for w in want if w not in a and w not in b]
if miss:
    print(f"missing lambda: {miss} -> no merged scan")
elif ok:
    M = sorted(({**b, **a}).values(), key=lambda r: r["lam"])
    open(sys.argv[7], "w", newline="\n").write("".join(json.dumps(r) + "\n" for r in M))
    print(f"merged {len(M)} points ({want[0]:.2f} to {want[-1]:.2f}) into {sys.argv[7]}")
else:
    print("the repeat check failed: no merged scan")
