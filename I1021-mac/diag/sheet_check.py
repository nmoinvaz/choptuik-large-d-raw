"""#1021: do an M = 3 count's values lie on one sheet of S_3 = 0? F_3 does not depend on xi1 on a sheet (common
valued points of the stored files at different radii agree to 2.3e-3), and the sheets seen are 0.3-0.42 apart in F_3,
while consecutive points of one sheet differ by at most 0.062 (all stored files without a switch). Along every edge
of every leaf (LEAVES a leaves file), or along every line of constant A or w/w_inf (LEAVES = lines, pairs at most
0.25 in A or 0.1 in w/w_inf apart), the cache's valued points are taken in order and a consecutive pair is flagged
when |dF_3| > DMAX (0.1; set after the distribution above was seen), or when |dF_3| > DMIN (0.02) and its step per
length exceeds RATIO (20) x the median. With --count, each located zero is listed with its cell and whether that
cell's boundary holds a flagged pair; in leaves mode each flagged cell is listed with its winding.
    python sheet_check.py CACHE LEAVES|lines [--count COUNT.json] [--dmax 0.1] [--ratio 20] [--dmin 0.02]
                          [--mutate=switch]
--mutate=switch moves F_3 of the middle valued point of the longest run by 0.3i (the sheets' distance at A 3.55,
w/w_inf 0.41): the check must then flag it (exit 1). Exit 1 when any pair is flagged."""
import json, sys
import numpy as np

cache, leaves = sys.argv[1], sys.argv[2]
opt = dict(zip(sys.argv[3::2], sys.argv[4::2]))
ratio, dmin, dmax = float(opt.get("--ratio", 20)), float(opt.get("--dmin", 0.02)), float(opt.get("--dmax", 0.1))
mutate = "--mutate=switch" in sys.argv
rk = lambda x: round(x, 9)


def valued(r):
    return ((isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))) and \
        np.isfinite(r["re"]) and np.isfinite(r["F3re"])


last = {}
for line in open(cache):
    r = json.loads(line)
    last[(rk(r["A"]), rk(r["wf"]))] = r                  # the last record per point, as argcount reads the cache
pts = {k: complex(r["F3re"], r["F3im"]) for k, r in last.items() if valued(r)}
start = {k: ((last[k].get("fix") or {}).get("trail") or ["inner"])[0] for k in pts}
byA, byW = {}, {}
for k in pts:
    byA.setdefault(k[0], []).append(k)
    byW.setdefault(k[1], []).append(k)
runs, cells = [], []
if leaves == "lines":
    for ks in byW.values():
        ks = sorted(ks, key=lambda k: k[0])
        runs += [[p, q] for p, q in zip(ks[:-1], ks[1:]) if q[0] - p[0] <= 0.25 + 1e-9]
    for ks in byA.values():
        ks = sorted(ks, key=lambda k: k[1])
        runs += [[p, q] for p, q in zip(ks[:-1], ks[1:]) if q[1] - p[1] <= 0.1 + 1e-9]
else:
    for line in open(leaves):
        L = json.loads(line)
        cells.append(L)
        a0, a1, w0, w1 = (rk(L[x]) for x in ("a0", "a1", "w0", "w1"))
        for kind, c, lo, hi in (("w", w0, a0, a1), ("w", w1, a0, a1), ("A", a0, w0, w1), ("A", a1, w0, w1)):
            if kind == "w":
                on = sorted((k for k in byW.get(c, []) if lo - 1e-9 <= k[0] <= hi + 1e-9), key=lambda k: k[0])
            else:
                on = sorted((k for k in byA.get(c, []) if lo - 1e-9 <= k[1] <= hi + 1e-9), key=lambda k: k[1])
            if len(on) >= 2:
                runs.append(on)
if mutate and runs:
    k = max(runs, key=len)[len(max(runs, key=len)) // 2]
    pts[k] += 0.3j
    print(f"mutate=switch: F3 of {k} moved by 0.3i")
pairs = {}
for on in runs:
    for p, q in zip(on[:-1], on[1:]):
        L = np.hypot(q[0] - p[0], q[1] - p[1])
        pairs[(p, q)] = (abs(pts[q] - pts[p]), L)
name = "/".join(cache.split("/")[-3:])
if not pairs:
    print(f"{name}: {len(pts)} valued points, no pairs to compare; sheet check: EMPTY")
    sys.exit(0)
med = float(np.median([d / L for d, L in pairs.values()]))
flag = {pq: v for pq, v in pairs.items() if v[0] > dmax or (v[0] > dmin and v[0] / v[1] > ratio * med)}
dmx = max(v[0] for v in pairs.values())
print(f"{name} ({'lines' if leaves == 'lines' else leaves.split('/')[-1]}): {len(pts)} valued points, {len(pairs)} "
      f"pairs, median |dF3|/length {med:.3g}, largest |dF3| {dmx:.3g}; {len(flag)} flagged")
for (p, q), (d, L) in sorted(flag.items(), key=lambda x: -x[1][0])[:12]:
    print(f"  FLAG ({p[0]:.7f}, {p[1]:.8f}) -> ({q[0]:.7f}, {q[1]:.8f}): |dF3| {d:.3g} over {L:.3g}; "
          f"F3 {pts[p]:.4f} -> {pts[q]:.4f}; starts {start[p]} -> {start[q]}")
if len(flag) > 12:
    print(f"  ... {len(flag) - 12} more")


def cell_flagged(a0, a1, w0, w1):
    a0, a1, w0, w1 = rk(a0), rk(a1), rk(w0), rk(w1)
    on = lambda k: ((abs(k[1] - w0) < 1e-9 or abs(k[1] - w1) < 1e-9) and a0 - 1e-9 <= k[0] <= a1 + 1e-9) or \
                   ((abs(k[0] - a0) < 1e-9 or abs(k[0] - a1) < 1e-9) and w0 - 1e-9 <= k[1] <= w1 + 1e-9)
    return [pq for pq in flag if on(pq[0]) and on(pq[1])]


if cells:
    bad = [L for L in cells if cell_flagged(L["a0"], L["a1"], L["w0"], L["w1"])]
    print(f"  cells across a switch: {len(bad)} of {len(cells)}" + "".join(
        f"\n    A {L['a0']:.7f}-{L['a1']:.7f}, wf {L['w0']:.8f}-{L['w1']:.8f}: W {L['W']}, ok {L['ok']}" for L in bad[:20]))
if "--count" in opt:
    for z in json.load(open(opt["--count"]))["zeros"]:
        c, loc = z["cell"], z.get("located")
        f = cell_flagged(*c)
        print(f"  zero W {z['W']:+d} in cell A {c[0]:.7f}-{c[1]:.7f}, wf {c[2]:.8f}-{c[3]:.8f}"
              + (f" at ({loc['A']:.6f}, {loc['wf']:.6f})" if loc else " (not located)")
              + (f": its cell's boundary holds {len(f)} flagged pairs" if f else ": its cell's boundary is on one sheet"))
print(f"sheet check: {'FAIL' if flag else 'PASS'}")
sys.exit(1 if flag else 0)
