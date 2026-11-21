#!/usr/bin/env python3
"""#1025 win2b, the D 18.0625 scan above the first window: where a plus-to-minus change of the hybrid sign puts D 18's upper root, and how fast it then rose (the coordinator's reading).
usage: rate_up.py MERGED.jsonl
D 18's upper root is my hybrid root 1.8074339746330934 (comment 7062464335); D 18.0625 is 0.0625 above D 18. A change is two consecutive points with signs plus then minus, ROBUST if both points
pass their 1e-15 noise test. Prints each such change with the rise per unit D at the bracket's two ends. No robust plus-to-minus change over the window: the root is not there (the reading)."""
import json, sys
ROOT18, DD = 1.8074339746330934, 0.0625
P = sorted((json.loads(l) for l in open(sys.argv[1]) if l.strip()), key=lambda r: r["lam"])
print(f"D {P[0]['D']}: {len(P)} points, lambda {P[0]['lam']:.2f} to {P[-1]['lam']:.2f}")
n = 0
for a, b in zip(P, P[1:]):
    if a["sign"] > 0 and b["sign"] < 0:
        rob = a["noise_robust"] and b["noise_robust"]
        n += rob
        print(f"plus-to-minus change in ({a['lam']:.2f}, {b['lam']:.2f}), {'ROBUST' if rob else 'NOT ROBUST (a point fails its noise test)'}: from D 18's root {ROOT18!r} the rise is "
              f"{a['lam'] - ROOT18:.4f} to {b['lam'] - ROOT18:.4f} in {DD} D, i.e. {(a['lam'] - ROOT18) / DD:.3f} to {(b['lam'] - ROOT18) / DD:.3f} per unit D")
if n == 0:
    print(f"RATE: no robust plus-to-minus change from {P[0]['lam']:.2f} to {P[-1]['lam']:.2f}: the root is not there (the coordinator's reading)")
else:
    print(f"RATE: {n} robust plus-to-minus change(s) place the root")
