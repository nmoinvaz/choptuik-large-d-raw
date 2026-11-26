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

## Stopped (2026-11-26 10:47:40 UTC) with h19 and h21 released, h23 floored

Stopped by hand, with SIGTERM to the `timeout` pid 21326 (python 21327), after 14 min 46 s, on the coordinator's order, so the queued
`../m48_1000/` test starts: h23's inner floor is the same in od as in qd, so it belongs to the M 32 system and more trials would not settle it.

| harmonic | outer steps (times) | change in Delta, od (diff script) | the qd run's change |
|---|---|---|---|
| h19 | 2 (240.2 s, 43 s: released) | +1.13137e-20 | +1.13137e-20 (od - qd 1.0e-39) |
| h21 | 2 (222.1 s, 44 s: released) | +1.43289e-20 | +1.43289e-20 (od - qd 6.0e-39) |
| h23 | outer 0, no step accepted | | no step accepted |

Delta after h21 is identical in od and qd to 32 digits (1.6542408541458917222971626962757). h23's lines, od against qd:

    od: h23 outer 0: target |F| 2.77e-46, harmonic-23 step 1.35e-09 (43 s)
    od: trial lam 1:   inner floor in 3 steps (|F| 1.71e-40), target |F| 1.71e-40 against 2.77e-46 (176 s)
    od: trial lam 0.5: inner floor in 3 steps (|F| 1.08e-41), target |F| 1.08e-41 against 2.77e-46 (310 s)
    qd: trial lam 1:   inner floor in 3 steps (|F| 1.71e-40) (613 s);  lam 0.5: 1.08e-41 (1013 s)

The floor falls 16x per halving (lam^4) in both. An od trial took about 130 s on the relaxed kernel against about 400 s for a qd trial on the old
one. The exit code of the killed run is not meaningful.
