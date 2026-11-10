"""#277: anm_run.py with the octo-double corrector's zero-iteration case made to print the start residual.

    python3 series_start.py RAW OUTDIR [anm_run.py options] --corrector od --qd_it 0

Run from the hp directory of the checkout. anm_run.main() is the stock driver. Only anm_run.newton_od is replaced, and only
for it_max == 0 (every other call goes to octo_corrector.newton_od unchanged): the replacement makes newton_od's first call,
s.newton_o(z) on the same ElimO/PinnedO object (so the same projection of the start, or the same StartNotProjected), prints
the start's max |F| and the first step's |dz| and pivots, takes no step and reports not converged. Every attempt of the
step therefore ends at its start, and the driver halves a three times: a, a/2, a/4, a/8 on one series."""
import os
import sys

import numpy as np

HP = os.getcwd()
assert os.path.exists(os.path.join(HP, "anm_run.py")), "run from the hp directory"
sys.path.insert(0, HP)
import anm_run  # noqa: E402
import octo_corrector as oc  # noqa: E402

_orig = oc.newton_od


def newton_od(s, z, tol=1e-40, it_max=12, **kw):
    if it_max != 0:
        return _orig(s, z, tol=tol, it_max=it_max, **kw)
    z = oc.o8(z)
    st = s.newton_o(z)
    nf = oc.omax(st[1:3])
    print(f"  start: |F| {nf:.2e}, |dz| {float(np.abs(st[0][0]).max()):.1e}, piv {st[3]:.1e}..{st[4]:.1e}, no step taken"
          f"{', below tol' if nf <= tol else ''}", flush=True)
    return z, [], bool(nf <= tol)


anm_run.newton_od = newton_od
sys.argv = ["anm_run.py"] + sys.argv[1:]
anm_run.main()
