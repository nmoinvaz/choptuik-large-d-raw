#!/usr/bin/env python3
"""#1029 (win), supplementary to the issue's readings (not one of them): where the amplitude series stops being usable at the two low-omega zeros.
Per run: |sigma_n| (n = 0 .. 12, order 2n + 1), the order k of the first |sigma| above 1e3 or non-finite, and for nu = 3, 5, 7 the sizes |f(k, nu) A^k| of the terms of F_nu's sum
(k = nu, nu + 2, ..., 13) beside hier's |F_nu| (|F_nu/F_1| of #1027 times A / 2); and the same terms of the stored K 45 file at its zero (A 2.72) as the working case.
usage: python -I -X utf8 terms_1029.py > terms_1029.txt"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i1029"
K45 = os.path.join(WT, "solver", "inner_amp", "scan45J1250", "sigF_w1.0000_K45_J1250_p1280.json")
RUNS = [("0.065740", 2.233308, (0.330, 0.194, 0.131)), ("0.100532", 2.573290, (0.332, 0.184, 0.117))]


def fnum(v):
    return f"{v:.2e}" if math.isfinite(v) else "inf"


def terms(f, A, nu, kmax):
    out = []
    for k in range(nu, kmax + 1, 2):
        z = f.get(f"{k}_{nu}")
        out.append((k, abs(complex(*z)) * A ** k if z else float("nan")))
    return out


def show(label, d, A, ref, kmax):
    sg = [complex(float(a), float(b)) for a, b in d["sigma_str"]]
    bad = next((n for n, z in enumerate(sg) if not math.isfinite(abs(z)) or abs(z) > 1e3), None)
    print(f"\n{label}: K {d['K']} J {d['J']}, {d['seconds']:.0f} s")
    print("|sigma_n|, n = 0 .. %d: " % (len(sg) - 1) + " ".join(fnum(abs(z)) for z in sg))
    print(f"first |sigma_n| above 1e3 (or non-finite): " + (f"n = {bad}, order k = {2 * bad + 1}" if bad is not None else "none"))
    print("| nu | hier \|F_nu\| | " + " | ".join(f"k {k}" for k in range(3, kmax + 1, 2)) + " |\n|---|---|" + "---|" * len(range(3, kmax + 1, 2)))
    for i, nu in enumerate((3, 5, 7)):
        t = dict(terms(d["f"], A, nu, kmax))
        print(f"| {nu} | {ref[i]:.3f} | " + " | ".join(fnum(t[k]) if k in t else "" for k in range(3, kmax + 1, 2)) + " |")


for wf, A, hr in RUNS:
    for J in (750, 1000):
        d = json.load(open(os.path.join(HERE, f"sigF_w{wf}_K25_J{J}.json")))
        show(f"wf {wf} (A {A})", d, A, [x * A / 2 for x in hr], 13)
d = json.load(open(K45))
show("the working case, wf 1.0 (A 2.72, stored K 45 file)", d, 2.72, [0.05508 * 2.72 / 2 * (0.0572 ** i) for i in range(3)], 13)
print("\n(the last row's reference is the same file's own |F_nu|: 0.0551 |F_1|, then times 0.0572 and 0.0574 per pair)")
