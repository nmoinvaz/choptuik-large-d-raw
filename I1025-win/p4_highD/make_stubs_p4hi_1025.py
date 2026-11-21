#!/usr/bin/env python3
"""#1025 winb follow-on: the guesses (quadratic through the signtested k_c 63 rows D 16.5, 16.75, 17, evaluated at D 17.5 and 17.75, 4 decimals)
and the two stub records p4_hybrid.py reads (it takes lam_guess from the record's line at D and needs lam, kc, kappa, u0, Ks, F, steps).
Row A: the D 17.5 line of raw I1025-win/out/l1kc63Fw1025.jsonl unchanged, except lam_guess (the record's own is D 17's lambda 2.0265465).
Row B: the D 17.75 line of raw I1025-win/leap_kc63.log unchanged (no lam: it is a leap state), plus lam_guess and lam = the guess (placeholder: p4_hybrid.py
needs a lam; its minus_record for this row is the root minus the guess, not a record)."""
import json, subprocess, sys
import numpy as np
RAW = "C:/Users/nathan/Source/p4hi_1025/raw/"
OUT = "C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/"
rows63 = {}
for l in open(RAW + "I1025-win/out/l1kc63Fw1025.jsonl"):
    d = json.loads(l)
    rows63[d["D"]] = d
# signtested k_c 63 rows: D 16.5 (winb, passed), 16.75 (win2b, passed; winb's record), 17 (winb, passed): lambda from raw
lam = {16.5: 2.1454677042524617, 16.75: 2.0834870037231608, 17.0: rows63[17.0]["lam"]}
p = np.polyfit(list(lam), list(lam.values()), 2)
GA, GB = round(float(np.polyval(p, 17.5)), 4), round(float(np.polyval(p, 17.75)), 4)
print("trend: quadratic through", lam, "-> D 17.5", float(np.polyval(p, 17.5)), "D 17.75", float(np.polyval(p, 17.75)))
print("guesses (4 decimals): A", GA, "B", GB)
a = dict(rows63[17.5]); a["lam_guess_record"] = a["lam_guess"]; a["lam_guess"] = GA
a["stub_note"] = "raw l1kc63Fw1025.jsonl D 17.5 line, lam_guess replaced by the trend guess; lam is the float64 record (suspect, failed its signtest)"
leap = [json.loads(l) for l in open(RAW + "I1025-win/leap_kc63.log") if l.startswith('{"D": 17.75,')][0]
b = dict(leap); b["lam_guess"] = GB; b["lam"] = GB
b["stub_note"] = "raw leap_kc63.log D 17.75 line plus lam_guess and lam = the trend guess (placeholder: no lambda record exists at this D)"
for fn, r in (("stub_rowA_l1kc63Fw1025_D17.5_trendguess.jsonl", a), ("stub_rowB_l1kc63W1025_D17.75_leapline.jsonl", b)):
    open(OUT + fn, "w", newline="\n").write(json.dumps(r) + "\n")
    print("wrote", fn, {k: r[k] for k in ("D", "kc", "kappa", "u0", "Ks", "F", "steps", "lam_guess", "lam")})
for g, name in ((GA, "A"), (GB, "B")):
    print(f"row {name}: guess {g}; windows " + ", ".join(f"w {w}: [{g * (1 - w):.5f}, {g * (1 + w):.5f}]" for w in (0.02, 0.06, 0.15, 0.35)))
