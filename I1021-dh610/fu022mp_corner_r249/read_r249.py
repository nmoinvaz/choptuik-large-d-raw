#!/usr/bin/env python3
"""#1076 fu022mp_corner_r249 (dh610) read_r249.py control NW.json | reading NW.json LOWER.json CACHE249 | selftest [--mutate]: the reading of the recount at xi1 0.249 of the quarters of the unresolved box.
control: the coordinator's control for "the zero set does not depend on xi1": the NW quarter (no zero at xi1 0.17, boundary winding 0) recounted at 0.249 must be resolved with winding 0 and no zero: PASS (exit 0);
resolved with a nonzero winding, a leaf sum or a zero: FIRES (exit 1, the work stops); unresolved: INCONCLUSIVE (exit 2). reading: the control, each box of the lower quarters (resolved or not, boundary winding, leaf sum,
unresolved leaves), the zeros with the location at xi1 0.249 and at xi1 0.17 and their difference, and the points of the 0.249 cache without value. No number is typed by hand.
selftest: planted counts (winding 0, winding 1, an unresolved box) must read PASS, FIRES, INCONCLUSIVE; --mutate makes the control ignore the winding and the selftest exits 1."""
import json, math, sys


def control(c, mutate=False):
    b = c["boxes"][0]
    w = b["boundary_winding"]
    if b["unresolved"] > 0 or not isinstance(w, (int, float)) or not math.isfinite(w):
        return "INCONCLUSIVE"
    bad = (round(w) != 0 or abs(w - round(w)) > 1e-6 or b["leaf_sum"] != 0 or len(c["zeros"]) > 0) if not mutate else False
    return "FIRES" if bad else "PASS"


def selftest(mutate):
    nan = float("nan")
    mk = lambda w, un, ls, z: dict(boxes=[dict(box=[[0, 1], [0, 1]], boundary_winding=w, leaf_sum=ls, unresolved=un)], zeros=z)
    got = [control(mk(1e-16, 0, 0, []), mutate), control(mk(1.0, 0, 1, [dict(W=1)]), mutate), control(mk(nan, 1, 0, []), mutate)]
    ok = got == ["PASS", "FIRES", "INCONCLUSIVE"]
    print("selftest" + (" --mutate" if mutate else ""), got, "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def valued(r):
    fin = all(isinstance(r.get(k), float) and math.isfinite(r[k]) for k in ("re", "im"))
    return fin and ((isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok")))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["selftest"]:
        sys.exit(selftest("--mutate" in a))
    if a[:1] == ["control"]:
        v = control(json.load(open(a[1])))
        print("control NW at xi1 0.249:", v)
        sys.exit({"PASS": 0, "FIRES": 1, "INCONCLUSIVE": 2}[v])
    nw, lo, cache = json.load(open(a[1])), json.load(open(a[2])), a[3]
    print("control NW at xi1 0.249:", control(nw))
    for nm, c in (("NW (control)", nw), ("lower quarters", lo)):
        print(f"{nm}: {c['nleaves']} leaves after {c['splits']} splits, {c['npoints']} points, {len(c['unresolved'])} unresolved cells, {len(c['zeros'])} zeros, {c['sec']:.0f} s, r1 {c['r1']}, r1b {c['r1b']}")
        for b in c["boxes"]:
            (a0, a1), (w0, w1) = b["box"]
            w = b["boundary_winding"]
            st = "resolved" if b["unresolved"] == 0 and isinstance(w, (int, float)) and math.isfinite(w) else "UNRESOLVED"
            print(f"  box A {a0!r} to {a1!r}, wf {w0!r} to {w1!r}: {st}, boundary winding {w!r}, leaf sum {b['leaf_sum']}, unresolved leaves {b['unresolved']}")
        for z in c["zeros"]:
            l, l2 = z["located"], z.get("located_r1b")
            d = (f"; difference at xi1 {c['r1b']}: dA {l['A'] - l2['A']:+.3e}, dwf {l['wf'] - l2['wf']:+.3e}" if l and l2 else "")
            print(f"  zero W {z['W']:+d} in cell {z['cell']}: at xi1 {c['r1']}: {l}; at xi1 {c['r1b']}: {l2}{d}")
    rows = [json.loads(l) for l in open(cache) if l.strip()]
    last = {}
    for r in rows:
        last[(round(r["A"], 12), round(r["wf"], 12))] = r
    nv = sorted(k for k, r in last.items() if not valued(r))
    print(f"cache {cache}: {len(rows)} rows, {len(last)} points, {sum(1 for r in rows if r.get('fu') == 'mp')} fu mp rows, without value {len(nv)}: {nv}")
