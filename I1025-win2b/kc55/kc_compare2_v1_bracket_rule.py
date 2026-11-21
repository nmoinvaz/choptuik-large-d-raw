#!/usr/bin/env python3
"""#1025 win2b, the k_c test at D 18.25 (the coordinator's reading, fixed before the run): compare the robust sign changes of the hybrid det at k_c 55 with the k_c 63 roots (xfkappa, comment 7070296128:
1.3885, 1.7425, 2.3187). Each k_c 55 change within 0.02 of a k_c 63 root counts as stable; the rest are k_c-dependent.
usage: kc_compare2.py MERGED.jsonl --band 0.02 --r63 1.3885,1.7425,2.3187 [--cov63 LO,HI] [--ori63 o1,o2,o3]
Definitions. A k_c 55 change is two consecutive points of different hybrid sign, both passing the 1e-15 noise test (ROBUST); it lies in its bracket (a, b), b - a = the step. "Within 0.02 of a k_c 63 root r"
is read as: the distance from r to the bracket [a, b] is at most 0.02 (0 if r is inside). That is the coordinator's two-class rule. The bracket is as wide as the band, so it is also said whether the bracket lies
wholly inside the band [r - 0.02, r + 0.02] (then the k_c 55 root is certainly within 0.02 of r: "wholly inside") or straddles its edge (the root may be up to 0.04 from r: "straddles the band edge"); both are STABLE
by the rule, and the count of each is printed. A change farther than 0.02 from every k_c 63 root is k_c-DEPENDENT (k_c 55 only); a k_c 63 root with no robust k_c 55 change within 0.02 is k_c-DEPENDENT (k_c 63 only).
A change that touches a non-robust point is listed and not counted; a k_c 63 root with only such a change near it is UNDETERMINED. A k_c 55 change outside the k_c 63 coverage is not compared. --ori63: the k_c 63
roots' orientations (plus-to-minus or minus-to-plus), printed beside each match as information; the rule does not use orientation, and orientation readings wait for xfkappa's sign-convention check."""
import json, sys
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
f = lambda x: f"{x:.3f}"
print(f"D {P[0]['D']} k_c {P[0]['kc']}: {len(P)} points, lambda {f(P[0]['lam'])} to {f(P[-1]['lam'])}; k_c 63 coverage {f(cov[0])} to {f(cov[1])}, k_c 63 roots {r63}, band {band}")
ch = []
for a, b in zip(P, P[1:]):
    if a["sign"] != b["sign"]:
        ch.append((a["lam"], b["lam"], a["noise_robust"] and b["noise_robust"], "minus-to-plus" if a["sign"] < 0 else "plus-to-minus"))
dist = lambda a, b, r: 0.0 if a - eps <= r <= b + eps else min(abs(r - a), abs(r - b))
wholly = lambda a, b, r: a >= r - band - eps and b <= r + band + eps
n = dict(wholly=0, straddle=0, dep55=0, dep63=0, undet=0, notcmp=0)
for a, b, rob, ori in ch:
    tag = f"k_c 55 change in ({f(a)}, {f(b)}), {ori}, {'ROBUST' if rob else 'NOT ROBUST (a point fails its noise test), not counted'}"
    if not rob:
        print(tag); continue
    if not (a >= cov[0] - eps and b <= cov[1] + eps):
        n["notcmp"] += 1
        print(f"{tag}: not compared (k_c 63 is not scanned over this bracket, coverage {f(cov[0])} to {f(cov[1])})"); continue
    near = sorted(r63, key=lambda r: dist(a, b, r))[:1]
    if near and dist(a, b, near[0]) <= band + eps:
        r = near[0]; i = r63.index(r)
        o = f"; the k_c 63 root's orientation is {ori63[i]}, {'the same' if ori63[i] == ori else 'the opposite'} (information)" if ori63 and i < len(ori63) else ""
        if wholly(a, b, r):
            n["wholly"] += 1
            print(f"{tag}: STABLE (the bracket is wholly inside the band {r - band:.4f} to {r + band:.4f} of the k_c 63 root {r}{o})")
        else:
            n["straddle"] += 1
            print(f"{tag}: STABLE (within {band} of the k_c 63 root {r}: distance {dist(a, b, r):.4f} from the bracket, which straddles the band edge, so the root may be up to {max(abs(r - a), abs(r - b)):.4f} from it{o})")
    else:
        n["dep55"] += 1
        rr = f"; the nearest k_c 63 root {near[0]} is {dist(a, b, near[0]):.4f} from the bracket" if near else ""
        print(f"{tag}: k_c-DEPENDENT (k_c 55 only: no k_c 63 root within {band}{rr})")
for r in r63:
    if not (P[0]["lam"] - eps <= r <= P[-1]["lam"] + eps):
        print(f"k_c 63 root {r}: outside the k_c 55 window, not compared"); continue
    touch = [(a, b, rob) for a, b, rob, _ in ch if dist(a, b, r) <= band + eps]
    rb = [t for t in touch if t[2]]
    if rb:
        a, b, _ = rb[0]
        print(f"k_c 63 root {r}: MATCHED by the k_c 55 robust change in ({f(a)}, {f(b)}) ({'wholly inside its band' if wholly(a, b, r) else 'straddling the band edge'})")
    elif not touch:
        n["dep63"] += 1
        print(f"k_c 63 root {r}: k_c-DEPENDENT (k_c 63 only: no k_c 55 change, robust or not, within {band} of it)")
    else:
        n["undet"] += 1
        print(f"k_c 63 root {r}: UNDETERMINED (only non-robust k_c 55 change(s) within {band}: " + ", ".join(f"({f(a)}, {f(b)})" for a, b, _ in touch) + ")")
nrob = [c for c in ch if c[2]]
print(f"SUMMARY: {len(nrob)} robust k_c 55 change(s); stable: {n['wholly']} wholly inside a band + {n['straddle']} straddling a band edge; k_c-dependent: {n['dep55']} k_c 55 only + {n['dep63']} k_c 63 only; "
      f"undetermined {n['undet']}; not compared {n['notcmp']}")
