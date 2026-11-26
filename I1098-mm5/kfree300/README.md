# I1098-mm5/kfree300: D 300's p1 horizon harmonics 15-31 released (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Order of coordinator t5 (2026-11-26, the jump agent's command relayed unchanged). "Full" today means harmonics 1-13 of p1
released, with p1's horizon harmonics 15-31 held at zero. This run releases them one by one (`form_s.py release_ls --harm
15,17,...,31 --kmax 31`) at D 300 and records Delta's change for each, so the frozen tail's size is measured.

- Input: `input/release_ls_h13_D300.0000.npz`, git blob e5a3b5f85d19cb7de392261274778920a9ddf448 (verified with `git hash-object`),
  from `I1088-dh610/out/rls300/` of this repository: D 300, M 32, 5 nodes, ks 306, kc 146, kfreeze 13, solved, u horizon
  (no Moebius). Its Delta is 1.678171015400871567732214178493592019810.
- Code: worktree `~/Source/choptuik-1098` at 992c86c3 (wip/large-d-form-s). The hp kernel installed in `~/venv-314` is the
  1ccd32ab build of I1088-mm5/build/; the only change in hp/src between the two commits is a statistics hook behind mutate 55
  that leaves the arithmetic alone (checked with `git diff 1ccd32ab 992c86c3 -- hp/src`).
- Command, from `~/Source/choptuik-1098/hp`, `~/venv-314`'s python, nice 10, detached under `timeout 6h` (the stop),
  9 threads (the L50000 solve keeps its own 9):

      python -u form_s.py release_ls <the input here> <this folder> --harm 15,17,19,21,23,25,27,29,31 --kmax 31 \
        --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit 992c86c3 > rls.log

## Bars and what to expect (written 2026-11-26 07:43 UTC, before the run)

| item | bar or expectation |
|---|---|
| released | each harmonic ends with `released` (its harmonic-k step below --tol_h 1e-44, or the target |F| below --tol 1e-48) within 6 outer steps. The final record `direct_s.jsonl` is written only when harmonic 31 is released |
| stop and report | a harmonic that ends at the outer floor stop without being released; an exception; an outer step 3x past its predicted end; the 6 h timeout |
| expected change in Delta | the coordinator: the changes from releasing h11 and h13 fall by only 0.3-0.5 per step, so the frozen tail may be 1e-14 to 3e-14 in all. At D 300 the h11 -> h13 change was +2.75e-14 (+5.3e-14 for h11); at a factor 0.3-0.5 per step, h15 would add about 0.8e-14 to 1.4e-14 and h17 about 0.2e-14 to 0.7e-14. These are the extrapolation, not a check |
| time | a few minutes per outer step, about 1 to 1.5 h in all (the coordinator) |
| reports | after h15 and h17, each with Delta's change, then at the end; the folder is pushed at each |

Delta's change per harmonic is the difference of the log's Delta digits, computed by script (mpmath), never by hand.
