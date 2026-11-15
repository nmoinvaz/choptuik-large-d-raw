#!/usr/bin/env python3
"""#830's diagnostic: planted's truth is read by load_q (four parts), but the chain states store eight (parts 4-7 up
to 1.9e-65). In planted's own system (pinned_o, whose plan and held values read only parts 0-1, so the same either
way), the pinned max|F| and the plain Newton step's Delta part at the state read in eight parts (octo_corrector.load_o)
against the four-part state that planted, proj_shift and step_spread use. Diagnostic only: nothing is judged.
usage (from hp/): python3 diag_parts.py RAW STATE [STATE ...] [--threads=3] [--steps=1]"""
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import mpmath as mp                                                       # noqa: E402
import numpy as np                                                        # noqa: E402
from hpkernel.driver import load_q                                        # noqa: E402
from octo_corrector import load_o, o8, o8_of_q, omax, pinned_o, plant_start   # noqa: E402
from reseed import offsets                                                # noqa: E402


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in argv if a.startswith("--") and "=" in a)
    mp.mp.dps = 150
    raw = args[0]
    for path in args[1:]:
        t0 = time.time()
        z4, meta = load_q(os.path.join(raw, path))
        z4 = o8(z4)
        z8, _ = load_o(os.path.join(raw, path))
        s, sp, sq, so = pinned_o(meta, z4, threads=int(opts.get("threads", 3)))
        M = int(meta["M"])
        K = (len(z4[0]) - 1) // (4 * M) - 1

        class RS:
            off = offsets(M, K)
        RS.K = K
        zq = o8_of_q(plant_start(z4, RS, 0.0, 1, 0)[0])             # planted --rel 0's start
        diff = max(float(np.abs(np.asarray(z8[q]) - np.asarray(zq[q])).max()) for q in range(8))
        Fq, F8 = omax(so.residual_o(zq)), omax(so.residual_o(z8))
        print(f"{path}: D {mp.nstr(mp.mpf(meta['D_str']), 12)}; the largest part difference between the eight-part "
              f"state and planted's start {diff:.3e}; pinned max|F| (octo): four-part start {Fq:.4e}, eight-part state "
              f"{F8:.4e} ({time.time() - t0:.0f} s)", flush=True)
        if opts.get("steps", "1") == "1":
            for name, z in (("four-part start", zq), ("eight-part state", z8)):
                t1 = time.time()
                st = so.newton_o(z)
                d = o8(st[0])
                dD = mp.fsum(mp.mpf(float(p[-1])) for p in d)
                print(f"  plain step at the {name}: dDelta {mp.nstr(dD, 10)}, max|dz| {float(np.abs(d[0]).max()):.4e}, "
                      f"smallest pivot {st[3]:.4e} ({time.time() - t1:.0f} s)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
