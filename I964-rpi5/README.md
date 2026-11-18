# I964-rpi5: the inner selection, stage 1: the compiled backend's checks on aarch64 (stopped at the setup)

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, Ubuntu aarch64, Python 3.13.7), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/964 (coordinator task, toward #355). Code: worktree of origin/main
0fc2fab0, branch `wip/i964-rpi5`, venv `~/Source/venv-choptuik` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1
(`setup_checks/env.txt`). Started 2026-11-18 17:05 UTC, stopped 17:08 UTC at the setup, as the issue says: no solve was run.

## Setup checks (`sh inner_nb_checks.sh`, 72 s in all, logs in `setup_checks/`)

| log | must end | got |
|---|---|---|
| `inner_nb_capcheck` | PASS, exit 0 | PASS, exit 0 |
| `inner_nb_capcheck_mutate` | FAIL, exit 1 | FAIL, exit 1 |
| `inner_nb_check` (M 1 3 5 7) | PASS, exit 0 | **FAIL, exit 1** (M 7, worst ratio 30 against the bar 10) |
| `inner_nb_check_mutate` (sign) | FAIL, exit 1 | FAIL, exit 1 (ratio 1.3e15 at M 5) |
| `hier_nb_selftest` | PASS, exit 0 | PASS, exit 0 |
| `hier_nb_selftest_mutate` | FAIL, exit 1 | FAIL, exit 1 (2.9e+02) |

M 1, 3 and 5 pass (worst ratios 1.7, 0.55, 1.6). At M 7 the four used entries at xi 0.1515 and 0.2 (r_7 at 0.1515; r_1, r_3,
r_5 at 0.2) have ratios 28, 30, 29 and 28, the other two used entries 1.5 (xi 0.1028, r_7) and 6.2 (xi 0.1188, r_5). The stored
log (`logs/inner_nb_check.log` at 0fc2fab0) has M 7 ratios 3.6, 1.7, 0.78, 0.71, 0.78, 0.78 for the same six entries.

## What the failing entries are

The check's yardstick is one scipy pair, rtol 1e-12 against 0.8e-12. On this machine that pair moved the M 7 entries at xi 0.2
by 1.3e-2 (r_3), against 1.9e-1 in the stored log, while |numba - scipy| is 3.8e-1 here and 1.5e-1 there (2.6e-9 and 1.1e-9
relative). So the difference is 2.5x the stored one and the yardstick 15x smaller. `setup_checks/diag_check_M7.py` (a scratch
script of this task, not in the repository; its worktree path is absolute) runs the same M 7 point with scipy at five rtols
and with both backends at 1e-13 (`diag_check_M7.log`):

| entry | scipy spread, rtol 1e-12 to 4e-13 | numba - scipy at 1e-12 | numba - scipy at 1e-13 | relative at 1e-12 |
|---|---|---|---|---|
| xi 0.2 r_1 | 3.5e+03 | 4.1e+03 | 2.1e+03 | 2.6e-9 |
| xi 0.2 r_3 | 2.9e-01 | 3.8e-01 | 2.0e-01 | 2.6e-9 |
| xi 0.2 r_5 | 2.3e-05 | 2.7e-05 | 1.4e-05 | 2.6e-9 |
| xi 0.1515 r_7 | 1.2e-09 | 1.3e-09 | 6.9e-10 | 5.2e-9 |

The numba - scipy difference is the size of scipy's own spread over rtol (1.2x to 1.3x), and halves at rtol 1e-13, so it reads as
integration noise of the leaked jumps and not as a different right-hand side, but the check as written does not say that, and the
frozen bar is not changed. Not established: whether the 2.6e-9 is the FMA contraction LLVM may apply on aarch64 (x86-64 numba
builds do not contract without fastmath) or the integrator's step-size path; a bit-level comparison of one right-hand-side call
against a scalar reference would tell.

## Not run

Step 1 (`fit3_repeat` reproduction), Jobs A (xi 0.14) and B (xi 0.16). The `fit3_repeat` log has no command line as its first line
(it starts at `pretune level 7 (approach ...`); the command is `proof/B_tail_M7.md` line 609 (`python -u hier_nb.py 7 2.719228
1.000028 --x=0.148978088,0.01477086,0.008424263,0.001511212,0.000474211,0.000121683 --xi1=0.15 --pretune --fixA --schur --predict
--floor --procs 2 --h3=1e-4`), whose pretuned x (0.148978088 0.01477086 0.008424263 0.001511212, then B, C_7 pretuned) equals the
log's `pretuned x` line.
