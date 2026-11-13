#!/usr/bin/env python3
"""#712: the bars of the issue at each base past D 255, from jet_712.json (jet_singularity.py summary), and the old bases of #685 against their stored locate entries.
    python3 report712.py JET712.json JET685.json [--out TXT] [--D_min=255] [--mutate=shiftA]
Self-test: --D_min=252 on I685's json reads its bases as new (the 5% bar fails at D 252.25, as the table of #685 has it), and --mutate=shiftA moves A by +0.5, which must fail the bars.
Bars (README.md, written before any series was read): (2) Delta's root test within 5% of |A - D0|, A = 255.71 + 4.99i; (3) the Pade pole of Delta within 0.4 of A has Im D*
within 0.1 of 4.99. The other stable poles of Delta's Pade and the rows' nearest poles are listed, as in I685-dh370/table685.txt."""
import cmath
import json
import math
import statistics
import sys

import numpy as np

J, J5 = (json.load(open(f)) for f in sys.argv[1:3])
A = complex(255.71, 4.99)
DMIN = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--D_min=")), 255.0))
if "--mutate=shiftA" in sys.argv:
    A += 0.5       # the control: the bars must then fail
out = []


def p(s=""):
    print(s)
    out.append(s)


loc = {k: v for k, v in J["locate"].items() if v["N"] == 24}
old = [k for k in loc if float(k) < DMIN]
new = sorted((k for k in loc if float(k) > DMIN), key=float)
p("Check of the tool: the old bases' locate entries against I685-dh370/jet_685.json (the code changed since aedb403b)")
for k in sorted(old, key=float):
    if k in J5["locate"]:
        a, b = loc[k], J5["locate"][k]
        same = json.dumps(a["delta"]["pade"], sort_keys=True) == json.dumps(b["delta"]["pade"], sort_keys=True) and a["delta"]["root_radius"] == b["delta"]["root_radius"] and a["rows"] == b["rows"]
        p(f"   D0 {float(k):9.4f}: Delta's Pade poles, root test and rows {'equal' if same else 'DIFFER'} to I685's")
p()
p("D0         root test of Delta   |A - D0|   ratio    within 5%   A pole of Delta's Pade: |s| arg n -> D*, Im D* - 4.99   within 0.1   other stable poles of Delta (D*)")
for k in new:
    d = loc[k]["delta"]
    D0 = d["D0"]
    dist = abs(A - D0)
    r = d["root_radius"] / dist - 1
    near = [x for x in d["pade"] if abs(complex(x["D_re"], x["D_im"]) - A) < 0.4]
    others = [x for x in d["pade"] if x not in near]
    pa = "; ".join(f"{x['abs']:.3f} {x['arg_deg']:.1f} n{x['n']} -> {x['D_re']:.2f}+{x['D_im']:.2f}i, {x['D_im'] - 4.99:+.3f}" for x in near) or "none within 0.4 of A"
    ok3 = bool(near) and all(abs(x["D_im"] - 4.99) <= 0.1 for x in near)
    po = "; ".join(f"{x['D_re']:.2f}+{x['D_im']:.2f}i (n{x['n']})" for x in others) or "none"
    p(f"{D0:9.4f}   {d['root_radius']:8.3f}            {dist:7.3f}   {r:+.1%}    {'yes' if abs(r) <= 0.05 else 'NO':>3}         {pa}    {'yes' if ok3 else 'NO'}    {po}")
p()
p("the rows' nearest stable poles per new base (the 24 rows with the largest |z_8|): D* = D0 + s, median and range")
for k in new:
    L = loc[k]
    D0 = L["delta"]["D0"]
    f = [x for x in L["rows"] if x.get("abs") is not None]
    z = [D0 + x["abs"] * cmath.exp(1j * math.radians(x["arg_deg"])) for x in f]
    nearA = [q for q in z if abs(q - A) < 0.4]
    p(f"   D0 {D0:9.4f}: {len(f)} of 24 rows with a pole; median D* {statistics.median([q.real for q in z]):.2f}{statistics.median([q.imag for q in z]):+.2f}i, Im D* {min(q.imag for q in z):.2f} to {max(q.imag for q in z):.2f}; "
      f"{len(nearA)} rows within 0.4 of A" + (f", their Im D* {statistics.median([q.imag for q in nearA]):.3f}" if nearA else ""))
if "--out" in sys.argv:
    open(sys.argv[sys.argv.index("--out") + 1], "w").write("\n".join(out) + "\n")
