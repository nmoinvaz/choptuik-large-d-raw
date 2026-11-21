#!/usr/bin/env python3
"""#1025 winb, the D 18.125 scan: the reading fixed by the coordinator (hc 2026-11-21 13:2x UTC): report every robust change of the hybrid sign with its
orientation, and every ln|det| local minimum without a change. Two changes give the gap at this D, beside D 18's 0.0325. No change where the pair was, with
a ln|det| minimum, means they met before this D.
usage: read_d18mid_1025.py SCAN.jsonl           (the records of d18_hybsign.py: D, lam, sign, ln, noise_robust, f64_sign)
- point: robust if the hybrid's sign survives its 1e-15 noise test (2 seeds);
- change: consecutive points (lam_i, lam_i+1) with different hybrid signs; ROBUST if both points are robust; orientation minus-to-plus or plus-to-minus;
- minimum: an interior point whose ln|det| is below both neighbours'; 'beside a change' if its sign differs from a neighbour's, else 'WITHOUT a change'; a point at the
  scan's end with a lower ln|det| than its only neighbour is listed as 'at the scan edge';
- gap (two robust changes): between the brackets, [lo2 - hi1, hi2 - lo1] and centre to centre, to compare with D 18's 0.0325 (the step is 0.01);
- float64 beside the hybrid: points where its sign differs (information)."""
import json, sys
fn = sys.argv[1]
P = sorted((json.loads(l) for l in open(fn) if l.strip()), key=lambda r: r["lam"])
D = P[0]["D"]
print(f"D {D} k_c {P[0]['kc']}: {len(P)} points, lam {P[0]['lam']} to {P[-1]['lam']}, state {P[0]['state']}")
nonrob = [r["lam"] for r in P if not r["noise_robust"]]
print(f"points whose hybrid sign is NOT noise robust: {nonrob if nonrob else 'none'}")
print("signs (hybrid): " + " ".join(f"{r['lam']:.2f}:{'+' if r['sign'] > 0 else '-'}" for r in P))
ch = []
for a, b in zip(P, P[1:]):
    if a["sign"] != b["sign"]:
        rb = a["noise_robust"] and b["noise_robust"]
        ori = "minus-to-plus" if a["sign"] < 0 else "plus-to-minus"
        ch.append((a["lam"], b["lam"], rb, ori))
        print(f"change in ({a['lam']:.2f}, {b['lam']:.2f}): {ori}, {'ROBUST' if rb else 'NOT ROBUST (a point fails its noise test)'}")
if not ch:
    print("no change of the hybrid sign over the window")
mins = []
for i, r in enumerate(P):
    nb = [P[j] for j in (i - 1, i + 1) if 0 <= j < len(P)]
    if len(nb) == 2 and r["ln"] < nb[0]["ln"] and r["ln"] < nb[1]["ln"]:
        beside = any(r["sign"] != n["sign"] for n in nb)
        mins.append((r["lam"], r["ln"], "beside a change" if beside else "WITHOUT a change"))
    elif len(nb) == 1 and r["ln"] < nb[0]["ln"]:
        mins.append((r["lam"], r["ln"], "at the scan edge"))
for lam, ln, w in mins:
    print(f"ln|det| local minimum at {lam:.2f} (ln {ln:.6f}): {w}")
if not mins:
    print("no ln|det| local minimum")
rc = [c for c in ch if c[2]]
if len(rc) == 2:
    (l1, h1, _, o1), (l2, h2, _, o2) = rc
    print(f"two robust changes ({o1} in ({l1:.2f}, {h1:.2f}), {o2} in ({l2:.2f}, {h2:.2f})): gap between {l2 - h1:.2f} and {h2 - l1:.2f}, centre to centre {0.5 * (l2 + h2) - 0.5 * (l1 + h1):.3f} (step 0.01; D 18: 0.0325)")
print("ln|det|: " + " ".join(f"{r['lam']:.2f}:{r['ln']:.3f}" for r in P))
d64 = [r["lam"] for r in P if r.get("f64_sign") is not None and r["f64_sign"] != r["sign"]]
print(f"float64 sign differs from the hybrid's at {len(d64)} of {len(P)} points: {[f'{x:.2f}' for x in d64]} (information)")
