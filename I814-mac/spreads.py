import csv, sys, mpmath as mp
mp.mp.dps = 60
for path in sys.argv[1:]:
    rows = list(csv.DictReader(x for x in open(path) if not x.startswith("#")))
    g = {}
    for r in rows:
        g.setdefault(round(float(r["D"]), 6), []).append(r)
    sp = lambda v: float(max(mp.mpf(r["lam_g"]) for r in v) - min(mp.mpf(r["lam_g"]) for r in v))
    out = {}
    for D, v in sorted(g.items()):
        if len(v) < 2: continue
        k = "+".join(sorted({r["kind"] for r in v}))
        out.setdefault(k, []).append((D, sp(v), len(v), sorted({r["state"].split("/")[0] for r in v})))
    print("==", path.split("/")[-1])
    for k, v in out.items():
        w = max(v, key=lambda x: x[1])
        print(f"{k:20s} {len(v):4d} D  max {w[1]:.2e} at {w[0]}  folders {sorted({f for x in v for f in x[3]})[:6]}")
    ch = out.get("chain", [])
    print("chain D:", [x[0] for x in ch])
    pn = out.get("pinned", [])
    print("pinned D range", pn[0][0], pn[-1][0])
