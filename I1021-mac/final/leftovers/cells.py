"""#1021: the recount of record per cell (box) of the 32: boundary winding, leaf sum, unresolved leaves, the zeros inside,
and the distinct blocking points of its unresolved leaves with their causes (from leftovers.txt).
    python cells.py COUNT LEAVES LEFTOVERS"""
import json, re, sys
K = json.load(open(sys.argv[1])); L = [json.loads(l) for l in open(sys.argv[2])]
txt = open(sys.argv[3]).read()
block = {}
for m in re.finditer(r"leaf A (\S+)-(\S+) w (\S+)-(\S+) \(depth \d+\)[^\n]*((?:\n    \(.*)*)", txt):
    pts = re.findall(r"\n    \((\S+), (\S+)\): (.*)", m.group(5))
    block[tuple(round(float(v), 6) for v in m.groups()[:4])] = pts
e = 1e-9
nres = 0
for i, b in enumerate(K["boxes"], 1):
    (a0, a1), (w0, w1) = b["box"]
    inside = [x for x in L if a0 - e <= x["a0"] and x["a1"] <= a1 + e and w0 - e <= x["w0"] and x["w1"] <= w1 + e]
    un = [x for x in inside if not x["ok"]]
    zs = [z for z in K["zeros"] if a0 - e <= z["cell"][0] and z["cell"][1] <= a1 + e and w0 - e <= z["cell"][2] and z["cell"][3] <= w1 + e]
    bw = b["boundary_winding"]
    pts = {}
    for x in un:
        for A, w, why in block.get(tuple(round(v, 6) for v in (x["a0"], x["a1"], x["w0"], x["w1"])), []):
            pts[(A, w)] = why
    nres += not un
    print(f"{i:2d} A {a0:.4f}-{a1:.4f} w {w0:.4f}-{w1:.4f}: W {'nan' if bw is None or bw != bw else round(bw)}, leaf sum {b['leaf_sum']}, "
          f"{len(inside)} leaves, {len(un)} unresolved; zeros " + (", ".join(f"{z['W']:+d} at ({z['located']['A']:.6f}, {z['located']['wf']:.6f})" if z.get('located') else f"{z['W']:+d}" for z in zs) or "none")
          + "".join(f"\n      blocked by ({A}, {w}): {why}" for (A, w), why in pts.items()))
print(f"{nres} of {len(K['boxes'])} cells resolved; {len(K['boxes']) - nres} with unresolved leaves; "
      f"{len(K['unresolved'])} unresolved leaves; {len(K['zeros'])} zeros")
