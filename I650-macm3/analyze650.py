#!/usr/bin/env python3
"""#650: Delta(eta) at M 64 against M 48 at the six couplings of this task, and the fit's eta_min at M 64 against M 48's.
M 48 and the M 64 records of eta = 7 and inf: I639-mac/data/sm_records.jsonl (the last converged record of each eta and M); the six M 64 records: data/sm_records.jsonl of this folder.
Delta = Delta_hi + Delta_lo (exact; the 'Delta' string of the old records has the hi part only). The fit is matter/sigma_ms/fit_min.py's own (fit_all, summarize: polynomials in eps = 1/eta of degree 4 to 7
through the eight couplings eta = 5, 6, 7, 8.5, 10, 14, 20, inf, the degree-6 minimum quoted), imported; fit_min.py's main loops over M = 32 and 48 only, so this script applies it to M 64.
Usage: python3 analyze650.py [I639 records] [this folder's records]"""
import json, os, sys
import mpmath as mp
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-b650/matter/sigma_ms")
import fit_min as fm
mp.mp.dps = 40
here = os.path.dirname(os.path.abspath(__file__))
r639 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "I639-mac", "data", "sm_records.jsonl")
r650 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "data", "sm_records.jsonl")
best = {}   # (M, eta) -> record, the last converged one; this task's records override I639's
for path in (r639, r650):
    for l in open(path):
        r = json.loads(l)
        if r.get("converged") and r["eta"] in fm.ETAS: best[(r["M"], r["eta"])] = r
D = lambda M, e: mp.mpf(best[(M, e)]["Delta_hi"]) + mp.mpf(best[(M, e)]["Delta_lo"])
new = ["5", "6", "8.5", "10", "14", "20"]
print("| eta | Delta at M 48 | Delta at M 64 | M 64 − M 48 | within 3e-11 | |F| at M 64 | source of the M 64 record |")
print("|---|---|---|---|---|---|---|")
ok = True
for e in fm.ETAS:
    if (64, e) not in best: print(f"| {e} | {mp.nstr(D(48, e), 20)} | missing | | | | |"); continue
    d = D(64, e) - D(48, e)
    src = "this task" if e in new else "I639-mac"
    flag = abs(d) <= mp.mpf("3e-11")
    if e in new: ok &= flag
    print(f"| {e} | {mp.nstr(D(48, e), 20)} | {mp.nstr(D(64, e), 20)} | {mp.nstr(d, 4)} | {'yes' if flag else 'NO'} | {best[(64, e)]['F']:.1e} | {src} |")
print(f"\nacceptance 1 (|M64 - M48| <= 3e-11 at each of the six): {'PASS' if ok else 'FAIL'}")
fits = {}
for M in (48, 64):
    if all((M, e) in best for e in fm.ETAS):
        eps = [fm.eps_of(e) for e in fm.ETAS]
        fits[M] = fm.fit_all(eps, [D(M, e) for e in fm.ETAS])
        s = fm.summarize(fits[M])
        print(f"M {M}: " + ", ".join(f"d{d} eta_min {fits[M][d]['eta_min']:.7f}" for d in fm.DEGREES) + f"; quoted (d{fm.QUOTED}) eta_min {s['eta_min']:.7f}, Delta_min {s['Delta_min']}, residual {s['residual']:.1e}")
if 48 in fits and 64 in fits:
    e48 = fm.summarize(fits[48])["eta_min"]; e64 = fm.summarize(fits[64])["eta_min"]
    print(f"\nacceptance 2: eta_min(M 64) − eta_min(M 48) = {e64 - e48:+.3e} (limit 2e-6): {'PASS' if abs(e64 - e48) <= 2e-6 else 'FAIL'}")
    for d in fm.DEGREES:
        print(f"  degree {d}: {fits[64][d]['eta_min'] - fits[48][d]['eta_min']:+.3e}")
    D48 = fm.summarize(fits[48])["Delta_min_f"]; D64 = fm.summarize(fits[64])["Delta_min_f"]
    print(f"Delta_min(M 64) − Delta_min(M 48) = {mp.nstr(D64 - D48, 4)}")
