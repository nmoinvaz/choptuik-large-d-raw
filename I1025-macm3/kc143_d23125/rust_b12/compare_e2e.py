#!/usr/bin/env python3
"""compare_e2e.py [--mutate=ln|sign] : gate 3 of t5's order (hc 04:23 UTC 27 Nov, #1102): the record of the one re-evaluated point (lambda 0.015, k_c 143, D 23.0625) with
--b12=rust --b12_threads=4 (e2e/scan_D23.0625_rust.jsonl) against the stored Python records of that point (two, the scan and its repeat:
../../kc87_leg_lambda/23.0625_kc143/scan/scan_D23.0625_1025.jsonl). Every field must be equal (floats compared exactly as written in the files, as parsed by json) except the timing fields
sec and sec_parts and the label b12, which are listed. Exit 0 when only those differ, else 1. --mutate=ln adds one ulp to the Rust record's ln|det| (must exit 1), --mutate=sign flips its sign (must exit 1)."""
import json, math, os, sys
H = os.path.dirname(os.path.abspath(__file__))
STORED = os.path.join(H, "../../kc87_leg_lambda/23.0625_kc143/scan/scan_D23.0625_1025.jsonl")
RUST = os.path.join(H, "e2e/scan_D23.0625_rust.jsonl")
ALLOWED = {"sec", "sec_parts", "b12"}
mut = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), "")
st = [r for r in map(json.loads, open(STORED)) if r["lam"] == 0.015]
rs = [json.loads(l) for l in open(RUST) if l.strip()]
assert len(st) == 2 and len(rs) == 1, (len(st), len(rs))
r = dict(rs[0])
if mut == "ln":
    r["ln"] = math.nextafter(r["ln"], math.inf)
if mut == "sign":
    r["sign"] = -r["sign"]
bad = 0
for i, s in enumerate(st):
    keys = sorted(set(s) | set(r))
    diff = [k for k in keys if s.get(k) != r.get(k)]
    print("stored record %d (%s) vs Rust: %d of %d fields equal; differing: %s" % (i, "scan" if i == 0 else "repeat", len(keys) - len(diff), len(keys), diff))
    for k in diff:
        print("    %s: stored %r, rust %r" % (k, s.get(k), r.get(k)))
    if set(diff) - ALLOWED:
        bad += 1
print("equal fields include: ln %r, f64_ln %r, noise_ln %r, dln %r, signs %r/%r (mutate %s)" % (r["ln"], r["f64_ln"], r["noise_ln"], r["dln"], r["sign"], r["f64_sign"], mut or "none"))
print("compare: %s" % ("FAIL" if bad else "PASS (only timing fields and the b12 label differ)"))
sys.exit(1 if bad else 0)
