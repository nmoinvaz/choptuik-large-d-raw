#!/usr/bin/env python3
"""#673: sigma_1..4 of near_null's json for the two layouts at the same D, each weak vector's share of the norm in the last node's block
(node4: p, m, a, c), the horizon block (m_h, a_h), Delta, p1 and the rest (c0 and nodes 0 to 3), and the pinned step's size and Delta part.
    python3 nn_table.py nn_0975.json nn_070.json"""
import json
import sys

for f in sys.argv[1:]:
    d = json.load(open(f))
    print(f"{f}: {d['state']}, D {d['D']:.4f}, pivots {d['pivots'][0]:.2e}..{d['pivots'][1]:.2e}")
    print("   i  sigma_i     conv     last node  horizon   Delta     p1        rest      sum")
    for i, v in enumerate(d["vectors"], 1):
        b = v["blocks"]
        last = sum(x for k, x in b.items() if k.startswith("node4."))
        hor = b["m_h"] + b["a_h"]
        p1 = b["p1"]
        rest = sum(x for k, x in b.items() if k not in ("p1", "m_h", "a_h") and not k.startswith("node4."))
        s = last + hor + v["delta"] + p1 + rest
        print(f"   {i}  {v['sigma']:.3e}  {v['conv']:.0e}  {last:.3e}  {hor:.3e}  {v['delta']:.3e}  {p1:.3e}  {rest:.3e}  {s:.4f}")
    for key, name in (("step", "step dz = -J^-1 F"), ("step_pinned", "pinned step")):
        st = d[key]
        print(f"   {name}: max {st['max']:.3e}, norm {st['norm']:.3e}, Delta {st['delta']:+.3e}, share on V {st['share']:.4f}, V^T dz " + " ".join(f"{x:+.2e}" for x in st["vt"]))
