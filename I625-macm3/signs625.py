#!/usr/bin/env python3
"""Signs of the exact det M on a #625 grid from the four modecount_qdet --json files of one M.
Usage: python3 signs625.py M [dir]. Prints the table; exit 0 and the line 'sign changes N' for the gate."""
import json, math, os, sys
M = int(sys.argv[1])
here = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
pts = [l.split() for l in open(os.path.join(here, f"points_M{M}.txt"))]
pts = [(int(k), float(x)) for k, x in pts]
res = {}   # (index in points file) -> record
for p in range(4):
    f = os.path.join(here, f"qdet_M{M}_p{p}.json")
    if not os.path.exists(f): continue
    recs = json.load(open(f))
    if isinstance(recs, dict): recs = recs.get("points", recs.get("records", [recs]))
    idx = [i for i in range(len(pts)) if i % 4 == p]
    assert len(recs) == len(idx), (p, len(recs), len(idx))
    for i, r in zip(idx, recs):
        assert float(r["lam"][0]) == pts[i][1], (i, r["lam"], pts[i])
        res[i] = r
if len(res) < len(pts):
    print(f"{len(res)} of {len(pts)} points done"); sys.exit(2)
def sgn(r):
    b = r["ball"]
    assert b["exact_input"] and b["rad_arg"] < 1e-6, b
    assert min(abs(b["arg"]), math.pi - abs(b["arg"])) < 1e-6, ("arg det is neither 0 nor pi", b)
    return 1 if abs(b["arg"]) < math.pi / 2 else -1
grid = [(pts[i][0], pts[i][1], sgn(res[i]), res[i]["ball"]["lndet"], res[i]["ball"]["arg"]) for i in range(65)]
print("| k | lambda | sign | ln abs det (ball) | arg det |")
print("|---|---|---|---|---|")
for k, x, s, ld, a in grid:
    print(f"| {k:+d} | {x!r} | {s:+d} | {ld:.9f} | {a:+.9f} |")
chg = [(grid[j][0], grid[j + 1][0]) for j in range(64) if grid[j][2] != grid[j + 1][2]]
print()
print("signs from k=-32: " + "".join("+" if g[2] > 0 else "-" for g in grid))
print(f"sign changes {len(chg)} between k pairs {chg}")
if chg:
    lo, hi = chg[0][0], chg[-1][1]
    print(f"band holding all sign changes: from between k={chg[0][0]} and {chg[0][1]} to between k={chg[-1][0]} and {chg[-1][1]}, i.e. at most {(hi - lo) * 1e-14:.2e} and at least {(chg[-1][0] - chg[0][1]) * 1e-14:.2e} wide")
a, b = res[32]["ball"], res[65]["ball"]
print(f"repeat of k=0 (index 32 in process {32 % 4}, index 65 in process {65 % 4}): ln|det| {'bit for bit equal' if a['lndet'] == b['lndet'] else 'DIFFERENT'}, arg {'bit for bit equal' if a['arg'] == b['arg'] else 'DIFFERENT'}")
