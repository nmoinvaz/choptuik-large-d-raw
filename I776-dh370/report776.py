#!/usr/bin/env python3
"""#776 (#760's report with the bars moved to the real-axis point P = 259.95): the bars at each base past D_min, from
jet_776.json (jet_singularity.py summary), and the old bases against jet_760.json's locate entries.
    python3 report776.py JET776.json JET760.json [--out TXT] [--D_min=258.9] [--mutate=shiftP]
Self-test: --D_min=255.8 on jet_760.json reads #760's bases as new (bars 2 and 3 then pass at D 258.7829 and fail at
256.5686 and 257.6853, where the nearest pole is track T), and --mutate=shiftP moves P by +1.0, which must fail bar 3 at
every base. Exit 1 when a bar fails at a new base (0 under --mutate=shiftP only when bar 3 fails at every new base).
Bars (#776, written before any series was read): (2) Delta's root test within 5% of |P - D0|; (3) Delta's nearest stable
Pade pole has |Im D*| <= 0.1 and |Re D* - 259.95| <= 0.2. The other stable poles of Delta and the rows' nearest poles
are listed, as in I685-dh370/table685.txt."""
import cmath
import json
import math
import statistics
import sys

J, J7 = (json.load(open(f)) for f in sys.argv[1:3])
P = complex(259.95, 0.0)
DMIN = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--D_min=")), 258.9))
shift = "--mutate=shiftP" in sys.argv
if shift:
    P += 1.0       # the control: bar 3 must then fail
out = []


def p(s=""):
    print(s)
    out.append(s)


def bar3(x):
    return x is not None and abs(x["D_im"] - P.imag) <= 0.1 and abs(x["D_re"] - P.real) <= 0.2


loc = {k: v for k, v in J["locate"].items() if v["N"] == 24}
old = [k for k in loc if float(k) < DMIN]
new = sorted((k for k in loc if float(k) > DMIN), key=float)
p("Check of the tool: the old bases' locate entries against the earlier summary's")
for k in sorted(old, key=float):
    if k in J7["locate"]:
        a, b = loc[k], J7["locate"][k]
        same = (json.dumps(a["delta"]["pade"], sort_keys=True) == json.dumps(b["delta"]["pade"], sort_keys=True)
                and a["delta"]["root_radius"] == b["delta"]["root_radius"] and a["rows"] == b["rows"])
        p(f"   D0 {float(k):9.4f}: Delta's Pade poles, root test and rows {'equal' if same else 'DIFFER'} to the earlier summary's")
p()
p(f"P = {P.real:.2f}{P.imag:+.2f}i" + ("  (--mutate=shiftP)" if shift else ""))
p("D0         root test of Delta   |P - D0|   ratio    bar 2   nearest stable Pade pole of Delta: |s| arg n -> D*   bar 3   other stable poles of Delta (D*)")
fails2 = fails3 = 0
for k in new:
    d = loc[k]["delta"]
    D0 = d["D0"]
    dist = abs(P - D0)
    r = d["root_radius"] / dist - 1
    ok2 = abs(r) <= 0.05
    pade = sorted(d["pade"], key=lambda x: x["abs"])
    nst = pade[0] if pade else None
    ok3 = bar3(nst)
    fails2 += not ok2
    fails3 += not ok3
    pa = f"{nst['abs']:.3f} {nst['arg_deg']:.1f} n{nst['n']} -> {nst['D_re']:.2f}{nst['D_im']:+.2f}i" if nst else "no stable pole"
    po = "; ".join(f"{x['D_re']:.2f}{x['D_im']:+.2f}i (n{x['n']})" for x in pade[1:]) or "none"
    p(f"{D0:9.4f}   {d['root_radius']:8.3f}            {dist:7.3f}   {r:+.1%}    {'met' if ok2 else 'FAILED':>6}   {pa}    "
      f"{'met' if ok3 else 'FAILED':>6}   {po}")
p()
p("the rows' nearest stable poles per new base (the 24 rows with the largest |z_8|): D* = D0 + s, median and range")
for k in new:
    L = loc[k]
    D0 = L["delta"]["D0"]
    f = [x for x in L["rows"] if x.get("abs") is not None]
    z = [D0 + x["abs"] * cmath.exp(1j * math.radians(x["arg_deg"])) for x in f]
    if not z:
        p(f"   D0 {D0:9.4f}: no row with a stable pole")
        continue
    nearP = [q for q in z if abs(q - P) < 0.2]
    p(f"   D0 {D0:9.4f}: {len(f)} of 24 rows with a pole; median D* {statistics.median([q.real for q in z]):.2f}"
      f"{statistics.median([q.imag for q in z]):+.2f}i, Im D* {min(q.imag for q in z):.2f} to {max(q.imag for q in z):.2f}; "
      f"{len(nearP)} rows within 0.2 of P")
p()
p(f"bar 2 failed at {fails2} of {len(new)} new bases, bar 3 at {fails3} of {len(new)}")
if "--out" in sys.argv:
    open(sys.argv[sys.argv.index("--out") + 1], "w").write("\n".join(out) + "\n")
if shift:
    sys.exit(0 if new and fails3 == len(new) else 1)
sys.exit(0 if new and not fails2 and not fails3 else 1)
