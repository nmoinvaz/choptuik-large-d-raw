"""I856-mac tables: the Delta block's return at D 252.6135, from power.json and the dl_*.json runs (rel 1e-67 is #850's,
I850-mac/dl_D252_r67.json beside this folder).

q = dev / rel^2; q's change per decade is relative to the larger rel's q. The pivot change is the seed run's smallest
pivot over the unperturbed one, less 1. rel_x = (move / rel) / |q| at the smallest rel is where q rel^2 equals the move
(an extrapolation of the quadratic term, not a measurement).

Run: python3 tables.py [folder], default the folder of this script. Writes tables.md beside it.
"""
import json
import math
import os
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
pw = json.load(open(os.path.join(d, "power.json")))
g = pw["groups"][0]
out = ["# I856-mac tables (tables.py)", "",
       f"D {g['D_str'][:12]}, blocks {', '.join(g['blocks'])}, seed {g['seed']}: {g['reading']}, "
       f"p {g['p'][0]:.4f}, {g['p'][1]:.4f}", "",
       "| rel | run | move | dev | \\|dev\\| / move | q = dev / rel² | smallest pivot / unperturbed − 1 |",
       "| --- | --- | --- | --- | --- | --- | --- |"]
qs, last = [], None
for rel, dev in sorted(g["devs"], key=lambda t: -t[0]):
    name = f"dl_D252_r{round(-math.log10(rel))}.json"
    f = os.path.join(d, name)
    if not os.path.exists(f):
        f = os.path.join(d, "..", "I850-mac", name)
    js = json.load(open(f))
    u = next(r for r in js["runs"] if r["run"] == "unperturbed")
    s = next(r for r in js["runs"] if r["seed"] == g["seed"] and not r["control"])
    q = dev / rel ** 2
    qs.append(q)
    out.append(f"| {rel:.0e} | {os.path.relpath(f, d)} | {s['move']:.4e} | {dev:+.6e} | {abs(dev) / s['move']:.4e} | "
               f"{q:+.6e} | {s['piv'][0] / u['piv'][0] - 1:+.3e} |")
    last = (rel, s["move"], q)
dq = [qs[i + 1] / qs[i] - 1 for i in range(len(qs) - 1)]
rel, mv, q = last
out += ["", "q's change per decade (relative): " + ", ".join(f"{x:+.3e}" for x in dq)
        + f"; the second over the first: {dq[1] / dq[0]:.3e}",
        f"rel_x = (move / rel) / |q| at rel {rel:.0e}: {(mv / rel) / abs(q):.3e}", ""]
txt = "\n".join(out)
open(os.path.join(d, "tables.md"), "w").write(txt + "\n")
print(txt)
