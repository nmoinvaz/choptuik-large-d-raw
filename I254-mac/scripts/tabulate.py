"""Tables of #254's measurements: every record of the given jsonl files (hp/series_truncation.py), one row per state and
layout (own M, the resampled start, the re-converged M, the fitted layout), as CSV, and a summary per group.

    python3 tabulate.py OUT.csv FILE.jsonl [...]
"""
import csv
import json
import os
import sys

GATE = 1e-15
rows = []


def row(rec, layout, M, F, tails, extra=None):
    t0, t1 = tails
    r = dict(group=rec.get("tag", ""), state=rec["state"].split("choptuik-large-d-raw/")[-1].split("agent-a4611844c54c6e6b3/")[-1],
             D=rec["D"], layout=layout, M=M, kf=rec.get("kf"), x0=rec["nodes"][0], kc=rec.get("kc"), ks=rec.get("ks"),
             F=F, centre=t0["tail"], centre_ratio=t0["ratio"], centre_radius=t0["radius"], horizon=t1["tail"],
             horizon_ratio=t1["ratio"], horizon_radius=t1["radius"], worst=max(t0["tail"], t1["tail"]))
    r.update(extra or {})
    rows.append(r)


for f in sys.argv[2:]:
    for line in open(f):
        rec = json.loads(line)
        if "error" in rec:
            rows.append(dict(group=rec.get("tag", ""), state=rec["state"], layout="error", worst=float("nan"),
                             note=rec["error"]))
            continue
        row(rec, "own M", rec["M"], rec["F"], rec["tails"], dict(Delta=rec["Delta"], lam=rec.get("lam")))
        if "fitted" in rec:
            fr = rec["fitted"]
            row(dict(rec, nodes=fr["nodes"], ks=fr["ks"]), "own M fitted", rec["M"], fr["F"], fr["tails"],
                dict(Delta_diff=fr["Delta_diff"], lam=fr.get("lam")))
        hi = rec.get("Mhi")
        if hi:
            row(rec, "resampled start", hi["M"], hi["F_start"], hi["tails_start"])
            if "tails" in hi:
                row(rec, "re-converged", hi["M"], hi["F"], hi["tails"], dict(Delta_diff=hi["Delta_diff"],
                                                                            lam=hi.get("lam")))
                if "fitted" in hi:
                    fr = hi["fitted"]
                    row(dict(rec, nodes=fr["nodes"], ks=fr["ks"]), "re-converged fitted", hi["M"], fr["F"],
                        fr["tails"], dict(Delta_diff=fr["Delta_diff"], lam=fr.get("lam")))
keys = []
for r in rows:
    for k in r:
        if k not in keys:
            keys.append(k)
with open(sys.argv[1], "w", newline="") as fo:
    w = csv.DictWriter(fo, keys)
    w.writeheader()
    w.writerows(rows)
groups = {}
for r in rows:
    groups.setdefault((r["group"], r["layout"]), []).append(r)
print(f"{'group':16s} {'layout':20s} {'n':>4s} {'above':>5s} {'worst':>9s}  worst state")
for (g, l), rs in groups.items():
    good = [r for r in rs if r["worst"] == r["worst"]]
    above = [r for r in good if r["worst"] > GATE]
    wr = max(good, key=lambda r: r["worst"]) if good else None
    print(f"{g:16s} {l:20s} {len(rs):4d} {len(above):5d} {wr['worst'] if wr else float('nan'):9.1e}  "
          f"{os.path.basename(wr['state']) if wr else ''} (D {wr['D'] if wr else ''}, M {wr['M'] if wr else ''})")
print()
print("above the gate (1e-15):")
for r in rows:
    if r["worst"] > GATE:
        print(f"  {r['group']:12s} {r['layout']:20s} {r['state']}: D {r['D']:.4f} M {r['M']} kf {r['kf']} x0 {r['x0']} "
              f"kc {r['kc']} ks {r['ks']} |F| {r['F']:.1e} centre {r['centre']:.1e} (ratio {r['centre_ratio']:.3f}, "
              f"radius {r['centre_radius']:.3f}) horizon {r['horizon']:.1e} (ratio {r['horizon_ratio']:.3f}, radius "
              f"{r['horizon_radius']:.3f})" + (f" dDelta {r['Delta_diff']:+.2e}" if r.get("Delta_diff") is not None
                                               else ""))
