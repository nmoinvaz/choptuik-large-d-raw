#!/usr/bin/env python3
"""#1076 fu022mp_corner_d (dh610) read_corner.py CACHE N0 [COUNT.json] | selftest [--mutate]: the rows the recount appended to the cache (lines after N0) at the corner (3.9123456, 0.20654321),
and the registered reading: VALUED when the corner's last row has a finite re and im and a tuned S_3 (info below 1e-8, or the continuation's fix ok), i.e. a branch to xi1 0.17 exists from the 0.2 start;
UNVALUED otherwise. With COUNT.json, the box's boundary winding, leaf sum, unresolved leaves and zeros. No number is typed by hand.
usage (from this folder): python3 -I read_corner.py m3/points_M3_r0.17.jsonl 4159 m3/count_M3_fu022mp_corner_d_r0.17.json > reading.txt
selftest: planted rows (a valued continuation row from the 0.2 start, an unvalued row, a valued row after an unvalued one) must read as planted; --mutate reads a planted valued row as unvalued, the selftest exits 1."""
import json, math, sys

KEY = (3.9123456, 0.20654321)


def valued(r):
    finite = all(isinstance(r.get(k), float) and math.isfinite(r[k]) for k in ("re", "im"))
    tuned = (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
    return finite and tuned


def read(rows, mutate=False):
    """rows: the corner's appended rows in order; the verdict is the last row's"""
    if not rows:
        return "NO ROW", None
    last = rows[-1]
    v = valued(last)
    if mutate:
        v = not v
    return ("VALUED" if v else "UNVALUED"), last


def selftest(mutate):
    nan = float("nan")
    val = dict(A=KEY[0], wf=KEY[1], re=1.0, im=2.0, info=3e-10, fix=dict(trail=[0.2, 0.19, 0.18, 0.17], ok=True))
    unv = dict(A=KEY[0], wf=KEY[1], re=nan, im=nan, info=3.8e6, fix=dict(trail=[0.25, 0.24875], ok=False))
    ok = (read([unv], mutate)[0] == "UNVALUED" and read([val], mutate)[0] == "VALUED" and read([unv, val], mutate)[0] == "VALUED"
          and read([val, unv], mutate)[0] == "UNVALUED" and read([], mutate)[0] == "NO ROW")
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    cache, n0 = sys.argv[1], int(sys.argv[2])
    lines = [l for l in open(cache) if l.strip()]
    new = [(i, json.loads(l)) for i, l in enumerate(lines, 1) if i > n0]
    print(f"cache {cache}: {len(lines)} lines, {len(new)} appended after line {n0}; {sum(1 for _, r in new if r.get('fu') == 'mp')} of them fu mp")
    mine = [(i, r) for i, r in new if (round(r["A"], 12), round(r["wf"], 12)) == (round(KEY[0], 12), round(KEY[1], 12))]
    for i, r in mine:
        fx = r.get("fix") or {}
        print(f"  line {i}: {'mp' if r.get('fu') == 'mp' else 'float64'} row at the corner: re {r['re']!r}, im {r['im']!r}, info {r['info']!r}, sig {r.get('sig')!r}, "
              f"F3 ({r.get('F3re')!r}, {r.get('F3im')!r}), trail {fx.get('trail')}, fix ok {fx.get('ok')}, bound {fx.get('bound')}, valued flag {r.get('valued')}")
    v, last = read([r for _, r in mine])
    print(f"corner reading: {v}" + ("" if last is None else f" (last row line {mine[-1][0]})"))
    if len(sys.argv) > 3:
        c = json.load(open(sys.argv[3]))
        print(f"count: boundary winding {c['boundary_winding']!r}, leaf sum {c['leaf_sum']}, {c['nleaves']} leaves after {c['splits']} splits, {c['npoints']} points, "
              f"{len(c['unresolved'])} unresolved cells {c['unresolved']}, {len(c['zeros'])} zeros, {c['sec']:.0f} s")
        for z in c["zeros"]:
            print(f"  zero W {z['W']:+d} in cell {z['cell']}: located {z['located']}; at xi1 {c['r1b']}: {z.get('located_r1b')}")
