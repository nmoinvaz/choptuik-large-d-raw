#!/usr/bin/env python3
"""#1025 D 17 k_c 71: the stub record p4_hybrid.py reads. The Mac's D 17 line of I1025-mac/out/l1kc71Fm1025.jsonl unchanged, except lam_guess (set to the
k_c 63 hybrid root at D 17 plus D 16.5's offset: 2.0399399392 - 6.6e-4 = 2.0392799, written in README.md before the run; the record's own guess is kept
as lam_guess_record). Its lam stays the Mac's float64 record. usage: make_stub_d17.py RECORD.jsonl OUT.jsonl"""
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
assert len(rec) == 1 and rec[0]["D"] == 17.0 and rec[0]["kc"] == 71, "expected the single D 17 k_c 71 line"
r = dict(rec[0]); r["lam_guess_record"] = r["lam_guess"]; r["lam_guess"] = 2.0392799
r["stub_note"] = "raw I1025-mac/out/l1kc71Fm1025.jsonl D 17 line; lam_guess = 2.0399399392 - 6.6e-4 (coordinator, 2026-11-21); lam is the Mac's float64 record"
open(sys.argv[2], "w", newline="\n").write(json.dumps(r) + "\n")
print("stub", {k: r[k] for k in ("D", "kc", "kappa", "u0", "Ks", "F", "steps", "lam_guess", "lam", "lam_guess_record")})
