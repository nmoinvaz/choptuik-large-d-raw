# I1039-win: route 3's #990 commands (notes/P6_route3.md §10.6) on x86-64 Windows, compared line by line with rpi5's I1030-rpi5 logs (#1039)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7 x86-64, 4 cores / 8 threads, 32 GB, Windows 11), agent claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1039 (coordinator's plan, before #990's review; follows #1030). Status: **done** (runs 2026-11-19 18:13 to 19:21 UTC). Reading: **IDENTICAL TO RPI5** (all eight runs exit as §10 lists, every printed line equals rpi5's, only the tuned logs' timings differ, conclusion the same, so #990's review can use the two machines' runs as reference). See Result.

## Question

#1030 reproduced route 3 on aarch64 (rpi5, raw I1030-rpi5 cc9c41c5): every constant equal to §10's, and the head logs byte-identical to the Mac's. For §10's own commands (`route3_bound.py`, `route3_tuned.py`) rpi5's run is the only stored one, since #990's Mac logs were never stored. This task runs those eight commands on a second machine and build, and compares every printed line with rpi5's log of the same command.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i1039`, detached at main `51e33d8c` (the issue asks for 51e33d8c or later; `solver/proof` as of that commit) |
| interpreter | `venv-choptuik-314`, Python 3.14.10, python-flint 0.9.0, FLINT 3.6.0 (30600), mpmath 1.3.0, sympy 1.14.0, numpy 2.5.4 (also in `logs/versions.txt`). The Mac's runs used venv-314 (python-flint 0.9.0, FLINT 3.6.0, sympy 1.14.0 per §10.1), rpi5's Python 3.13.7 with the same python-flint, FLINT, mpmath and sympy versions |
| reference | `I1030-rpi5/logs/<name>.log` at raw cc9c41c5 (aarch64, Linux 6.17, Python 3.13.7, numpy 2.5.4), 8 logs of §10 |
| scheduling | `run_1039.py` via `start_1039.cmd`: one process at a time, BelowNormal (nice 10 on Linux), the commands from `solver/proof`, `python -u`, stdout and stderr to `logs/<name>.log` with a final `exit N` line as rpi5's driver wrote, a cap of 2 h per run |
| text encoding | the child runs with `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`; on Windows its newlines are CRLF, which the comparison strips |

## Commands, in order (the §10 block of notes/P6_route3.md, as I1030's `run1030.sh` ran them; cwd `<worktree>\solver\proof`)

| log | command | expected exit |
|---|---|---|
| route3_bound_lemmas | `route3_bound.py --lemmas` | 0 |
| route3_bound_constants | `route3_bound.py --constants` | 0 |
| route3_bound_constants_J0100 | `route3_bound.py --constants --J0=100` | 0 |
| route3_bound_check | `route3_bound.py --check` | 0 |
| route3_bound_check_plant | `route3_bound.py --check --mutate=plant` | 1 |
| route3_bound_check_psi | `route3_bound.py --check --mutate=psi` | 1 |
| route3_tuned_7_800 | `route3_tuned.py 7 800` | 0 |
| route3_tuned_7_800_demix | `route3_tuned.py 7 800 --mutate=demix` | 1 |

Checks and comparison:

```
python -I -X utf8 run_1039.py --selftest                       # the driver on dummy children (logs/selftest_run.log)
python -I -X utf8 compare1039.py RPI5_RAW --selftest           # the comparison on I1030's logs against themselves, with its controls (logs/selftest_compare_final.log; logs/selftest_compare.log is the first run, which reported one WRONG: my expected size bound of a test case was off by a hair, the case was corrected and the script's size() not changed)
python -I -X utf8 run_1039.py                                  # the eight runs, via start_1039.cmd
python -I -X utf8 compare1039.py RPI5_RAW > compare1039.log    # RPI5_RAW = a checkout of choptuik-large-d-raw holding I1030-rpi5 (exit 0 when no check differs)
python -I -X utf8 compare1039.py RPI5_RAW --mutate > compare1039_mutate.log   # the controls on altered copies of this folder's logs (exit 1 when all are reported)
```

