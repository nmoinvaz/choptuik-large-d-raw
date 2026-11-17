"""#903 p_min question: is the double-double horizon series right at D 229? The residual in double-double against
octo-double at the same stored z.

series_profile.py, which reads Solver.series in double-double, found the horizon terms at u0 growing past order ~50 at
D 226-229 (1.7e9 at order 160), while near_null.py's octo-double F changed by only 6.8e-22 in the horizon rows from
order 142 to 200 (k142, D 229.13). If the double-double terms were the series', its residual and the octo-double one
would agree; if they are rounding grown by the recursion, the double-double horizon rows are far above the octo-double
ones at a converged state. Printed, at each order K: max|F| over the horizon rows and over the other rows, from
Solver.residual (double-double, hi + lo) and Solver.residual_o (octo-double, hi part), on the stored plan (a state
without one gets a new plan, as near_null.py does). Then the same for the pinned residual F - c, c the held offset of
p1's harmonics (kfreeze, 13] at the state's own coefficients (pinning.PinnedSolver's c8, as near_null.py's pinned
step), which the chain drives to zero: at a converged state the octo-double F - c is at the chain's tolerance.

Run: python3 dd_vs_od.py RAWDIR STATE K1 [K2 ...]
"""
import os
import sys

import numpy as np

HP = "/Users/nathan/Source/choptuik-large-d-902/hp"
sys.path.insert(0, HP)
from hpkernel.driver import make_solver  # noqa: E402
from multidouble import od_axpy  # noqa: E402
from octo_corrector import load_o  # noqa: E402
from pinning import PinnedSolver, band_coeffs, band_field  # noqa: E402

raw, st, Ks = sys.argv[1], sys.argv[2], [int(k) for k in sys.argv[3:]]
z, m = load_o(os.path.join(raw, st))
z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
M, nodes = int(m["M"]), list(m["nodes"])
D = m.get("D_str", repr(float(m["D"])))
Kn = len(nodes)
h0, h1 = 4 * M * Kn, 4 * M * (Kn + 1)
print(f"{st}: D {float(m['D']):.4f}, the state's order {m.get('ks')}; horizon rows {h0}..{h1 - 1} of {len(z[0])}")
for K in Ks:
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=K, threads=3,
                    kfreeze=int(m.get("kfreeze", 3)))
    s.set_segs(m["segs"] if "segs" in m else s.plan(z[0], z[1], 1e-32, 0.05))
    kf = int(m.get("kfreeze", 3))
    held = [h for h in range(kf + 1, 14) if h % 2 == 1]
    if held:
        hc = band_coeffs(z[0][:M], z[1][:M], M, held, exact=True, rest=[p[:M] for p in z[2:]])
        hf = band_field(hc, held, M, parts=8)
        c8 = [np.ascontiguousarray(p) for p in PinnedSolver(s, M, hf[0], hf[1], h_rest=hf[2:]).c8]
    else:   # kfreeze 13: nothing held, c = 0
        c8 = [np.zeros(len(z[0])) for _ in range(8)]
    fh, fl = s.residual(z[0], z[1])
    fd = np.asarray(fh) + np.asarray(fl)
    f8 = [np.asarray(p) for p in s.residual_o(z)]
    fo = f8[0]
    po = np.asarray(od_axpy(-1.0, *c8, *f8)[0])
    pd = fd - (c8[0] + c8[1])
    rest = np.r_[0:h0, h1:len(fd)]
    for name, a, b in (("F", fd, fo), ("F - c", pd, po)):
        a, b = np.abs(a), np.abs(b)
        print(f"  order {K}, {name}: double-double horizon {a[h0:h1].max():.3e}, other rows {a[rest].max():.3e}; "
              f"octo-double horizon {b[h0:h1].max():.3e}, other rows {b[rest].max():.3e}")
