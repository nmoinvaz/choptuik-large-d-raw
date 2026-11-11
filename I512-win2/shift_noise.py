#!/usr/bin/env python3
"""#512: the spread of ln|det M| at #509's two check points over random rounding-sized changes of the complex shift's output in dtau_c.
usage: python shift_noise.py HP_DIR CX_BUILD_DIR OUT.json   (modecount_cx built with patch_shiftnoise.py)
Per point: ln|det| of today's code (rel 0); the control A: rel 0 with a seed is the same value to the bit; the control B (a fixed known change): the shift in its old DotAcc form, whose change of ln|det|
(old minus new) must equal -(#509's first-order prediction new minus old: +8.10816260e-9, -1.67013830e-8) to 1e-3 relative; then seeds 1..30 with rel 1e-30 (uniform in [-1, 1) per element, deterministic in the seed and
the element's inputs), and seeds 1..5 at rel 1e-29 (the linearity check: the change must scale with rel to 20%). Prints the 30 values, their mean, sample standard deviation, min and max relative to the baseline.
Exit 1 if a control fails."""
import json, math, os, sys
import numpy as np
HP, CX, OUT = sys.argv[1:4]
RAW = "D:/choptuik-large-d-raw"
S = f"{RAW}/I250-mac/states/modecount_state_D30.0688_M48_october.npz"
PTS = [(4.267, 0.9740000000000001), (3.94364216362105, 1.1900607986722187)]
FIRST_ORDER = [8.10816260e-9, -1.67013830e-8]    # #509: Re tr(M_old^-1 (M_new - M_old)), new form minus old form
TODAY = [-940.4586634376807, -965.1149263918375]
sys.path.insert(0, HP)
import modecount_common as mc  # noqa: E402
sys.path.insert(0, CX)
sys.modules.pop("modecount_cx", None)
st = mc.setup(S, M=None, kf=None, fmax=1e-15, threads=2)
import modecount_cx  # noqa: E402
assert os.path.dirname(os.path.abspath(modecount_cx.__file__)) == os.path.abspath(CX), "wrong build"
ok = True
res = []
def det(k):
    lr, li = PTS[k]
    return float(st.c.mode_det(st.zh, st.zl, float(lr), float(li))[0])
for k, (lr, li) in enumerate(PTS):
    modecount_cx.set_shift_old(False); modecount_cx.set_shift_noise(0.0, 0)
    d0 = det(k)
    a_ok = d0 == TODAY[k]
    modecount_cx.set_shift_noise(0.0, 17)
    dA = det(k)
    a_ok = a_ok and dA == d0
    modecount_cx.set_shift_noise(0.0, 0)
    modecount_cx.set_shift_old(True)
    dB = det(k)
    modecount_cx.set_shift_old(False)
    shift = dB - d0
    pred = -FIRST_ORDER[k]
    b_ok = abs(shift / pred - 1) < 1e-3
    print(f"point {k + 1} ({lr}, {li}): baseline {d0!r} (today's {TODAY[k]!r}: {'same' if d0 == TODAY[k] else 'DIFFERENT'}); rel 0 with a seed: {'same' if dA == d0 else 'DIFFERENT'}; "
          f"control B old form: change {shift:+.6e} against the prediction {pred:+.6e} (ratio {shift / pred:.6f}) {'ok' if b_ok else 'FAIL'}", flush=True)
    ok = ok and a_ok and b_ok
    vals = []
    for seed in range(1, 31):
        modecount_cx.set_shift_noise(1e-30, seed)
        vals.append(det(k) - d0)
    modecount_cx.set_shift_noise(0.0, 0)
    v = np.array(vals)
    lin = []
    for seed in range(1, 6):
        modecount_cx.set_shift_noise(1e-29, seed)
        lin.append(det(k) - d0)
    modecount_cx.set_shift_noise(0.0, 0)
    lin = np.array(lin)
    # linearity: the change at 1e-29 over the change at 1e-30 for the same seed should be 10
    ratios = lin / v[:5]
    l_ok = bool(np.all(np.abs(ratios / 10 - 1) < 0.2))
    ok = ok and l_ok
    print(f"  30 seeds at rel 1e-30, change of ln|det| from the baseline:", flush=True)
    print("   " + " ".join(f"{x:+.3e}" for x in v), flush=True)
    print(f"  mean {v.mean():+.3e}, sample std {v.std(ddof=1):.3e}, min {v.min():+.3e}, max {v.max():+.3e}, range {v.max() - v.min():.3e}; "
          f"linearity (rel 1e-29 over rel 1e-30, seeds 1..5): {' '.join(f'{r:.2f}' for r in ratios)} {'ok' if l_ok else 'FAIL'}", flush=True)
    res.append(dict(point=k + 1, lam=[lr, li], baseline=d0, control_a=a_ok, control_b=dict(change=shift, prediction=pred, ratio=shift / pred, ok=b_ok), values=vals, mean=float(v.mean()),
                    std=float(v.std(ddof=1)), min=float(v.min()), max=float(v.max()), lin_ratios=ratios.tolist(), lin_ok=l_ok))
json.dump(dict(results=res, ok=ok), open(OUT, "w"), indent=1)
print("controls: " + ("all passed" if ok else "FAILED"), flush=True)
sys.exit(0 if ok else 1)
