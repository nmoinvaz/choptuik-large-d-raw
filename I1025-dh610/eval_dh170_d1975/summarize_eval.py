#!/usr/bin/env python3
"""#1025 eval_dh170_d1975 (dh610) summarize_eval.py: the exact differences between this build's evaluation of dh170's state and his rows, and ln|det| per unit of |dz| for the pairs of states. No number is typed by hand.
usage (from this folder): ~/Source/venv-i1058/bin/python -I summarize_eval.py > summary_eval.txt"""
import json, numpy as np
rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
mine = {round(r["lam"], 2): r for f in ("run/eval_D19.75_p0.jsonl", "run/eval_D19.75_p1.jsonl") for r in rd(f)}
his = {round(r["lam"], 2): r for r in rd("in/ref_dh170_scan_D19.75_1025.jsonl")}
lin = {1.32: rd("in/ref_linRe_D19.75_1.32.jsonl")[-1], 1.33: rd("in/ref_linRe_D19.75_1.33.jsonl")[-1]}
print("| lambda | ln|det| this build on dh170's state | ln|det| dh170's row | difference | same float | hybrid sign (mine, his) | f64 sign (mine, his) | f64 ln (mine, his) | seconds (mine, his) |".replace("|det|", " of abs det"))
print("|---|---|---|---|---|---|---|---|---|")
for lam in (1.32, 1.33):
    m, h = mine[lam], his[lam]
    print(f"| {lam:.2f} | {m['ln']!r} | {h['ln']!r} | {m['ln'] - h['ln']:+.3e} | {m['ln'] == h['ln']} | {m['sign']:+.0f}, {h['sign']:+.0f} | {m['f64_sign']:+.0f}, {h['f64_sign']:+.0f} | {m['f64_ln']!r}, {h['f64_ln']!r} | {m['sec']}, {h['sec']} |")
print()
st = {k: np.load(f"in/sol_{k}_D19.7500.npy") for k in ("l1kc87dh170d1975", "l1kc87linRe", "l1kc87macRe", "l1kc87macm3d1975")}
dz = float(np.linalg.norm(st["l1kc87linRe"] - st["l1kc87dh170d1975"]))
print(f"norm dz (dh170's state, linRe) {dz:.4e}")
print("ln of abs det, linRe minus dh170's state (both on this build or his, which agree), per unit of norm dz:")
for lam in (1.32, 1.33):
    d = lin[lam]["ln"] - mine[lam]["ln"]
    print(f"  {lam:.2f}: {d:+.6f}, {d / dz:+.3e} per unit")
print(f"the same-build pairs of the step 4 result were about 2.5e+05 per unit (linRe, macRe: 2.474e+05, -2.485e+05); ratio at 1.32: {(lin[1.32]['ln'] - mine[1.32]['ln']) / dz / 2.474e+05:.0f}")
