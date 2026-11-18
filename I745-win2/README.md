# I745-win2: start a's twelve rough rt_sigma bounds at D 40.02 at 1000 products

Machine win2 (Core Ultra 7 265K, 20 threads, 95 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/745 (coordinator's `hc` message of 2026-11-17 18:54 UTC; recommended by #720, `I720-win2/`, 59e5c975, which followed #681 `I681-win/` and #701).

I745-rpi5 is superseded: its run (2026-11-17 01:43 to 13:43 UTC) thrashed on the 8 GB Pi, with swap full and the load at 60 it got 39 CPU minutes in 4 h and printed no start, and its token had expired so it could not post (raw `I745-rpi5/`, 089b2616). Its driver `run_745.py` and `table_745.py` are reused here, the first ported to Windows. An earlier win2 attempt (2026-11-14) left no output.

Worktree `D:\choptuik-i745` (new, detached) at origin/main 808b1fac, `solver/rt` identical to #720's 989e103c (`git diff 989e103c HEAD -- solver/rt` is empty, last change b5d69cc2). Interpreter `C:\Users\nathan\Source\venv-t177` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0, multidouble Python package 0.1.0), the stack of #720 and #721, through `rt_launch.py` (copied unchanged from `I720-win2/`, byte-identical to `I721-win2/`'s; it supplies `multidouble._dd_dot` and `math.fma` if missing).

Input, read in place from this raw worktree (origin/main a9ca29a1), never copied or changed: `I671-win/solves/k7_D40_D40.0201_32x121.npz` (sha256 df81e4d2a6f098a6..., 329,670 bytes, last changed at 07961b4b). Reference: `I681-win/logs/K7_D40_rough.log` (and the other five logs of that folder for the bootstrap).

Files: `run_745.py` (driver), `table_745.py` (the table, copied unchanged from `I745-rpi5/`, imports `table_681` and `table_423` from `../I681-win`), `compare_rpi5.py` (win2 against rpi5, added after the coordinator's message that rpi5 had printed eight starts), `sample_child.ps1` (memory and cpu of the solve, see Deviations), `rt_launch.py`, `logs/`.

## Plan, fixed before the run (2026-11-17 18:57 UTC, before the run)

1. `rt_sigma.py --planted` exits 0 (best bound 1.4103e-21) and `--planted --mutate=shift` exits 1 (1.4244e-19, FAIL), on this worktree and stack. Done before this README: `logs/planted.log`, `logs/planted_mutate_shift.log` (+ `.exit`), exits 0 and 1 with those two numbers.
2. The run: `rt_sigma.py STATE --starts 12 --rough --max_products 1000` through `rt_launch.py`, `OPENBLAS_NUM_THREADS=2`, `OMP_NUM_THREADS=2`, BelowNormal (logs `logs/main_1000.log`, `logs/main_1000.exit`, `logs/run_745.log`). 2 busy threads, beside win2b's chain and #945, which are left alone. A run unfinished after 8 h is killed (exit 5) and reported with what it printed. A file `STOP_745` stops it (exit 4).
3. Acceptance 1 (the control, watched as the starts appear): the printed bounds of starts 0 to 2 equal #720's (1.257e-34, 9.921e-34, 7.797e-34), the printed digits being the four significant digits of the log line. The rule is equality of the printed numbers, the relative difference is recorded as well. The first miss stops the task (the process tree killed, exit 3, `logs/control_745_MISS.txt`), because a miss means this stack does not reproduce #720's.
4. Acceptance 2: each of the other nine starts (3 to 11) is reported as within a factor 1.5 of #681's bound for the same start (new / #681 in [1/1.5, 1.5]) or not, with its products used and how many of the twelve starts reach 1000 products (the cap).
5. Acceptance 3: R_a = median(the twelve bounds at 1000 products) / median(#681's K = 0 twelve at D 40.02, 2.463e-34), the median being the geometric mean of the 6th and 7th smallest (`table_681.median`), with its 95% interval from the one-state bootstrap of #681's rule (10000 resamples with replacement of each sample's twelve, `random.Random(681)`), against #681's 0.98. As context, the full rule of #681 (`table_681.verdict`, seed 681) with this run's twelve in place of #681's K = 7 sample at D 40.02. Controls, before the run: `table_745.py --control` recomputes R = 0.98 from #681's own logs (and the full rule's 0.17, 0.06 to 0.91, UNDECIDED), `table_745.py --selftest` and `run_745.py --selftest` pass (`logs/control_table_745.log`, `logs/selftest_table_745.log`, `logs/selftest_run_745.log`).
6. The numbers are single-start upper bounds on the smallest gain (max norm), not enclosures. The bounds' differences between runs of this stack and #681's stack (Python 3.10, numpy 2.2.6, scipy 1.15.3, x86 Windows) are reported as found: #720 found the iterates differ in their last digits and the bounds do not.

## Results (run 2026-11-17 18:58:48 to 2026-11-18 00:57:03 UTC, exit 0 after 5.97 h)

`logs/main_1000.log`, `logs/main_1000.exit` (0), `logs/table_745.txt` (`table_745.py`), `logs/compare_rpi5.txt` (`compare_rpi5.py`). All twelve starts printed, 5992 products in all, and none reaches the 1000 cap (the largest is start 0 at 654).

| start | bound | #681 bound (250 products) | ratio | products | max\|J x - v\| |
|---|---|---|---|---|---|
| 0 | 1.257e-34 | 1.257e-34 | 1.000 | 654 | 2.7e-14 |
| 1 | 9.921e-34 | 9.921e-34 | 1.000 | 363 | 2.6e-15 |
| 2 | 7.797e-34 | 7.797e-34 | 1.000 | 336 | 1.8e-15 |
| 3 | 1.263e-34 | 1.263e-34 | 1.000 | 559 | 2.1e-14 |
| 4 | 1.564e-34 | 1.564e-34 | 1.000 | 591 | 8.1e-15 |
| 5 | 2.188e-34 | 2.188e-34 | 1.000 | 522 | 2.7e-14 |
| 6 | 1.805e-33 | 1.805e-33 | 1.000 | 341 | 2.1e-15 |
| 7 | 4.881e-34 | 4.881e-34 | 1.000 | 427 | 5.7e-15 |
| 8 | 2.639e-34 | 2.639e-34 | 1.000 | 538 | 6.9e-15 |
| 9 | 1.297e-34 | 1.297e-34 | 1.000 | 559 | 9.1e-15 |
| 10 | 3.667e-34 | 3.667e-34 | 1.000 | 506 | 1.0e-14 |
| 11 | 1.606e-34 | 1.606e-34 | 1.000 | 596 | 6.7e-14 |

| acceptance | verdict | numbers |
|---|---|---|
| 1, first three bounds equal #720's | **met** | 1.257e-34, 9.921e-34, 7.797e-34, equal in every printed digit (`logs/control_745.log`, 19:43, 20:01, 20:15 UTC); their products (654, 363, 336) and final residuals (2.7e-14, 2.6e-15, 1.8e-15) equal #720's too |
| 2, the other nine within a factor 1.5 of #681's | **9 of 9 within, each ratio 1.000** | equal to four digits; products 341 to 596, where #681's capped every start at 250 |
| 2, starts reaching 1000 products | **0 of 12** | 654, 363, 336, 559, 591, 522, 341, 427, 538, 559, 506, 596 |
| 3, R_a against 0.98 | **0.98** | median 2.403e-34 / #681's K = 0 median 2.463e-34, one-state bootstrap 95% interval 0.32 to 2.92 (seed 681, 10000 resamples). The full rule of #681 with these twelve gives R(40.02) / R(50.007) = 0.17 (0.06 to 0.91), R(54.996) / R(50.007) = 1.21 (0.54 to 5.00), verdict UNDECIDED, the numbers of #681 |

So the 250-product cap set none of the twelve bounds, and R_a at 1000 products is #681's 0.98, because the twelve bounds are the same numbers. The bounds are single-start upper bounds on the smallest gain (max norm), not enclosures, and the interval is a bootstrap spread over the twelve random starts, not an enclosure.

### x86 (win2) against aarch64 (rpi5), starts 0 to 7 (`I745-rpi5/`, fd9d22ca)

Same state and command, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0 and multidouble Python package 0.1.0 on both; the interpreter (rpi5: Python 3.13.7, aarch64 Ubuntu; win2: Python 3.14.10, x86 Windows) and the platform differ.

| | equal as printed | not equal |
|---|---|---|
| bound | 8 of 8 | 0 |
| max\|x\| | 8 of 8 | 0 |
| products used | 0 of 8 | 8 (win2 / rpi5 from 0.80 to 1.38: 654/606, 363/276, 336/421, 559/527, 591/501, 522/480, 341/248, 427/448) |
| final residual max\|J x - v\| | 0 of 8 | 8 (the table in `logs/compare_rpi5.txt`) |

The two machines print the same bounds and stop at different product counts, as #720 found across stacks: the iterates differ in their last digits, the bounds do not. Against #720 on this machine and stack, starts 0 to 2 equal in the bound, the products and the final residual.

## Deviations and findings

- The driver's `logs/resource.log` reads the venv launcher stub (4 MB, no cpu), not the solve. `sample_child.ps1` records the real python process every 10 min in `logs/resource_child.log`: peak working set 3,371 MB, 0.96 to 0.98 busy threads on average (the solve is mostly single-threaded arb), the machine 70 to 100% busy with win2b's jobs, 58 to 60 GB free. `logs/resource_child_wrongpid.log` is its first line from a wrong pid (the console host), kept as is.
- The driver was started with PowerShell `Start-Process` at BelowNormal, after a `cmd start` launch left a hung `cmd.exe` and no python (`logs/driver.out`, `driver.err`).
- #681's log has start 6 at 250 products, the cap, with the bound 1.805e-33 equal to this run's. The README of `I745-rpi5/` says start 6 "stopped at 248 in both"; its own log has 248 and this run has 341. Reported, not changed.
