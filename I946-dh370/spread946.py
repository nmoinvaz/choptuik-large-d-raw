"""#946 addendum: the seed spread of c = |dev| / rel^2 at D 245.6366, 250.1676 and 252.6135, and the growth of c with D per seed.

    python spread946.py RAW        (RAW: the raw clone with I851-dh370 and I946-dh370)

Sources, all step_spread.py power's exact devs: #851's power.json (seed 1 on the stored states at 245.6366 and 252.6135), #946's
power.json (seeds 1 and 2 on the re-converged state at 250.1676; #851's stored 250.1676 is not used) and #946's power_seed2.json
(seed 2 on the stored states at 245.6366 and 252.6135, the same states as #851's). rel 1e-80 is the one rel that is clean at every D
(pivot within 1% of the unperturbed at all three, #851 and #946 tables) and quadratic in each source. The slope is of ln c
against D per unit D, as step_spread.py sum's, at rel 1e-80, and #805's 1.44 and twice it are the references."""
import json
import os
import sys

import numpy as np

R = sys.argv[1]
SRC = [("851", "I851-dh370/power.json"), ("946", "I946-dh370/power.json"), ("946s2", "I946-dh370/power_seed2.json")]
c = {}      # (D, seed) -> {rel: (c, reading, p)}
for tag, rel_path in SRC:
    for g in json.load(open(os.path.join(R, rel_path)))["groups"]:
        D = round(float(g["D_str"][:12]), 4)
        if tag == "851" and D == 250.1676:
            continue                          # the stored state, superseded by the polished one
        c[(D, g["seed"])] = {r: (abs(d) / r ** 2, g["reading"], g["p"]) for r, d in g["devs"]}
Ds = sorted({k[0] for k in c})
print("c = |dev| / rel^2 per D and seed (rel 1e-80 and 1e-75 where it exists; the readings are step_spread.py power's)")
print("D          seed  reading     p                      c(1e-80)      c(1e-75)")
for D in Ds:
    for sd in (1, 2):
        e = c[(D, sd)]
        c75 = e.get(1e-75, (float("nan"),))[0]
        print(f"{D:<10.4f} {sd}     {e[1e-80][1]:<10}  {str([round(x, 4) if x else None for x in e[1e-80][2]]):<22} {e[1e-80][0]:.5e}   {c75:.5e}")
print("\nseed 2 against seed 1 (c2 / c1 - 1):")
for D in Ds:
    for rel in (1e-80, 1e-75):
        if rel in c[(D, 1)] and rel in c[(D, 2)]:
            print(f"  D {D:.4f} rel {rel:.0e}: {c[(D, 2)][rel][0] / c[(D, 1)][rel][0] - 1:+.4f}")
print("\nln c against D at rel 1e-80, per unit D:")
for sd in (1, 2):
    lc = np.log([c[(D, sd)][1e-80][0] for D in Ds])
    steps = ", ".join(f"{Ds[i]:.4f}->{Ds[i + 1]:.4f}: {(lc[i + 1] - lc[i]) / (Ds[i + 1] - Ds[i]):.4f}" for i in range(len(Ds) - 1))
    fit = float(np.polyfit(Ds, lc, 1)[0])
    print(f"  seed {sd}: steps {steps}; least squares {fit:.4f} (1.44: ratio {fit / 1.44:.3f}; 2.88: ratio {fit / 2.88:.3f})")
