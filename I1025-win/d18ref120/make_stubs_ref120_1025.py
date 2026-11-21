#!/usr/bin/env python3
"""#1025 winb, the lambda 1.20 dd check: stub records for signtest.py's system check (syscheck): the leap line of each state (F, steps, kappa, u0, Ks) plus lam = 1.20
(signtest.py's around= needs a lam; with dl 0 it only reads it). D 18: the D 18.0 line of raw I1025-win/out/l1kc63W1025.jsonl (blob c33039df); D 18.0625: the D 18.0625
line of raw I1025-mac/d18/l1kc63Wm1025.jsonl (blob 08f4dbf3). ell_ddm.py det itself checks nothing against a record; its _setup uses Ks 30, u0 0.04, kappa 0.7, the records'."""
import json
R = "C:/Users/nathan/Source/ref120_1025/"
O = R + "I1025-win/d18ref120/"
for tag, fn, D in (("D18", "raw/I1025-win/out/l1kc63W1025.jsonl", 18.0), ("D18.0625", "raw/I1025-mac/d18/l1kc63Wm1025.jsonl", 18.0625)):
    r = [json.loads(l) for l in open(R + fn) if l.strip() and abs(json.loads(l)["D"] - D) < 1e-9][-1]
    r["lam"] = 1.2
    r["stub_note"] = f"{fn} D {D} line plus lam = 1.2 (placeholder for signtest.py syscheck)"
    open(O + f"stub_ref120_{tag}.jsonl", "w", newline="\n").write(json.dumps(r) + "\n")
    print(tag, {k: r[k] for k in ("D", "kc", "kappa", "u0", "Ks", "F", "steps", "lam")})
