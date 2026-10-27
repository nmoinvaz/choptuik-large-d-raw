"""T84: the exact check of the quad-double LU's solves (qd_ludump.py's dump) with python-flint at 320 bits: |J x - b| /
|b| for the plain solve, |J^T y - b| / |b| for the transposed one, and |J dz + F| / |F| for the Newton step; the parts
of J and of the vectors summed exactly. A correct quad-double solve gives about 1e-60 relative; f64 products cannot
see that (entries 1e7, cancellation).

    python3 qd_luexact.py DUMP.npz
"""
import sys

import numpy as np
from flint import arb, arb_mat, ctx

ctx.prec = 320
d = np.load(sys.argv[1])
L = len(d["b"])
Jp = [d[f"J{q}"] for q in range(4)]


def vec(parts):
    return [sum(arb(float(p[i])) for p in parts) for i in range(L)]


print(f"L {L}, pivots {d['piv'][0]:.1e}..{d['piv'][1]:.1e}", flush=True)
Jsum = Jp[0] + Jp[1] + Jp[2] + Jp[3]      # the parts are non-overlapping f64, their f64 sum has ~1e-16 relative error
Jx = arb_mat([[arb(float(Jp[0][i, j])) + arb(float(Jp[1][i, j])) + arb(float(Jp[2][i, j])) + arb(float(Jp[3][i, j]))
               for j in range(L)] for i in range(L)])
print("J built", flush=True)


def check(M, v, rhs, name):
    r = M * arb_mat([[c] for c in v])
    num = max(abs((r[i, 0] - rhs[i])) for i in range(L))
    den = max(abs(c) for c in rhs)
    print(f"{name}: max |M v - rhs| / max |rhs| = {float(num / den):.2e}   (max |v| {float(max(abs(c) for c in v)):.1e})", flush=True)


b = [arb(float(v)) for v in d["b"]]
check(Jx, vec([d[f"x{q}"] for q in range(4)]), b, "plain solve  J x = b ")
check(Jx.transpose(), vec([d[f"y{q}"] for q in range(4)]), b, "transposed   J^T y = b")
F = vec([d["F0"], d["F1"]])
check(Jx, vec([d[f"dz{q}"] for q in range(4)]), [-c for c in F], "Newton step  J dz = -F")
