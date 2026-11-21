#!/usr/bin/env python3
"""#1025 win2b, the finer D 18.5 scan at k_c 55: the reading fixed by the coordinator (hc ~22:26 UTC 21 Nov). winb's pinned reader (read_d18mid_1025.py) prints lambda to two decimals, which a 0.002
grid cannot use, so this reader has the same definitions with the step as a parameter and lambda to three decimals (checked against the pinned reader on real 0.01 scans, plant_checks_fine.py).
usage: read_fine.py SCAN.jsonl [--step 0.002] [--ends -,-]
Definitions (as in the pinned reader):
- point: robust if the hybrid's sign survives its 1e-15 noise test (2 seeds); change: two consecutive points of different hybrid sign, ROBUST if both points are; orientation minus-to-plus / plus-to-minus;
- minimum: an interior point whose ln|det| is below both neighbours'; 'beside a change' if its sign differs from a neighbour's, else 'WITHOUT a change'; a point at the scan's end below its only neighbour is
  'at the scan edge' (not resolved).
The coordinator's reading, fixed before the run: TWO robust changes inside the window = a close pair at k_c 55 where k_c 63 has one root (1.6772): report the pair's positions and gap. NO change, with the
ln|det| minimum resolved (an interior minimum WITHOUT a change), = a near miss: k_c 55 has no root there. Any other count is reported as OTHER (not covered by the fixed reading). --ends: the signs the 0.01 scan
had at this window's two ends (minus, minus): a mismatch is printed as INCONSISTENT (an odd number of changes between equal endpoint signs is impossible). The det-linear estimate of each change's root
(the line through the bracket's det = sign exp(ln); xfkappa's estimator, 1.677016 on the k_c 63 scan) is information, not a reading; the bracket is the position."""
import json, math, sys
args = sys.argv[1:]
step = 0.002
if "--step" in args:
    i = args.index("--step"); step = float(args[i + 1]); del args[i:i + 2]
ends = None
if "--ends" in args:
    i = args.index("--ends"); ends = args[i + 1].split(","); del args[i:i + 2]
P = sorted((json.loads(l) for l in open(args[0]) if l.strip()), key=lambda r: r["lam"])
nd = 3 if step < 0.0095 else 2
f = lambda x: f"{x:.{nd}f}"
print(f"D {P[0]['D']} k_c {P[0]['kc']}: {len(P)} points, lambda {f(P[0]['lam'])} to {f(P[-1]['lam'])} (step {step:g}), state {P[0]['state']}")
nonrob = [f(r["lam"]) for r in P if not r["noise_robust"]]
print(f"points whose hybrid sign is NOT noise robust: {nonrob if nonrob else 'none'}")
gaps = [(f(a['lam']), f(b['lam'])) for a, b in zip(P, P[1:]) if abs(b["lam"] - a["lam"] - step) > 1e-9]
if gaps:
    print(f"GRID GAPS (consecutive points not one step apart): {gaps}")
print("signs (hybrid): " + " ".join(f"{f(r['lam'])}:{'+' if r['sign'] > 0 else '-'}" for r in P))
ch = []
for a, b in zip(P, P[1:]):
    if a["sign"] != b["sign"]:
        rb = a["noise_robust"] and b["noise_robust"]
        ori = "minus-to-plus" if a["sign"] < 0 else "plus-to-minus"
        w = math.exp(a["ln"] - b["ln"])
        est = a["lam"] + (b["lam"] - a["lam"]) * w / (1.0 + w)
        ch.append(dict(a=a["lam"], b=b["lam"], rob=rb, ori=ori, est=est))
        print(f"change in ({f(a['lam'])}, {f(b['lam'])}): {ori}, {'ROBUST' if rb else 'NOT ROBUST (a point fails its noise test)'}; det-linear estimate {est:.6f} (information)")
if not ch:
    print("no change of the hybrid sign over the window")
mins = []
for i, r in enumerate(P):
    nb = [P[j] for j in (i - 1, i + 1) if 0 <= j < len(P)]
    if len(nb) == 2 and r["ln"] < nb[0]["ln"] and r["ln"] < nb[1]["ln"]:
        beside = any(r["sign"] != n["sign"] for n in nb)
        mins.append((r["lam"], r["ln"], "beside a change" if beside else "WITHOUT a change", r["ln"] - nb[0]["ln"], r["ln"] - nb[1]["ln"]))
    elif len(nb) == 1 and r["ln"] < nb[0]["ln"]:
        mins.append((r["lam"], r["ln"], "at the scan edge", r["ln"] - nb[0]["ln"], None))
for lam, ln, w, dl, dr in mins:
    tail = f" (below the left neighbour by {-dl:.4f}" + (f", the right by {-dr:.4f})" if dr is not None else ")") if w != "at the scan edge" else f" (below its neighbour by {-dl:.4f})"
    print(f"ln|det| local minimum at {f(lam)} (ln {ln:.6f}): {w}{tail}")
if not mins:
    print("no ln|det| local minimum")
print("ln|det|: " + " ".join(f"{f(r['lam'])}:{r['ln']:.4f}" for r in P))
s0, s1 = ("-" if P[0]["sign"] < 0 else "+"), ("-" if P[-1]["sign"] < 0 else "+")
msg = f"endpoint signs: {s0} at {f(P[0]['lam'])}, {s1} at {f(P[-1]['lam'])}"
if ends:
    msg += " (the 0.01 scan: " + ", ".join(ends) + f") -> {'consistent' if [s0, s1] == ends else 'INCONSISTENT'}"
print(msg)
rc = [c for c in ch if c["rob"]]
nn = len(ch) - len(rc)
note = f" ({nn} non-robust change(s) not counted)" if nn else ""
if len(rc) == 2:
    (c1, c2) = rc
    print(f"FINE READING: PAIR. Two robust changes inside the window: {c1['ori']} in ({f(c1['a'])}, {f(c1['b'])}) and {c2['ori']} in ({f(c2['a'])}, {f(c2['b'])}); gap between the brackets "
          f"{f(c2['a'] - c1['b'])} to {f(c2['b'] - c1['a'])}, centre to centre {0.5 * (c2['a'] + c2['b']) - 0.5 * (c1['a'] + c1['b']):.4f}; det-linear estimates {c1['est']:.6f} and {c2['est']:.6f}, "
          f"gap {c2['est'] - c1['est']:.6f} (information){note}")
elif len(rc) == 0:
    inter = [m for m in mins if m[2] == "WITHOUT a change"]
    if inter:
        m = inter[0]
        print(f"FINE READING: NEAR MISS. No robust change; the ln|det| minimum is resolved: an interior local minimum WITHOUT a change at {f(m[0])} (ln {m[1]:.6f}, below its neighbours by {-m[3]:.4f} and {-m[4]:.4f}); k_c 55 has no root there{note}")
    elif mins:
        print(f"FINE READING: NO CHANGE, MINIMUM NOT RESOLVED. No robust change; the ln|det| minimum is at the scan edge ({f(mins[0][0])}){note}")
    else:
        print(f"FINE READING: NO CHANGE, NO ln|det| MINIMUM{note}")
else:
    print(f"FINE READING: OTHER. {len(rc)} robust change(s) inside the window; the fixed reading covers 0 and 2, so this is reported and not read{note}")
