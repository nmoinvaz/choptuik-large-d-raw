#!/usr/bin/env python3
"""I243-mac: planted-truth test of offset_check.check on the synthetic det M of hp/modecount_planted.py's group D61.

    python3 planted_offset.py HP_DIR [--phi=0.381966] [--mutate=interp]     exit 1 if a criterion fails

Each case is counted with the OLD rule (modecount_wind --mutate=flat, the rule of the counts being re-checked), and the
offset check then runs on that record with the synthetic g. Criteria, fixed before running:
  (a) every case whose old count is wrong in a box using T or T0 because of a uniform rate along them (the rows,
      long rows and held-out rows) gets at least one flag, and after the re-sampling of the flags every box equals the
      planted number to 1e-6;
  (b) every case whose old count is right gets no change of any box (flags are allowed, re-sampling must confirm);
  (c) the close pairs are reported (flagged or not, corrected or not), not tested: the check is phase-only and is not
      meant for them (the alias rule's ln|g| scale is).
Control (first version): --phi=0.5 (the midpoint) must fail (a) on a row with an even number of turns per interval
(long row k4). It did not fail (planted_offset_control_phi0.5.log): the old rule's samples on T hold one turn per
interval there (the conjugate row doubles the rate to 2 pi per zero spacing), an odd number, which midpoints catch too.
A different design is not a broken input, so the control is now --mutate=interp: the golden point's phase is taken
from the endpoints by linear interpolation (no new sample). It must fail (a).
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
phi = float(([a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--phi=")] or [(3 - math.sqrt(5)) / 2])[0])
mutate = ([a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--mutate=")] or [None])[0]
sys.path.insert(0, hp)
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import modecount_wind as W  # noqa: E402
import modecount_planted as P  # noqa: E402
import modecount_moment_planted as MP  # noqa: E402
import offset_check as OC  # noqa: E402

ok = True
for name, extra in P.d61_cases().items():
    with tempfile.TemporaryDirectory() as tmp:
        info = dict(D=MP.N + 2, M=0, omega=MP.OM, lam_g=MP.LG, lam_f=MP.LP)
        det = MP.det_for(extra)
        rec = W.count(det, info, MP.POLES, dict(MP.LAYOUT, data=tmp, h0="0.6", resolve="last", mutate="flat"),
                      lambda m: None, "x", os.path.join(tmp, "r.jsonl"))
    Q = np.array([p for p in MP.POLES if abs(p.imag) < rec["y2"] + 3 * MP.OM], complex)
    K = np.array([complex(*z) for z in rec["expected_zeros"]])

    def gfun(lam):
        la, arg, _, _ = det(lam.real, lam.imag)
        return (complex(la, arg) + complex(np.sum(np.log(lam - Q)) - np.sum(np.log(lam - K)))
                - complex(np.polyval(rec["trend"], lam)))
    out, boxes = OC.check(rec, gfun, phi, mutate=mutate)
    planted = list(extra) + [z.conjugate() for z in extra]
    want = {b: P.expected(rec["boxes"][b]["rect"], extra) for b in boxes}
    old_ok = all(rec["boxes"][b]["winding_g_int"] == want[b] for b in boxes)
    new_ok = all(abs(x["new"] - want[b]) < 1e-6 for b, x in boxes.items())
    nflag = sum(len(v["flags"]) for v in out.values())
    rows = "row" in name
    if rows and not old_ok:
        verdict = "pass" if nflag and new_ok else "FAIL (a)"
    elif old_ok:
        verdict = "pass" if new_ok else "FAIL (b)"
    else:
        verdict = "reported" + (", corrected" if new_ok else ", not corrected")
    ok &= not verdict.startswith("FAIL")
    print(f"{verdict:24s} {name}: old count {'right' if old_ok else 'wrong'}, {nflag} flags, after re-sampling "
          + ", ".join(f"{b} {x['new']:+.3f}" for b, x in boxes.items() if abs(x['new'] - x['old']) > 1e-6), flush=True)
print(("all criteria pass" if ok else "SOME CRITERIA FAIL") + f" (phi {phi}, mutate {mutate})")
sys.exit(0 if ok else 1)
