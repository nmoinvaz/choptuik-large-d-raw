#!/usr/bin/env python3
"""#1025 D 18 upper root, k_c 63: the stub record p4_hybrid.py reads. The D 18 line of winb's raw I1025-win/out/l1kc63W1025.jsonl unchanged (F 2.630345255831752e-10, 2552 steps,
kappa 0.7, u0 0.04, Ks 30, no lambda), plus lam_guess = 1.825 and lam = the guess (p4_hybrid's filter needs a lam; its minus_record reads root minus guess), as xfkappa's D 18 stub
(raw I1025-mac/d18/d18_stub_l1kc63W1025.jsonl) did with another guess. usage: make_stub_d18.py RECORDS.jsonl OUT.jsonl"""
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip() and json.loads(l)["D"] == 18.0]
assert len(rec) == 1 and rec[0]["kc"] == 63 and rec[0]["steps"] == 2552, "expected the single D 18 k_c 63 line"
r = dict(rec[0]); r["lam_guess"] = 1.825; r["lam"] = 1.825
r["stub_note"] = "winb's leap record at D 18 (l1kc63W1025.jsonl); lam_guess 1.825 puts the w 0.02 grid at 1.7885, 1.825, 1.8615 (the upper root only); lam is the guess (no float64 root), so minus_record is root minus guess"
open(sys.argv[2], "w", newline="\n").write(json.dumps(r) + "\n")
print("stub", {k: r[k] for k in ("D", "kc", "kappa", "u0", "Ks", "F", "steps", "lam_guess", "lam")})
