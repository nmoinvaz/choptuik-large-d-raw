#!/usr/bin/env python3
"""Is the asymmetry of sym_582.py exactly where the cached conjugate points are not bit-for-bit conjugates? Counts the matched points (rounded to 9 digits) by
(Re identical and Im exactly negated, or not) x (|d ln|det|| > 1e-9, or not). Pass: no bit-identical conjugate point is asymmetric and no non-identical one is symmetric.
--mutate=bump adds 1e-6 to ln|det| of the lower value at the first 5 bit-identical points, which must make the check fail (exit 1).
usage: python ulp_split_582.py [--mutate=bump]"""
import glob, json, sys
RAW = "D:/choptuik-large-d-raw"
def load(f): return [json.loads(l) for l in open(glob.glob(f"{RAW}/{f}/modecount_*_evals.jsonl")[0])]
ns = {}
exec(open(f"{RAW}/I582-win2/sym_582.py").read().split("def load")[0].split('"""', 2)[2], ns)
cnt = {(a, b): 0 for a in (True, False) for b in (True, False)}  # (bit-identical conjugate, asymmetric)
seen, bumped = set(), 0
for lo, up in ns["PAIRS"]:
    Uk = {(round(r["re"], 9), round(r["im"], 9)): r for r in load(up)}
    for r in load(lo):
        k = (round(r["re"], 9), round(r["im"], 9))
        u = Uk.get((k[0], -k[1]))
        if u is None or (lo, k) in seen:
            continue
        seen.add((lo, k))
        same = r["re"] == u["re"] and r["im"] == -u["im"]
        d = abs(r["lnabs"] - u["lnabs"])
        if "--mutate=bump" in sys.argv and same and bumped < 5:
            d, bumped = d + 1e-6, bumped + 1
        cnt[(same, d > 1e-9)] += 1
print("bit-identical conjugate & symmetric %d | bit-identical & asymmetric %d | not bit-identical & symmetric %d | not bit-identical & asymmetric %d" % (cnt[(True, False)], cnt[(True, True)], cnt[(False, False)], cnt[(False, True)]))
ok = cnt[(True, True)] == 0 and cnt[(False, False)] == 0
print("pass" if ok else "FAIL")
sys.exit(0 if ok else 1)
