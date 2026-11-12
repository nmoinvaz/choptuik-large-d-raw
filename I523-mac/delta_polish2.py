#!/usr/bin/env python3
"""Delta before and after an octo-double polish of a converged chain state (#523), as the chain's corrector polishes
a base: octo_corrector's PinnedO on the state's own system (pinned_o, the plan at the state at 1e-32, the held offset
exact in eight parts as renode_o.pinned forms it), inside ElimO with a Reseeder (anm_run.py --reseed 2), newton_od to
max |F| 1e-40 in at most 12 steps, junk directions frozen as given; with whichever hpkernel is first on PYTHONPATH.

    PYTHONPATH=<site>:HPDIR python3 delta_polish2.py RAWDIR STATE OUT.json [--junk=0] [--threads=2]
"""
import json
import os
import sys
import time

import mpmath as mp


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    raw, st, out = args
    import hpkernel
    from octo_corrector import _delta, _run_od, load_o, omax, pinned_o
    from reseed import Reseeder
    threads = int(opts.get("threads", 2))
    junk = int(opts.get("junk", 0))
    z, meta = load_o(os.path.join(raw, st))
    D = mp.mpf(meta["D_str"])
    _, _, _, so = pinned_o(meta, z, threads=threads, held_exact=True)
    rs = Reseeder(meta, D, threads=threads, qd=True)
    F0 = omax(so.residual_o(z))
    t0 = time.time()
    zo, hist, conv, Fo, counts = _run_od(so, rs, z, dict(tol=1e-40, it_max=12, mutate=0, junk=junk))
    with mp.workdps(60):
        d0, d1 = _delta(z), _delta(zo)
        rec = dict(state=st, hpkernel=hpkernel.__file__, D=meta["D_str"], junk=junk, Delta=mp.nstr(d0, 40),
                   Delta_new=mp.nstr(d1, 40), dDelta=float(d1 - d0), F_before=F0, F_after=Fo, converged=bool(conv),
                   steps=len(hist), projections=counts, seconds=round(time.time() - t0))
    for k, v in rec.items():
        print(f"  {k}: {v}", flush=True)
    json.dump(rec, open(out, "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
