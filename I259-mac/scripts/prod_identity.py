"""#259: the production det M is unchanged by the diagnostic modes (criterion in ../README.md, written before the run).

    python prod_identity.py HP_DIR STATE.npz KF LAM BUILD_DIR OUT.json

Loads modecount_cx from BUILD_DIR (put first on the path after modecount_common's own insert) and writes
mode_det at z = lam + 0.2 e^{2 pi i / 20} and at z + 2^-46 (the control's point) as exact hex floats.
"""
import json
import sys

import numpy as np

hp_dir, path, kf, lam, build, out = sys.argv[1:7]
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

sys.path.insert(0, build)
st = mc.setup(path, M=None, kf=int(kf), fmax=1e-15, threads=2)
import modecount_cx  # noqa: E402

print(f"modecount_cx {modecount_cx.__file__}", flush=True)
z = float(lam) + 0.2 * np.exp(2j * np.pi / 20)
res = {}
for name, w in (("z", z), ("z_plus_d", z + 2.0 ** -46)):
    d = st.c.mode_det(st.zh, st.zl, float(w.real), float(w.imag))
    res[name] = [float(x).hex() for x in d]
    print(name, d, flush=True)
json.dump(dict(module=modecount_cx.__file__, det=res), open(out, "w"), indent=1)
