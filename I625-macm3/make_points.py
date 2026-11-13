#!/usr/bin/env python3
"""Grid points of #625: lambda = centre + k * 1e-14 for k = -32..32 (exact in rational arithmetic, rounded once to the nearest double).
centre(M 48) = the mean of the five ball lambda(48) of I615-macm3 (b1 to b5), centre(M 32) = the mean of the five ball lambda(32).
Prints the centres and writes points_M32.txt and points_M48.txt (one 'k RE' line per point; k = 0 appears twice, the repeat)."""
import json, os
from fractions import Fraction
here = os.path.dirname(os.path.abspath(__file__))
i615 = os.path.join(here, "..", "I615-macm3")
recs = [json.loads(open(os.path.join(i615, f"gamma_up12_D58.0060_{b}.jsonl")).readline()) for b in ("b1", "b2", "b3", "b4", "b5")]
cent = {32: sum(Fraction(r["lam"]) for r in recs) / 5, 48: sum(Fraction(r["M48"]["lam"]) for r in recs) / 5}
for M, c in cent.items():
    pts = [(k, float(c + k * Fraction(1, 10 ** 14))) for k in range(-32, 33)]
    pts.append((0, pts[32][1]))
    assert pts[32][0] == 0 and len(pts) == 66
    with open(os.path.join(here, f"points_M{M}.txt"), "w") as f:
        for k, x in pts:
            f.write(f"{k} {x!r}\n")
    print(f"M {M}: centre {float(c)!r} (mean of five), k=-32 {pts[0][1]!r}, k=+32 {pts[64][1]!r}")
