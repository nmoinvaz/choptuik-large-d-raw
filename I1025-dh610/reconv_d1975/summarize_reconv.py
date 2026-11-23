#!/usr/bin/env python3
"""#1025 reconv_d1975 (dh610) summarize_reconv.py: prints the result tables of the README from the records in in/ and the ell_cond files in cond/.
No number is typed by hand. usage (from this folder): ~/Source/venv-i1058/bin/python -I summarize_reconv.py > summary.txt"""
import json, math

R = lambda f: json.loads(open(f).read().splitlines()[-1])
J = lambda f: json.load(open(f))

srcs = {"dh170": ("in/l1kc87dh170d1975.jsonl", "in/l1kc87linRe.jsonl", "linRe"),
        "macm3": ("in/l1kc87macm3d1975.jsonl", "in/l1kc87macRe.jsonl", "macRe")}
print("| state | record norm F before | norm F of the first evaluation in ell_refine (F_start) | record norm F after | steps | Delta before | Delta after | seconds |")
print("|---|---|---|---|---|---|---|---|")
for k, (a, b, name) in srcs.items():
    ra, rb = R(a), R(b)
    print(f"| {k} start -> {name} | {ra['F']:.10e} | {rb['F_start']:.10e} | {rb['F']:.10e} | {ra['steps']} -> {rb['steps']} | {ra['Delta']:.12f} | {rb['Delta']:.12f} | {rb['seconds']} |")

print()
print("| pair (A, B) | norm F(A) | norm F(B) at A's freeze | smallest 8 singular values of J(A) | norm dz | Delta entry of dz | part of dz outside the 8 | largest component along one of the 8 | norm J dz | norm F(B)-F(A) | norm J dz / norm dz |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for name, f in [("(linRe, macRe)", "cond/f_lin_mac.json"), ("(dh170 start, linRe)", "cond/f_dh170_lin.json"), ("(macm3 start, macRe)", "cond/f_macm3_mac.json"),
                ("planted control", "cond/f_plant.json")]:
    d = J(f)
    sm = ", ".join(f"{s:.2e}" for s in d["smin"])
    big = max(abs(c) for c in d["comp"])
    print(f"| {name} | {d['FA']:.4e} | {d['FB']:.4e} | {sm} | {d['dz']:.4e} | {d['dDelta']:+.4e} | {d['rest']:.4e} ({d['rest'] / d['dz']:.3f}) | {big:.2e} ({big / d['dz']:.1e}) | {d['lin']:.4e} | {d['dF']:.4e} | {d['lin'] / d['dz']:.2e} |")
d = J("cond/f_lin_mac.json")
print()
print(f"smax(J) {d['smax']:.6f}, n {d['n']}, condition (linRe, macRe) {d['smax'] / min(d['smin']):.3e}")

# distances between states, Delta included (L2 of the whole vector), as ell_cond's |dz|; needs numpy (run with the venv's python)
import numpy as np
S = {k: np.load(f"in/sol_{k}_D19.7500.npy") for k in ["l1kc87dh170d1975", "l1kc87macm3d1975", "l1kc87linRe", "l1kc87macRe"]}
print()
print("| pair | norm dz (L2, Delta included) | Delta entry |")
print("|---|---|---|")
for a, b in [("l1kc87dh170d1975", "l1kc87macm3d1975"), ("l1kc87linRe", "l1kc87macRe"), ("l1kc87dh170d1975", "l1kc87linRe"), ("l1kc87macm3d1975", "l1kc87macRe"),
             ("l1kc87dh170d1975", "l1kc87macRe"), ("l1kc87macm3d1975", "l1kc87linRe")]:
    d = S[b] - S[a]
    print(f"| ({a[6:]}, {b[6:]}) | {np.linalg.norm(d):.4e} | {d[-1]:+.4e} |")
