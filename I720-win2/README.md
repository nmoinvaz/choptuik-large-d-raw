# I720-win2: start a's R(40.02) at 1000 products (rt_sigma --max_products 1000 on #671's K = 7 state)

Machine win2 (Core Ultra 7 265K, 20 threads, 95 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/720 (coordinator's message `1794619394259-0`; recommended by #701, raw `I701-win/` bba14771). Worktree `D:\choptuik-i721` at main 989e103c (`solver/rt`), venv-t177 (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0; #701 used venv-t151 on the laptop, Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` (copied from `I701-win/`, it supplies `multidouble._dd_dot`, no repository file changes).

Input, read in place from the raw repository's push checkout (origin/main 06b66a7d): `I671-win/solves/k7_D40_D40.0201_32x121.npz` (sha256 df81e4d2a6f098a6..., 329,670 bytes, last changed at 07961b4b). Reference: `I681-win/logs/K7_D40_rough.log`, starts 0 to 2.

Driver `run_720.py`: the control first (`rt_sigma.py STATE --starts 3 --rough --max_products 250`), then `--max_products 1000`, 2 BLAS threads, BelowNormal. `--selftest` passes: the reference parsed from #681's log equals the issue's three numbers, identical passes and a 1% change of one bound misses.

## Plan, fixed before the run (2026-11-14 01:26 UTC)

1. `rt_sigma.py --planted` exits 0 and `--planted --mutate=shift` exits 1 (shared with I721-win2, `../I721-win2/logs/planted*.log`).
2. Control (acceptance 1): the 250-product run reproduces #681's first three bounds (1.257e-34, 9.921e-34, 7.797e-34) to 3 digits. Rule: |a - b| / b <= 1e-3 against the printed value, each start as it appears. The first miss stops the task (exit 3, `logs/control_720_MISS.txt`) and the 1000-product run is not started.
3. Acceptance 2: each of the three bounds at 1000 products is reported as within a factor 1.5 of #681's or not, with how many of the three starts still reach the cap (products = 1000).
4. 2 busy threads, BelowNormal. A run unfinished after 7 h is killed and reported with what it printed. Bounds are single-start upper bounds on the smallest gain, not enclosures.
