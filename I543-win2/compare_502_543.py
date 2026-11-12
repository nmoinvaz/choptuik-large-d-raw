#!/usr/bin/env python3
"""#543: the five-node layout 0.3, 0.4, 0.5, 0.6, 0.8 of this task against #502's six-node 0.3-0.8 layout (0.3 ... 0.7, 0.8), at D 242.36, equilibrated and raw sigma_1..4.
usage: python compare_502_543.py [--mutate]       (run from I543-win2; the #502 values are those of its closing comment, 2026-11-11 18:49 UTC, not new data)
If the law is about the last node, the two layouts have the same sigma. Reports ln(sigma_i(0.8)) - ln(sigma_i(0.7)) for both, against the same 0.3-0.7 baseline (equilibrated: I537-win2's; #502's own 0.7 values are equal to its digits).
Exits 1 if any equilibrated difference exceeds 0.05 in ln. --mutate compares #502 against this task's 0.76 layout instead, which must exit 1."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
I502 = {"raw07": [2.551e-27, 2.530e-27, 4.392e-26, 7.930e-26], "eq07": [1.8825e-61, 9.3856e-61, 2.6498e-59, 2.4555e-57],
        "raw08": [8.433e-38, 6.954e-35, 6.968e-35, 1.766e-34], "eq08": [1.4235e-56, 1.9109e-54, 2.7718e-54, 4.5224e-53]}


def vals(path, method):
    s = open(path, encoding="utf-8").read()
    if method == "raw":
        v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    else:
        v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+Curtis-Reid \+ Ruiz sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    return [v[i] for i in (1, 2, 3, 4)]


tag = "last076" if "--mutate" in sys.argv else "last080"
base = os.path.join(HERE, "..", "I537-win2")
bad = 0
print(f"five-node layout {tag} against #502's six-node 0.3-0.8 layout: ln sigma_i(new) - ln sigma_i(0.3-0.7 baseline)")
print("| reading | sigma_1 here / #502 | sigma_2 | sigma_3 | sigma_4 | largest difference |\n|---|---|---|---|---|---|")
for name, key, ours_new, ours_base in (("raw", "raw", vals(os.path.join(HERE, f"nn_{tag}.log"), "raw"), vals(os.path.join(base, "nn_base.log"), "raw")),
                                       ("equilibrated", "eq", vals(os.path.join(HERE, f"eq_{tag}.log"), "eq"), vals(os.path.join(base, "eq_base.log"), "eq"))):
    a = [math.log(n / b) for n, b in zip(ours_new, ours_base)]
    c = [math.log(n / b) for n, b in zip(I502[key + "08"], I502[key + "07"])]
    dmax = max(abs(x - y) for x, y in zip(a, c))
    print(f"| {name} | " + " | ".join(f"{x:+.3f} / {y:+.3f}" for x, y in zip(a, c)) + f" | {dmax:.3f} |")
    if key == "eq" and dmax > 0.05:
        bad = 1
print("equilibrated spectra agree to 0.05 in ln" if not bad else "equilibrated spectra differ by more than 0.05 in ln")
sys.exit(bad)
