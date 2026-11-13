#!/usr/bin/env python3
"""#686: the singularity tracks of the kept-plan series (I685-dh370/jet_685.json) against those of the series with the plan made again at the state
(I686-dh370/jet_686.json), per base, by the rule of README.md: spread = the largest |D* - median| over a track's poles in either series, d = the distance
between the two medians; d <= spread: the solution's, d > 3 spread: the discretization's, otherwise undecided; a track with fewer than 3 poles in the kept series is undecided.
    python3 compare686.py KEPT.json NEW.json [--out TABLE.txt] [--mutate=shift]
Control --mutate=shift moves every pole of the new-plan series by +0.5 in Re D*, which must turn the agreeing tracks into the discretization's."""
import cmath
import json
import math
import statistics
import sys

kept, new = (json.load(open(f)) for f in sys.argv[1:3])
out = []


def p(s=""):
    print(s)
    out.append(s)


def clusters(L, tol=0.4):
    D0 = L["delta"]["D0"]
    pts = [complex(x["D_re"], x["D_im"]) for x in L["delta"]["pade"]]
    pts += [D0 + x["abs"] * cmath.exp(1j * math.radians(x["arg_deg"])) for x in L["rows"] if x.get("abs") is not None]
    cl = []
    for z in sorted(pts, key=lambda z: z.imag):
        for c in cl:
            if abs(c["z"] - z) < tol:
                c["pts"].append(z)
                c["z"] = complex(statistics.median([q.real for q in c["pts"]]), statistics.median([q.imag for q in c["pts"]]))
                break
        else:
            cl.append(dict(z=z, pts=[z]))
    return sorted(cl, key=lambda c: abs(c["z"] - D0))


def spread(c):
    return max(abs(q - c["z"]) for q in c["pts"])


p("base D0   track D* (kept plan)   poles  spread   D* (new plan)      poles  spread   d        verdict")
for k in sorted(kept["locate"], key=float):
    if k not in new["locate"] or kept["locate"][k]["N"] != 24:
        continue
    Lk, Ln = kept["locate"][k], new["locate"][k]
    ck, cn = clusters(Lk), clusters(Ln)
    if "--mutate=shift" in sys.argv:
        for c in cn:
            c["z"] += 0.5
            c["pts"] = [q + 0.5 for q in c["pts"]]
    for c in ck:
        if len(c["pts"]) < 1:
            continue
        m = min(cn, key=lambda x: abs(x["z"] - c["z"])) if cn else None
        if m is None or abs(m["z"] - c["z"]) > 2.0:
            p(f"{float(k):9.4f}  {c['z'].real:8.2f}{c['z'].imag:+6.2f}i   {len(c['pts']):4d}  {spread(c):6.3f}   absent in the new-plan series")
            continue
        d = abs(m["z"] - c["z"])
        sp = max(spread(c), spread(m))
        if len(c["pts"]) < 3:
            v = "undecided (fewer than 3 poles in the kept series)"
        elif d <= sp:
            v = "the solution's"
        elif d > 3 * sp:
            v = "the discretization's"
        else:
            v = "undecided (between 1 and 3 spreads)"
        p(f"{float(k):9.4f}  {c['z'].real:8.2f}{c['z'].imag:+6.2f}i   {len(c['pts']):4d}  {spread(c):6.3f}   {m['z'].real:8.2f}{m['z'].imag:+6.2f}i   {len(m['pts']):4d}  {spread(m):6.3f}   {d:7.4f}  {v}")
    extra = [c for c in cn if all(abs(c["z"] - q["z"]) > 2.0 for q in ck)]
    for c in extra:
        p(f"{float(k):9.4f}  (not in the kept series)    {c['z'].real:8.2f}{c['z'].imag:+6.2f}i   {len(c['pts']):4d}  {spread(c):6.3f}")
    p(f"{float(k):9.4f}  root test of Delta: kept {Lk['delta']['root_radius']:.4f}, new plan {Ln['delta']['root_radius']:.4f}; rows found {len([x for x in Lk['rows'] if x.get('abs') is not None])} and "
      f"{len([x for x in Ln['rows'] if x.get('abs') is not None])} of 24")
if "--out" in sys.argv:
    open(sys.argv[sys.argv.index("--out") + 1], "w").write("\n".join(out) + "\n")
