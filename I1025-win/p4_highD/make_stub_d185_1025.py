#!/usr/bin/env python3
"""#1025 winb, D 18.5: the stub record p4_hybrid.py reads. The leap's D 18.5 line of raw I1025-mac/d18/l1kc63Wm1025.jsonl (blob 08f4dbf3) unchanged (it has
no lambda: a leap state), plus lam_guess = 1.6771 (the coordinator's) and lam = the guess (placeholder, as for row B: minus_record is root minus guess)."""
import json
RAW = "C:/Users/nathan/Source/p4hi_1025/raw/I1025-mac/d18/l1kc63Wm1025.jsonl"
OUT = "C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/stub_d185_l1kc63Wm1025_D18.5_leapline.jsonl"
G = 1.6771
leap = [json.loads(l) for l in open(RAW) if l.strip() and abs(json.loads(l)["D"] - 18.5) < 1e-9][-1]
r = dict(leap); r["lam_guess"] = G; r["lam"] = G
r["stub_note"] = "raw I1025-mac/d18/l1kc63Wm1025.jsonl D 18.5 line (blob 08f4dbf3) plus lam_guess and lam = the coordinator's guess 1.6771 (placeholder: no lambda record at this D)"
open(OUT, "w", newline="\n").write(json.dumps(r) + "\n")
print({k: r[k] for k in ("D", "kc", "kappa", "u0", "Ks", "F", "steps", "lam_guess", "lam")})
print("windows:", ", ".join(f"w {w}: [{G * (1 - w):.6f}, {G * (1 + w):.6f}]" for w in (0.02, 0.06, 0.15, 0.35)))
