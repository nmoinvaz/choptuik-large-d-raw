"""#1021: for each valued point of a relocation cache, the nearest valued point of a part's cache (in (A, 2.5 w/w_inf))
and |dF3| to it; the relocation is on the part's sheet when every |dF3| <= 0.1 (sheet_check.py's bar). Exit 1 if not.
    python nearest_f3.py PART_CACHE CACHE [CACHE ...]"""
import json, sys
import numpy as np
from scipy.spatial import cKDTree
ok = lambda r: ((isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))) \
    and r["re"] is not None and np.isfinite(r["F3re"])
def load(f):
    last = {}
    for l in open(f):
        r = json.loads(l); last[(r["A"], r["wf"])] = r
    return [(k[0], k[1], complex(r["F3re"], r["F3im"])) for k, r in last.items() if ok(r)]
part = load(sys.argv[1])
T = cKDTree([(a, 2.5 * w) for a, w, _ in part])
bad = False
for f in sys.argv[2:]:
    pts = load(f)
    d, i = T.query([(a, 2.5 * w) for a, w, _ in pts])
    dF = [abs(F - part[j][2]) for (_, _, F), j in zip(pts, i)]
    print(f"{'/'.join(f.split('/')[-2:])}: {len(pts)} valued points; nearest part point at {d.min():.3g}-{d.max():.3g}; "
          f"|dF3| {min(dF):.3g}-{max(dF):.3g}")
    bad |= max(dF) > 0.1
print("on the part's sheet" if not bad else "NOT on the part's sheet")
sys.exit(1 if bad else 0)
