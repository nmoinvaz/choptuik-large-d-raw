#!/usr/bin/env python3
"""#1025 winb follow-on: the dd sign check of a hybrid root (the coordinator's amendment, 2026-11-21 06:30 UTC and his order after it).
usage: read_ddB_1025.py LO.jsonl HI.jsonl ROOT        (the det records of ell_ddm.py det at ROOT - 0.02 and ROOT + 0.02; prints the reading)
A dd sign COUNTS at a lambda if its 5 exact variants agree and relative noise 1e-24 on the dd propagator entries leaves it unchanged (both seeds), as in
raw I1025-mac/dd_signtest_D17.5_criteria.log and d18_dd_criteria.log; the noise at 1e-20 and 1e-16 is information.
Reading (the coordinator's, fixed before the run): minus at the lower point and plus at the upper: the root passes. The same sign at both: no
root between them. A sign that does not count at either point: neither reading applies, and that is reported."""
import json, sys
def rec(fn):
    r = [json.loads(l) for l in open(fn) if l.strip()]
    return r[-1] if r else None
lo, hi, root = rec(sys.argv[1]), rec(sys.argv[2]), float(sys.argv[3])
def sign(r):
    if r is None:
        return None, False, "no record"
    s = {x["sign"] for x in r["dd"]}
    agree = len(s) == 1
    n24 = [e for e in (r.get("noise") or []) if abs(e["eps"] - 1e-24) < 1e-30]
    n24ok = bool(n24) and all(x == r["dd"][0]["sign"] for x in n24[0]["signs"])
    info = {f"{e['eps']:g}": e["signs"] for e in (r.get("noise") or [])}
    return (r["dd"][0]["sign"] if agree else None), (agree and n24ok), f"5 variants {[x['sign'] for x in r['dd']]} agree {agree}, noise {info}, ln|det| {r['dd'][0]['ln']:.10f}, float64 sign {r.get('f64_sign')}"
(sl, cl, tl), (sh, ch, th) = sign(lo), sign(hi)
mism = [n for n, r, x in (("lower", lo, root - 0.02), ("upper", hi, root + 0.02)) if r is not None and abs(r["lam"] - x) > 1e-9]
print(f"root {root!r}: lower point {root - 0.02!r} (record lam {lo and lo['lam']!r}): dd sign {sl}, counts {cl}; {tl}")
print(f"           upper point {root + 0.02!r} (record lam {hi and hi['lam']!r}): dd sign {sh}, counts {ch}; {th}")
if mism:
    out = "NEITHER READING APPLIES: the record lambda differs from root -/+ 0.02 at the " + " and ".join(mism) + " point"
elif not (cl and ch):
    out = "NEITHER READING APPLIES: a dd sign does not count at " + ("the lower" if not cl else "") + (" and " if not (cl or ch) else "") + ("the upper" if not ch else "") + " point"
elif sl < 0 < sh:
    out = "ROOT PASSES: minus at the lower point, plus at the upper"
elif sl == sh:
    out = "NO ROOT BETWEEN THEM: the same sign at both points"
else:
    out = f"PLUS at the lower point and MINUS at the upper (signs {sl}, {sh}): not covered by the fixed reading; reported as it stands"
print("DDREAD:", out)
