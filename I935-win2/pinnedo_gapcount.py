"""#935 follow-up (b): how many elements of the helpers' operands and results, in the calls of pinnedo_dump.py's held8
and heldfloat variants, are in the gap class (a zero part before a nonzero one, or a part more than 60 bits below the
previous). od_axpy and od_add_dd of the running multidouble are wrapped before the same calls are made; the results are
not changed. A call with every element outside the class would make equal bits uninformative about the class.

    python pinnedo_gapcount.py HP_DIR STATES_ROOT"""
import sys

import numpy as np

hp, root = sys.argv[1:3]
sys.path.insert(0, hp)
import multidouble as md
from pinnedo_dump import STATE, VARIANTS

tally = {}


def classify(parts):
    P = np.array([np.asarray(p, dtype=np.float64).ravel() for p in parts])        # (8, n)
    nz = P != 0
    any_later = np.flip(np.logical_or.accumulate(np.flip(nz, 0), 0), 0)         # a nonzero at this index or later
    interior = np.any((~nz) & any_later, axis=0)                                  # zero part before a nonzero one
    a, b = np.abs(P[:-1]), np.abs(P[1:])
    big = np.any(nz[:-1] & nz[1:] & (b < a * 2.0 ** -(53 + 60)), axis=0)         # a part >60 bits below the previous
    return int(P.shape[1]), int(np.count_nonzero(~nz.any(axis=0))), int(np.count_nonzero(interior | big))


def wrap(name, f, spans):
    def g(*args):
        out = f(*args)
        t = tally.setdefault(name, {"calls": 0})
        t["calls"] += 1
        for label, parts in [(lab, [args[i] for i in rng]) for lab, rng in spans] + [("out", list(out))]:
            n, zero, gap = classify(parts)
            e = t.setdefault(label, [0, 0, 0])
            e[0] += n
            e[1] += zero
            e[2] += gap
        return out
    return g


md.od_axpy = wrap("od_axpy", md.od_axpy, [("x", range(1, 9)), ("y", range(9, 17))])
md.od_add_dd = wrap("od_add_dd", md.od_add_dd, [("z", range(0, 8))])
from octo_corrector import truth_system

print(f"multidouble {md.__file__}", flush=True)
for name, kw in VARIANTS.items():
    if name.startswith("ctl"):
        continue
    tally.clear()
    z, meta, (s, sp, sq, so), info = truth_system(root, STATE, threads=5, **kw)
    zo = [np.ascontiguousarray(np.asarray(x)) for x in z]
    print(f"{name}: setup helper calls {dict((k, v['calls']) for k, v in tally.items())}", flush=True)
    tally.clear()
    so.residual_o(list(zo))
    so.newton_o(list(zo))
    for fn, t in sorted(tally.items()):
        parts = ", ".join(f"{k}: {v[0]} elements, {v[1]} all-zero, {v[2]} in the gap class" for k, v in t.items() if k != "calls")
        print(f"{name} {fn}: {t['calls']} calls; {parts}", flush=True)
