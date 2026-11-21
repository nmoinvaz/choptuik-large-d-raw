#!/usr/bin/env python3
"""#1064 (dh170): anm_run.py run unchanged except that ElimO.project prints what it is given and what it returns: the pinned quad-double residual that decides whether the iterate is projected (switch), the pinned octo-double
max|F| before and after, and the displacement of the iterate. Same arguments as anm_run.py (run from hp/).   anm_probe1064.py <anm_run.py's arguments>"""
import os
import sys
import time

import numpy as np

HP = os.environ.get("HP_DIR", os.getcwd())
sys.path.insert(0, HP)
import octo_corrector as oc  # noqa: E402

_orig = oc.ElimO.project


def project(self, z):
    z8 = oc.o8(z)
    nf = oc.qmax(self.sq.residual_q(*oc.q4_of_o(z8)))
    Rb = self.so.residual_o(list(z8))
    mb = float(np.abs(np.asarray(Rb[0]) + np.asarray(Rb[1])).max())
    t0 = time.time()
    out = _orig(self, z)
    o8z = oc.o8(out)
    Ra = self.so.residual_o(list(o8z))
    ma = float(np.abs(np.asarray(Ra[0]) + np.asarray(Ra[1])).max())
    disp = max(float(np.abs(np.asarray(a[0]) - np.asarray(b[0]) + np.asarray(a[1]) - np.asarray(b[1])).max()) for a, b in [(o8z, z8)]) if False else float(np.abs((np.asarray(o8z[0]) + np.asarray(o8z[1])) - (np.asarray(z8[0]) + np.asarray(z8[1]))).max())
    print(f"PROBE project: pinned quad-double max|F| of the rounding {nf:.3e} (switch {self.switch:g}); pinned octo-double max|F| before {mb:.3e}, after {ma:.3e}; max displacement of the iterate {disp:.3e}; counts {dict(self.counts)}, u0o {getattr(self, 'counts', {}).get('u0o', 0)}; {time.time() - t0:.0f} s", flush=True)
    return out


oc.ElimO.project = project
sys.argv = ["anm_run.py"] + sys.argv[1:]
import runpy  # noqa: E402
runpy.run_path(os.path.join(HP, "anm_run.py"), run_name="__main__")
