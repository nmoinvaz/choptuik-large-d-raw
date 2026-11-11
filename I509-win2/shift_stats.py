#!/usr/bin/env python3
"""#509: applications of the complex shift per determinant and the difference between the two forms at each application (modecount_cx built with patch_shiftstats.py).
usage: python shift_stats.py HP_DIR CX_BUILD_DIR OUT.json
For each of the two check points: reset, one mode_det, read shift_stats() = (calls, elements, nonzero, max_rel, rms_rel, max_abs). Then the control: set_shift_plant(1e-20) (the OLD form's lo part plus 1e-20 times its hi part) and the
same point 1 again: the rms and the max relative difference must come out at 1e-20 (to 1%), else exit 1. The determinant itself must be today's (-940.4586634376807 at point 1): the instrumentation keeps the new form."""
import json, os, sys
HP, CX, OUT = sys.argv[1:4]
RAW = "D:/choptuik-large-d-raw"
S = f"{RAW}/I250-mac/states/modecount_state_D30.0688_M48_october.npz"
PTS = [(4.267, 0.9740000000000001), (3.94364216362105, 1.1900607986722187)]
sys.path.insert(0, HP)
import modecount_common as mc  # noqa: E402
sys.path.insert(0, CX)
sys.modules.pop("modecount_cx", None)
st = mc.setup(S, M=None, kf=None, fmax=1e-15)
import modecount_cx  # noqa: E402
assert os.path.dirname(os.path.abspath(modecount_cx.__file__)) == os.path.abspath(CX), "wrong build"
res = dict(points=[], control=None)
modecount_cx.set_shift_plant(0.0)
modecount_cx.shift_stats()
for k, (lr, li) in enumerate(PTS, 1):
    d = st.c.mode_det(st.zh, st.zl, float(lr), float(li))
    c, e, nz, mx, rms, mxa = modecount_cx.shift_stats()
    row = dict(point=k, lam=[lr, li], ln_det=d[0], calls=c, elements=e, nonzero=nz, max_rel=mx, rms_rel=rms, max_abs=mxa)
    res["points"].append(row)
    print(f"point {k} ({lr}, {li}): ln|det| {d[0]!r}; applications (calls of the shift on 8-lane fields) {c:.0f}, elements {e:.0f}, differing {nz:.0f} ({100 * nz / e:.1f}%), max relative difference {mx:.3e}, rms {rms:.3e}, max absolute {mxa:.3e}", flush=True)
modecount_cx.set_shift_plant(1e-20)
d = st.c.mode_det(st.zh, st.zl, float(PTS[0][0]), float(PTS[0][1]))
c, e, nz, mx, rms, mxa = modecount_cx.shift_stats()
modecount_cx.set_shift_plant(0.0)
ok = abs(rms / 1e-20 - 1) < 0.01 and abs(mx / 1e-20 - 1) < 0.05
res["control"] = dict(plant=1e-20, rms_rel=rms, max_rel=mx, ok=ok)
print(f"control (the old form's lo part plus 1e-20 x its hi part): rms relative difference {rms:.4e}, max {mx:.4e}; {'PASS' if ok else 'FAIL'}", flush=True)
json.dump(res, open(OUT, "w"), indent=1)
sys.exit(0 if ok else 1)
