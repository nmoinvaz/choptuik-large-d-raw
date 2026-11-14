# I721-win2: 48 rough rt_sigma starts on #701's start-b pair at D 40.02 (K = 7 and K = 0)

Machine win2 (Core Ultra 7 265K, 20 threads, 95 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/721 (coordinator's message `1794619394259-0` on the `choptuik-large-d` channel; recommended by #701, raw `I701-win/` bba14771). Worktree `D:\choptuik-i721` at main 989e103c (`solver/rt`), venv-t177 (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0; #701 used venv-t151 on the laptop, Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` (copied from `I701-win/`, it supplies `multidouble._dd_dot`, no repository file changes).

Inputs, read in place from the raw repository's push checkout (origin/main 06b66a7d), never copied or changed: `I701-win/solves/k7b_D40_D40.0201_32x121.npz` (sha256 c5c3e03ceafb3b5e..., last changed at 1237f540) and `I701-win/solves/k0b_D40_mutnorows_D40.0201_32x121.npz` (b048df8c7504d477...). Both are 329,670 bytes.

Drivers: `run_721.py` (two `rt_sigma.py STATE --starts 48 --rough` at once, 4 BLAS threads each, BelowNormal; compares each of the first 12 starts to #701's log as it appears; `--selftest` passes: identical passes and a 1% change of one start misses), `table_701.py` and `table_423.py` (copied from `I701-win/`), `table_721.py` (the table).

## Plan, fixed before the run (2026-11-14 01:26 UTC)

1. `rt_sigma.py --planted` exits 0 (best bound 1.4103e-21) and `--planted --mutate=shift` exits 1 (1.4244e-19, FAIL), the same numbers as #701's (`logs/planted*.log`).
2. Control (acceptance 1): the first 12 bounds of each run agree with #701's `logs/K7b_D40_rough.log` and `K0b_D40_rough.log` to 3 digits. Rule: |a - b| / b <= 1e-3 against #701's printed value (4 significant digits), each start as it appears. The first miss stops the task and is reported (exit 3, `logs/control_721_MISS.txt`).
3. Acceptance 2: R_b = median(K 7) / median(K 0) over all 48 starts of each run, with its 95% bootstrap interval (10000 resamples of each run's 48 bounds with replacement, `random.Random(701)`), judged against [1/3, 3] by #701's rule (HOLDS if the point and the interval lie inside, FAILS if the point is outside and the interval entirely outside, UNDECIDED otherwise). The 12-start value (5.90, 2.13 to 14.67 in #701) is recomputed from this run's first 12 as a further control.
4. 8 busy threads (4 + 4), BelowNormal. A run unfinished after 7 h is killed and reported with what it printed. Error bars are bootstrap spreads over the random starts, not enclosures.
