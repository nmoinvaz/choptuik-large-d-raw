#!/usr/bin/env python3
"""#1109 stage 1c2: this machine's scan of R0 at dh170's two lambdas against dh170's records (c2/dh170/), the two-point det-linear
root, and the Brent-refined roots of stage 1c and 1c2 (run from c2/)."""
import json, math
REF = 0.045967998
mine = {r["lam"]: r for r in (json.loads(l) for l in open("scan_r0_rust.jsonl") if l.strip())}
theirs = {}
for f in ("dh170/scan_ctl_scan_D23.0_p0.jsonl", "dh170/scan_ctl_scan_D23.0_p1.jsonl"):
    for l in open(f):
        r = json.loads(l); theirs[r["lam"]] = r
print("| lambda | hybrid sign (here / dh170) | ln\\|det\\| here | ln\\|det\\| dh170 | difference | dln (here / dh170) | float64 sign (here / dh170) | float64 ln\\|det\\| (here / dh170) | difference |")
print("|---|---|---|---|---|---|---|---|---|")
ok = True
for lam in sorted(mine):
    a, b = mine[lam], theirs[lam]
    d = a["ln"] - b["ln"]; df = a["f64_ln"] - b["f64_ln"]
    ok &= (a["sign"] == b["sign"]) and abs(d) <= 1e-4
    print(f"| {lam} | {int(a['sign']):+d} / {int(b['sign']):+d} | {a['ln']:.10f} | {b['ln']:.10f} | {d:+.3e} | {a['dln']:.3e} / {b['dln']:.3e} | {int(a['f64_sign']):+d} / {int(b['f64_sign']):+d} | {a['f64_ln']:.6f} / {b['f64_ln']:.6f} | {df:+.4f} |")
def two_point(r0, r1, l0, l1):
    ref = max(r0["ln"], r1["ln"])
    f0, f1 = r0["sign"] * math.exp(r0["ln"] - ref), r1["sign"] * math.exp(r1["ln"] - ref)
    return l0 + (l1 - l0) * f0 / (f0 - f1)
rm = two_point(mine[0.045], mine[0.05], 0.045, 0.05); rt = two_point(theirs[0.045], theirs[0.05], 0.045, 0.05)
print()
print(f"two-point det-linear root of (0.045, 0.05): here {rm!r}, dh170's records {rt!r}; here - {REF} = {rm - REF:+.3e} (bar 1e-5: {'PASS' if abs(rm - REF) <= 1e-5 else 'FAIL'}); here - dh170's = {rm - rt:+.3e}")
print(f"bars: signs +1, -1 equal and ln|det| within 1e-4 at both lambda: {'PASS' if ok else 'FAIL'}")
b = [json.loads(l) for l in open("root_r0_rust.jsonl") if l.strip()]
bf = [x for x in b if x.get("kind") == "root"][-1]
print(f"B (--b12=rust, Brent, tol 1e-6): status {bf['status']}, bracket [{bf['bracket'][0]!r}, {bf['bracket'][1]!r}], width {bf['width']:.3e}, det-linear {bf['lam_lin']!r}, {bf['n_eval']} evaluations, {bf['sec']} s")
c = [json.loads(l) for l in open("../c/root_r0.jsonl") if l.strip()]
cf = [x for x in c if x.get("kind") == "root"][-1]
print(f"stage 1c control (--b12=fast, Brent): status {cf['status']}, bracket [{cf['bracket'][0]!r}, {cf['bracket'][1]!r}], det-linear {cf['lam_lin']!r}")
print(f"B - dh170's two-point estimate: {bf['lam_lin'] - REF:+.4e}; B - the stage 1c control's det-linear: {bf['lam_lin'] - cf['lam_lin']:+.3e}")
