# I1098-mm5/kfree1000od: D 1000 p1 harmonics 19-31 released with the octo-double residual on the relaxed kernel (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Continues `../kfree1000qd/` (stopped after h21 on the coordinator's order, 2026-11-26 10:25:55 UTC), but from its **h17 state**: in the
quad-double-residual run h19 and h21 did not fall (+1.1314e-20, +1.4329e-20) where D 300's did (-3.0887e-19, +3.7004e-21), which
may be the qd residual's floor times Delta's gain and not a real tail, and h23's inner solves floored at 1e-40 in qd against a
target of 2.8e-46. Here the residual is octo-double, on the relaxed-horizon kernel (about 13x faster od residual):
the comparison of h19's and h21's changes in od against the qd ones decides the question.

- Input: `input/release_ls_h17_D1000.0000.npz`, git blob 884f4df86701ba198d5745881250a4097013df7a (verified with
  `git hash-object`), the state after h17 of `../kfree1000qd/` (Delta 1.654240854145891722271520081, the input's
  1.654240854145891738985793904 with h15 and h17 released).
- Kernel and code: worktree `~/Source/choptuik-fastmul3` at 34ca1745 (wip/large-d-fastmul3), the release build of
  `../fastmul3-build/` in `~/Source/fastmul3-site` (its check PASSED: |F_relaxed - F_naive| 3.62e-57 against 1e-50, control
  3.69e-05; 34.3 min, 23.05 GB), run with `PYTHONPATH=~/Source/fastmul3-site HP_HORIZON_RELAXED=1`. The log's first line is the loaded
  `hpkernel.__file__`.
- Command, from `~/Source/choptuik-fastmul3/hp`, `~/venv-314`'s python, nice 10, detached under `timeout 8h`, 9 threads:

      python -u form_s.py release_ls <the input here> <this folder> --harm 19,21,23,25,27,29,31 --kmax 31 \
        --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit 34ca1745 \
        --jac_by 19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq > rls.log

## Bars and what to expect (written 2026-11-26 10:32 UTC, before the run)

| item | bar or expectation |
|---|---|
| the question | h19 and h21's changes in od (diff_delta.py), against the qd run's +1.1314e-20 and +1.4329e-20 and D 300's -3.0887e-19 and +3.7004e-21. If the od values agree with the qd ones, they are real and D 1000's tail falls more slowly than D 300's; if not, the qd ones were the residual's floor times Delta's gain |
| released | each harmonic ends with `released` (harmonic step below --tol_h 1e-44, or target \|F\| below --tol 1e-48) within 6 outer steps; h23 is the one that floored in qd. `direct_s.jsonl` is written when h31 is released, with the end check in quad-double (release_ls: `chk = "qd"` when res = od) |
| stop and report | a harmonic that ends at the outer floor stop without being released; an exception; an outer step more than 3x the first one's time; the 8 h timeout |
| time | the first outer step's time is reported; at D 300 a qq od outer step took 87 s, the serial od residual costs about 14x more at D 1000 (about 920 s per trial before), and the relaxed kernel's od residual is about 13x faster |
| Delta's change | reported per harmonic, in od, with the qd ones beside them |

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.
