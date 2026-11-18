# I975-win2: M = 7 at xi1 0.15 and 0.14 on x86, beside rpi5's aarch64 runs (#965)

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session, runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/975 (coordinator task, beside #965 and #974 on rpi5, toward #355).

Code: worktree `D:\choptuik-i962` fast-forwarded from 290e9d04 to origin/main 5e603e30 (hp/ unchanged, so venv-i962's
hpkernel still matches). Venv `C:\Users\nathan\Source\venv-i962` plus `pip install numba`: numba 0.68.1, llvmlite 0.50.0
(rpi5's versions), numpy 2.5.4, scipy 1.18.1. The pip dry run listed only those two packages, no existing package changed.
win2b's ks_chain2 and #945 run on the same machine and venv-i962 is also its venv, so processes are told apart by exact pid.

Started 2026-11-18 22:27 UTC, ended 22:54 UTC. Nothing of this task runs.

Files (written as they appear):

- `run_checks.py`: the six commands of `solver/inner_stokes/inner_nb_checks.sh`, one by one, BelowNormal, logs in
  `setup_checks/` (the script's own `logs/` holds tracked files, so they are not overwritten).
- `run_job.py`: rpi5's #965 driver (`I965-rpi5/run_job.py`, raw-data repository) with the Windows changes only (no `nice`,
  BelowNormal priority class, `taskkill /T` at the cap, interpreter and log paths), logs in `logs/`. Its selftest passes and
  fails under `--mutate=r3` and `--mutate=endstate` (`selftest_run_job.log`).
- `chain975.py`: Job 0 then Job A, one at a time, `INNER_NB_RTOL=1e-13`, 3 h cap each; `exits_975.txt` has their exits.
- `summarize.py`, `affine_all.py` (copies of #964's), `zero_digits.py` (m7_outer's local zero with 9 digits, refuses as it does).
- `logs/`: the 6 + 8 solve logs (Job 0, Job A) (`hier_nb_M7_win2_rtol13_xi015_*`, `..._xi014_*`), driver logs, `m7_outer_win2_*.txt`,
  `affine_all_win2_rtol13_xi014.txt`. Every log has one Traceback, the exit-time `BytesIO` one after the FIXED-A line.

## Setup checks (22:28 to 22:30 UTC, `setup_checks/`): all six end as stored

| command | exit | stored |
|---|---|---|
| `inner_nb.py capcheck` | PASS, 0 | 0 |
| `INNER_NB_MAXFEV=100 inner_nb.py capcheck` | FAIL, 1 | 1 |
| `inner_nb.py check 1 3 5 7` | PASS, 0 (M 7 worst ratio 1.6, stored 3.6) | 0 |
| `inner_nb.py check 3 5 --mutate=sign` | FAIL, 1 | 1 |
| `hier_nb.py selftest` | PASS, 0 | 0 |
| `hier_nb.py selftest --mutate=radius` | FAIL, 1 | 1 |

The `check 1 3 5 7` line that failed on aarch64 (#964) passes here. `INNER_NB_RTOL=1e-13` reaches the spawn workers (a probe
pool of two reads `1e-13` in `os.environ` and in `inner_nb.RTOL_OVERRIDE`).

## Jobs (`INNER_NB_RTOL=1e-13`, `--procs 2`, BelowNormal, one at a time)

Job 0 22:30:47 to 22:42:34 UTC (707 s), Job A 22:42:34 to 22:53:53 (679 s), the 3 h cap not near. Memory was not sampled.

**Job 0 (xi1 0.15).** `m7_outer.py --local`: zero A 2.719240421, w/w_inf 1.000025476, error estimate 4.1e-6 (2.8e-6 the centre's
noise, 1.2e-6 J), centre r_1 -0.1153+0.0598i from 2 solves, noise 0.016, J singular values 1.05e4 and 5.6e3. Against
(2.71922, 1.000022): +2.042e-5 in A (the bar is 2e-5, missed by 2%; the reference has 5 decimals) and +3.5e-6 in w/w_inf.
Against rpi5's Job 0 (2.719236, 1.000028): +4.4e-6 and -2.5e-6, inside both error estimates (4.1e-6, 5.8e-6).

| log | A | w/w_inf | r_1 | abs r_3 | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.0994 +0.0509i | 3.0e-08 | 929 | 186 |
| `dA` | 2.719419000 | 1.000022000 | +1.8714 -0.1443i | 4.6e-05 (above) | 769 | 93 |
| `dA_endstate` | 2.719419000 | 1.000022000 | +0.8758 -0.8079i | 6.3e-08 | 617 | 71 |
| `dw` | 2.719219000 | 1.000122000 | +2.8819 +3.7933i | 6.1e-06 (above) | 860 | 116 |
| `dw_endstate` | 2.719219000 | 1.000122000 | +0.1482 +1.0132i | 3.6e-08 | 572 | 93 |
| `zero_repeat` | 2.719219000 | 1.000022000 | -0.1313 +0.0687i | 5.0e-07 | 652 | 131 |

**Job A (xi1 0.14): `m7_outer.py --local` refuses, exit 1** ("not enough solves with |r_3| < 1e-6"): after the repeats dA
and dw stay at 1.9e-6 and 2.8e-6, so no zero and no error estimate. Only `zero_endstate` is under the bar, and
`zero_repeat_endstate` is the same point (identical r_1, the repeat starts from the same 9-decimal end state).

| log | A | w/w_inf | r_1 | abs r_3 | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | +0.1076 -0.3271i | 1.1e-06 (above) | 705 | 146 |
| `zero_endstate` | 2.719219000 | 1.000022000 | +0.7020 +0.4995i | 3.2e-07 | 703 | 76 |
| `dA_r3high` | 2.719419000 | 1.000022000 | -0.7816 -2.8219i | 6.9e-06 (above) | 564 | 57 |
| `dA_endstate_r3high` | 2.719419000 | 1.000022000 | -0.6146 -1.0552i | 1.9e-06 (above) | 569 | 58 |
| `dw_r3high` | 2.719219000 | 1.000122000 | +0.1300 -0.5973i | 4.7e-06 (above) | 704 | 74 |
| `dw_endstate_r3high` | 2.719219000 | 1.000122000 | +1.2449 +5.1443i | 2.8e-06 (above) | 663 | 65 |
| `zero_repeat` | 2.719219000 | 1.000022000 | -2.9490 +5.8176i | 2.0e-06 (above) | 728 | 77 |
| `zero_repeat_endstate` | 2.719219000 | 1.000022000 | +0.7020 +0.4995i | 3.2e-07 | 703 | 106 |

Labelled affine zeros of all four solves (`affine_all.py`, `logs/affine_all_win2_rtol13_xi014.txt`), **not accepted by the
1e-6 bar**: first attempts A 2.719204, w/w_inf 1.000117 (J singular values 4.6e4 and 7.1e3, the two same-point solves
miss the model by 3.4 in r_1); after the end-state repeat A 2.719332, w/w_inf 1.000030 (4.8e4 and 5.5e3; two of the four are
the same point, so three distinct points fit the model exactly, residuals 2e-12). The after-repeat line against this Job 0:
+9.2e-5 in A and +4.5e-6 in w/w_inf (rpi5's Job A against rpi5's Job 0: +9.0e-5 and +1.4e-5).

## Beside rpi5 (#965 comment 6986578830)

| | win2 (x86, Windows) | rpi5 (aarch64) |
|---|---|---|
| Job 0 zero | (2.719240, 1.000025), err 4.1e-6 | (2.719236, 1.000028), err 5.8e-6 |
| Job 0 first attempts above the bar | dA 4.6e-5, dw 6.1e-6 (zero_repeat passed, 5.0e-7) | dA 1.5e-5, dw 4.6e-6, zero_repeat 5.8e-6 |
| Job 0 repeats | dA 6.3e-8, dw 3.6e-8 | dA 2.0e-8, dw 2.3e-8, zero_repeat 4.5e-8 |
| Job A solves under the bar | 1 distinct (zero_endstate 3.2e-7) | 3 (7.2e-7, 9.3e-7, 8.8e-7) |
| Job A m7_outer zero | refuses | (2.719326, 1.000042), err nan |
| Job A after-repeat affine zero | (2.719332, 1.000030), not accepted | not given |
| wall per job | 707 s and 679 s | 10.2 and 9.0 min, three jobs side by side |
