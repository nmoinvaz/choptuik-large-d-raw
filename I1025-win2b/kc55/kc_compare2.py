#!/usr/bin/env python3
"""#1025 win2b, the k_c test at D 18.25 (the coordinator's reading, fixed before the run, tightened by the coordinator before any result: see the README, Part 3, "Amendment 1"): compare the robust sign
changes of the hybrid det at k_c 55 with the k_c 63 roots (xfkappa, comment 7070296128: 1.3885, 1.7425, 2.3187).
AMENDED RULE: compare the k_c 55 change's DET-LINEAR ESTIMATE (as d18f_read and xfkappa's readers compute it) with the k_c 63 root: within 0.02 is STABLE; otherwise the root depends on k_c. The bracket-to-root
distance with its inside / straddling marks (the first version's rule, kc_compare2_v1_bracket_rule.py a7289a19) stays in each line as information.
usage: kc_compare2.py MERGED.jsonl --band 0.02 --r63 1.3885,1.7425,2.3187 [--cov63 LO,HI] [--ori63 o1,o2,o3]
Definitions. A k_c 55 change is two consecutive points of different hybrid sign, both passing the 1e-15 noise test (ROBUST); it lies in its bracket (a, b). Its det-linear estimate is the zero of the line through
the bracket's two points of f = sign * exp(ln - ref), ref the scan's largest ln|det| (it cancels): x_a + (x_b - x_a) f_a / (f_a - f_b), the same formula as `changes()` in xfkappa's d185_scan_read.py (blob 7c9d400f; its
`lin`, which d18f_read.py uses; the planted controls check this script's estimate against that function). STABLE: some k_c 63 root within BAND of the estimate; k_c-DEPENDENT (k_c 55 only): none; a k_c 63 root with no
robust k_c 55 change whose estimate is within BAND: k_c-DEPENDENT (k_c 63 only). A change that touches a non-robust point is listed with its estimate and not counted; a k_c 63 root with only such a change within BAND is
UNDETERMINED. A k_c 55 change whose bracket is outside the k_c 63 coverage is not compared. --ori63: the k_c 63 roots' orientations, printed beside each match as information; the rule does not use orientation, and
orientation readings wait for xfkappa's sign-convention check. The information marks: the bracket is wholly inside the band [r - BAND, r + BAND], straddles its edge (distance from r to the bracket at most BAND), or lies outside it."""
import json, sys
import numpy as np
args = sys.argv[1:]
band, cov, r63, ori63 = 0.02, None, [], None
for opt in ("--band", "--cov63", "--r63", "--ori63"):
    if opt in args:
        i = args.index(opt); v = args[i + 1]; del args[i:i + 2]
        if opt == "--band": band = float(v)
        elif opt == "--cov63": cov = tuple(float(x) for x in v.split(","))
        elif opt == "--r63": r63 = [float(x) for x in v.split(",") if x]
        else: ori63 = v.split(",")
P = sorted((json.loads(l) for l in open(args[0]) if l.strip()), key=lambda r: r["lam"])
cov = cov or (P[0]["lam"], P[-1]["lam"])
eps = 1e-9
f3 = lambda x: f"{x:.3f}"
print(f"D {P[0]['D']} k_c {P[0]['kc']}: {len(P)} points, lambda {f3(P[0]['lam'])} to {f3(P[-1]['lam'])}; k_c 63 coverage {f3(cov[0])} to {f3(cov[1])}, k_c 63 roots {r63}, band {band} (rule: the det-linear estimate within the band of a k_c 63 root)")
x = np.array([r["lam"] for r in P]); ref = max(r["ln"] for r in P)
fv = np.array([r["sign"] * np.exp(r["ln"] - ref) for r in P])
ch = []
for i in range(len(P) - 1):
    if P[i]["sign"] != P[i + 1]["sign"]:
        est = float(x[i] + (x[i + 1] - x[i]) * fv[i] / (fv[i] - fv[i + 1]))
        ch.append((float(x[i]), float(x[i + 1]), P[i]["noise_robust"] and P[i + 1]["noise_robust"], "minus-to-plus" if P[i]["sign"] < 0 else "plus-to-minus", est))
