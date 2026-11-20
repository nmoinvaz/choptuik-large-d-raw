"""#1021: which sheet of S_3 = 0 each located M = 3 zero is on, and whether it connects to the known zero's sheet. The
valued points of every given points file (any xi1: on a sheet F_3 does not depend on it) are pooled as nodes, one
per record (the last per point and file). Two nodes are adjacent when they are at the same point, consecutive
points of the pooled set on a line of constant w/w_inf (at most 0.25 apart in A) or constant A (at most 0.1 in
w/w_inf), or within 0.02 of each other in (A, 2.5 w/w_inf) (the locate steps lie off the grid lines).
Adjacent nodes are joined when |dF_3| <= T (0.1, as in sheet_check.py); the components are the sheets as sampled.
For each zero's cell the components of its corner and edge nodes are listed, with their F_3, and the bottleneck to
the known zero's component: the smallest possible largest |dF_3| step over all paths of adjacent nodes (the
minimum spanning tree's), which is about the sheets' distance when they meet only across a switch, and infinite when
no path exists. --mutate=split adds 0.3i to F_3 of every node with A > 3.0: the known zero's sheet must then not
reach box 7's zero (its bottleneck becomes about 0.3), and the run exits 1.
    python sheet_connect.py ZEROS.json FILE [FILE ...] [--T 0.1] [--mutate=split]"""
import json, sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components, breadth_first_order

