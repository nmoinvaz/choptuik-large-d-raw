"""#1012 stage 4: unit check of the --h5/--h7/--h9 plumbing (and --h3) on the file itself: LazyHier.h(l, x) at #999's pretuned x with the environment variables that hier_nb's
main sets from --hK= and that the spawn workers inherit. For each case the step of every level 3, 5, 7, 9 is compared with hier's default 1e-6 * max(|b|, 1e-3 |A|), computed by the parent class.

    python unit_h579.py SRC CASE            SRC = the solver/inner_stokes directory; CASE one of
      default | h5_1e-4 | h7_1e-4 | h9_1e-4 | h579_1e-4 | h579_1e-6 | wrongenv
Expected ratio to the default: 100 at a level set to 1e-4, 1 at a level set to 1e-6 or not set, never anything else. --mutate=expect reads the h9 case's 100 as 1: must fail.
Exit 0 when every level's ratio is as expected."""
import os, sys
import numpy as np

SRC, case = sys.argv[1], sys.argv[2]
SET = {"default": {}, "h5_1e-4": {5: "1e-4"}, "h7_1e-4": {7: "1e-4"}, "h9_1e-4": {9: "1e-4"}, "h579_1e-4": {5: "1e-4", 7: "1e-4", 9: "1e-4"},
       "h579_1e-6": {5: "1e-6", 7: "1e-6", 9: "1e-6"}, "wrongenv": {}}[case]
for lvl, v in SET.items():
    os.environ[f"HIER_NB_H{lvl}"] = v
if case == "wrongenv":
    os.environ["HIER_NB_H5X"] = "1e-4"
sys.path.insert(0, SRC)
import hier_nb as HN, hier as H

x = np.array([2.719219, 1.000022, 0.148977988, 0.014770713, 0.008424206, 0.001511189, 0.000474205, 0.00012168, 2.6602985034854245e-05, 8.947854197796251e-06])
h = HN.LazyHier(9, 0.15, top=99, verbose=0)
PARENT = HN.LazyHier.__mro__[1]                      # hier_nb replaces H.Hier by LazyHier on import: the baseline is the parent class
ok = True
for l in (3, 5, 7, 9):
    b = x[H.idx(l)]
    default = 1e-6 * np.maximum(np.abs(b), 1e-3 * np.abs(x[0]))
    assert np.array_equal(PARENT.h(h, l, x), default), f"level {l}: hier's default is not the formula"
    got = h.h(l, x)
    ratio = got / default
    want = {"1e-4": 100.0, "1e-6": 1.0}.get(SET.get(l), 1.0)
    if "--mutate=expect" in sys.argv and l == 9 and case == "h9_1e-4":
        want = 1.0
    good = np.allclose(ratio, want, rtol=1e-12) and (SET.get(l) is None or HN.FD_STEP.get(l) == float(SET[l]))
    ok = ok and good
    print(f"case {case} level {l}: step {got}, {ratio} x the default (want {want}), FD_STEP {HN.FD_STEP.get(l)} -> {'ok' if good else 'FAIL'}")
sys.exit(0 if ok else 1)
