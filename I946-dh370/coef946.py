"""#946: c = |dev| / rel^2 per seed and rel from power.json (step_spread.py power's exact devs), against #851's value at D 250.1676.

    python coef946.py FOLDER [ #851 folder ]"""
import json
import os
import sys

pw = json.load(open(os.path.join(sys.argv[1], "power.json")))
print("D 250.1676 re-converged (max|F| 3.0e-92): c = |dev| / rel^2")
for g in pw["groups"]:
    cs = [abs(d) / r ** 2 for r, d in g["devs"]]
    print(f"  seed {g['seed']}: " + ", ".join(f"rel {r:.0e} {c:.5e}" for (r, _), c in zip(g["devs"], cs)) + f"; p {g['p']}; {g['reading']}")
if len(sys.argv) > 2:
    p851 = json.load(open(os.path.join(sys.argv[2], "power.json")))
    g = [x for x in p851["groups"] if x["D_str"].startswith("250.16758")][0]
    print("#851, the stored state (max|F| 3.05e-61), seed 1: " + ", ".join(f"rel {r:.0e} {abs(d) / r ** 2:.5e}" for r, d in g["devs"]))
