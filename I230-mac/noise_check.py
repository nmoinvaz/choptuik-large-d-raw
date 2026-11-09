#!/usr/bin/env python3
"""I230-mac: the noise floor of ln|det M| at lam = 3 on this machine, after repro_check.py failed its 1e-8 criterion
(1.3e-8 against the I212 cache).

    python3 noise_check.py HP_DIR OUT.jsonl

Two determinants of the same matrix through different code: the crate's complex double-double LU (modecount_cx, the
one the counts use) and hpkernel's real one (Solver.mode_det). Their difference is the rounding of the LU on this
ill-conditioned matrix (pivots down to 2e-15 of the largest, #212), independent of the machine. Reading, fixed before
the run: if the two differ by 1e-8 or more, the cross-machine difference of repro_check.py is within this machine's
own rounding noise of the determinant; if they agree to much better than 1e-8, the cross-machine difference comes from
another source (the segment plan or the build) and is reported as such. Either way the phase differences (below 1e-9
rad) are far below the steps that decide a winding (about 0.1 rad).
"""
import json
import sys
import time

hp, out = sys.argv[1:3]
sys.path.insert(0, hp)
from modecount_common import setup  # noqa: E402

st = setup(f"{hp}/data/seeds/local/up23_D61.0264.npz", M=48, kf=23, fmax=1e-15)
t = time.time()
la_c, arg_c, _, _ = st.det(3.0, 0.0)
t1 = time.time()
r = st.det_real(3.0)
t2 = time.time()
# hpkernel's Solver.mode_det returns (sign, ln|det|, smallest pivot, largest pivot); the first run of this script read
# the sign (its log line "hpkernel 1.000000000000" is that sign; the tuple it printed holds ln|det| 273.2516217710863)
la_h = float(r[1]) if isinstance(r, (tuple, list)) else float(r)
rec = dict(lam=3.0, lnabs_crate=la_c, arg_crate=arg_c, hpkernel=repr(r), lnabs_hpkernel=la_h, diff=abs(la_c - la_h),
           sec=[round(t1 - t, 1), round(t2 - t1, 1)], time=time.strftime("%Y-%m-%d %H:%M:%S"))
with open(out, "a") as fo:
    fo.write(json.dumps(rec) + "\n")
print(f"lam 3: ln|det| crate {la_c:.12f}, hpkernel {la_h:.12f} (returned {r!r}), difference {rec['diff']:.1e}")
