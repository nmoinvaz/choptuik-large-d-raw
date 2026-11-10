# I296-win2: the rest of the I19-win2 crawl, D 214.6 to 215.03125, reproduced on win2's new firmware

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/296 (recommended by win2 in #287's summary).

The crawl's command (`../I19-win2/README.md`) with `--steps 40` (its own stop rule), from `../T138-win2/chain_o/anm_pin3_D214.5000.npz`, run
from `hp/` of the worktree `D:\choptuik-t126` that ran #19 (hp code equal to e743608 and c691ae3), `venv-t126` (Python 3.12.8), 18 threads (the
crawl's count), Normal priority, no affinity (`run_i296.sh`). It waits for #295 step 1 to end. Output `crawl/`, log `crawl.log`, exits `exits.txt`.

Stop rules, before the run: the crawl's own acceptance and halving rule, a 4 h cap, and the crawl's hang rule (no log line for 20 min while one
core is busy: one py-spy dump, kill the tree, post).

A fact about the reference. `../I19-win2/crawl.log` (169 lines) does not end with a stop line. The crawl was stopped by the coordinator's call at
03:25 UTC on 2026-11-08 (process tree killed, #19's comments of 03:19Z and 03:27Z) in its third attempt past D 215.03125, after about 40 min with
nothing accepted. The issue's third acceptance item ("stops at D 215.03125 after three halvings, as the crawl did") cannot be checked against the
crawl as written. What is compared: every line of the crawl's log against the new log. What the new run does after the crawl's last line (accepts a
step, or reaches its own stop line, or runs to the cap) is reported as new information.

`compare_296.py` (`--selftest`) compares the logs line by line with elapsed times removed, the seven accepted steps (D 214.6, 214.7, 214.8, 214.9,
215.0, 215.025, 215.03125) with `hp/data/delta_all.csv` (Delta as a double, the correction to its 5 printed digits), the first seven records of
`anm_run.jsonl`, and every saved state and prediction file bit for bit.

## Result (2026-11-10 10:22 UTC)

Run: started 2026-11-10 07:22:48 UTC at 18 threads, stopped by me at 10:22:15 UTC (wall 10 767 s, 2 h 59 min) once `compare_296.py` had checked the crawl's 169 lines,
as the coordinator decided at 08:27 UTC (the hour past the crawl's last line is dropped). `exits.txt` reads "exit 1": that is the force-kill of the process
tree (`taskkill /T /F`), not a failure of the run. The new log has exactly 169 lines, so nothing is known here about what the unfixed code does past the crawl's
last line.

`compare_296.py` (`--selftest` ok), output in `compare_296_result.txt`, exit 0, **ACCEPTED**:
- Part A, log against `../I19-win2/crawl.log`, elapsed times removed: **identical for all 169 lines** (the issue's third acceptance item as the coordinator rewrote it).
- Part B, the seven accepted steps (D 214.6, 214.7, 214.8, 214.9, 215.0, 215.025, 215.03125): Delta equal to `delta_all.csv` Delta_q0 as a double and the correction equal to
  Delta_q1 in its 5 printed digits at every step (215.03125: Delta 1.69155271301216303, correction +4.6924e-18).
- Part C, the first seven records of `crawl/anm_run.jsonl` equal the crawl's with the timing keys dropped.
- Part D, the 20 saved state and prediction files (7 states `anm_pin3_D*.npz`, 13 predictions `pred_pin3_D*.npz`, the last one pred_pin3_D215.0344.npz): all bit for bit equal to
  the crawl's, none missing.

Timing (the jsonl's `t_coef` and `t_corr`, seven steps): series 2771 s and corrector 3691 s, 6462 s in all, against the crawl's 2562 s, 3604 s and 6166 s (ratio 1.05). The crawl ran
below normal priority on the old firmware, this run at Normal beside #461 part A (4 threads, 08:21 to 08:26 UTC).

Machine over the run (`../I204-win2/sensor_log.txt`, 36 five-minute readings 07:24 to 10:19 UTC): utilization mean 96.1% (8 to 131, Windows processor-utility counter), package power mean 151.2 W
(28.7 to 198.7), free memory 75.8 to 76.2 GB, no temperature (Core Temp is off). No crash, WHEA, Kernel-Power 41, BugCheck or Application Error event since the watchers' restart at 23:44 UTC on
2026-11-08 (queried at 2026-11-10 10:22 UTC).
