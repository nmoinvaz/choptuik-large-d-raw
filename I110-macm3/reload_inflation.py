"""How much does lemma6_jump_M.py's --load-B inflate each stored radius? (I110-macm3, an addition to the issue's commands.)

For every [midpoint, radius] pair in a B file's X and B fields, build the ball the way lemma6_jump_M.parse does,
arb(mid, rad), and compare its radius with the stored radius string. Run with venv-macm3's python from anywhere:
    python reload_inflation.py <raw>/I103-macm3/B_M5_sub1e-18.json [more files]
"""
import json
import statistics
import sys

from flint import arb, ctx

ctx.prec = 320


def ratios(path):
    d = json.load(open(path))
    out = []

    def visit(p):
        if isinstance(p, list) and len(p) == 2 and isinstance(p[0], str):
            r_loaded = arb(p[0], p[1]).rad()
            r_stored = arb(p[1])
            if r_stored > 0:
                out.append(float(((r_loaded - r_stored) / r_stored).mid()))
        elif isinstance(p, list):
            for q in p:
                visit(q)

    visit(d["X"])
    visit(d["B"])
    return out


for path in sys.argv[1:]:
    r = ratios(path)
    print(f"{path}: {len(r)} balls, radius after reload over stored minus 1: min {min(r):.2e}, "
          f"median {statistics.median(r):.2e}, mean {statistics.mean(r):.2e}, max {max(r):.2e}, all >= 0: {min(r) >= 0}")
print("2^-29 =", 2.0 ** -29, "(the 30-bit mantissa of an arb radius)")