bd = lambda a, b, r: 0.0 if a - eps <= r <= b + eps else min(abs(r - a), abs(r - b))
wholly = lambda a, b, r: a >= r - band - eps and b <= r + band + eps


def mark(a, b, r):
    if wholly(a, b, r):
        return f"information, the bracket reading: the bracket is wholly inside the band {r - band:.4f} to {r + band:.4f} of the k_c 63 root {r}"
    if bd(a, b, r) <= band + eps:
        return f"information, the bracket reading: the bracket straddles the band edge, {bd(a, b, r):.4f} from the k_c 63 root {r}, so the root may be up to {max(abs(r - a), abs(r - b)):.4f} from it"
    return f"information, the bracket reading: the bracket is outside the band, {bd(a, b, r):.4f} from the nearest k_c 63 root {r}"


n = dict(stable=0, wholly=0, straddle=0, outside=0, dep55=0, dep63=0, undet=0, notcmp=0)
for a, b, rob, ori, est in ch:
    tag = f"k_c 55 change in ({f3(a)}, {f3(b)}), {ori}, {'ROBUST' if rob else 'NOT ROBUST (a point fails its noise test), not counted'}, det-linear estimate {est:.6f}"
    if not rob:
        print(tag); continue
    if not (a >= cov[0] - eps and b <= cov[1] + eps):
        n["notcmp"] += 1
        print(f"{tag}: not compared (k_c 63 is not scanned over this bracket, coverage {f3(cov[0])} to {f3(cov[1])})"); continue
    near = min(r63, key=lambda r: abs(est - r)) if r63 else None
    if near is not None and abs(est - near) <= band + eps:
        i = r63.index(near)
        o = f"; the k_c 63 root's orientation is {ori63[i]}, {'the same' if ori63[i] == ori else 'the opposite'} (information)" if ori63 and i < len(ori63) else ""
        n["stable"] += 1
        key = "wholly" if wholly(a, b, near) else ("straddle" if bd(a, b, near) <= band + eps else "outside")
        n[key] += 1
        print(f"{tag}: STABLE (the estimate is {abs(est - near):.4f} from the k_c 63 root {near}, within {band}{o}) [{mark(a, b, near)}]")
    else:
        n["dep55"] += 1
        if near is None:
            print(f"{tag}: k_c-DEPENDENT (k_c 55 only: there is no k_c 63 root)")
        else:
            print(f"{tag}: k_c-DEPENDENT (k_c 55 only: the estimate is {abs(est - near):.4f} from the nearest k_c 63 root {near}, farther than {band}) [{mark(a, b, near)}]")
for r in r63:
    if not (P[0]["lam"] - eps <= r <= P[-1]["lam"] + eps):
        print(f"k_c 63 root {r}: outside the k_c 55 window, not compared"); continue
    touch = [(a, b, rob, est) for a, b, rob, _, est in ch if abs(est - r) <= band + eps]
    rb = [t for t in touch if t[2]]
    if rb:
        a, b, _, est = rb[0]
        print(f"k_c 63 root {r}: MATCHED by the k_c 55 robust change in ({f3(a)}, {f3(b)}) (estimate {est:.6f}, {abs(est - r):.4f} from it)")
    elif not touch:
        n["dep63"] += 1
        print(f"k_c 63 root {r}: k_c-DEPENDENT (k_c 63 only: no k_c 55 change, robust or not, has its det-linear estimate within {band} of it)")
    else:
        n["undet"] += 1
        print(f"k_c 63 root {r}: UNDETERMINED (only non-robust k_c 55 change(s) with the estimate within {band}: " + ", ".join(f"({f3(a)}, {f3(b)}) estimate {e:.6f}" for a, b, _, e in touch) + ")")
nrob = [c for c in ch if c[2]]
print(f"SUMMARY: {len(nrob)} robust k_c 55 change(s); stable (the rule): {n['stable']} (information, the bracket marks: {n['wholly']} wholly inside a band, {n['straddle']} straddling a band edge, {n['outside']} outside every band); "
      f"k_c-dependent: {n['dep55']} k_c 55 only + {n['dep63']} k_c 63 only; undetermined {n['undet']}; not compared {n['notcmp']}")
