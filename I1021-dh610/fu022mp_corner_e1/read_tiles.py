#!/usr/bin/env python3
"""#1076 fu022mp_corner_e (dh610) read_tiles.py CACHE N0 COUNT.json | selftest [--mutate]: the reading of one tiling level from the recount's own files: each quarter's boundary winding, leaf sum and unresolved
leaves (count's `boxes`), the zeros, and the points the recount appended to the cache after line N0 with and without value (a row has a value when its re and im are finite and S_3 is tuned: info below 1e-8
or the continuation's fix ok). No number is typed by hand. usage (from this folder): python3 -I read_tiles.py m3/points_M3_r0.17.jsonl 4159 m3/count_TAG.json > reading.txt
selftest: a planted count with one resolved and one unresolved box and planted rows; --mutate counts the unresolved box as resolved: the selftest exits 1."""
import json, math, sys


def valued(r):
    finite = all(isinstance(r.get(k), float) and math.isfinite(r[k]) for k in ("re", "im"))
    tuned = (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
    return finite and tuned


def box_status(b, mutate=False):
    if mutate:                                  # the control: every box reads as resolved
        return "resolved"
    w = b["boundary_winding"]
    return "resolved" if b["unresolved"] == 0 and isinstance(w, (int, float)) and math.isfinite(w) else "UNRESOLVED"


def point_status(rows):
    """last row per key: (key, valued, fu mp?)"""
    last = {}
    for r in rows:
        last[(round(r["A"], 12), round(r["wf"], 12))] = r
    return {k: (valued(r), r.get("fu") == "mp") for k, r in last.items()}


def selftest(mutate):
    nan = float("nan")
    boxes = [dict(box=[[0, 1], [0, 1]], boundary_winding=1.0, leaf_sum=1, unresolved=0), dict(box=[[1, 2], [0, 1]], boundary_winding=nan, leaf_sum=0, unresolved=1)]
    rows = [dict(A=0.5, wf=0.5, re=1.0, im=1.0, info=1e-12), dict(A=1.5, wf=0.5, re=nan, im=nan, info=3e6)]
    st = [box_status(b, mutate) for b in boxes]
    ps = point_status(rows)
    ok = st == ["resolved", "UNRESOLVED"] and ps[(0.5, 0.5)] == (True, False) and ps[(1.5, 0.5)] == (False, False)
    print("selftest" + (" --mutate" if mutate else ""), st, "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    cache, n0, cj = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    lines = [l for l in open(cache) if l.strip()]
    new = [json.loads(l) for i, l in enumerate(lines, 1) if i > n0]
    print(f"cache {cache}: {len(lines)} lines, {len(new)} appended after line {n0}, {sum(1 for r in new if r.get('fu') == 'mp')} of them fu mp")
    ps = point_status(new)
    nv = [k for k, (v, _) in ps.items() if not v]
    print(f"appended points (last row per key): {len(ps)}, with value {len(ps) - len(nv)}, without value {len(nv)}: {sorted(nv)}")
    c = json.load(open(cj))
    print(f"count: {c['nleaves']} leaves after {c['splits']} splits, {c['npoints']} points, {len(c['unresolved'])} unresolved cells, {len(c['zeros'])} zeros, {c['sec']:.0f} s")
    for b in c["boxes"]:
        (a0, a1), (w0, w1) = b["box"]
        w = b["boundary_winding"]
        print(f"  box A {a0!r} to {a1!r}, wf {w0!r} to {w1!r}: {box_status(b)}, boundary winding {w!r}, leaf sum {b['leaf_sum']}, unresolved leaves {b['unresolved']}")
    for z in c["zeros"]:
        print(f"  zero W {z['W']:+d} in cell {z['cell']}: located {z['located']}; at xi1 {c['r1b']}: {z.get('located_r1b')}")
