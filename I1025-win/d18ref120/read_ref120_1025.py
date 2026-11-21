#!/usr/bin/env python3
"""#1025 winb, the lambda 1.20 dd check (the coordinator's order, hc 2026-11-21 about 16:1x UTC; his reading fixed before the run):
usage: read_ref120_1025.py DD_D18.jsonl DD_D18.0625.jsonl      (the det records of ell_ddm.py det at lambda 1.20 on D 18's and D 18.0625's states)
The hybrid at lambda 1.20 (xfkappa's d18_refsign_1025.jsonl, raw blob 3e2d8b4e; noise-robust, the Mac): D 18 minus, D 18.0625 plus.
Reading: dd equal to the hybrid at both (D 18 minus, D 18.0625 plus) confirms a root crossing 1.20 between them. dd differing from the hybrid at either means a
structured hybrid error at that reference, and that crossing reading is void.
A dd sign COUNTS if its 5 exact variants agree and relative noise 1e-24 on the dd propagator entries leaves it unchanged (both seeds), as in every dd check of this task
(the noise at 1e-20 and 1e-16 is information). If a dd sign does not count at either state, neither reading applies, and that is reported."""
import json, sys
HYB = {18.0: (-1.0, -1929.5742472863), 18.0625: (1.0, -1923.7847417121)}       # sign and ln|det| of the hybrid at lambda 1.20 (xfkappa's d18_refsign_1025.jsonl)
def rec(fn):
    r = [json.loads(l) for l in open(fn) if l.strip()]
    return r[-1] if r else None
def sign(r):
    if r is None:
        return None, False, "no record"
    s = {x["sign"] for x in r["dd"]}
    agree = len(s) == 1
    n24 = [e for e in (r.get("noise") or []) if abs(e["eps"] - 1e-24) < 1e-30]
    ok24 = bool(n24) and all(x == r["dd"][0]["sign"] for x in n24[0]["signs"])
    info = {f"{e['eps']:g}": e["signs"] for e in (r.get("noise") or [])}
    return (r["dd"][0]["sign"] if agree else None), (agree and ok24), f"5 variants {[x['sign'] for x in r['dd']]} agree {agree}, noise {info}, ln|det| dd {r['dd'][0]['ln']:.10f}, float64 sign {r.get('f64_sign')} ln {r.get('f64_ln'):.10f}"
res = []
for fn in sys.argv[1:3]:
    r = rec(fn)
    D = r["D"] if r else None
    s, c, t = sign(r)
    h = HYB.get(D)
    lam = r["lam"] if r else None
    print(f"D {D}, lambda {lam}: dd sign {s}, counts {c}; {t}")
    if h and r:
        print(f"   hybrid (xfkappa) at 1.20: sign {h[0]:+.0f}, ln|det| {h[1]:.10f}; dd ln minus hybrid ln {r['dd'][0]['ln'] - h[1]:+.4f}")
    res.append((D, s, c, h[0] if h else None, lam))
bad_lam = [D for D, s, c, h, lam in res if lam is not None and abs(lam - 1.2) > 1e-12]
notc = [D for D, s, c, h, lam in res if not c]
diff = [D for D, s, c, h, lam in res if c and s != h]
if len(res) < 2 or bad_lam:
    out = "NEITHER READING APPLIES: a record is missing or not at lambda 1.20"
elif diff:
    out = ("HYBRID ERROR at " + " and ".join(f"D {D}" for D in diff) + ": the counting dd sign differs from the hybrid's; the root-crossing reading is VOID" +
           ("; a dd sign does not count at " + " and ".join(f"D {D}" for D in notc) if notc else ""))
elif notc:
    out = "NEITHER READING APPLIES: a dd sign does not count at " + " and ".join(f"D {D}" for D in notc)
else:
    out = "CROSSING CONFIRMED: dd equals the hybrid at both (D 18 minus, D 18.0625 plus), a root crossing lambda 1.20 between D 18 and D 18.0625"
print("DDREAD:", out)
