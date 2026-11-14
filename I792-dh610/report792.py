#!/usr/bin/env python3
"""#792: bars 2 and 3 at each saved series (I792-dh610/repro/jet_pin3_D<D>.npz), from Delta's series in octo-double through
jet_singularity.locate_one: (2) the root test within 5% of |P - D0|, P = 259.95; (3) the nearest stable Pade pole has
|Im D*| <= 0.1 and |Re D* - 259.95| <= 0.2. --mutate=shiftP moves P by +1.0, which must fail bar 3 at every base.
    PYTHONPATH=<checkout>/hp python3 report792.py JET.npz [JET.npz ...] [--mutate=shiftP]
Exit 0 when bars 2 and 3 hold at every base (with --mutate=shiftP: when bar 3 fails at every base)."""
import io
import sys
from contextlib import redirect_stdout

import mpmath as mp
from jet_singularity import DPS, load_jet, locate_one, row_series

mp.mp.dps = DPS
P = 259.95 + (1.0 if "--mutate=shiftP" in sys.argv else 0.0)
files = [a for a in sys.argv[1:] if a.endswith(".npz")]
f2 = f3 = 0
print(f"P = {P:.2f}" + ("  (--mutate=shiftP)" if "--mutate=shiftP" in sys.argv else ""))
for f in files:
    Z, m = load_jet(f)
    c, _ = row_series(Z, "delta")
    with redirect_stdout(io.StringIO()):
        r = locate_one(c, m["D"], label="delta")
    D0 = r["D0"]
    dist = abs(P - D0)
    ratio = r["root_radius"] / dist - 1
    ok2 = abs(ratio) <= 0.05
    pade = sorted(r["pade"], key=lambda x: x["abs"])
    nst = pade[0] if pade else None
    ok3 = nst is not None and abs(nst["D_im"]) <= 0.1 and abs(nst["D_re"] - P) <= 0.2
    f2 += not ok2
    f3 += not ok3
    others = "; ".join(f"{x['D_re']:.3f}{x['D_im']:+.3f}i (n{x['n']})" for x in pade[1:]) or "none"
    print(f"D0 {D0:.4f}: root test {r['root_radius']:.4f}, |P - D0| {dist:.4f}, {ratio:+.1%} -> bar 2 {'met' if ok2 else 'FAILED'}; "
          f"nearest Pade pole " + (f"{nst['D_re']:.4f}{nst['D_im']:+.4f}i (n{nst['n']}, spread {nst['spread']:.1e})" if nst else "none")
          + f" -> bar 3 {'met' if ok3 else 'FAILED'}; other stable poles {others}")
print(f"bar 2 failed at {f2} of {len(files)}, bar 3 at {f3} of {len(files)}")
if "--mutate=shiftP" in sys.argv:
    sys.exit(0 if files and f3 == len(files) else 1)
sys.exit(0 if files and not f2 and not f3 else 1)
