"""#1021 fu021: the points fu_value.py --auto selects (without value as the recount reads it, inside or on an unresolved
leaf), minus those already run in earlier rows files. Prints "A,w;A,w" (empty when none), and the count to stderr.
    python select_points.py CODE CACHE LEAVES [ROWS_EARLIER.jsonl ...]"""
import json, math, sys
code, cache, leaves = sys.argv[1:4]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac  # noqa: E402
recs = {}
for line in open(cache):
    r = json.loads(line); recs[ac.Multiplier.key((r["A"], r["wf"]))] = r
fin = lambda x: isinstance(x, float) and math.isfinite(x)
def has_value(r):
    if not (ac.Multiplier.valued3(r) and fin(r.get("re")) and fin(r.get("im"))):
        return False
    return r.get("ymax", 0.0) <= 1e2 and math.hypot(r["re"], r["im"]) >= 10 * r.get("sig", 0.0)
cells = [(c["a0"], c["a1"], c["w0"], c["w1"]) for c in map(json.loads, open(leaves)) if not c["ok"]]
pts = [k for k, r in sorted(recs.items()) if not has_value(r) and any(a0 - 1e-9 <= k[0] <= a1 + 1e-9 and w0 - 1e-9 <= k[1] <= w1 + 1e-9 for a0, a1, w0, w1 in cells)]
done = {ac.Multiplier.key((r["A"], r["wf"])) for f in sys.argv[4:] for r in map(json.loads, open(f))}
new = [p for p in pts if p not in done]
print(";".join(f"{a!r},{w!r}" for a, w in new))
print(f"{len(pts)} points without value in {len(cells)} unresolved leaves; {len(pts) - len(new)} already run; {len(new)} to run", file=sys.stderr)
