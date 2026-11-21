#!/usr/bin/env python3
"""#1025 win2b, the finer D 18.5 scan at k_c 55 (lambda 1.660 to 1.700 at 0.002) in two processes with 1.680 first in both: merge A and B, check the repeated point.
The same logic and bar as merge_scan.py of this folder (blob 378ccc17), with the step as an argument and lambda keyed to three decimals.
usage: merge_fine.py LO N STEP REP D SCAN_A.jsonl SCAN_B.jsonl MERGED.jsonl PRIOR.jsonl     (lambda LO + STEP i for i < N; REP first in both files; D the record's D)
REPEAT CHECK (the gate): the two records at REP have the same hybrid sign and |ln|det| difference| <= 1e-6. The merged file (each lambda once, ascending, the repeated point from A) is written only if
that check passes, the two files share exactly the point REP, every record is at D and every lambda of the window is present. PRIOR (information, not a gate): every lambda of the merged window that
the prior (0.01) scan also holds is compared with it, sign and |ln|det| difference| <= 1e-6 -> AGREES or DIFFERS."""
import json, os, sys
LO, N, STEP, REP, D = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
BAR = 1e-6
load = lambda f: [json.loads(l) for l in open(f) if l.strip()] if os.path.exists(f) else []
A, B, prior = load(sys.argv[6]), load(sys.argv[7]), load(sys.argv[9])
key = lambda r: round(r["lam"], 3)
a = {key(r): r for r in A}; b = {key(r): r for r in B}
print(f"A: {len(A)} records, B: {len(B)} records")
wrongD = [r["lam"] for r in A + B if abs(r["D"] - D) > 1e-9]
if wrongD:
    print(f"records at a D other than {D}: lambda {wrongD} -> no merged scan")
rep = sorted(set(a) & set(b))
ok = rep == [round(REP, 3)] and not wrongD
for k in rep:
    x, y = a[k], b[k]
    d = abs(x["ln"] - y["ln"])
    good = x["sign"] == y["sign"] and d <= BAR
    ok = ok and good
    print(f"REPEAT CHECK at lambda {k:.3f}: sign A {x['sign']:+.0f} B {y['sign']:+.0f}; ln|det| A {x['ln']!r} B {y['ln']!r}, difference {d:.3e} (bar 1e-6); noise robust A {x['noise_robust']} B {y['noise_robust']}; "
          f"float64 sign A {x['f64_sign']:+.0f} B {y['f64_sign']:+.0f}; {x['sec']} s and {y['sec']} s -> {'PASS' if good else 'FAIL'}")
if not rep:
    print("REPEAT CHECK: no repeated point in both files -> FAIL")
elif rep != [round(REP, 3)]:
    print(f"REPEAT CHECK: the points in both files are {rep}, not [{round(REP, 3)}] -> FAIL")
allr = {**b, **a}
pk = {key(r): r for r in prior}
for k in sorted(set(allr) & set(pk)):
    p, x = pk[k], allr[k]
    d = abs(p["ln"] - x["ln"])
    print(f"PRIOR SCAN at lambda {k:.3f} (the 0.01 scan, D {p['D']}): sign {p['sign']:+.0f} against {x['sign']:+.0f}; ln|det| {p['ln']!r} against {x['ln']!r}, difference {d:.3e} (bar 1e-6) -> "
          f"{'AGREES' if p['sign'] == x['sign'] and d <= BAR else 'DIFFERS'} (information, not a gate)")
want = [round(LO + STEP * i, 3) for i in range(N)]
miss = [w for w in want if w not in allr]
if miss:
    print(f"missing lambda: {miss} -> no merged scan")
elif ok:
    M = sorted(allr.values(), key=lambda r: r["lam"])
    open(sys.argv[8], "w", newline="\n").write("".join(json.dumps(r) + "\n" for r in M))
    print(f"merged {len(M)} points ({want[0]:.3f} to {want[-1]:.3f}) into {sys.argv[8]}")
else:
    print("the repeat check failed: no merged scan")
