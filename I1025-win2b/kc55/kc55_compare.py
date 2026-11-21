#!/usr/bin/env python3
"""#1025 win2b, D 18.5: which roots are k_c-stable (the coordinator's reading, fixed before the run): compare the robust sign changes of the hybrid det at k_c 55 with the roots at k_c 63.
A root at both k_c within 0.01 is k_c-stable; a root at one k_c only depends on the discretization.
usage: kc55_compare.py MERGED.jsonl [--cov63 LO,HI] [--r63 R1,R2,...]    defaults: k_c 63 scanned over 1.55 to 2.10 with its one root 1.6772 (the coordinator's figure; the det-linear estimate on
the Mac's scan is 1.677016, estimator range [1.677016, 1.677225]). When xfkappa's k_c 63 scan of 2.10 to 2.40 is in, rerun with --cov63 1.55,2.40 and its roots.
Definitions. A k_c 55 root is a ROBUST change (two consecutive points of different hybrid sign, both passing the 1e-15 noise test); it lies in its bracket (a, b), b - a = 0.01. A k_c 63 root r
and a k_c 55 root are within 0.01 when the root is in the band [r - 0.01, r + 0.01]. With the bracket only: the bracket inside the band -> STABLE; the bracket disjoint from the band of every
k_c 63 root -> k_c 55 ONLY; otherwise UNDETERMINED at this step (reported, not decided). The same for each k_c 63 root: a robust k_c 55 bracket inside its band -> MATCHED; no k_c 55 change (robust or not)
touching the band -> k_c 63 ONLY; otherwise UNDETERMINED. A k_c 55 change outside the k_c 63 coverage: not compared. A change that touches a non-robust point is listed and not counted;
orientation is printed as the scan gives it and is not used by the rule."""
import json, sys
args = sys.argv[1:]
cov, r63 = (1.55, 2.10), [1.6772]
if "--cov63" in args:
    i = args.index("--cov63"); cov = tuple(float(x) for x in args[i + 1].split(",")); del args[i:i + 2]
if "--r63" in args:
    i = args.index("--r63"); r63 = [float(x) for x in args[i + 1].split(",") if x]; del args[i:i + 2]
P = sorted((json.loads(l) for l in open(args[0]) if l.strip()), key=lambda r: r["lam"])
BAND = 0.01
print(f"D {P[0]['D']} k_c {P[0]['kc']}: {len(P)} points, lambda {P[0]['lam']:.2f} to {P[-1]['lam']:.2f}; k_c 63 coverage {cov[0]:.2f} to {cov[1]:.2f}, k_c 63 roots {r63}")
ch = []
for a, b in zip(P, P[1:]):
    if a["sign"] != b["sign"]:
        ch.append((a["lam"], b["lam"], a["noise_robust"] and b["noise_robust"], "minus-to-plus" if a["sign"] < 0 else "plus-to-minus"))
eps = 1e-9
inside = lambda a, b, r: a >= r - BAND - eps and b <= r + BAND + eps          # bracket inside the band
disjoint = lambda a, b, r: b < r - BAND - eps or a > r + BAND + eps           # bracket outside the band
for a, b, rob, ori in ch:
    tag = f"k_c 55 change in ({a:.2f}, {b:.2f}), {ori}, {'ROBUST' if rob else 'NOT ROBUST (a point fails its noise test), not counted'}"
    if not rob:
        print(tag); continue
    if not (a >= cov[0] - eps and b <= cov[1] + eps):
        print(f"{tag}: not compared (k_c 63 is not scanned over this bracket, coverage {cov[0]:.2f} to {cov[1]:.2f})"); continue
    if any(inside(a, b, r) for r in r63):
        r = [r for r in r63 if inside(a, b, r)][0]
        print(f"{tag}: STABLE (the bracket is inside the band of the k_c 63 root {r}: {r - BAND:.4f} to {r + BAND:.4f})")
    elif all(disjoint(a, b, r) for r in r63):
        print(f"{tag}: k_c 55 ONLY (the bracket is outside the band of every k_c 63 root {r63})")
    else:
        print(f"{tag}: UNDETERMINED at the 0.01 step (the bracket straddles the edge of a k_c 63 root's band)")
for r in r63:
    if not (P[0]["lam"] <= r <= P[-1]["lam"]):
        print(f"k_c 63 root {r}: outside the k_c 55 window, not compared"); continue
    near = [(a, b, rob, ori) for a, b, rob, ori in ch if not (disjoint(a, b, r))]
    ins = [c for c in near if c[2] and inside(c[0], c[1], r)]
    if ins:
        print(f"k_c 63 root {r}: MATCHED, k_c 55 robust change {ins[0][3]} in ({ins[0][0]:.2f}, {ins[0][1]:.2f}) inside its band")
    elif not near:
        print(f"k_c 63 root {r}: k_c 63 ONLY (no k_c 55 change, robust or not, touches its band {r - BAND:.4f} to {r + BAND:.4f})")
    else:
        print(f"k_c 63 root {r}: UNDETERMINED at the 0.01 step (k_c 55 change(s) touching its band: " + ", ".join(f"({a:.2f}, {b:.2f}) {'robust' if rb else 'not robust'}" for a, b, rb, _ in near) + ")")
nrob = [c for c in ch if c[2]]
print(f"SUMMARY: {len(nrob)} robust k_c 55 change(s) in {P[0]['lam']:.2f} to {P[-1]['lam']:.2f}; " + (", ".join(f"({a:.2f}, {b:.2f}) {o}" for a, b, _, o in nrob) if nrob else "none"))
