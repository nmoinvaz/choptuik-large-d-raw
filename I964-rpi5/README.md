# I964-rpi5: the inner selection, stage 1: the compiled backend on aarch64 and M = 7 at xi1 0.14 and 0.16

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, Ubuntu aarch64, Python 3.13.7), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/964 (coordinator task, toward #355). Code: worktree of origin/main
0fc2fab0, branch `wip/i964-rpi5`, venv `~/Source/venv-choptuik` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1
(`setup_checks/env.txt`). Started 2026-11-18 17:05 UTC; the setup stopped at 17:08 on the check below, the coordinator said go on (comment 6985779731), step 1
ran 17:09 to 17:11 and Jobs A and B 17:13 to 17:22 UTC. Closed the same day.

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

## Step 1: the fit3_repeat reproduction (`logs/hier_nb_M7_rpi5_fit3_repeat.log`)

The first line of the stored `logs/hier_nb_M7_fixA_xi015_fit3_repeat.log` is not a command line; the command is `proof/B_tail_M7.md`
line 609 (`hier_nb.py 7 2.719228 1.000028 --x=0.148978088,0.01477086,0.008424263,0.001511212,0.000474211,0.000121683 --xi1=0.15
--pretune --fixA --schur --predict --floor --procs 2 --h3=1e-4`), whose pretuned x equals the log's `pretuned x` line.

| solve | r_1 | \|r_3\| | seconds, residuals |
|---|---|---|---|
| rpi5 | -0.0404 + 0.0744i | 3.4e-08 | 81, 987 |
| stored `fit3_repeat` | -0.0225 + 0.0424i | 1.2e-07 | 184, 806 |
| stored `fit3` | +0.1732 + 0.0200i | 3.1e-07 | 187, 850 |

Distance to `fit3_repeat` 0.037, to `fit3` 0.22; the stored pair is 0.197 apart. Within the issue's 0.2 and the coordinator's 0.1 for a repeat
of one point: reproduced. F_3/F_1 = +0.054787 + 0.005432i, <F^2> 3.7083 and Delta 1.64385 equal the stored ones to the printed digits.

## Jobs A (xi1 0.14) and B (xi1 0.16)

`run_job.py XI1 TAG` (this folder, selftest in `logs/script_selftests.txt`: passes on stored logs, fails under `--mutate=r3` and
`--mutate=endstate`) runs the four solves of `proof/B_tail_M7.md` 3.1 (zero; A + 2e-4; w/w_inf + 1e-4; zero again without `--x=`), the
repeat from the end state of a solve with |r_3| > 1e-6, `_r3high` if it stays above, then `m7_outer.py --local`. Both jobs at nice 10,
`--procs 2` each, side by side, 5.0 to 5.6 GB available, about 180 MB per process. Job A 17:13:01 to 17:21:22 UTC (8.4 min), Job B
to 17:22:27 (9.4 min); the 6 h cap was not near. No Traceback before a FIXED-A line (the BytesIO one at exit is in every log).
Every solve is deterministic: the two end-state repeats of the zero and of zero_repeat start from the same state and give the same r_1
to every printed digit.

**Both radii: `m7_outer.py --local` refuses (exit 1, "not enough solves with |r_3| < 1e-6").** Job A has one solve under the bar
(dw after its repeat, 7.7e-7), Job B none. So there is no accepted zero at either radius and Lemma R's independence at 2e-5 is
neither confirmed nor refuted here.

xi1 0.14 (`logs/table_xi014.md`, output `logs/m7_outer_rpi5_xi014.txt`):

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero_r3high` | 2.719219000 | 1.000022000 | -0.1510 +1.2630i | 2.2e-06 (above) | 523 | 49 |
| `zero_endstate_r3high` | 2.719219000 | 1.000022000 | -0.7642 +0.1845i | 1.0e-06 (above) | 563 | 53 |
| `dA_r3high` | 2.719419000 | 1.000022000 | +0.1195 +0.3587i | 2.5e-06 (above) | 979 | 82 |
| `dA_endstate_r3high` | 2.719419000 | 1.000022000 | +0.4910 -5.2224i | 3.3e-06 (above) | 668 | 55 |
| `dw` | 2.719219000 | 1.000122000 | -1.3697 +3.3223i | 2.3e-06 (above) | 800 | 70 |
| `dw_endstate` | 2.719219000 | 1.000122000 | +1.2114 +1.0940i | 7.7e-07 | 775 | 64 |
| `zero_repeat_r3high` | 2.719219000 | 1.000022000 | +0.1684 +0.1994i | 1.4e-06 (above) | 820 | 66 |
| `zero_repeat_endstate_r3high` | 2.719219000 | 1.000022000 | -0.7642 +0.1845i | 1.0e-06 (above) | 563 | 52 |

xi1 0.16 (`logs/table_xi016.md`, output `logs/m7_outer_rpi5_xi016.txt`):

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero_r3high` | 2.719219000 | 1.000022000 | -1.3138 +1.2446i | 3.7e-05 (above) | 675 | 64 |
| `zero_endstate_r3high` | 2.719219000 | 1.000022000 | -1.2407 +0.1294i | 8.4e-06 (above) | 817 | 76 |
| `dA_r3high` | 2.719419000 | 1.000022000 | +0.4293 -0.8456i | 8.2e-06 (above) | 761 | 68 |
| `dA_endstate_r3high` | 2.719419000 | 1.000022000 | +0.8230 -0.1910i | 5.9e-05 (above) | 703 | 62 |
| `dw_r3high` | 2.719219000 | 1.000122000 | -0.3302 +1.4205i | 1.6e-05 (above) | 893 | 84 |
| `dw_endstate_r3high` | 2.719219000 | 1.000122000 | -0.2621 +1.7812i | 1.9e-05 (above) | 744 | 67 |
| `zero_repeat_r3high` | 2.719219000 | 1.000022000 | +0.1363 -0.0204i | 4.0e-05 (above) | 671 | 59 |
| `zero_repeat_endstate_r3high` | 2.719219000 | 1.000022000 | -1.2407 +0.1294i | 8.4e-06 (above) | 817 | 75 |

The T36 observation at xi1 0.14 (raw `T36-win/`: |r_3| 1.0e-6 to 2.2e-6) recurs here (7.7e-7 to 3.3e-6), so it is not a property of the
Windows build. At 0.16 |r_3| is 8.2e-6 to 5.9e-5, worse than at 0.14, and than the 3.4e-8 of step 1 at 0.15. The repeat from the end state
lowers |r_3| in 5 of the 8 solves and raises it in 3 (dA at both radii, dw at 0.16); it brings 1 of 8 under the bar (dw at 0.14).
r_1 at the same point differs by 1.1 (zero against zero_repeat, first attempts) to 5.6 (dA's two attempts) at 0.14, against about 0.1 at
0.15 with |r_3| below 1e-6 (B_tail_M7.md 2), consistent with an error of about 1e5 to 1e6 times |r_3|.

## The affine zero of all four solves (not accepted by the 1e-6 bar)

`affine_all.py LOGS` (selftest and `--mutate=sign` in `logs/script_selftests.txt`; output `logs/affine_all_rpi5.txt`): the least-squares
affine model of r_1 through all four solves of a radius whatever their |r_3|. Under `--schur` r_1 is corrected for r_3 to first order, so
this shows what a looser bar would give. It is not a result until the bar is justified. The reference zero at xi1 0.15 is
(2.71922, 1.000022).

| radius | the four solves | zero A | zero w/w_inf | J singular values | difference from the 0.15 zero (A, w/w_inf) |
|---|---|---|---|---|---|
| 0.14 | first attempts | 2.720129 | 1.000059 | 2.9e4, 3.8e2 | +9.1e-4, +3.7e-5 |
| 0.14 | after the end-state repeat (two of the four are the same point) | 2.719237 | 1.000055 | 2.9e4, 2.1e4 | +1.7e-5, +3.3e-5 |
| 0.16 | first attempts | 2.719325 | 1.000042 | 1.1e4, 5.4e3 | +1.05e-4, +2.0e-5 |
| 0.16 | after the end-state repeat (two the same point) | 2.719336 | 1.000026 | 2.0e4, 9.4e3 | +1.16e-4, +4e-6 |

The four A values span 8.9e-4 (the 0.14 first-attempt line is the outlier; the other three span 1.0e-4), against the 2e-5 the protocol asks. At 0.14 the
choice of attempts alone moves A by 9e-4, so at this |r_3| the zero is set by the noise of r_1 (1 to 5, over singular values of 4e2 to 3e4) and
a radius dependence at 2e-5 cannot be seen.

## Discrepancies and recommended tasks

- The first line of the stored `fit3_repeat` log is not its command line (above).
- `inner_nb.py check` fails its M 7 line on aarch64 on a one-pair yardstick (setup, above); the coordinator decided to go on (comment
  6985779731) and asked for a yardstick from the spread over several rtols, with the mutation control rerun, as its own task.
- Recommended, for the coordinator: **A and B at a finer floor.** `INNER_NB_RTOL=1e-13` (inner_nb.py's own switch for this at M 7; the
  diagnostic above halves the numba - scipy difference at 1e-13) and/or `--h3=1e-5`, rerun `run_job.py 0.14 xi014f`, `0.16 xi016f` (about 10
  min each on this machine); acceptance: at least one solve per role with |r_3| < 1e-6 at both radii so that `m7_outer.py --local` prints a
  zero, then its distance from (2.71922, 1.000022) against 2e-5; depends on #964. `INNER_NB_RTOL` passes through `run_job.py` by the
  environment (spawn workers inherit it); `--h3=1e-5` is a one-line change of `S` in it.

## Files

`setup_checks/` (the six check logs, the diagnostic `diag_check_M7.py` and its log, `env.txt`), `logs/` (step 1, the 16 job logs, the
two `m7_outer_rpi5_*.txt`, the driver logs, the tables, `affine_all_rpi5.txt`, `script_selftests.txt`), `run_job.py`, `affine_all.py`,
`summarize.py`. Scripts run from `solver/inner_stokes/` of a worktree of origin/main 0fc2fab0 with the venv python
(`/home/nathan/Source/venv-choptuik/bin/python`; `run_job.py` and `summarize.py` are stdlib only).
