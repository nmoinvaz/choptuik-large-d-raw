# I721-win: 48 rough rt_sigma starts on #701's start-b K = 7 state at D 40.02, finishing #721

Machine win (Surface Laptop 4, i7-1185G7, 4 cores and 8 threads, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/721 (the coordinator's `hc` message on 2026-11-17, after win2's K 7 run of this issue stopped at start 28 and was lost; recommended by #701, raw `I701-win/` bba14771). Worktree `C:\Users\nathan\Source\choptuik-i721` at origin/main f9833796, branch `wip/i721-win` (`solver/rt` is identical to win2's 989e103c and to #701's 5135cdeb, `git diff --stat` empty), venv-t151 (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, the venv #701 used) through `rt_launch.py` (copied from `I701-win/`, it supplies `multidouble._dd_dot` and `math.fma`, no repository file changes).

Input, read in place from the raw repository's push worktree (origin/main a54d1407), never copied or changed: `I701-win/solves/k7b_D40_D40.0201_32x121.npz` (sha256 c5c3e03ceafb3b5e7b3a302f23bffffba4f7c49b1be5f9bcce4d97afd60f2126, last changed at 1237f540, the hash win2 recorded for the same file). The K = 0 side is win2's, not rerun here: `I721-win2/logs/K0b_D40_rough.log` (48 starts, exit 0, `K0b_D40_rough.exit` 0, raw commit 59e5c975, sha256 3dd5fcd6cda6113f...), read in place by `table_721.py`.

Drivers: `checks_721.py` (the two planted checks), `run_721.py` (one `rt_sigma.py STATE --starts 48 --rough`, 2 BLAS threads, BelowNormal; compares each of the first 12 starts to #701's log as it appears, from `I721-win2/run_721.py` with the one job; `--selftest` passes: identical passes and a 1% change of one start misses), `table_721.py` (the table; `--selftest` passes: HOLDS, FAILS, UNDECIDED and the mutation FAILS, and a 1% change of one reference bound is flagged), `table_701.py` and `table_423.py` (copied from `I701-win/`), `rt_launch.py` (copied from `I701-win/`; `--selftest` passes, 0 of 20000 differ from arb).

## Plan, fixed before the run (2026-11-17 01:40 UTC, the run started at 01:41:08 UTC)

1. `rt_sigma.py --planted` exits 0 (best bound 1.4103e-21 in #701's and win2's runs) and `rt_sigma.py --planted --mutate=shift` exits 1 (1.4244e-19, FAIL), `checks_721.py`, logs `logs/planted*.log`.
2. `rt_sigma.py k7b_D40_D40.0201_32x121.npz --starts 48 --rough` on the state above, `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=2`, BelowNormal, detached, log `logs/K7b_D40_rough.log`, exit code `logs/K7b_D40_rough.exit`, driver log `logs/run_721.log`. One job, 2 busy threads of mine. The negative-mass jobs of the same machine use about 4 more threads and are left alone, so the wall time is the laptop's, not a quiet machine's (#701's 12 starts took 3861 s at 2 BLAS threads, about 4.3 h for 48).
3. Acceptance 1 (the control): each of the first 12 bounds reproduces #701's `I701-win/logs/K7b_D40_rough.log` to 3 digits, |a - b| / b <= 1e-3 against #701's printed value (4 significant digits, so printing alone is up to 5e-4), each start as it appears. The first miss stops the run (exit 3, `logs/control_721_MISS.txt`) and is reported.
4. Acceptance 2: R_b = median(K 7, these 48) / median(K 0, win2's 48), the median of a run being the geometric mean of its 24th and 25th smallest bounds, with the 95% bootstrap interval (10000 resamples of each run's 48 bounds with replacement, `random.Random(701)`, the 2.5th and 97.5th percentiles of R_b), judged against [1/3, 3] by #701's rule: HOLDS if the point and the interval lie inside, FAILS if the point is outside and the interval lies entirely outside, UNDECIDED otherwise. R_b / R_a (R_a = 0.98) is printed beside it as in #701, and if the two readings disagree it is said so and not resolved. The 12-start value (#701: 5.90, 2.13 to 14.67) is recomputed from the first 12 of each run as a further control. Error bars are bootstrap spreads over the random starts, not enclosures.
5. **Mixing machines.** R_b takes K 7 from this laptop and K 0 from win2 (Core Ultra 7 265K, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, a different stack from this venv). That is sound only because win2's K 0 run passed the control against #701's K 0 run on this laptop: its first 12 K 0 bounds equal #701's with a relative difference of 0.0 in the printed digits (`I721-win2/logs/control_721.log`, recomputed by `table_721.py` from the logs themselves), and win2's first 12 K 7 bounds did too. `table_721.py` prints the K 0 control beside the K 7 one, and, as context and not a criterion, win2's 29 K 7 starts from its run that stopped against this run's starts 0 to 28.
6. A run unfinished after 9 h is killed and reported with what it printed (exit 5, `STOP_721` stops it by hand, exit 4). Posts on the issue every 3 hours, at most five lines, the closing comment per AGENTS.md. Raw is pushed at the start and at the end (`raw_check.py I721-win`), from a separate worktree of the raw clone, never by a pull in the live folder while the job writes.

## Run record

- 01:41:09 UTC: `run_721.py` started the K 7 run (`start_721.cmd`, BelowNormal, 2 BLAS threads, pid 17036 under the launcher), `rt_sigma.py` printed its header line equal to #701's. The laptop's other jobs kept about 6 more threads busy throughout, so the run took 9 min a start for starts 0 to 19 and about 8 min after that (#701's K 7 took 5.4 min a start with 4 busy threads).
- 03:29:34 UTC: start 11 printed, the 12th and last control start: all 12 equal #701's (relative difference 0.0 in the printed digits, `logs/control_721.log`, 12 lines, 0 MISS).
- 04:41 UTC and 07:41 UTC: the 3 h and 6 h posts on the issue (comments 6938570268 and 6941917070).
- 08:24:49 UTC: exit 0 after 24219 s (6 h 44 min), 48 starts. Memory peak 2.0 GB (working set 1,985 MB at 3 h and 2,001 MB at 6 h, the last reading), CPU 21490 s at 6 h (the process had ended before a last reading). `table_721.py` output is `table_721.txt`.

## Results

| criterion | verdict | number |
|---|---|---|
| 1. First 12 K 7 bounds reproduce #701's to 3 digits (|a - b| / b <= 1e-3, each start as it appeared) | **PASSES** | 12 of 12 starts, largest relative difference 0.0e+00, no miss |
| 2. R_b = median(K 7, these 48) / median(K 0, win2's 48), 95% bootstrap interval, against [1/3, 3] by #701's rule | **FAILS** | R_b = 1.582e-32 / 2.610e-33 = 6.06, interval 4.56 to 9.26 (the point and the whole interval above 3) |

| K | n starts | best | Q1 | median (the bound) | Q3 | max | max/min | starts at the 250 cap | worst residual max abs J x - v |
|---|---|---|---|---|---|---|---|---|---|
| 7 (this run, win) | 48 | 3.38e-33 | 1.03e-32 | **1.582e-32** | 2.67e-32 | 8.37e-32 | 24.8 | 0 of 48 | 3.4e-15 (start 32) |
| 0 (win2, raw 59e5c975) | 48 | 8.57e-34 | 1.44e-33 | **2.610e-33** | 4.43e-33 | 1.26e-32 | 14.7 | 0 of 48 | 6.3e-20 |

Further rows of the verdict table (`table_721.txt`): R_b / R_a (R_a = 0.98, #681's 12-start median ratio at start a) = 6.18, interval 4.65 to 9.45, FAILS, so the two readings of P2 agree; the best-of-48 ratio (context) is 3.94; the 12-start value recomputed from the first 12 of each run is 5.90 with interval 2.13 to 14.67, UNDECIDED, #701's numbers to the digit. The 12-start medians of #701 (K 7 1.426e-32, K 0 2.417e-33) moved to 1.582e-32 and 2.610e-33 at 48. The error bars are bootstrap spreads over the random starts (10000 resamples of each run's 48 bounds, `random.Random(701)`), not enclosures.

**Mixing machines.** R_b takes K 7 from this laptop (Python 3.10.0, numpy 2.2.6, scipy 1.15.3) and K 0 from win2 (Python 3.14.10, numpy 2.5.4, scipy 1.18.1). That rests on win2's K 0 control having matched #701's run here: win2's first 12 K 0 bounds equal #701's with a relative difference of 0.0 (`table_721.txt`, from the logs themselves), and as context win2's 29 K 7 starts from its run that stopped equal this run's starts 0 to 28 in every printed digit (29 of 29, difference 0.0). So the two stacks gave the same bounds on the same state wherever they could be compared. It is not a check of win2's K 0 starts 12 to 47 on this laptop, which no run here covers.

## Discrepancies, reported and not resolved here

- #701's prediction (comment 6862130458) is that, given P1, R_b lies in [1/3, 3], and it says the rival hypothesis (D sets R) predicts [1/3, 3] too. P1 held at start b (|DD| = 6.4e-18, #701), and R_b is 6.06 with an interval that excludes 3, so P2 fails at 48 starts and neither hypothesis's prediction for start b held. #701's 12-start verdict was UNDECIDED (5.90, 2.13 to 14.67), and the 36 further starts of each run narrow the interval to 4.56 to 9.26 and move the point only from 5.90 to 6.06.
- At the same D 40.02 start a has the 12-start medians K 7 2.403e-34 and K 0 2.463e-34 (R_a = 0.98, `I681-win/table_681.txt`), and start b has 1.582e-32 and 2.610e-33, about 66 and 11 times larger. The two states' ΔΔ are 6.8e-18 and 6.4e-18. This run does not explain the difference.

## Recommended tasks (for the coordinator to file)

1. **Start a at 48 starts, K 7 and K 0.** What: `rt_sigma.py STATE --starts 48 --rough` on #681's two start-a states at D 40.02 (the runs behind R_a = 0.98), the same rules and bootstrap as here. Why: R_a rests on 12 starts, and #721 shows a 12-start ratio (5.90, 2.13 to 14.67) that 48 starts moved to a clean FAILS, so whether start a's 0.98 survives 48 starts decides whether the difference between the two starts is real or a small-sample reading. Acceptance (each can fail): the first 12 bounds of each run reproduce #681's logs to 3 digits (|a - b| / b <= 1e-3); R_a(48) with its 95% bootstrap interval is judged against [1/3, 3] by #701's rule; R_a(48) / R_b(48) with its bootstrap interval (10000 resamples of the four runs' 48 bounds, seed 701) is compared with 1 (an interval excluding 1 means the ratio depends on the start). Depends on: #721 (R_b(48) = 6.06, 4.56 to 9.26, raw `I721-win/` and `I721-win2/`).

## Files

`README.md` (this file), `checks_721.py`, `run_721.py`, `start_721.cmd`, `table_721.py`, `table_701.py`, `table_423.py`, `rt_launch.py` (the last three copied from `I701-win/`), `table_721.txt`, and `logs/`: `K7b_D40_rough.log` (the run's output), `K7b_D40_rough.exit` (0), `run_721.log`, `control_721.log`, `planted.log`, `planted_mutate_shift.log` and their `.exit` files. The K = 0 log is read in place from `I721-win2/logs/K0b_D40_rough.log` (raw 59e5c975), and the state from `I701-win/solves/` (last changed at 1237f540).
