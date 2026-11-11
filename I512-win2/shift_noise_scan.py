#!/usr/bin/env python3
"""#512: the spread of ln|det M| against the size of the random relative change of the shift's output (modecount_cx built with patch_shiftnoise.py).
usage: python shift_noise_scan.py HP_DIR CX_BUILD_DIR OUT.json
For rel in 1e-34 ... 1e-24 and seeds 1..10, at both check points: the change of ln|det| from today's value; prints the sample std, mean and range per rel. Below the double-double rounding of the lo part (about 1e-32) the change
must vanish (rel 1e-34: every value 0, the control that the noise is not applied below the arithmetic's resolution); at large rel it must grow in proportion to rel (the first-order regime); in between the spread is the
spread over rounding realisations (the perturbation re-rolls the roundings downstream). Exit 1 if rel 1e-34 gives a nonzero change."""
import json, os, sys
import numpy as np
HP, CX, OUT = sys.argv[1:4]
RAW = "D:/choptuik-large-d-raw"
S = f"{RAW}/I250-mac/states/modecount_state_D30.0688_M48_october.npz"
PTS = [(4.267, 0.9740000000000001), (3.94364216362105, 1.1900607986722187)]
sys.path.insert(0, HP)
import modecount_common as mc  # noqa: E402
sys.path.insert(0, CX)
sys.modules.pop("modecount_cx", None)
st = mc.setup(S, M=None, kf=None, fmax=1e-15, threads=2)
import modecount_cx  # noqa: E402
assert os.path.dirname(os.path.abspath(modecount_cx.__file__)) == os.path.abspath(CX), "wrong build"
def det(k):
    lr, li = PTS[k]
    return float(st.c.mode_det(st.zh, st.zl, float(lr), float(li))[0])
RELS = [1e-34, 1e-32, 1e-31, 1e-29, 1e-28, 1e-26, 1e-24]
res = {}
ok = True
for k in range(2):
    modecount_cx.set_shift_noise(0.0, 0)
    d0 = det(k)
    for rel in RELS:
        v = []
        for seed in range(1, 11):
            modecount_cx.set_shift_noise(rel, seed)
            v.append(det(k) - d0)
        modecount_cx.set_shift_noise(0.0, 0)
        v = np.array(v)
        res[f"p{k + 1}_{rel:g}"] = v.tolist()
        print(f"point {k + 1} rel {rel:.0e}: std {v.std(ddof=1):.3e} mean {v.mean():+.3e} min {v.min():+.3e} max {v.max():+.3e}  (std / rel = {v.std(ddof=1) / rel:.3e})", flush=True)
        if rel == 1e-34 and np.any(v != 0):
            ok = False
json.dump(dict(rels=RELS, values=res, ok=ok), open(OUT, "w"), indent=1)
print("control (rel 1e-34 changes nothing): " + ("passed" if ok else "FAILED"))
sys.exit(0 if ok else 1)
