#!/usr/bin/env python3
"""#685: per base, the singularity of the chain's 24-order series from jet_singularity.py summary's json (hp/data/jet_634.json layout).
    python3 table685.py JET.json [--out TABLE.txt]
Per base D0 (N = 24 series only): the root test of Delta's coefficients; Delta's stable Pade poles and the recurrence fit, each as |s|, arg and
D* = D0 + s; the 24 rows with the largest |z_8|: how many give a stable pole, their |s| and arg (min, median, max), the median root test of the
rows, and #685's acceptance numbers (at least 12 of 24 rows, median |s| within 20% of the root test). Then the singularity tracks: every stable
pole of Delta's Pade and every row's nearest stable pole as D* = D0 + s, grouped across the bases when within 0.4 of the track's median, and for each
track seen at 3 or more bases the least-squares drift of D* with D0 and where Im D* would reach 0."""
import cmath
import json
import math
import statistics
import sys

import numpy as np

J = json.load(open(sys.argv[1]))
out = []


def p(s=""):
    print(s)
    out.append(s)


loc = {k: v for k, v in J["locate"].items() if v["N"] == 24}
p(f"{J.get('source', '')}; bases with 24 orders: {sorted(loc, key=float)}")
p()
p("D0        root(Delta)  Delta Pade stable poles: |s| arg n -> D*                                  recurrence |s| arg -> D*")
for k in sorted(loc, key=float):
    L = loc[k]
    d = L["delta"]
    pol = "; ".join(f"{x['abs']:.3f} {x['arg_deg']:.1f} n{x['n']} -> {x['D_re']:.2f}+{x['D_im']:.2f}i" for x in d["pade"]) or "none"
    r = d["recurrence"]
    p(f"{float(k):9.4f} {d['root_radius']:8.3f}     {pol:78s} {r['abs']:.3f} {r['arg_deg']:.1f} -> {r['D_re']:.2f}+{r['D_im']:.2f}i (spread {r['spread']:.2f})")
p()
p("D0        rows found  |s| min / median / max      arg min / median / max        median root of the rows  median|s|/root-1  >=12 rows  within 20%")
for k in sorted(loc, key=float):
    L = loc[k]
    f = [x for x in L["rows"] if x.get("abs") is not None]
    ab = [x["abs"] for x in f]
    ag = [x["arg_deg"] for x in f]
    root = statistics.median(L["root_rows"])
    med = statistics.median(ab)
    rat = med / root - 1
    p(f"{float(k):9.4f} {len(f):3d} of 24   {min(ab):.3f} / {med:.3f} / {max(ab):.3f}     {min(ag):.1f} / {statistics.median(ag):.1f} / {max(ag):.1f}"
      f"      {root:.3f}                  {rat:+.1%}          {'yes' if len(f) >= 12 else 'NO'}        {'yes' if abs(rat) <= 0.2 else 'NO'}")
p()

TOL = 0.4
pts = []
for k in sorted(loc, key=float):
    L = loc[k]
    D0 = L["delta"]["D0"]
    for x in L["delta"]["pade"]:
        pts.append((D0, complex(x["D_re"], x["D_im"]), "delta"))
    for x in L["rows"]:
        if x.get("abs") is not None:
            pts.append((D0, D0 + x["abs"] * cmath.exp(1j * math.radians(x["arg_deg"])), "row"))
tracks = []
for D0, z, src in sorted(pts, key=lambda t: (t[0], t[1].imag)):
    for t in tracks:
        if abs(t["z"] - z) < TOL:
            t["pts"].append((D0, z, src))
            t["z"] = complex(statistics.median([q[1].real for q in t["pts"]]), statistics.median([q[1].imag for q in t["pts"]]))
            break
    else:
        tracks.append(dict(z=z, pts=[(D0, z, src)]))
p(f"singularity tracks (D* within {TOL} of the track's median; counts are poles: Delta's Pade poles and the rows' nearest ones)")
p("track median D*          bases that show it (poles per base)                                  D* per base: Re, Im (median)")
tracks.sort(key=lambda t: -len({q[0] for q in t["pts"]}))
for t in tracks:
    bases = sorted({q[0] for q in t["pts"]})
    if len(t["pts"]) < 3:
        continue
    cnt = " ".join(f"{b:.2f}:{sum(1 for q in t['pts'] if q[0] == b)}" for b in bases)
    per = " ".join(f"({statistics.median([q[1].real for q in t['pts'] if q[0] == b]):.2f},{statistics.median([q[1].imag for q in t['pts'] if q[0] == b]):.2f})" for b in bases)
    p(f"{t['z'].real:8.2f}{t['z'].imag:+6.2f}i    {cnt:70s} {per}")
p()
p("per track seen at 3 or more bases: D* against the base D0 by least squares (slope per unit D0), and the D0 where Im D* would reach 0")
for t in tracks:
    bases = sorted({q[0] for q in t["pts"]})
    if len(bases) < 3:
        continue
    x = np.array(bases)
    re = np.array([statistics.median([q[1].real for q in t["pts"] if q[0] == b]) for b in bases])
    im = np.array([statistics.median([q[1].imag for q in t["pts"] if q[0] == b]) for b in bases])
    sre = np.polyfit(x, re, 1)[0]
    m, c = np.polyfit(x, im, 1)
    cross = f"Im D* reaches 0 at D0 = {-c / m:.0f}" if m < 0 else "no crossing ahead"
    p(f"track {t['z'].real:.2f}{t['z'].imag:+.2f}i, {len(bases)} bases {bases[0]:.2f}..{bases[-1]:.2f}: Re D* {re.min():.2f}..{re.max():.2f} (slope {sre:+.3f}), "
      f"Im D* {im.min():.2f}..{im.max():.2f} (slope {m:+.3f}); {cross}")
p()
a = [t for t in tracks if len({q[0] for q in t["pts"]}) == len(loc) - 1]
for t in a[:1]:
    z = t["z"]
    p(f"consistency with the root test (read after the fact, not a pre-registered check): if the nearest singularity were the track {z.real:.2f}{z.imag:+.2f}i alone, "
      "the root test would be |D* - D0|")
    for k in sorted(loc, key=float):
        d = loc[k]["delta"]
        if abs(d["D0"] - 236.63) < 1:
            continue
        p(f"   D0 {d['D0']:.4f}: |D* - D0| {abs(z - d['D0']):.3f}, Delta's root test {d['root_radius']:.3f}, ratio {d['root_radius'] / abs(z - d['D0']):.3f}")
p()
ks = sorted(loc, key=float)
x = np.array([loc[k]["delta"]["D0"] for k in ks if float(k) > 251.9])
rec = [loc[k]["delta"]["recurrence"] for k in ks if float(k) > 251.9]
im = np.array([r["D_im"] for r in rec])
re = np.array([r["D_re"] for r in rec])
m, c = np.polyfit(x, im, 1)
p("Delta's two-term recurrence fit (a single conjugate pair, its windows' spread in |s|) from D 252 on:")
for D0, r in zip(x, rec):
    p(f"   D0 {D0:.4f}: D* {r['D_re']:.2f}{r['D_im']:+.2f}i, |s| {r['abs']:.3f}, spread {r['spread']:.2f}")
p(f"   Im D* slope {m:+.3f} per unit D0" + (f", reaching 0 at D0 = {-c / m:.1f}" if m < 0 else "") + f"; Re D* slope {np.polyfit(x, re, 1)[0]:+.3f}")
if len(sys.argv) > 3 and sys.argv[2] == "--out":
    open(sys.argv[3], "w").write("\n".join(out) + "\n")
