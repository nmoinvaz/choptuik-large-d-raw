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

## Results (2026-11-26 08:03 UTC)

Started 07:43:55 UTC, ended 08:03 UTC (19 min; timeout pid 15843, python 15844; 9 threads, nice 10). The job's exit code was
not captured (detached); the log ends with the full-system line and `direct_s.jsonl` holds the record. Delta's changes
come from `diff_delta.py` (rls.log's digits, mpmath, 50 digits); the release_ls.jsonl column is the Newton step's own
first-order dDelta.

| harmonic | outer steps | change in Delta | the step's dDelta (jsonl) | released by |
|---|---|---|---|---|
| h15 | 3 (qd J floored, then qq J) | **-4.8083e-17** | -4.81e-17 | harmonic step 4.1e-24 < tol_h |
| h17 | 3 (qd, then qq) | +4.9397e-18 | +4.94e-18 | harmonic step 6.3e-25 < tol_h |
| h19 | 3 (qd, then qq) | -3.0887e-19 | -3.09e-19 | harmonic step 2.1e-23 < tol_h |
| h21 | 3 (qd, then qq) | +3.7004e-21 | +3.70e-21 | harmonic step 6.4e-22 < tol_h |
| h23 | 3 (qd, then qq) | -4.9622e-24 | -5.17e-24 | harmonic step 9.0e-26 < tol_h |
| h25 | 1 | 0 (no step taken) | +2.9e-25 | target \|F\| 7.1e-49 <= tol 1e-48 |
| h27 | 1 | 0 (no step taken) | +9.2e-25 | target \|F\| 8.0e-49 <= tol |
| h29 | 1 | 0 (no step taken) | +5.9e-25 | target \|F\| 8.1e-49 <= tol |
| h31 | 1 | 0 (no step taken) | -1.3e-24 | target \|F\| 8.1e-49 <= tol |
| **total** | | **-4.34487e-17** | | |

- Delta of the full D 300 system (harmonics 1-13): 1.678171015400871567732214178493592019810 (the input). With p1's horizon
  harmonics 15-31 free: **1.678171015400871524283476783790070385048**. The frozen tail is -4.3e-17, not the expected 1e-14 to 3e-14:
  the changes fall by a factor 0.1 or smaller per harmonic (h17/h15 -0.10, h19/h17 -0.063, h21/h19 -0.012, h23/h21 -0.0013).
  The h13 release itself moved Delta by +2.75e-14 (I1088-dh610), so h15 is 1.7e-3 of it.
- In every harmonic the first outer step with the quad-double Jacobian floored (the inner solve stalled at about 1e-29 to
  1e-32 above the 1e-44 to 1e-48 target) and the harmonic went on with the "qq" Jacobian (quad-double, solved in quad-double); the
  qd Jacobian's harmonic step is off by 3 to 4 orders from the qq one (h15: 5.05e-13 against 9.70e-10).
- **h25 to h31 were released by the residual criterion**, not by the harmonic step: their target \|F\| (7e-49 to 8e-49) is at or below
  --tol 1e-48 at the first outer step, while their harmonic steps (1.5e-16, 2.9e-16, 1.5e-16, 1.35e-13) are far above --tol_h
  1e-44. No step was taken, so Delta's change for them is the first-order dDelta of the unaccepted Newton step, 9.2e-25 or
  less each (a near-null direction: step 1e-16 from a residual of 1e-48), not a measurement.
- Delta - Track C at D 300 (delta_all.csv series 1.67817101541652, +- 1.25e-10, the record's trackC): -1.5648e-11, inside.
- **Discrepancy:** the record's Hamiltonian code check has a rows up to **1.06e-20**, against 2.8e-22 (I1088-dh610) and 4.8e-22
  (I1088-dh370) for the earlier D 300 full records. Cause not examined; reported, not fixed. The record's `disc` is null
  (release_ls runs no discretization tails), `valid` is null.
- Quad-double check max \|F\| 8.13e-49 (the solve's octo-double 8.12e-49).
- Files: `rls.log`, `release_ls.jsonl`, `direct_s.jsonl`, `release_ls_h<k>_D300.0000.npz` (the state after each harmonic),
  `..._step.npz` (each accepted outer step), `diff_delta.py`, `pid.txt`, `input/`.
