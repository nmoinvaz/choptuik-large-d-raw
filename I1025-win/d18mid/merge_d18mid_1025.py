#!/usr/bin/env python3
"""#1025 winb, the D 18.125 scan split in two processes: merge A and B and check the repeated point.
usage: merge_d18mid_1025.py SCAN_A.jsonl SCAN_B.jsonl MERGED.jsonl
The repeated point (lambda 1.82, first in both halves): REPEAT CHECK passes if the two records have the same hybrid sign and |ln|det| difference| <= 1e-6 (the coordinator's
bar); the noise flags and the float64 signs are printed too. The merged file has each lambda once, ascending (the repeated point from A); it is written only if
the check passes and every lambda from 1.70 to 1.95 at 0.01 is present."""
import json, sys
A = [json.loads(l) for l in open(sys.argv[1]) if l.strip()] if __import__("os").path.exists(sys.argv[1]) else []
B = [json.loads(l) for l in open(sys.argv[2]) if l.strip()] if __import__("os").path.exists(sys.argv[2]) else []
key = lambda r: round(r["lam"], 2)
a = {key(r): r for r in A}; b = {key(r): r for r in B}
print(f"A: {len(A)} records, B: {len(B)} records")
rep = sorted(set(a) & set(b))
ok = bool(rep)
for k in rep:
    x, y = a[k], b[k]
    d = abs(x["ln"] - y["ln"])
    good = x["sign"] == y["sign"] and d <= 1e-6
    ok = ok and good
    print(f"REPEAT CHECK at lambda {k}: sign A {x['sign']:+.0f} B {y['sign']:+.0f}; ln|det| A {x['ln']!r} B {y['ln']!r}, difference {d:.3e} (bar 1e-6); noise robust A {x['noise_robust']} B {y['noise_robust']}; "
          f"float64 sign A {x['f64_sign']:+.0f} B {y['f64_sign']:+.0f}; {x['sec']} s and {y['sec']} s -> {'PASS' if good else 'FAIL'}")
if not rep:
    print("REPEAT CHECK: no repeated point in both files -> FAIL")
want = [round(1.70 + 0.01 * i, 2) for i in range(26)]
miss = [w for w in want if w not in a and w not in b]
if miss:
    print(f"missing lambda: {miss} -> no merged scan")
elif ok:
    M = sorted(({**b, **a}).values(), key=lambda r: r["lam"])
    open(sys.argv[3], "w", newline="\n").write("".join(json.dumps(r) + "\n" for r in M))
    print(f"merged {len(M)} points (1.70 to 1.95) into {sys.argv[3]}")
else:
    print("the repeat check failed: no merged scan")
