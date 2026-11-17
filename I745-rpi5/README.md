# I745-rpi5: start a's twelve rough rt_sigma bounds at D 40.02 at 1000 products

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, aarch64 Ubuntu), issue https://github.com/nmoinvaz/choptuik-large-d/issues/745 (the coordinator's `hc` message of 2026-11-16; win2 started the task on 2026-11-14 and left no output, its `I745-win2/` was never pushed). Recommended by #720 (`I720-win2/`, 59e5c975), which followed #681 (`I681-win/`) and #701.

Worktree `~/Source/choptuik-large-d-745` on `wip/i745-rpi5` at origin/main f9833796 (`solver/rt`, last changed at 01499651). Interpreter: `~/Source/venv-choptuik` (Python 3.13.7, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0 with FLINT 3.6.0). The venv had no multidouble, so rustc 1.100.0 (rustup, minimal profile, `~/.cargo`, shell profile untouched) and multidouble's Python package 0.1.0 at commit a93e0896 (the one `hp/pyproject.toml` names) were built with `pip install --target ~/Source/md-site-745` (the venv itself is unchanged); the run sets `PYTHONPATH=~/Source/md-site-745`. The package has `dd_dot` and not `_dd_dot`, so the run goes through `I720-win2/rt_launch.py` (the alias; its `math.fma` shim is inactive on Python 3.13), read in place, unchanged (raw e63c5143).

Input, read in place: `I671-win/solves/k7_D40_D40.0201_32x121.npz` (sha256 df81e4d2a6f098a6..., 329,670 bytes, last changed at 07961b4b). Reference: `I681-win/logs/K7_D40_rough.log` (and `K0_D40_rough.log`, `K7_D50_rough.log`, `K0_D50_rough.log`, `K7_D55_rough.log`, `K0_D55_rough.log` for the bootstrap).

## Plan, fixed before the run (written before the run started at 2026-11-17 01:43:22 UTC)

1. `rt_sigma.py --planted` exits 0 (x86 value: best bound 1.4103e-21) and `--planted --mutate=shift` exits 1 (1.4244e-19). First aarch64 runs of rt_sigma. A difference in the printed digits is reported as a finding; a wrong exit code stops the task. Logs `logs/planted.log`, `logs/planted_mutate_shift.log`.
2. The run: `rt_sigma.py STATE --starts 12 --rough --max_products 1000`, `OPENBLAS_NUM_THREADS=2` and `OMP_NUM_THREADS=2`, `nice -n 10`, `nohup`, started by `run_745.py` (logs `logs/main_1000.log`, `logs/main_1000.exit`, `logs/run_745.log`). 2 busy threads; the other 2 cores belong to the negative-mass jobs. A run unfinished after 12 h is killed (exit 5) and reported with what it printed. A file `STOP_745` stops it (exit 4).
3. Acceptance 1 (the control, watched as the starts appear): the printed bounds of starts 0 to 2 equal #720's (1.257e-34, 9.921e-34, 7.797e-34), the printed digits being the four significant digits of the log line. The rule is equality of the printed numbers; the relative difference is recorded as well. The first miss stops the task (the process killed, exit 3, `logs/control_745_MISS.txt`), because a miss means this stack does not reproduce #720's.
4. Acceptance 2: each of the other nine starts (3 to 11) is reported as within a factor 1.5 of #681's bound for the same start (new / #681 in [1/1.5, 1.5]) or not, with its products used and how many of the twelve starts reach 1000 products (the cap; those are the starts whose bound the cap may still set).
5. Acceptance 3: R_a = median(the twelve bounds at 1000 products) / median(#681's K = 0 twelve at D 40.02, 2.463e-34), the median being the geometric mean of the 6th and 7th smallest (`table_681.median`). Its 95% interval is the one-state bootstrap of #681's rule (10000 resamples with replacement of each sample's twelve, `random.Random(681)`, 2.5 and 97.5 percentiles as in `table_681.verdict`), and it is compared with #681's 0.98. As context, the full rule of #681 (`table_681.verdict`, seed 681, R(40.02) / R(50.007) and R(54.996) / R(50.007) against the window of 3) is applied with the D 40.02 K = 7 sample replaced by this run's, the other five samples being #681's. Control, before the run: `table_745.py --control` recomputes from #681's own logs R = 0.98, and the full rule's 0.17, interval 0.06 to 0.91, UNDECIDED. `table_745.py --selftest`: identical bounds pass acceptance 1, a 1% change of one bound misses, a start 1.6 times #681's fails acceptance 2, and K = 7 bounds scaled by 3 move R_a to 2.93 and the full rule's R(40.02) / R(50.007) to 0.50.
6. The numbers are single-start upper bounds on the smallest gain (max norm), not enclosures. The bounds' differences between runs of this stack and #681's stack (Python 3.10, numpy 2.2.6, scipy 1.15.3, x86 Windows) are reported as found: #720 found the iterates differ in their last digits and the bounds do not.

## Results (the run was killed by its own 12 h cap at 2026-11-17 13:43:30 UTC, exit code 5; 8 of 12 starts printed)

The planted check passes on aarch64 with the x86 digits (exit 0, best bound 1.4103e-21; `--mutate=shift` exit 1, 1.4244e-19; `logs/planted*.log`).

| acceptance | verdict | numbers |
|---|---|---|
| 1, first three bounds equal #720's in the printed digits | **met** | 1.257e-34, 9.921e-34, 7.797e-34, relative difference 0 each (`logs/control_745.log`, at 06:51, 07:18 and 08:15 UTC) |
| 2, the other nine within a factor 1.5 of #681's | **5 of 9 reported, all within** | starts 3 to 7, ratio 1.000 each; starts 8 to 11 never printed |
| 2, starts reaching 1000 products | **0 of 8** | products 606, 276, 421, 527, 501, 480, 248, 448 |
| 3, R_a against 0.98 | **not formed** | needs all twelve starts; `table_745.py` prints it when they exist |

`logs/table_745_partial.txt` is `table_745.py` on the 8 printed starts. Starts 3, 4, 5 and 7 stop at 448 to 527 products where #681's capped them at 250, with the same bound to four digits, so the 250 cap did not set them either (start 6 stopped at 248 in both).

Against #720 on win2 the bounds are equal and the iterates differ, as #720 found across stacks: start 0 stopped at 606 products (win2 654), start 1 at 276 (363), start 2 at 421 (336), and the final residuals max|J x - v| are 1.3e-14, 1.6e-14, 7.7e-16 (win2 2.7e-14, 2.6e-15, 1.8e-15).

What ran: 8 starts in 12 h of wall time on 2 cores that the negative-mass jobs, other Claude sessions and a full 1 GB swap shared. The first 4 h gave 39 CPU-minutes (I/O pressure averaged 76 to 84%, load up to 60; `logs/resource.log`), RSS grew from 1.5 to 2.8 GB (fgmres keeps two arb vectors per product). The task moved to win2 (I745-win2). The 4 h progress post of #745 was never made (the gh token had expired); raw pushes went by SSH. These are single-start upper bounds on the smallest gain, not enclosures.