## Pass criteria, fixed before the runs (the issue's)

- Each run exits as §10 lists: verdict runs 0 (last line before `exit` is `PASS`), controls 1 (`FAIL`).
- Every printed line equals rpi5's log of the same command (I1030-rpi5), timings masked (`[N s]`), by `compare1039.py`, an adaptation of I1030-rpi5's `compare1030.py` with its control (`--mutate`: altered copies of this folder's logs must each be reported).
- A difference is reported with its size, and left unfixed. Certified bounds built from upper bounds may differ in last digits between machines and both pass (#111): I say whether the conclusion is the same.
- Also checked, as in I1030 (not a separate criterion): the constants log prints C_(nu-2), C_nu, C_(nu+2) = 28.45, 56.87, 4.77e+6, and with `--J0=100` 1.60, 3.17, 3.63e+5.

Decision it informs: two machines' identical lines mean #990's review uses them as its reference. A verdict that differs reopens #990.

## Estimate

About 30 min on the Mac by §10's times, about 1 h here (a guess). rpi5 needed 5 to 18 min per run in #1030 (its `times.txt`: 2 s, 260 s, 261 s, 1073 s, 1071 s, 1078 s, 574 s, 575 s for these eight). One process at a time.

## Files

| file | what |
|---|---|
| `README.md` | this file |
| `run_1039.py`, `start_1039.cmd` | the driver (one process at a time, BelowNormal, 2 h cap per run, a final `exit N` line in each log) and its detached launcher; `run_1039.py --selftest` ran on dummy children first (`logs/selftest_run.log`, passed) |
| `compare1039.py` | the comparison (checks, line by line against I1030-rpi5, `--mutate` controls, `--selftest`) |
| `compare1039.log` | its output on the eight logs: 19 checks, 0 differ, 0 missing, exit 0 |
| `compare1039_mutate.log` | the controls on altered copies of the eight logs: 4 of 4 reported, exit 1 |
| `logs/<name>.log`, `logs/<name>.exit` | the eight runs' stdout and stderr (Windows Python wrote CRLF line endings in the runner's folder; git stores them with LF, see Observations) and each run's exit text |
| `logs/driver.log`, `logs/times.txt`, `logs/versions.txt`, `logs/run_1039.exit` | start and end of every run in UTC, wall seconds, Python and library versions with the code commit, the driver's exit (0) |
| `logs/selftest_run.log`, `logs/selftest_compare.log`, `logs/selftest_compare_final.log` | the selftests |
| `tmp/` | the issue comments as posted (start comment and its fix) |

## Result

Every one of the eight runs ended as §10 lists, and every printed line equals rpi5's line. The only lines that differ are the two timing lines of each `route3_tuned.py` log. The conclusion of each run (PASS or FAIL, and the exit code) is the same on both machines. Decision: #990's review can use the two machines' runs as its reference; no verdict differs, so nothing reopens.

| log | exit (win / expected) | last line before `exit` | wall s win | wall s rpi5 | lines | differing lines (timings masked) | conclusion |
|---|---|---|---|---|---|---|---|
| route3_bound_lemmas | 0 / 0 | PASS | 5 | 2 | 9 | 0 | same |
| route3_bound_constants | 0 / 0 | PASS | 260 | 260 | 20 | 0 | same |
| route3_bound_constants_J0100 | 0 / 0 | PASS | 255 | 261 | 20 | 0 | same |
| route3_bound_check | 0 / 0 | PASS | 880 | 1073 | 36 | 0 | same |
| route3_bound_check_plant | 1 / 1 | FAIL | 890 | 1071 | 36 | 0 | same |
| route3_bound_check_psi | 1 / 1 | FAIL | 885 | 1078 | 36 | 0 | same |
| route3_tuned_7_800 | 0 / 0 | PASS | 455 | 574 | 13 | 0 | same |
| route3_tuned_7_800_demix | 1 / 1 | FAIL | 455 | 575 | 13 | 0 | same |

Total wall time 4085 s (68 min, 18:13:33 to 19:21:38 UTC) against rpi5's 4894 s (82 min); the driver exited 0, no cap was hit and no run needed a retry.

Acceptance, as fixed before the runs:

| check | result |
|---|---|
| each run exits as §10 lists (verdict runs 0 and PASS, controls 1 and FAIL) | yes, 8 of 8 |
| every printed line equals I1030-rpi5's log of the same command, timings masked | yes, 8 of 8 logs, 0 differing lines of 183 |
| differences reported with size | none to report |
| C_(nu-2), C_nu, C_(nu+2) = 28.45, 56.87, 4.77e+6 (J0 10) and 1.60, 3.17, 3.63e+5 (J0 100) | yes |
| control: four altered copies of these logs (one digit of `route3_bound_check`'s worst-ratio line, one digit of the tuned table, C_0 56.8735 changed to 57.8735, the exit line of the plant log) each reported | yes, 4 of 4 (`compare1039_mutate.log`) |
| `compare1039.py --selftest` (I1030's logs against themselves: 0 of 19 differ; the controls; size and timing cases) and `run_1039.py --selftest` | both passed before the runs |

A second check that does not use the comparison script: `diff` of each win log against rpi5's with carriage returns stripped and no masking. Six logs give 0 differing lines. Each tuned log gives 4 (its first line `amp_flint to order 7, J = 800, tuned [430 s]` against `[554 s]` and its timing line `[451 s]` against `[574 s]`; the demix log `[431 s]` against `[553 s]` and `[454 s]` against `[575 s]`). So the masks hide nothing but those two timings per tuned log.

Observations:

- The certified bounds agree to every printed digit, not only to the digits §10 quotes: C_0 = 56.8735, C_p = 4.76610e+6, the max relative radii of `route3_bound_check` (2.3e-121 to 6.1e-32), the 5 violations in every row of the plant control and the violation counts and first-violation columns of the psi control. #111's allowance for last-digit differences between machines was not needed.
- The controls behave as rpi5's did: plant reaches a worst ratio 3.0 to 3.03 with 5 violations per row, psi violates only the perturbation 0 rows (worst 2.348 at nu = 3, down to 1.006 at nu = 7 and below 1 from nu = 9), and demix breaks the tuned table's "form C nu/j^2" in every row.
- Versions: Python 3.14.10 (CPython, AMD64, Windows 11 10.0.26200), python-flint 0.9.0, FLINT 3.6.0 (30600), mpmath 1.3.0, sympy 1.14.0, numpy 2.5.4. rpi5 used Python 3.13.7 on aarch64 Linux with the same python-flint, FLINT, mpmath, sympy and numpy versions. So this is a second architecture, operating system and Python, not a second FLINT.
- Line endings: the runner's folder holds the logs with CRLF (Python text mode on Windows; the final `exit N` line has LF), so `compare1039.py` strips `\r` and the comparison above is line by line. The push worktree has `core.autocrlf=true`, so git stores the logs with LF. As stored in git, the six `route3_bound_*` logs are byte-identical to I1030-rpi5's (checked with `cmp` on the two blobs of each), and the two tuned logs differ from rpi5's only in the timing numbers. The tuned tables print the Greek letter nu as UTF-8 on both machines.
- Timing: the win laptop was faster than rpi5 on the slow runs (880 to 890 s against 1071 to 1078 s for the `--check` runs, 455 s against 574 s for the tuned runs) and took the same time on the `--constants` runs.

Limits:

- The agreement is of the printed lines, which show certified bounds to 3 to 5 digits. It shows the output does not depend on the architecture, operating system or Python version here. It does not re-derive §10's mathematics, and it does not cover the internal ball midpoints and radii beyond what the logs print.
- Both machines ran the same python-flint, FLINT, mpmath and sympy versions. A different FLINT version could change last digits of an upper bound (#111).
- #990's own Mac logs were never stored, so there is no third comparison; rpi5's I1030 logs are the only reference.
- One run of each command on each machine; nothing was repeated here.
