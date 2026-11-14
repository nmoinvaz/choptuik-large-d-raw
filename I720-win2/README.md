# I720-win2: start a's R(40.02) at 1000 products (rt_sigma --max_products 1000 on #671's K = 7 state)

Machine win2 (Core Ultra 7 265K, 20 threads, 95 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/720 (coordinator's message `1794619394259-0`; recommended by #701, raw `I701-win/` bba14771). Worktree `D:\choptuik-i721` at main 989e103c (`solver/rt`), venv-t177 (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0; #701 used venv-t151 on the laptop, Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` (copied from `I701-win/`, it supplies `multidouble._dd_dot`, no repository file changes).

Input, read in place from the raw repository's push checkout (origin/main 06b66a7d): `I671-win/solves/k7_D40_D40.0201_32x121.npz` (sha256 df81e4d2a6f098a6..., 329,670 bytes, last changed at 07961b4b). Reference: `I681-win/logs/K7_D40_rough.log`, starts 0 to 2.

Driver `run_720.py`: the control first (`rt_sigma.py STATE --starts 3 --rough --max_products 250`), then `--max_products 1000`, 2 BLAS threads, BelowNormal. `--selftest` passes: the reference parsed from #681's log equals the issue's three numbers, identical passes and a 1% change of one bound misses.

## Plan, fixed before the run (2026-11-14 01:26 UTC)

1. `rt_sigma.py --planted` exits 0 and `--planted --mutate=shift` exits 1 (shared with I721-win2, `../I721-win2/logs/planted*.log`).
2. Control (acceptance 1): the 250-product run reproduces #681's first three bounds (1.257e-34, 9.921e-34, 7.797e-34) to 3 digits. Rule: |a - b| / b <= 1e-3 against the printed value, each start as it appears. The first miss stops the task (exit 3, `logs/control_720_MISS.txt`) and the 1000-product run is not started.
3. Acceptance 2: each of the three bounds at 1000 products is reported as within a factor 1.5 of #681's or not, with how many of the three starts still reach the cap (products = 1000).
4. 2 busy threads, BelowNormal. A run unfinished after 7 h is killed and reported with what it printed. Bounds are single-start upper bounds on the smallest gain, not enclosures.

## Results (2026-11-14 02:43 UTC, both runs exit 0)

| | control, `--max_products 250` (01:27:00 to 01:50:50 UTC) | run, `--max_products 1000` (01:50:50 to 02:43:40 UTC) | #681 (250) |
|---|---|---|---|
| start 0 bound, max\|x\|, products, max\|J x - v\| | 1.257e-34, 7.955e+33, 250, 9.5e-14 | 1.257e-34, 7.955e+33, 654, 2.7e-14 | 1.257e-34, 7.955e+33, 250, 1.6e-15 |
| start 1 | 9.921e-34, 1.008e+33, 250, 3.4e-15 | 9.921e-34, 1.008e+33, 363, 2.6e-15 | 9.921e-34, 1.008e+33, 250, 1.5e-15 |
| start 2 | 7.797e-34, 1.283e+33, 250, 4.3e-15 | 7.797e-34, 1.283e+33, 336, 1.8e-15 | 7.797e-34, 1.283e+33, 250, 2.0e-16 |

Acceptance 1 (control): all three bounds equal #681's in every printed digit, `logs/control_720.log`, rule 1e-3 relative. Acceptance 2: each of the three bounds at 1000 products is within a factor 1.5 of #681's (ratio 1.000 for each), and 0 of the 3 starts reach the 1000 cap (654, 363 and 336 products). The same three starts, so nothing is said about #681's other nine.

The capped solves' final residuals differ from #681's at 250 products (9.5e-14 against 1.6e-15, 3.4e-15 against 1.5e-15, 4.3e-15 against 2.0e-16) on this stack (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0, against #681's 3.10.0, 2.2.6, 1.15.3), so the iterates differ in their last digits, and the bounds and max\|x\| do not. These bounds are single-start upper bounds on the smallest gain, not enclosures.
