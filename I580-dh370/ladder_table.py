#!/usr/bin/env python3
"""The tables of #580 from the eq_*.json files of this folder (Curtis-Reid + Ruiz, the result), and the F = 0 values of
the earlier issues (#505 for 0.70, #543 for 0.80, #554 for 0.92; none exists at 0.975). Run from this folder."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LAYS = ["070", "080", "092", "0975"]
FS = ["0", "1e-14", "1e-12", "1e-10"]
OLD = {"070": "I505-win2/eq_D242.3642.json", "080": "I543-win2/eq_last080.json", "092": "I554-win2/eq_last092.json"}
M = "Curtis-Reid + Ruiz"


def load(lay, F):
    return json.load(open(os.path.join(HERE, f"eq_{lay}_F{F}.json")))


def sig(d):
    return [v["sigma"] for v in d["methods"][M]["vectors"]]


print("1. equilibrated sigma_1..4, the planted check's max |sigma(J S)/sigma(J) - 1| (bound 1e-3) and its verdict")
for lay in LAYS:
    for F in FS:
        d = load(lay, F)
        p = d["plant"]
        print(f"  0.{lay[1:]:<3} F={F:<6}", " ".join(f"{s:.4e}" for s in sig(d)),
              f" rel {p['methods'][M]['rel']:.2e}", "pass" if p["ok"] else "FAIL")
print()
print("2. spread of sigma_i over the floors 1e-14, 1e-12, 1e-10 (max/min; criterion: below 2), and F = 0 against F = 1e-12")
for lay in LAYS:
    S = [sig(load(lay, F)) for F in FS[1:]]
    spread = [max(s[i] for s in S) / min(s[i] for s in S) for i in range(4)]
    s0, s12 = sig(load(lay, "0")), sig(load(lay, "1e-12"))
    print(f"  0.{lay[1:]:<3} spread", " ".join(f"{x:.3f}" for x in spread), "  F=1e-12 / F=0:", " ".join(f"{b / a:.3g}" for a, b in zip(s0, s12)))
print()
print("3. weakest equilibrated sigma (sigma_1) and its ratio to the 0.70 layout")
base = {k: sig(load("070", k))[0] for k in FS}
old0 = json.load(open(os.path.join(HERE, "..", OLD["070"])))["methods"][M]["vectors"][0]["sigma"]
print("  layout   old F=0 (double-double projector)   new F=0   new F=1e-12   ratios to 0.70: old | new F=0 | new F=1e-12")
for lay in LAYS:
    o = json.load(open(os.path.join(HERE, "..", OLD[lay])))["methods"][M]["vectors"][0]["sigma"] if lay in OLD else None
    n0, n12 = sig(load(lay, "0"))[0], sig(load(lay, "1e-12"))[0]
    print(f"  0.{lay[1:]:<5}", f"{o:.4e}" if o else "   -    ", f"      {n0:.4e}   {n12:.4e}   ",
          f"{o / old0:.3g}" if o else "-", "|", f"{n0 / base['0']:.3g}", "|", f"{n12 / base['1e-12']:.3g}")
