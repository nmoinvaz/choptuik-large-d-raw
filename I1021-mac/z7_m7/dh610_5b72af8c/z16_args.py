#!/usr/bin/env python3
"""z16_args.py WALK.json | input INPUTS.json: prints "A w B3 C3 B5 C5" for walk1027.py: of the converged M = 5 walk's zero (A, w of its verdict,
the harmonics of its best point) or of the input file's own point; exit 1 when the walk did not converge."""
import json
import sys

if sys.argv[1] == "input":
    d = json.load(open(sys.argv[2]))
    print(d["A"], d["wf"], *d["x_B3_C3_B5_C5"])
    sys.exit(0)
d = json.load(open(sys.argv[1]))
v = d["verdict"]
if not v.get("converged"):
    print("not converged: " + str(v.get("why")), file=sys.stderr)
    sys.exit(1)
b = next(p for p in d["points"] if p["A"] == v["solved_A"] and p["w"] == v["solved_w"])
print(repr(v["A"]), repr(v["w"]), *b["x"][:4])
