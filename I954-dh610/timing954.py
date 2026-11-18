#!/usr/bin/env python3
"""#954 timing of one build: truth_system, newton_o and coefficients_o(s, zo, N, by_order=True), each timed, with the load average before and after.

    cd <build>/hp && python3 timing954.py RAW STATE.npz OUT_PREFIX [--N 24] [--threads 8]

Prints one JSON line (hpkernel's path, the three seconds, the load averages) and saves the series z_1..z_N (eight parts each) as OUT_PREFIX.npz."""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.getcwd())
raw, state, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
N = int(sys.argv[sys.argv.index("--N") + 1]) if "--N" in sys.argv else 24
threads = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 8
import hpkernel  # noqa: E402
from anm_run import coefficients_o  # noqa: E402
from octo_corrector import truth_system  # noqa: E402

la0 = os.getloadavg()
t0 = time.time()
z, meta, (s, _, _, _), info = truth_system(raw, state, threads=threads)
t_truth = time.time() - t0
zo = [np.ascontiguousarray(np.asarray(p)) for p in z]
t0 = time.time()
s.newton_o(list(zo))
t_newton = time.time() - t0
t0 = time.time()
Bz, _ = coefficients_o(s, zo, N, by_order=True)
t_series = time.time() - t0
la1 = os.getloadavg()
np.savez(prefix + ".npz", **{f"z{k}_{q}": np.asarray(p) for k in range(1, len(Bz)) for q, p in enumerate(Bz[k])})
print(json.dumps(dict(hpkernel=hpkernel.__file__, N=N, threads=threads, t_truth=round(t_truth, 2), t_newton=round(t_newton, 2),
                      t_series=round(t_series, 2), ratio_series_newton=round(t_series / t_newton, 3),
                      load_before=[round(x, 2) for x in la0], load_after=[round(x, 2) for x in la1])))
