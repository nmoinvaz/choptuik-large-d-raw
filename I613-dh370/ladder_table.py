#!/usr/bin/env python3
"""The tables of #613 from the eq_*.json files of this folder (Curtis-Reid + Ruiz, the result), beside the files of
I580-dh370/ (the raw-max floor, and the F = 0 controls). Run from this folder."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "..", "I580-dh370")
LAYS = ["070", "080", "092", "0975"]
FS = ["0", "1e-14", "1e-12", "1e-10"]
M = "Curtis-Reid + Ruiz"


def load(lay, F, d=HERE):
    return json.load(open(os.path.join(d, f"eq_{lay}_F{F}.json")))


def sig(d):
    return [v["sigma"] for v in d["methods"][M]["vectors"]]


print("1. covariant floor (e929849): equilibrated sigma_1..4, the planted check's max |sigma(J S)/sigma(J) - 1| (bound 1e-3), verdict")
for lay in LAYS:
    for F in FS:
        d = load(lay, F)
        p = d["plant"]
        print(f"  0.{lay[1:]:<3} F={F:<6}", " ".join(f"{s:.4e}" for s in sig(d)),
              f" rel {p['methods'][M]['rel']:.2e}", "pass" if p["ok"] else "FAIL")
print()
print("2. spread of sigma_i over the floors 1e-14, 1e-12, 1e-10 (max/min), and F = 1e-12 over F = 0")
for lay in LAYS:
    S = [sig(load(lay, F)) for F in FS[1:]]
    spread = [max(s[i] for s in S) / min(s[i] for s in S) for i in range(4)]
    s0, s12 = sig(load(lay, "0")), sig(load(lay, "1e-12"))
    print(f"  0.{lay[1:]:<3} spread", " ".join(f"{x:.4g}" for x in spread), "  F=1e-12 / F=0:", " ".join(f"{b / a:.3g}" for a, b in zip(s0, s12)))
print()
print("3. sigma_1 against #580's raw-max floor (I580-dh370, same states): covariant / raw-max, and the F = 0 controls of both")
for lay in LAYS:
    row = []
    for F in FS[1:]:
        row.append(f"F={F}: {sig(load(lay, F))[0] / sig(load(lay, F, OLD))[0]:.4g}")
    same = sig(load(lay, "0")) == sig(load(lay, "0", OLD))
    print(f"  0.{lay[1:]:<3}", "  ".join(row), "  F=0 sigma_1..4 identical to #580's:", same)
print()
print("4. weakest equilibrated sigma (sigma_1) and its ratio to the 0.70 layout")
for F in FS:
    b = sig(load("070", F))[0]
    print(f"  F={F:<6}", "  ".join(f"0.{lay[1:]}: {sig(load(lay, F))[0]:.3e} (x{sig(load(lay, F))[0] / b:.3g})" for lay in LAYS))
