"""I850-mac tables: the Delta block's return per D and rel, from power.json and the dl_*.json runs.

dev = dDelta(seed) - dDelta(unperturbed), exact from eight parts (power.json). q = dev / rel^2 is the quadratic
coefficient, which a quadratic response holds fixed. The pivot change is the seed run's smallest pivot over the
unperturbed one, less 1. rel_x = (move / rel) / |q| at the smallest rel is where q rel^2 equals the move, the rel below
which a linear return of the move would dominate dev (an extrapolation of the quadratic term, not a measurement).
q's change per decade is relative to the larger rel's q; the second change over the first is about 0.1 for a cubic term.

Run: python3 tables.py [folder], default the folder of this script. Writes tables.md beside it.
"""
import json
import math
import os
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
pw = json.load(open(os.path.join(d, "power.json")))
tag = {"240": "D240", "252": "D252"}
out = ["# I850-mac tables (tables.py)", ""]
for g in pw["groups"]:
    key = tag[g["D_str"][:3]]
    out += [f"## D {g['D_str'][:12]}, blocks {', '.join(g['blocks'])}, seed {g['seed']}: {g['reading']}, "
            f"p {g['p'][0]:.4f}, {g['p'][1]:.4f}", "",
            "| rel | move | dev | \\|dev\\| / move | q = dev / rel² | smallest pivot / unperturbed − 1 | max\\|F\\| |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    last, qs = None, []
    for rel, dev in g["devs"]:
        e = round(-math.log10(rel))
        js = json.load(open(os.path.join(d, f"dl_{key}_r{e}.json")))
        u = next(r for r in js["runs"] if r["run"] == "unperturbed")
        s = next(r for r in js["runs"] if r["seed"] == g["seed"] and not r["control"])
        q = dev / rel ** 2
        out.append(f"| {rel:.0e} | {s['move']:.4e} | {dev:+.6e} | {abs(dev) / s['move']:.4e} | {q:+.4e} | "
                   f"{s['piv'][0] / u['piv'][0] - 1:+.3e} | {s['F']:.4e} |")
        last = (rel, s["move"], q)
        qs.append(q)
    rel, mv, q = last
    dq = [qs[i + 1] - qs[i] for i in range(len(qs) - 1)]
    out += ["", "q's change per decade (relative): " + ", ".join(f"{dq[i] / qs[i]:+.3e}" for i in range(len(dq)))
            + f"; the second change over the first: {dq[1] / dq[0]:.3e}",
            f"rel_x = (move / rel) / |q| at rel {rel:.0e}: {(mv / rel) / abs(q):.3e}", ""]
txt = "\n".join(out)
open(os.path.join(d, "tables.md"), "w").write(txt + "\n")
print(txt)
