#!/usr/bin/env python3
"""control_compare_kmm.py [--mutate=ln|field] : the control of t5's order (#1101 comment 7223316450): one point scanned with --kappa_mm=0.5 (R1's own kappa) must give the same ln|det M| as the R1 scan at the same lambda, bit for bit.
Reads kc87_leg_lambda/23.0_r1k050/scan/scan_D23.0_1025.jsonl (the R1 scan, lambda 0.100) and kc87_leg_lambda/23.0_r1k050_kmm050ctl/scan/scan_D23.0_1025.jsonl (the control). Every field of the R1 record except sec and sec_parts must be equal (ln, f64_ln, sign, f64_sign, dln,
noise fields, robust flags); fields only the control has (kappa_mm) are listed. Exit 0 when all equal, 1 otherwise. --mutate=ln moves the control's ln by one unit in the last place, --mutate=field changes its sign: both must exit 1."""
import json, math, sys
L = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/"
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()]
a = [r for r in rd(L + "23.0_r1k050/scan/scan_D23.0_1025.jsonl") if abs(r["lam"] - 0.100) < 1e-12]
c = [r for r in rd(L + "23.0_r1k050_kmm050ctl/scan/scan_D23.0_1025.jsonl") if abs(r["lam"] - 0.100) < 1e-12]
assert len(a) == 1 and len(c) == 1, (len(a), len(c))
a, c = a[0], c[0]
if "--mutate=ln" in sys.argv: c = dict(c, ln=math.nextafter(c["ln"], 0.0))
if "--mutate=field" in sys.argv: c = dict(c, sign=-c["sign"])
skip = {"sec", "sec_parts"}
diff = [k for k in a if k not in skip and a[k] != c.get(k, object())]
extra = [k for k in c if k not in a]
print("R1 scan at lambda 0.100: ln %r, f64_ln %r, sign %+d; control (kappa_mm 0.5): ln %r, f64_ln %r, sign %+d" % (a["ln"], a["f64_ln"], a["sign"], c["ln"], c["f64_ln"], c["sign"]))
print("ln difference %r; fields compared: %d (all but sec and sec_parts); fields that differ: %s; fields only the control has: %s; seconds %s (R1 scan) against %s (control)" % (c["ln"] - a["ln"], len([k for k in a if k not in skip]), diff or "none", extra or "none", a["sec"], c["sec"]))
sys.exit(0 if not diff else 1)
