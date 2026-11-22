#!/usr/bin/env python3
"""#1025 win2b, the k_c break scan at D 18.375: one process per k_c evaluates lambda LO + STEP i (i < N) and then REP again; this checks the repeated point and writes the scan with each lambda once.
usage: merge_repeat.py SCAN.jsonl MERGED.jsonl LO N STEP REP D KC
REPEAT CHECK (the gate): the two records at REP have the same hybrid sign and |ln|det| difference| <= 1e-6 (the bar of the earlier scans). It is a determinism check inside one process (the earlier scans'
repeat check was between two processes). The merged file (each lambda once, ascending, the first record of REP) is written only if the check passes, REP occurs exactly twice and every other lambda once,
every record is at D and k_c KC, and all N lambda are present."""
import json, os, sys
f, out, LO, N, STEP, REP, D, KC = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), int(sys.argv[8])
BAR = 1e-6
R = [json.loads(l) for l in open(f) if l.strip()] if os.path.exists(f) else []
key = lambda r: round(r["lam"], 3)
print(f"{len(R)} records in {os.path.basename(f)}")
wrong = [(r["lam"], r["D"], r["kc"]) for r in R if abs(r["D"] - D) > 1e-9 or r["kc"] != KC]
if wrong:
    print(f"records at another D or k_c than D {D} k_c {KC}: {wrong} -> no merged scan")
cnt = {}
for r in R:
    cnt.setdefault(key(r), []).append(r)
dups = sorted(k for k, v in cnt.items() if len(v) > 1)
ok = dups == [round(REP, 3)] and len(cnt[round(REP, 3)]) == 2 and not wrong
if dups != [round(REP, 3)]:
    print(f"REPEAT CHECK: the lambda occurring more than once are {dups}, not [{round(REP, 3)}] -> FAIL")
for k in dups:
    x, y = cnt[k][0], cnt[k][-1]
    d = abs(x["ln"] - y["ln"])
    good = x["sign"] == y["sign"] and d <= BAR and len(cnt[k]) == 2
    ok = ok and good
    print(f"REPEAT CHECK at lambda {k:.3f}: sign first {x['sign']:+.0f} second {y['sign']:+.0f}; ln|det| first {x['ln']!r} second {y['ln']!r}, difference {d:.3e} (bar 1e-6); noise robust first {x['noise_robust']} second {y['noise_robust']}; "
          f"float64 sign first {x['f64_sign']:+.0f} second {y['f64_sign']:+.0f}; {x['sec']} s and {y['sec']} s -> {'PASS' if good else 'FAIL'}")
want = [round(LO + STEP * i, 3) for i in range(N)]
miss = [w for w in want if w not in cnt]
extra = [k for k in cnt if k not in want]
if miss or extra:
    print(f"missing lambda: {miss}; lambda outside the window: {extra} -> no merged scan")
elif ok:
    M = sorted((v[0] for v in cnt.values()), key=lambda r: r["lam"])
    open(out, "w", newline="\n").write("".join(json.dumps(r) + "\n" for r in M))
    print(f"merged {len(M)} points ({want[0]:.3f} to {want[-1]:.3f}) into {out}")
else:
    print("the repeat check failed: no merged scan")