args = [a for a in sys.argv[1:] if not a.startswith("--")]
T = float(dict(zip(sys.argv[1::2], sys.argv[2::2])).get("--T", 0.1)) if "--T" in sys.argv else 0.1
mutate = "--mutate=split" in sys.argv
zeros = json.load(open(args[0]))
rk = lambda x: round(x, 9)
nodes = []                                               # (A, wf, F3, file)
for f in args[1:]:
    last = {}
    for l in open(f):
        r = json.loads(l)
        last[(rk(r["A"]), rk(r["wf"]))] = r
    for k, r in last.items():
        ok = (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
        if ok and np.isfinite(r["re"]) and np.isfinite(r["F3re"]):
            nodes.append((k[0], k[1], complex(r["F3re"], r["F3im"]), "/".join(f.split("/")[-3:])))
if mutate:
    nodes = [(a, w, F + (0.3j if a > 3.0 else 0), f) for a, w, F, f in nodes]
n = len(nodes)
at = {}
for i, (a, w, _, _) in enumerate(nodes):
    at.setdefault((a, w), []).append(i)
E = set()
for ids in at.values():
    E |= {(i, j) for i in ids for j in ids if i < j}
for ax, lmax in ((0, 0.25), (1, 0.1)):                  # ax 0: along A on a line of constant w/w_inf
    lines = {}
    for p in at:
        lines.setdefault(p[1 - ax], []).append(p)
    for ps in lines.values():
        ps.sort(key=lambda p: p[ax])
        for p, q in zip(ps[:-1], ps[1:]):
            if q[ax] - p[ax] <= lmax + 1e-9:
                E |= {(min(i, j), max(i, j)) for i in at[p] for j in at[q]}
from scipy.spatial import cKDTree                       # and nodes off the grid lines (locate steps): adjacent
XY = np.array([(x[0], 2.5 * x[1]) for x in nodes])      # within 0.02 in (A, 2.5 w/w_inf)
E |= {(int(i), int(j)) for i, j in cKDTree(XY).query_pairs(0.02)}
E = sorted(E)
F3 = np.array([x[2] for x in nodes])
wgt = np.array([abs(F3[i] - F3[j]) for i, j in E])
I, J = np.array([e[0] for e in E]), np.array([e[1] for e in E])
keep = wgt <= T
G = coo_matrix((np.ones(keep.sum()), (I[keep], J[keep])), shape=(n, n))
nc, lab = connected_components(G, directed=False)
mst = minimum_spanning_tree(coo_matrix((wgt + 1e-15, (I, J)), shape=(n, n))).tocsr()
mst = mst + mst.T
sizes = np.bincount(lab)
print(f"{n} valued nodes from {len(args) - 1} files, {len(E)} adjacent pairs, {nc} components at |dF3| <= {T:g} "
      f"(largest: {sorted(sizes, reverse=True)[:6]})")


def cell_nodes(c):
    a0, a1, w0, w1 = (rk(x) for x in c)
    on = lambda a, w: ((abs(w - w0) < 1e-9 or abs(w - w1) < 1e-9) and a0 - 1e-9 <= a <= a1 + 1e-9) or \
                      ((abs(a - a0) < 1e-9 or abs(a - a1) < 1e-9) and w0 - 1e-9 <= w <= w1 + 1e-9)
    return [i for i, (a, w, _, _) in enumerate(nodes) if on(a, w)]


def bottleneck(src, dst):
    """largest edge on the MST path from src to dst (inf if none)"""
    order, pred = breadth_first_order(mst, src, directed=False, return_predecessors=True)
    if pred[dst] < 0 and dst != src:
        return float("inf"), None
    big, where, k = 0.0, None, dst
    while k != src:
        p = pred[k]
        if mst[p, k] > big:
            big, where = mst[p, k], (nodes[p][:2], nodes[k][:2], nodes[p][2], nodes[k][2])
        k = p
    return float(big), where


known = cell_nodes(zeros["known"]["cell"])
kc = np.bincount(lab[known]).argmax()
print(f"known zero {zeros['known']['at']}: {len(known)} cell nodes, component {kc} of {sizes[kc]} nodes, F3 "
      f"{np.mean(F3[known]):.4f}")
for f in sorted({x[3] for x in nodes}):
    ids = [i for i, x in enumerate(nodes) if x[3] == f]
    c = np.bincount(lab[ids], minlength=nc)
    top = [(int(k), int(c[k])) for k in np.argsort(-c)[:3] if c[k]]
    print(f"  {f}: {len(ids)} nodes; components (id, nodes) {top}"
          + (f"; off the known zero's sheet: {len(ids) - int(c[kc])}" if c[kc] < len(ids) else ""))
for c in np.argsort(-sizes):
    if c == kc or sizes[c] < 5:
        continue
    ids = np.flatnonzero(lab == c)
    A_, W_ = np.array([nodes[i][0] for i in ids]), np.array([nodes[i][1] for i in ids])
    b, where = bottleneck(known[0], int(ids[0]))
    print(f"  component {c}: {len(ids)} nodes, A {A_.min():.4f}-{A_.max():.4f}, wf {W_.min():.4f}-{W_.max():.4f}, "
          f"F3 {np.mean(F3[ids]):.4f}, bottleneck to the known zero {b:.3g}"
          + (f" between {where[0]} and {where[1]} (F3 {where[2]:.4f} -> {where[3]:.4f})" if where else ""))
fail = False
for name, z in zeros.items():
    ids = cell_nodes(z["cell"])
    if not ids:
        print(f"{name} {z['at']}: no valued node on its cell")
        continue
    comps = {int(c): int((lab[ids] == c).sum()) for c in np.unique(lab[ids])}
    same = kc in comps
    b, where = bottleneck(known[0], ids[0])
    print(f"{name} {z['at']} (W {z['W']}): {len(ids)} cell nodes, F3 {np.mean(F3[ids]):.4f} (spread "
          f"{np.ptp(np.abs(F3[ids] - np.mean(F3[ids]))):.2g}), components {comps}; "
          + ("on the known zero's sheet" if same else "NOT on the known zero's sheet")
          + f"; bottleneck to the known zero {b:.3g}"
          + (f" between {where[0]} and {where[1]} (F3 {where[2]:.4f} -> {where[3]:.4f})" if where and b > T else ""))
    if mutate and name == "box7" and same:
        fail = True
if mutate:
    print("mutate=split: " + ("the split was not seen (FAIL of the control)" if fail else "the split is seen"))
    sys.exit(1 if not fail else 0)
