"""#851: the quadratic coefficient c = |dev| / rel^2 of the horizon response, and its growth with D, from the runs' JSONs.

    python coef851.py FOLDER            (reads FOLDER/power.json and FOLDER/D*.json; prints a table and the log slopes)

dev is step_spread.py power's (the seed's dDelta minus the unperturbed one, exact from the eight parts), the pivot ratio is
each run's smallest pivot over the unperturbed one's. A rel is "pivot-clean" when that ratio is within 1% of 1. The slope is of
ln c against D (per unit D, as step_spread.py sum's), by least squares at rel 1e-75, the one rel that is pivot-clean at all
three D with a quadratic power (D 250.1676's 1e-80 has a sign change, so it is not), against #805's 1.44 and twice it."""
import glob
import json
import os
import sys

import numpy as np

folder = sys.argv[1]
pw = json.load(open(os.path.join(folder, "power.json")))
rows = []
for g in pw["groups"]:
    D = float(g["D_str"][:12])
    js = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(folder, "D*.json"))) if "power" not in f]
    rec = [j for j in js if j["D_str"] == g["D_str"]][0]
    piv0 = rec["runs"][0]["piv"][0]
    ps = [None] + list(g["p"])      # the power from the next larger rel
    for (rel, dev), r, pp in zip(g["devs"], [x for x in rec["runs"] if x.get("rel") is not None and x["seed"] == g["seed"]], ps):
        rows.append(dict(D=D, rel=rel, dev=dev, c=abs(dev) / rel ** 2, piv=r["piv"][0] / piv0 - 1, p=pp))
print("D          rel     pivot/unperturbed - 1   dev           c = |dev| / rel^2   pivot-clean   p from the next larger rel")
for r in rows:
    r["clean"] = abs(r["piv"]) <= 0.01
    print(f"{r['D']:<10.4f} {r['rel']:.0e}  {r['piv']:+.3e}  {r['dev']:+.4e}  {r['c']:.4e}   {'yes' if r['clean'] else 'no':<12}  "
          f"{'none' if r['p'] is None else format(r['p'], '.4f')}")
print("\nln c against D, per unit D, at rel 1e-75 (pivot-clean and quadratic at all three D):")
for rel in (1e-75,):
    sel = [r for r in rows if r["rel"] == rel and r["clean"]]
    Ds = np.array([r["D"] for r in sel])
    lc = np.log([r["c"] for r in sel])
    steps = ", ".join(f"{Ds[i]:.4f}->{Ds[i + 1]:.4f}: {(lc[i + 1] - lc[i]) / (Ds[i + 1] - Ds[i]):.4f}" for i in range(len(sel) - 1))
    fit = float(np.polyfit(Ds, lc, 1)[0]) if len(sel) >= 2 else float("nan")
    print(f"  rel {rel:.0e}: {len(sel)} D, steps {steps}; least squares {fit:.4f} (1.44: ratio {fit / 1.44:.3f}; 2.88: ratio {fit / 2.88:.3f})")
